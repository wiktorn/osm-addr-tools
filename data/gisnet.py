import logging
import math

import lxml.html
import tqdm

from .base import AbstractImport, Address, get_ssl_no_verify_opener
from utils.utils import groupby


class GISNET(AbstractImport):
    # parametry do EPSG 2180
    # __MAX_BBOX_X = 20000
    # __MAX_BBOX_Y = 45000
    __MAX_BBOX_X = 1000
    __MAX_BBOX_Y = 1000
    __PRECISION = 10
    __base_url = (
        "http://%s.gis-net.pl/geoserver-%s/wms?SERVICE=WMS&FORMAT=application/vnd.google-earth.kml+xml&"
        "VERSION=1.1.1&SERVICE=WMS&REQUEST=GetMap&LAYERS=Punkty_Adresowe&STYLES=&SRS=EPSG:2180&WIDTH=1000&"
        "HEIGHT=1000&BBOX="
    )
    __log = logging.getLogger(__name__).getChild("GISNET")

    def __init__(self, gmina, terc):
        super(GISNET, self).__init__(terc=terc)
        self.terc = terc
        self.gmina = gmina

    @staticmethod
    def divide_bbox(minx, miny, maxx, maxy):
        """divides bbox to tiles of maximum supported size by EMUiA WMS"""
        # noinspection PyTypeChecker
        return [
            (
                x / GISNET.__PRECISION,
                y / GISNET.__PRECISION,
                min(x / GISNET.__PRECISION + GISNET.__MAX_BBOX_X, maxx),
                min(y / GISNET.__PRECISION + GISNET.__MAX_BBOX_Y, maxy),
            )
            for x in range(
                math.floor(minx * GISNET.__PRECISION),
                math.ceil(maxx * GISNET.__PRECISION),
                GISNET.__MAX_BBOX_X * GISNET.__PRECISION,
            )
            for y in range(
                math.floor(miny * GISNET.__PRECISION),
                math.ceil(maxy * GISNET.__PRECISION),
                GISNET.__MAX_BBOX_Y * GISNET.__PRECISION,
            )
        ]

    def _convert_to_address(self, soup) -> Address:
        desc_soup = lxml.html.fromstring(
            str(soup.find("{http://www.opengis.net/kml/2.2}description").text)
        )
        addr_kv = dict(
            (str(x.find("strong").find("span").text), str(x.find("span").text))
            for x in desc_soup.find("ul").iterchildren()
        )

        coords = (
            soup.find("{http://www.opengis.net/kml/2.2}Point")
            .find("{http://www.opengis.net/kml/2.2}coordinates")
            .text.split(",")
        )
        ret = Address.mapped_address(
            addr_kv["numer_adr"],
            addr_kv.get("KOD_POCZTOWY"),
            addr_kv.get("nazwa_ulicy"),
            addr_kv["miejscowosc"],
            addr_kv.get("TERYT_ULICY"),
            addr_kv.get("TERYT_MIEJSCOWOSCI"),
            "%s.gis-net.pl" % (self.gmina,),
            {"lat": coords[1], "lon": coords[0]},
            addr_kv.get("id_adres"),
        )
        ret.status = addr_kv["status"]
        return ret

    def _is_eligible(self, addr: Address):
        # TODO: check status?
        if addr.status.upper() != "POGLĄDOWE":
            self.__log.debug(
                "Ignoring address %s, because status %s is not ZATWIERDZONY",
                addr,
                addr.status.upper(),
            )
            return False
        if not addr.get_point().within(self.shape):
            # do not report anything about this, this is normal
            return False
        return True

    def fetch_tiles(self):
        bbox = self.get_bbox_2180()
        ret = []
        for i in tqdm.tqdm(self.divide_bbox(*bbox), "Download"):
            url = GISNET.__base_url % (self.gmina, self.gmina) + ",".join(map(str, i))
            self.__log.info("Fetching from GISNET: %s", url)
            opener = get_ssl_no_verify_opener()

            data = opener.open(url).read()
            self.__log.debug("Reponse size: %d", len(data))
            soup = lxml.etree.fromstring(data)
            doc = soup.find(
                "{http://www.opengis.net/kml/2.2}Document"
            )  # be namespace aware
            if doc is not None:
                ret.extend(
                    filter(
                        self._is_eligible,
                        map(
                            self._convert_to_address,
                            doc.iterchildren(
                                "{http://www.opengis.net/kml/2.2}Placemark"
                            ),
                        ),
                    )
                )
            else:
                raise ValueError(
                    "No data returned from GISNET possibly to wrong scale. Check __MAX_BBOX_X, "
                    "__MAX_BBOX_Y, HEIGHT and WIDTH"
                )
        # take latest version for each point (version is last element after dot in id_)
        ret = [
            max(v, key=lambda z: z.id_)
            for v in groupby(ret, lambda z: z.id_.rsplit(".", 1)[0]).values()
        ]
        return ret
