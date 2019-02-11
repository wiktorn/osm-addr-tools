import json
import logging
import tempfile
import urllib
from urllib.parse import urlencode
from urllib.request import urlopen
import typing

import tqdm
from bs4 import BeautifulSoup
from bs4.element import Tag

from data.base import AbstractImport, Address, e2180_to_wgs, LocationStr


class TqdmUpTo(tqdm.tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b*bsize - self.n)


class iMPA(AbstractImport):
    __log = logging.getLogger(__name__).getChild('iMPA')
    __USE_GML = False

    def __init__(self, gmina: typing.Optional[str] = None, wms: typing.Optional[str] = None,
                 terc: typing.Optional[str] = None):
        self.wms = None

        if gmina:
            self._init_from_impa(gmina)
            self.source = '%s.e-mapa.net' % (gmina,)
        else:
            self.source = 'www.punktyadresowe.pl'
            if not wms and not terc:
                raise ValueError("If no gmina provided then wms and terc are required")
            super(iMPA, self).__init__(terc=terc)

        if wms:
            self.wms = wms

        if not self.wms:
            raise ValueError("No WMS address found")

    def _init_from_impa(self, gmina: str):
        url = 'http://%s.e-mapa.net/application/system/init.php' % (gmina,)
        self.__log.info(url)
        data = urlopen(url).read().decode('utf-8')
        init_data = {}
        try:
            init_data = json.loads(data)
        except ValueError as e:
            # ignore json parsing erros. If there is no json parsed data, try to parse
            # strings manually...
            pass

        def make_extract(d: str) -> typing.Callable[[str, str], str]:
            def extract(begin: str, end: str) -> typing.Optional[str]:
                start_pos = d.rfind(begin)
                end_pos = d.find(end, start_pos)
                if start_pos < 0 or end_pos < 0:
                    return None
                return d[start_pos + len(begin):end_pos]
            return extract

        if len(init_data) > 0 and 'spatialExtent' in init_data:
            self.set_bbox_from_2180(init_data['spatialExtent'])
            self.terc = init_data.get('teryt')
            address_layers = list(
                filter(
                    lambda x: x.get('title') and x['title'].upper() == 'ADRESY I ULICE',
                    init_data.get('map', {}).get('services', [{}, ])
                )
            )
        elif len(init_data) > 0 and 'error' in init_data:
            raise ValueError(init_data['error'])
        else:
            extract = make_extract(data)
            bbox = extract('"spatialExtent":[', '],"').split(',')
            self.set_bbox_from_2180(list(map(float, bbox)))
            self.terc = extract('"teryt":"', '","')
            address_layers = []

        if len(address_layers) == 0:
            self.__log.warning('No information about address layer in init.php')
            self.__log.debug(data)
            url = 'http://%s.punktyadresowe.pl' % (gmina,)
            self.__log.info(url)
            data = urlopen(url).read().decode('utf-8')

            extract = make_extract(data)
            wms = extract("wmsUrl = '", "';")
            terc = extract("var teryt_gminy = '", "';")
            if wms and terc:
                self.wms = wms
                self.terc = terc
                self.__log.info('setting wms to: %s and terc to %s', wms, terc)
            else:
                self.__log.warning('No information about address layer in %s', url)
                self.__log.debug(data)
        else:
            self.wms = address_layers[0]['address']

    def fetch_point(self, wms_addr, w, s, e, n, pointx, pointy, layer="punkty"):
        params = {
            'VERSION': '1.1.1',
            'SERVICE': 'WMS',
            'REQUEST': 'GetFeatureInfo',
            'LAYERS': layer,  # było: ulice,punkty
            'QUERY_LAYERS': layer,  # było: ulice, punkty
            'FORMAT': 'image/png',
            'INFO_FORMAT': 'application/vnd.ogc.gml' if self.__USE_GML else 'text/html',
            'SRS': 'EPSG:2180',
            'FEATURE_COUNT': '10000000',  # wystarczająco dużo, by ogarnąć każdą sytuację
            'WIDTH': 2,
            'HEIGHT': 2,
            'BBOX': '%s,%s,%s,%s' % (w, s, e, n),
            'X': pointx,
            'Y': pointy,
        }

        josm_wms = {
            'VERSION': '1.1.1',
            'SERVICE': 'WMS',
            'REQUEST': 'GetMap',
            'LAYERS': layer + ',ulice',
            'FORMAT': 'image/png',
            'TRANSPARENT': 'true',
        }

        # TODO: do proper URL parsing
        if '?' in wms_addr:
            url = "%s&%s" % (wms_addr, urlencode(params))
            self.__log.warning("JOSM layer: %s&%s&SRS={proj}&WIDTH={width}&HEIGHT={height}&BBOX={bbox}" % (
                wms_addr, urlencode(josm_wms)))
        else:
            url = "%s?%s" % (wms_addr, urlencode(params))
            self.__log.warning("JOSM layer: %s?%s&SRS={proj}&WIDTH={width}&HEIGHT={height}&BBOX={bbox}" % (
                wms_addr, urlencode(josm_wms)))
        self.__log.info(url)
        with tempfile.NamedTemporaryFile() as temp:
            with TqdmUpTo(unit='B', unit_scale=True, miniters=1, desc="Downloading from iMPA") as t:
                urllib.request.urlretrieve(url, filename=temp.name, reporthook=t.update_to)
            data = temp.read()
        return data

    def _convert_to_address_html(self, soup: Tag):
        kv = dict((x.name, x.text) for x in soup.find_all())
        try:
            (lon, lat) = kv['WGS_84'].split(' ', 1)

            if float(lon) < 14 or float(lon) > 25 or float(lat) < 49 or float(lat) > 56:
                self.__log.warning("Point out of Polish borders: (%s, %s), %s, %s, %s", lat, lon, kv.get('Miejscowosc',''), kv.get('Ulica', ''),
                                   kv['Numer'])

            return Address.mapped_address(
                housenumber=kv['Numer'].strip(),
                postcode=kv['Kod_pocztowy'].strip(),
                street=kv['Ulica'].strip(),
                city=kv['Miejscowosc'].strip(),
                sym_ul=kv['ULIC'].strip(),  # sym_ul
                simc=kv['SIMC'].strip(),  # simc
                source=kv.get('Zrodlo danych', ''),
                location=LocationStr(lat=lat, lon=lon),  # location
                id_=kv.get('idIIP', '')
            )
        except KeyError:
            self.__log.error(soup)
            self.__log.error(kv)
            self.__log.error("Exception during point analysis", exc_info=True)
            raise
        except ValueError:
            self.__log.error(soup)
            self.__log.error(kv)
            self.__log.error("Exception during point analysis", exc_info=True)
            raise

    def _convert_to_address_gml(self, soup: Tag) -> Address:
        def get(tag_name):
            ret = soup.find(tag_name)
            if ret:
                return ret.text
            else:
                return ''

        try:
            lon, lat = soup.find('coordinates').text.split(' ')[0].split(',')
            lon, lat = e2180_to_wgs(lon, lat)

            return Address.mapped_address(
                housenumber=get('numer'),
                postcode=get('kod'),
                street=get('ulica'),
                city=get('miejscowosc'),
                sym_ul=get('ulic'),
                simc=get('simc'),
                source=self.source,
                location=LocationStr(lat=str(lat), lon=str(lon))
            )
        except:
            self.__log.error(soup)
            self.__log.error("Exception during point analysis", exc_info=True)
            raise

    def fetch_tiles(self) -> typing.List[Address]:
        html = self.fetch_point(
            self.wms,
            *self.get_bbox_2180(),
            pointx=0, pointy=0  # sprawdź punkt (0,0) i tak powinno zostać zwrócone wszystko
        )
        if self.__USE_GML:
            ret = [self._convert_to_address_gml(x) for x in tqdm.tqdm(
                BeautifulSoup(html, "xml").find_all('punkty_feature'), desc="Conversion")
                   ]
        else:
            ret = [self._convert_to_address_html(x) for x in tqdm.tqdm(BeautifulSoup(html, "lxml-xml").find_all('Adres'),
                                                                       desc="Conversion")]
        return ret
