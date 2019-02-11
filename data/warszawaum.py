import json
import logging
import re
import typing

import rtree
import tqdm

from data.base import AbstractImport, Address, get_ssl_no_verify_opener, LocationStr
from data.gugik import GUGiK
from osmdb import distance, buffered_shape_poland


class WarszawaUM(AbstractImport):
    __base_url = "http://mapa.um.warszawa.pl/mapviewer/foi"
    # request zawiera odpytanie o obszar Warszawy w EPSG:2178
    # __base_data = "request=getfoi&version=1.0&bbox=7489837.24855:5773796.99219:7518467.53701:5803895.93273&width=1&
    # height=1&theme=dane_wawa.R_PUNKTY_ADRESOWE_TOOLTIP&clickable=yes&area=yes&dstsrid=2178&cachefoi=yes&tid=104_75201&
    # aw=no"
    # request zawiera odpytanie o obszar Warszawy w EPSG:4326
    # __base_data = "request=getfoi&version=1.0&bbox=20.8516882:52.0978507:21.2711512:52.3681531&width=1&height=1&
    # theme=dane_wawa.R_PUNKTY_ADRESOWE_TOOLTIP&clickable=yes&area=yes&dstsrid=4326&cachefoi=yes&tid=104_75201&aw=no"
    __base_data = "request=getfoi&version=1.0&bbox=%s:%s:%s:%s&width=1&height=1&" \
                  "theme=dane_wawa.R_PUNKTY_ADRESOWE_TOOLTIP&clickable=yes&area=yes&" \
                  "dstsrid=4326&cachefoi=yes&tid=104_75201&aw=no"
    __log = logging.getLogger(__name__).getChild('WarszawaUM')

    def __init__(self, gmina: str, terc: str):
        super(WarszawaUM, self).__init__(terc=terc)
        self.terc = terc
        self.gmina = gmina
        # GUGIK dictionary has only whole Warsaw
        self.gugik = GUGiK("1465011")
        self.gugik_data = {}
        self.gugik_index = rtree.index.Index()
        self.buffered_shape = buffered_shape_poland(self.shape, 500)

    def _find_nearest(self, location: LocationStr, street:str, housenumber: str) -> typing.Optional[Address]:
        lst = list(
            map(self.gugik_data.get, self.gugik_index.nearest((location.lat, location.lon) * 2, 10))
        )  # type: typing.List[Address]
        for addr in lst:
            if addr.housenumber == housenumber:
                if street in addr.street:
                    return addr
                for street_part in street.split(' '):
                    if len(street_part) > 3 and street_part in addr.street:
                        return addr
                if len(street) > 7 and street[4:] in addr.street:
                    self.__log.debug("Found candidate %d m away. Street names: %s and %s",
                                     distance(location, addr.location), street, addr.street)
                    return addr

        ret = lst[0]
        if distance(location, ret.get_point()) > 100:
            self.__log.warn("Distance between address: %s, %s and nearest GUGiK: %s is %d. Not merging with GUGIK",
                            street, housenumber, ret, distance(location, ret.get_point()))
            return None
        if ret.street != street:
            self.__log.debug(
                "Different street in GUGiK than in mapa.um.warszawa.pl. GUGiK: %s, mapa: %s. Housenumber: %s",
                ret.street, street, housenumber)
            return None
        if ret.housenumber != housenumber:
            self.__log.debug(
                "Different housenumber in GUGiK than in mapa.um.warszawa.pl. GUGiK: %s, mapa: %s, street: %s",
                ret.housenumber, housenumber, street)
        return ret

    def _convert_to_address(self, entry: typing.Dict[str, str]):
        desc_soup = entry['name']
        addr_kv = dict(x.split(': ', 2) for x in desc_soup.split('\n'))  # type: typing.Dict[str, str]
        (street, housenumber) = addr_kv['Adres'].rsplit(' ', 1)
        street = street.strip()
        if street.startswith('ul. '):
            street = street[4:]
        location = LocationStr(lat=entry['y'], lon=entry['x'])

        if location.to_location().to_point().within(self.buffered_shape):
            nearest = self._find_nearest(location, street, housenumber)
        else:
            nearest = None

        ret = Address.mapped_address_kpc(
            housenumber=housenumber,
            postcode=addr_kv.get('Kod pocztowy'),
            street=street,
            city='Warszawa',
            sym_ul=nearest.sym_ul if nearest else None,
            simc=nearest.simc if nearest else None,
            source='mapa.um.warszawa.pl',
            location=LocationStr(lat=entry['y'], lon=entry['x']),
            id_=entry['id']
        )
        return ret

    def _is_eligible(self, addr):
        if not addr.get_point().within(self.buffered_shape):
            # do not report anything about this, this is normal
            return False
        return True

    def fetch_tiles(self):
        opener = get_ssl_no_verify_opener()
        data = opener.open(WarszawaUM.__base_url,
                           (WarszawaUM.__base_data % self.get_bbox()).encode('utf-8')).read().decode('utf-8')
        self.__log.debug("Reponse size: %d", len(data))
        return self.convert_data(data)

    def convert_data(self, data):
        d = re.sub(r"{(foiarray|id)", r'{"\1"', data)
        d = re.sub(r",(name|gtype|imgurl|x|y|width|height|attrnames|themeMBR|isWholeImg):", r',"\1":', d)
        parsed = json.loads(d)
        for key, addr in enumerate(self.gugik.fetch_tiles()):
            self.gugik_data[key] = addr
            self.gugik_index.insert(key, (float(addr.location.lat), float(addr.location.lon)))
        return [x for x in [self._convert_to_address(x) for x in tqdm.tqdm(parsed['foiarray'],
                                                                           desc="Conversion")] if self._is_eligible(x)]
