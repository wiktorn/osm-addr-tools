import logging
import re
import typing

import lxml.etree
import lxml.html
import tqdm

from .base import AbstractImport, Address, LocationStr, XType, YType
from .data import srs_to_wgs, LocationXY
from converters import emuia


class GUGiK(AbstractImport):
    # parametry do EPSG 2180
    __MAX_BBOX_X = 20000
    __MAX_BBOX_Y = 45000
    __PRECISION = 10
    __base_url = "http://emuia1.gugik.gov.pl/wmsproxy/emuia/wms?SERVICE=WMS&" \
                 "FORMAT=application/vnd.google-earth.kml+xml&VERSION=1.1.1&" \
                 "SERVICE=WMS&REQUEST=GetMap&LAYERS=emuia:layer_adresy_labels&STYLES=&" \
                 "SRS=EPSG:2180&WIDTH=16000&HEIGHT=16000&BBOX="

    __log = logging.getLogger(__name__).getChild('GUGiK')
    __NUMER_RE = re.compile(r'(\d+)\s((?=\d+))')

    def __init__(self, terc: str):
        super(GUGiK, self).__init__(terc=terc)
        self.terc = terc

    def _convert_to_address(self, dct: typing.Dict[str, str]) -> Address:
        # Note: X and Y axis are reveresed?
        coords = LocationXY(projection='epsg:2180', x=XType(float(dct['pktY'])), y=YType(float(dct['pktX'])))
        ret = Address.mapped_address(
            housenumber=dct['pktNumer'],
            postcode=dct.get('pktKodPocztowy', ""),
            street=(dct.get('ulNazwaCzesc', "") + " " + dct.get('ulNazwaGlowna', "")).strip(),
            city=dct['miejscNazwa'],
            sym_ul=dct.get('ulIdTeryt'),
            simc=dct.get('miejscIdTeryt'),
            source='emuia.gugik.gov.pl',
            location=coords.to_location_str(),
            id_=dct.get('pktEmuiaIIPId', "")
        )
        ret.status = dct['pktStatus']
        return ret

    def _is_eligible(self, addr: Address) -> bool:
        # TODO: check status?
        if addr.status.upper() != 'ISTNIEJACY':
            self.__log.debug('Ignoring address %s, because status %s is not ISTNIEJACY', addr, addr.status.upper())
            return False
        if '?' in addr.housenumber or 'bl' in addr.housenumber:
            self.__log.debug('Ignoring address %s because has strange housenumber: %s', addr, addr.housenumber)
            return False
        return True

    def fetch_tiles(self) -> typing.List[Address]:
        return [
            x for x in [
                self._convert_to_address(x['adres']) for x in tqdm.tqdm(
                    emuia.get_addresses(self.terc),
                    desc="Conversion"
                )
            ] if self._is_eligible(x)
        ]


