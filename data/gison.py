import json
import logging
import re
from urllib.parse import urlencode
from urllib.request import urlopen

from data.base import AbstractImport, Address, e2180toWGS


class GISON(AbstractImport):
    __base_url = "http://portal.gison.pl/"
    # http://portal.gison.pl/brzeznica/
    # http://portal.gison.pl/brzeznica/js/map_config.js
    # szukamy: var searchAdminService="administracja.gison.pl/websearch/Handler1.ashx"
    #           var osmid=-2659216;
    # http://administracja.gison.pl/websearch/Handler1.ashx?typ=adresygemaOL&osmid=-2659216&
    # maxrows=10000&lang=en&continentCode=&adminCode1=&adminCode2=&adminCode3=&tag=&charset=UTF8&nazwa=
    __log = logging.getLogger(__name__).getChild('GISON')

    def __init__(self, gmina, terc):
        super(GISON, self).__init__(terc=terc)
        self.terc = terc
        self.gmina = gmina
        url = self.__base_url + self.gmina + "/js/map_config.js"
        self.__log.debug("Fetching configuration from: %s", url)
        map_config = urlopen(url).read().decode('utf-8')

        def make_extract(data):
            def extract(begin, end):
                start_pos = data.rfind(begin)
                end_pos = data.find(end, start_pos + 1)
                if start_pos < 0 or end_pos < 0:
                    return None
                return data[start_pos + len(begin):end_pos]

            return extract

        map_config_extract = make_extract(map_config)
        self.searchAdminService = map_config_extract("var searchAdminService=\"", "\"\n")
        if not self.searchAdminService:
            raise ValueError("Could not find searchAdminService")
        self.osmid = map_config_extract("var osmid=-", ";")
        self.lonlat_conv = lambda x, y: (x, y)

    def _convert_to_address(self, addr):
        # {'lat': 49.96449599576943, 'lng': 19.63283898037835, 'toponymName': 'Adama Gorczyńskiego 1, Brzeźnica',
        # 'fcodeName': 'ul. ', 'obreb': 'null', 'geom': None}
        street = ""
        if ',' in addr['toponymName']:
            streetnumber, city = map(str.strip, addr['toponymName'].rsplit(',', 1))
            street, housenumber = map(str.strip, streetnumber.rsplit(' ', 1))
        else:
            city, housenumber = map(str.strip, addr['toponymName'].rsplit(' ', 1))

        old_housenumber = None
        if 'stary numer' in city:
            m = re.search('^([^(]*) \(stary numer: (.+)( \))?$', city)
            city = m.group(1)
            old_housenumber = m.group(2)
        lon, lat = self.lonlat_conv(addr['lng'], addr['lat'])
        ret = Address.mapped_address(
            housenumber,
            '',
            street,
            city,
            '',  # teryt ulicy
            '',  # teryt miejscowosci
            self.__base_url + self.gmina,
            {'lat': lat, 'lon': lon},
            ''  # identyfikator punktu
        )
        if old_housenumber:
            ret.add_extra_tag('addr:houseumber_old', old_housenumber)
        return ret

    def fetch_tiles(self):
        def real_fetch(parameters):
            url = "http://" + self.searchAdminService + '?' + urlencode(parameters)
            self.__log.debug("Fetching data from URL: %s", url)
            resp = urlopen(url).read().decode('utf-8')
            ret_data = json.loads('[' + resp[1:-1] + ']')
            return ret_data

        maxrows = 20000
        params = {
            'osmid': "-" + self.osmid,
            'typ': 'adresygemaOL',
            'maxrows': maxrows,
            'lang': 'en',
            'continentCode': '',
            'adminCode1': '',
            'adminCode2': '',
            'adminCode3': '',
            'tag': '',
            'charset': 'UTF8',
            'nazwa': ''
        }
        data = real_fetch(params)
        if len(data[0]['geonames']) != data[0]['totalResultsCount'] or data[0]['totalResultsCount'] == maxrows or \
                data[0]['totalResultsCount'] == 0:
            params['typ'] = 'adresy'
            data = real_fetch(params)
            # adresy layer uses EPSG:2180, and adresygemaOL uses WGS84/EPSG:4326
            self.lonlat_conv = e2180toWGS
            if len(data[0]['geonames']) != data[0]['totalResultsCount'] or data[0]['totalResultsCount'] == maxrows:
                raise ValueError(
                    "Problem fetching data. {0} available to parse, while totalResulsts is {1}. Maxrows was {2}".format(
                        len(data[0]['geonames']), data[0]['totalResultsCount'], maxrows))

        ret = list(map(self._convert_to_address, data[0]['geonames']))
        return ret
