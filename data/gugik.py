import logging
import re
from functools import partial

import lxml.html
import tqdm

import converters.emuia
from data.base import AbstractImport, Address, srs_to_wgs, e2180toWGS


def nvl(obj, replacement):
    return obj if obj else replacement


class GUGiK(AbstractImport):
    # parametry do EPSG 2180
    __MAX_BBOX_X = 20000
    __MAX_BBOX_Y = 45000
    __PRECISION = 10
    __base_url = (
        "http://emuia1.gugik.gov.pl/wmsproxy/emuia/wms?SERVICE=WMS&"
        "FORMAT=application/vnd.google-earth.kml+xml&VERSION=1.1.1&"
        "SERVICE=WMS&REQUEST=GetMap&LAYERS=emuia:layer_adresy_labels&STYLES=&"
        "SRS=EPSG:2180&WIDTH=16000&HEIGHT=16000&BBOX="
    )

    __log = logging.getLogger(__name__).getChild("GUGiK")
    __NUMER_RE = re.compile("(\d+)\s((?=\d+))")

    def __init__(self, terc):
        super(GUGiK, self).__init__(terc=terc)
        self.terc = terc

    def _convert_to_address(self, dct) -> Address:
        coords = e2180toWGS(dct["pktY"], dct["pktX"])
        ret = Address.mapped_address(
            dct["pktNumer"],
            nvl(dct.get("pktKodPocztowy"), ""),
            (
                nvl(dct.get("ulNazwaCzesc"), "")
                + " "
                + nvl(dct.get("ulNazwaGlowna"), "")
            ).strip(),
            dct["miejscNazwa"],
            dct.get("ulIdTeryt"),
            dct.get("miejscIdTeryt"),
            "emuia.gugik.gov.pl",
            {"lat": coords[1], "lon": coords[0]},
            dct.get("pktEmuiaIIPId", ""),
        )
        ret.status = dct["pktStatus"]
        return ret

    def _is_eligible(self, addr: Address) -> bool:
        # TODO: check status?
        if addr.status.upper() != "ISTNIEJACY":
            self.__log.debug(
                "Ignoring address %s, because status %s is not ISTNIEJACY",
                addr,
                addr.status.upper(),
            )
            return False
        if "?" in addr.housenumber or "bl" in addr.housenumber:
            self.__log.debug(
                "Ignoring address %s because has strange housenumber: %s",
                addr,
                addr.housenumber,
            )
            return False
        return True

    def fetch_tiles(self):
        return [
            x
            for x in [
                self._convert_to_address(x["adres"])
                for x in tqdm.tqdm(
                    converters.emuia.get_addresses(self.terc), desc="Conversion"
                )
            ]
            if self._is_eligible(x)
        ]