class GUGiK_GML(AbstractImport):
    __log = logging.getLogger(__name__).getChild('GUGiK_GML')
    __GML_NS = "http://www.opengis.net/gml/3.2"
    __MUA = "urn:gugik:specyfikacje:gmlas:ewidencjaMiejscowosciUlicAdresow:1.0"
    __XLINK_HREF = "{http://www.w3.org/1999/xlink}href"

    def __init__(self, fname: str):
        self.soup = lxml.etree.fromstring(open(fname, 'rb').read())  # type: lxml.etree.ElementTree
        terc = max(
            (x.text for x in
             self.soup.findall('.//{{{0}}}AD_JednostkaAdministracyjna/{{{0}}}idTERYT'.format(self.__MUA))),
            key=len
        )  # type: str
        #    map(
        #        lambda x: x.text,
        #        self.soup.find('{%s}featureMembers' % self.__GML_NS).findall(
        #            '{%s}AD_JednostkaAdministracyjna/{%s}idTERYT' % (self.__MUA, self.__MUA)
        #        )),
        #    key=len
        # )
        super(GUGiK_GML, self).__init__(terc=terc)
        self.terc = terc

    def _convert_to_address(self, soup: lxml.etree.Element, ulic: typing.Dict[str, typing.Tuple[str, str]],
                            miejsc: typing.Dict[str, typing.Tuple[str, str]]):
        point = soup.find('{%s}pozycja/{%s}Point' % (self.__MUA, self.__GML_NS))
        srs = point.get('srsName')
        coords_el = point.find('{%s}coordinates' % self.__GML_NS)
        if coords_el:
            coords = srs_to_wgs(srs, *map(float, coords_el.text.split(coords_el.get('cs'))))
        else:
            coords_el = point.find('{{{0}}}pos'.format(self.__GML_NS))
            coords = [float(x) for x in coords_el.text.split(' ')]
            if coords_el.get('axisLabels') == 'Y X':
                coords = srs_to_wgs(srs, *reversed(coords))
            else:
                coords = srs_to_wgs(srs, *reversed(coords))

        try:
            ulica = ulic[soup.find('{%s}ulica2' % self.__MUA).get(self.__XLINK_HREF)]
        except KeyError:
            self.__log.error('No name for ulica: %s' % (soup.find('{%s}ulica2' % self.__MUA).get(self.__XLINK_HREF),))
            return None
        try:
            miejscowosc = miejsc[soup.find('{%s}miejscowosc' % self.__MUA).get(self.__XLINK_HREF)]
        except KeyError:
            self.__log.error(
                "No name for miejscowosc: %s" % (soup.find('{%s}miejscowosc' % self.__MUA).get(self.__XLINK_HREF),))
            return None

        ret = Address.mapped_address(
            housenumber=soup.find('{%s}numerPorzadkowy' % self.__MUA).text,
            postcode=soup.find('{%s}kodPocztowy' % self.__MUA).text,
            street=ulica[1],
            city=miejscowosc[1],
            sym_ul=ulica[0],
            simc=miejscowosc[0],
            source='emuia.gugik.gov.pl',
            location=LocationStr(lat=str(coords[1]), lon=str(coords[0])),  # TODO: needs to convert coords to LocationXY
        )
        ret.status = soup.find('{%s}status' % self.__MUA).text
        return ret

    def _is_eligible(self, addr: Address) -> bool:
        # TODO: check status?
        if not addr:
            return False
        if addr.status.upper() not in ('ZATWIERDZONY', 'ISTNIEJACY'):
            self.__log.debug('Ignoring address %s, because status %s is not ZATWIERDZONY', addr, addr.status.upper())
            return False
        if '?' in addr.housenumber or 'bl' in addr.housenumber:
            self.__log.debug('Ignoring address %s because has strange housenumber: %s', addr, addr.housenumber)
            return False
        if not addr.get_point().within(self.shape):
            # do not report anything about this, this is normal
            return False
        return True

    def fetch_tiles(self) -> typing.List[Address]:
        # doc = self.soup.find('{%s}featureMembers' % self.__GML_NS)
        miejsc = {}  # type: typing.Dict[str, typing.Tuple[str, str]]
        for miejscowosc in self.soup.findall('.//{%s}AD_Miejscowosc' % self.__MUA):
            miejsc[miejscowosc.get('{%s}id' % self.__GML_NS)] = (
                miejscowosc.find('{%s}idTERYT' % self.__MUA).text,
                miejscowosc.find('{{{0}}}nazwa/{{{0}}}AD_EndonimStandaryzowany[{{{0}}}jezyk="pol"]/{{{0}}}nazwa'.format(
                    self.__MUA)).text
            )

        ulic = {}  # type: typing.Dict[str, typing.Tuple[str, str]]
        for ulica in self.soup.findall('.//{%s}AD_Ulica' % self.__MUA):
            nazwa_ulicy = ulica.find('{{{0}}}nazwa/{{{0}}}AD_NazwaUlicy'.format(self.__MUA))
            ulic[ulica.get('{%s}id' % self.__GML_NS)] = (
                nazwa_ulicy.find('{%s}idTERYT' % self.__MUA).text,
                nazwa_ulicy.find('{%s}nazwaGlownaCzesc' % self.__MUA).text
            )

        return [self._convert_to_address(x, ulic=ulic, miejsc=miejsc) for x in
                self.soup.findall('.//{%s}AD_PunktAdresowy' % self.__MUA) if self._is_eligible(x)]

