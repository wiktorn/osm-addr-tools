import logging
import math
import re
import typing

import lxml.etree
import lxml.html
import tqdm

from data.base import Address, get_ssl_no_verify_opener, LocationStr
from data.gugik import GUGiK


class EGeoportal(GUGiK):
    # parametry do EPSG 2180
    __MAX_BBOX_X = 20000
    __MAX_BBOX_Y = 45000
    __PRECISION = 10
    __base_url = "http://wms10.e-geoportal.pl/?SERVICE=WMS&VERSION=1.1.1"
    __base_url_getmap = __base_url + "&REQUEST=GetMap&TRANSPARENT=true&LAYERS={layer:s}&" \
                                     "SRS=EPSG:2180&STYLES=&WIDTH=16000&HEIGHT=16000&FORMAT=kml&&BBOX={bbox}"

    __log = logging.getLogger(__name__).getChild('EGeoportal')
    __NUMER_RE = re.compile(r'(\d+)\s((?=\d+))')

    def __init__(self, layer: str, terc: str):
        super(GUGiK, self).__init__(terc=terc)
        self.terc = terc
        layer_list = self.list_layers()
        if layer not in layer_list:
            raise ValueError("Unknown layer: {0}. Available layers:\n{1}".format(layer, "\n".join(layer_list)))
        self.layer = layer

    def _convert_to_address(self, soup: lxml.etree.ElementTree) -> Address:
        desc_soup = lxml.html.fromstring(str(soup.find('{http://www.opengis.net/kml/2.2}description').text))
        addr_kv = dict(
            (
                str(x.find('strong').find('span').text),
                str(x.find('span').text).strip()
            ) for x in desc_soup.find('ul').iterchildren()
        )

        coords = soup.find('{http://www.opengis.net/kml/2.2}Point').find(
            '{http://www.opengis.net/kml/2.2}coordinates').text.split(',')
        # Hack for spaces in EMUiA addresses. Replace them with slash, if they are between numbers
        addr_kv['nr_budynku'] = self.__NUMER_RE.sub('\\1/\\2', addr_kv['nr_budynku'])
        addr_street = addr_kv.get('nazwa_ulicy')
        addr_teryt_ulicy = addr_kv.get('teryt_ulicy', '0')
        addr_teryt_miejscowosci = addr_kv.get('teryt_miejscowosci')
        if addr_teryt_ulicy == "0":
            addr_teryt_ulicy = ""
        if addr_teryt_miejscowosci == "0":
            addr_teryt_miejscowosci = ""
        try:
            ret = Address.mapped_address(
                housenumber=addr_kv['nr_budynku'],
                postcode=addr_kv.get('kod_pocztowy'),
                street=addr_street,
                city=addr_kv['miejscowosc'],
                sym_ul=addr_teryt_ulicy,
                simc=addr_teryt_miejscowosci,
                source='e-geoportal.pl/' + self.layer,
                location=LocationStr(lat=coords[1], lon=coords[0]),
                id_=addr_kv.get('id')
            )
        except KeyError as e:
            self.__log.warning('Not converting address error: {0}, input_data: {1}', str(e), addr_kv)
            raise
        return ret

    def _is_eligible(self, addr: Address) -> bool:
        return True

    def fetch_tiles(self) -> typing.Iterable[Address]:
        bbox = self.get_bbox_2180()
        ret = []
        for i in tqdm.tqdm(self.divide_bbox(*bbox), "Download"):
            url = self.__base_url_getmap.format(layer=self.layer, bbox=",".join(map(str, i)))
            self.__log.info("Fetching from e-Geoportal: %s", url)

            opener = get_ssl_no_verify_opener()

            soup = lxml.etree.fromstring(opener.open(url).read())
            doc = soup.find('{http://www.opengis.net/kml/2.2}Document')  # be namespace aware
            if doc is not None:
                for addr in soup.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
                    if self._is_eligible(addr):
                        try:
                            ret.append(self._convert_to_address(addr))
                        except KeyError:
                            pass
            else:
                raise ValueError(
                    'No data returned from GUGiK possibly to wrong scale. '
                    'Check __MAX_BBOX_X, __MAX_BBOX_Y, HEIGHT and WIDTH'
                )
        # take latest version for each point (version is last element after dot in id_)
        # ret = [max(v, key=lambda z: z.id_) for  v in groupby(ret, lambda z: z.id_.rsplit('.', 1)[0]).values()]
        if len(ret) == 0:
            raise ValueError('No data returned from source')
        return ret

    def list_layers(self) -> typing.List[str]:
        url = self.__base_url + "&REQUEST=Getcapabilities"
        opener = get_ssl_no_verify_opener()

        soup = lxml.etree.fromstring(opener.open(url).read())
        layer_names = sorted(x.text for x in soup.findall('.//Layer/Name'))
        return [
                   x for x in layer_names
                   if 'punkt' in x and not any(query in x for query in ('prognoz', 'archiw', 'budow'))
               ] + [
                   x for x in layer_names
                   if 'punkt' in x and any(query in x for query in ('prognoz', 'archiw', 'budow'))
               ]

    @staticmethod
    def divide_bbox(minx: float, miny: float, maxx:float , maxy: float) -> typing.Iterable[typing.Tuple[float, float]]:
        # TODO: LatType / XType?
        """divides bbox to tiles of maximum supported size by EMUiA WMS"""
        # noinspection PyTypeChecker
        return [
            (x / EGeoportal.__PRECISION,
             y / EGeoportal.__PRECISION,
             min(x / EGeoportal.__PRECISION + EGeoportal.__MAX_BBOX_X, maxx),
             min(y / EGeoportal.__PRECISION + EGeoportal.__MAX_BBOX_Y, maxy))
            for x in range(math.floor(minx * EGeoportal.__PRECISION), math.ceil(maxx * EGeoportal.__PRECISION),
                           EGeoportal.__MAX_BBOX_X * EGeoportal.__PRECISION)
            for y in range(math.floor(miny * EGeoportal.__PRECISION), math.ceil(maxy * EGeoportal.__PRECISION),
                           EGeoportal.__MAX_BBOX_Y * EGeoportal.__PRECISION)
        ]