class GUGiK_GML(AbstractImport):
    __log = logging.getLogger(__name__).getChild("GUGiK_GML")
    __GML_NS = "http://www.opengis.net/gml/3.2"
    __MUA = "urn:gugik:specyfikacje:gmlas:ewidencjaMiejscowosciUlicAdresow:1.0"
    __XLINK_HREF = "{http://www.w3.org/1999/xlink}href"

    def __init__(self, fname):
        self.soup = lxml.etree.fromstring(open(fname, "rb").read())
        terc = max(
            (
                x.text
                for x in self.soup.findall(
                    ".//{{{0}}}AD_JednostkaAdministracyjna/{{{0}}}idTERYT".format(
                        self.__MUA
                    )
                )
            ),
            key=len,
        )
        #    map(
        #        lambda x: x.text,
        #        self.soup.find('{%s}featureMembers' % self.__GML_NS).findall(
        #            '{%s}AD_JednostkaAdministracyjna/{%s}idTERYT' % (self.__MUA, self.__MUA)
        #        )),
        #    key=len
        # )
        super(GUGiK_GML, self).__init__(terc=terc)
        self.terc = terc

    def _convert_to_address(self, soup, ulic, miejsc):
        point = soup.find("{%s}pozycja/{%s}Point" % (self.__MUA, self.__GML_NS))
        srs = point.get("srsName")
        coords_el = point.find("{%s}coordinates" % (self.__GML_NS))
        if coords_el:
            coords = srs_to_wgs(
                srs, *map(float, coords_el.text.split(coords_el.get("cs")))
            )
        else:
            coords_el = point.find("{{{0}}}pos".format(self.__GML_NS))
            coords = [float(x) for x in coords_el.text.split(" ")]
            if coords_el.get("axisLabels") == "Y X":
                coords = srs_to_wgs(srs, *reversed(coords))
            else:
                coords = srs_to_wgs(srs, *reversed(coords))

        try:
            ulica = ulic[soup.find("{%s}ulica2" % self.__MUA).get(self.__XLINK_HREF)]
        except KeyError:
            self.__log.error(
                "No name for ulica: %s"
                % (soup.find("{%s}ulica2" % self.__MUA).get(self.__XLINK_HREF),)
            )
            return None
        try:
            miejscowosc = miejsc[
                soup.find("{%s}miejscowosc" % self.__MUA).get(self.__XLINK_HREF)
            ]
        except KeyError:
            self.__log.error(
                "No name for miejscowosc: %s"
                % (soup.find("{%s}miejscowosc" % self.__MUA).get(self.__XLINK_HREF),)
            )
            return None

        ret = Address.mapped_address(
            soup.find("{%s}numerPorzadkowy" % self.__MUA).text,
            soup.find("{%s}kodPocztowy" % self.__MUA).text,
            ulica[1],
            miejscowosc[1],
            ulica[0],
            miejscowosc[0],
            "emuia.gugik.gov.pl",
            {"lat": coords[1], "lon": coords[0]},
            None,
        )
        ret.status = soup.find("{%s}status" % self.__MUA).text
        return ret

    def _is_eligible(self, addr: Address):
        # TODO: check status?
        if not addr:
            return False
        if addr.status.upper() not in ("ZATWIERDZONY", "ISTNIEJACY"):
            self.__log.debug(
                "Ignoring address %s, because status %s is not ZATWIERDZONY",
                addr,
                addr.status.upper(),
            )
            return False
        if "?" in addr.housenumber or "bl" in addr.housenumber:
            self.__log.debug(
                "Ignoring address %s because has strange housenumber: %s",
                addr,
                addr.housenumber,
            )
            return False
        if not addr.get_point().within(self.shape):
            # do not report anything about this, this is normal
            return False
        return True

    def fetch_tiles(self):
        # doc = self.soup.find('{%s}featureMembers' % self.__GML_NS)
        miejsc = {}
        for miejscowosc in self.soup.findall(".//{%s}AD_Miejscowosc" % self.__MUA):
            miejsc[miejscowosc.get("{%s}id" % self.__GML_NS)] = (
                miejscowosc.find("{%s}idTERYT" % self.__MUA).text,
                miejscowosc.find(
                    '{{{0}}}nazwa/{{{0}}}AD_EndonimStandaryzowany[{{{0}}}jezyk="pol"]/{{{0}}}nazwa'.format(
                        self.__MUA
                    )
                ).text,
            )

        ulic = {}
        for ulica in self.soup.findall(".//{%s}AD_Ulica" % self.__MUA):
            nazwa_ulicy = ulica.find(
                "{{{0}}}nazwa/{{{0}}}AD_NazwaUlicy".format(self.__MUA)
            )
            ulic[ulica.get("{%s}id" % self.__GML_NS)] = (
                nazwa_ulicy.find("{%s}idTERYT" % self.__MUA).text,
                nazwa_ulicy.find("{%s}nazwaGlownaCzesc" % self.__MUA).text,
            )

        ret = list(
            filter(
                self._is_eligible,
                map(
                    partial(self._convert_to_address, ulic=ulic, miejsc=miejsc),
                    self.soup.findall(".//{%s}AD_PunktAdresowy" % self.__MUA),
                ),
            )
        )

        return ret
