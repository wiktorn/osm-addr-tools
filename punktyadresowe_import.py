#!/usr/bin/env python3.4
# # -*- coding: UTF-8 -*-
#
# punktyadresowe_import.py CC-BY-NC-SA 3.0 WiktorN
#
# Based on work by Grzegorz Sapijaszko (http://wiki.openstreetmap.org/wiki/User:Gsapijaszko/punktyadresowe_import)
#
# dependencies:
# Beautiful-Soup (http://www.crummy.com/software/BeautifulSoup/)
#       pip install beautifulsoup4
#       easy_install beautifulsoup4
#       apt-get install python-beautifulsoup4
#       portmaster www/py-beautifulsoup
#
# TODO:
# - add spellchecking for street and city based on TERYT dictionaries
#       - street spellchecking - split into words and look for similar words in dictionary
#       - ideas: http://en.wikipedia.org/wiki/Levenshtein_distance , ngrams (http://en.wikipedia.org/wiki/N-gram), Norvig spell-checker - http://norvig.com/spell-correct.html

import sys
if sys.version_info.major == 2:
    from urllib import urlencode
    from urllib2 import urlparse, urlopen
    import urllib2 as urequest
    str_normalize = lambda x: x.decode('utf-8')
else:
    from urllib.parse import urlencode, urlparse
    import urllib.request as urequest
    from urllib.request import urlopen
    str_normalize = lambda x: x
    import urllib.request

import argparse
from bs4 import BeautifulSoup
from collections import namedtuple
from functools import partial
import itertools
import json
import logging
import math
import pyproj
import re
import uuid
import ssl
from shapely.geometry import Point

from osmdb import OsmDb, distance
import overpass
from mapping import mapstreet, mapcity, mappostcode
from utils import parallel_execution, groupby
import lxml.html
import lxml.etree
import rtree
import functools


# stałe
#_EPSG2180 = Proj(init='epsg:2180')

__log = logging.getLogger(__name__)
# User-Agent dla requestów
__opener = urequest.build_opener()
__headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
}
__opener.addheaders = __headers.items()


# setup
urequest.install_opener(__opener)

__WGS84 = pyproj.Proj(proj='latlong',datum='WGS84')
__EPSG2180 = pyproj.Proj(init="epsg:2180")

def wgsTo2180(lon, lat):
    # returns lon,lat
    return pyproj.transform(__WGS84, __EPSG2180, lon, lat)

def e2180toWGS(lon, lat):
    # returns lon,lat
    return srs_to_wgs('epsg:2180', lon, lat)

@functools.lru_cache(maxsize=None)
def getProj(srs):
    return pyproj.Proj(init=srs)

def srs_to_wgs(srs, lon, lat):
    return pyproj.transform(getProj(srs), __WGS84, lon, lat)

def _filterOnes(lst):
    return list(filter(lambda x: x > 0, lst))


def convertToOSM(lst):
    ret = """<?xml version='1.0' encoding='UTF-8'?>
<osm version='0.6' upload='false' generator='punktyadresowe_import.php'>
"""
    ret = BeautifulSoup("", "xml")
    osm = ret.new_tag('osm', version='0.6', upload='false', generator='punktyadresowe_import.py')
    ret.append(osm)

    for (node_id, val) in enumerate(lst):
        osm.append(val.asOsmSoup(-1 * (node_id + 1)))

    return ret.prettify()


class Address(object): #namedtuple('BaseAddress', ['housenumber', 'postcode', 'street', 'city', 'sym_ul', 'simc', 'source', 'location'])):
    __POSTCODE = re.compile('^[0-9]{2}-[0-9]{3}$')
    __NUMERIC = re.compile('^[0-9]*$')

    def __init__(self, housenumber='', postcode='', street='', city='', sym_ul='', simc='', source='', location='', id_='', last_change=''):
        self.housenumber = housenumber
        
        if simc and self.__NUMERIC.match(simc):
            self.simc = simc
        else:
            self.simc = ''

        if postcode and postcode != '00-000' and self.__POSTCODE.match(postcode):
            self.postcode = postcode
        else:
            self.postcode = ''

        if street:
            self.street = street
        else:
            self.street = ''

        self.city = city

        if sym_ul and self.__NUMERIC.match(sym_ul):
            self.sym_ul = sym_ul
        else:
            self.sym_ul = ''

        self.source = source
        self.location = location
        self._fixme = []
        self.id_ = id_
        self.last_change = last_change
        assert all(map(lambda x: isinstance(getattr(self, x, ''), str), ('housenumber', 'postcode', 'street', 'city', 'sym_ul', 'simc', 'source')))
        assert isinstance(self.location, dict)
        assert 'lon' in self.location
        assert 'lat' in self.location
        assert not street or street == street.strip()

    @staticmethod
    def mappedAddress(*args, **kwargs):
        ret = Address.mappedAddress_kpc(*args, **kwargs)
        ret.postcode = mappostcode('', ret.simc)
        return ret

    @staticmethod
    def mappedAddress_kpc(*args, **kwargs):
        ret = Address(*args, **kwargs)
        ret.housenumber = ret.housenumber.replace(' ', '')
        if ret.street:
            assert ret.street == ret.street.strip()
            newstreet = mapstreet(re.sub(' +', ' ', ret.street), ret.sym_ul)
            assert newstreet == newstreet.strip()
            ret.street = newstreet
        ret.city = mapcity(ret.city, ret.simc)
        return ret

    def addFixme(self, value):
        self._fixme.append(value)

    @property
    def fixmes(self):
        return self._fixme

    def getFixme(self):
        return ", ".join(self._fixme)

    def asOsmSoup(self, node_id):
        ret = BeautifulSoup("", "xml")
        node = ret.new_tag('node', id=node_id, action='modify', visible='true', lat=self.location['lat'], lon=self.location['lon'])
        def addTag(key, value):
            if value:
                node.append(ret.new_tag('tag', k=key, v=value))

        addTag('addr:housenumber', self.housenumber)
        addTag('addr:postcode', self.postcode)
        if self.street:
            addTag('addr:street', self.street)
            addTag('addr:city', self.city)
        else:
            addTag('addr:place', self.city)

        addTag('addr:city:simc', self.simc)
        addTag('addr:street:sym_ul', self.sym_ul)
        addTag('source:addr', self.source)
        if self._fixme:
            addTag('fixme', self.getFixme())
        return node

    def osOsmXML(self, node_id):
        return asOsmSoup.prettify()

    def getLatLon(self):
        return tuple(map(float, (self.location['lat'], self.location['lon'])))

    def get_point(self):
        return Point(reversed(self.getLatLon()))

    @property
    def center(self):
        return self.get_point()

    def similar_to(self, other):
        ret = True
        if self.id_ and other.id_ and self.id_ == other.id_:
            return True
        ret &= (other.housenumber.upper().replace(' ', '') == self.housenumber.upper().replace(' ', ''))
        if ret and (not self.city or not other.city):
            # we have similar housenumbers, but one of the points does't have a city
            if self.sym_ul and other.sym_ul:
                ret &= (self.sym_ul == other.sym_ul)
            else:
                ret &= (self.street == other.street)
            return ret

        if self.simc and other.simc and self.simc == other.simc:
            ret &= True
        else:
            ret &= (other.city == self.city)
        if self.sym_ul and other.sym_ul:
            ret &= (self.sym_ul == other.sym_ul)
            # skip comparing street names, might be a bit different
        return ret

    def __str__(self):
        if self.street:
            return "%s, %s, %s" % (self.city, self.street, self.housenumber)
        return "%s, %s" % (self.city, self.housenumber)

    def __repr__(self):
         return type(self).__name__ +"(" + ", ".join(
                                      "%s=%s" % (x, getattr(self, x)) for x in (
                                                        'housenumber', 'postcode',
                                                        'street', 'city', 'sym_ul',
                                                        'simc', 'source', 'location')
         ) + ")"

    def get_index_key(self):
        return tuple(map(str.upper, (self.city.strip(), self.street.strip(), self.housenumber.replace(' ', ''))))

    def to_JSON(self):
        return {
            'addr:housenumber': self.housenumber,
            'addr:postcode': self.postcode,
            'addr:street': self.street,
            'addr:city': self.city,
            'addr:street:sym_ul': self.sym_ul,
            'addr:city:simc': self.simc,
            'source:addr': self.source,
            'location': self.location,
            'fixme': ",".join(self._fixme),
            'id': self.id_,
            'last_change': self.last_change,
        }
    
    def to_geoJSON(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.location['lon'], self.location['lat']]
            },
            "properties": self.to_JSON()
        }

    @staticmethod
    def from_JSON(obj):
        ret = Address(
            housenumber = obj['addr:housenumber'],
            postcode    = obj.get('addr:postcode'),
            street      = obj.get('addr:street'),
            city        = obj.get('addr:city'),
            sym_ul      = obj.get('addr:street:sym_ul'),
            simc        = obj.get('addr:city:simc'),
            source      = obj['source:addr'],
            location    = obj['location'],
            id_         = obj['id'],
        )
        if obj.get('fixme'):
            ret.addFixme(obj['fixme'])
        return ret

    @staticmethod
    def from_osmXML(elem):
        tags = dict(
            (x.get('k'), x.get('v')) for x in elem if x.tag == 'tag'
        )
        if 'addr:place' in tags and 'addr:city' not in tags:
            tags['addr:city'] = tags['addr:place']
        tags['location'] = {
            'lon': elem.get('lon'),
            'lat': elem.get('lat')
        }
        return Address.from_JSON(tags)

class AbstractImport(object):
    __log = logging.getLogger(__name__).getChild('AbstractImport')

    def __init__(self, terc, *args, **kwargs):
        if terc:
            query = """
[out:json];
relation
    ["teryt:terc"="%s"]
    ["boundary"="administrative"]
    ["admin_level"~"[79]"];
out bb;
>;
out bb;
            """ % (terc,)
            data = json.loads(overpass.query(query))
            try:
                relation  = tuple(x for x in data['elements'] if x['type'] == 'relation')[0]
            except IndexError as e:
                raise IndexError("No relation found in OSM for TERC: %s" % (terc,), e)
            bounds = relation['bounds']
            self.bbox = (
                bounds['minlon'],
                bounds['minlat'],
                bounds['maxlon'],
                bounds['maxlat'],
            )
            osmdb = OsmDb(data)
            self.shape = osmdb.get_shape(relation)

    def getBbox(self):
        """
        this functions returns bbox of imported area using WGS84 lonlat as tuple:
        (minlon, minlat, maxlon, maxlat)
        """
        return self.bbox

    def getBbox2180(self):
        return wgsTo2180(*self.bbox[:2]) + wgsTo2180(*self.bbox[2:])

    def setBboxFrom2180(self, bbox):
        self.bbox = e2180toWGS(*bbox[:2]) + e2180toWGS(*bbox[2:])


    def fetchTiles(self):
        """
        this function returns list of Address'es of imported area
        """
        raise NotImplementedError("")

    def _checkDuplicatesInImport(self, data):
        addr_index = groupby(data, lambda x: (x.city, x.simc, x.housenumber.replace(' ', '').upper(), x.street))

        for (addr, occurances) in filter(lambda x: len(x[1]) > 1, addr_index.items()):
            self.__log.warning("Duplicate addresses in import: %s", occurances[0])
            uid = uuid.uuid4()
            for i in occurances:
                i.addFixme('Duplicate address in import (id: %s)' % (uid,))
            if any(
                    map(
                        lambda x: distance(x[0].center, x[1].center) > 100,
                        itertools.combinations(occurances, 2)
                    )
                ):
                self.__log.warning("Address points doesn't fit into 100m circle. Points count: %d", len(occurances))
                for addr in occurances:
                    addr.addFixme('(distance over 100m, points: %d)' % (len(occurances),))

    def _checkMixedScheme(self, data):
        dups = groupby(data, lambda x: x.simc, lambda x: bool(x.street))

        dups_count = dict((k, len(_filterOnes(v))) for k, v in dups.items())
        dups = dict((k, len(_filterOnes(v))/len(v)) for k, v in dups.items())
        dups = dict((k,v) for k, v in filter(lambda x: 0 < x[1] and x[1] < 1, dups.items()))

        for i in filter(
                lambda x: not bool(x.street) and x.simc in dups.keys(),
                data
                ):
            i.addFixme('Mixed addressing scheme in city - with streets and without. %.1f%% (%d) with streets.' % (dups[i.simc]*100, dups_count[i.simc]))

    def getAddresses(self):
        data = self.fetchTiles()
        self._checkDuplicatesInImport(data)
        self._checkMixedScheme(data)
        return data


class iMPA(AbstractImport):
    __log = logging.getLogger(__name__).getChild('iMPA')

    def __init__(self, gmina=None, wms=None, terc=None):
        self.wms = None

        if gmina:
            self._initFromIMPA(gmina)

        else:
            if not wms and not terc:
                raise ValueError("If no gmina provided then wms and terc are required")
            super(iMPA, self).__init__(terc=terc)

        if wms:
            self.wms = wms

        if not self.wms:
            raise ValueError("No WMS address found")

    def _initFromIMPA(self, gmina):
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

        def extract(begin, end):
            start_pos = data.rfind(begin)
            end_pos = data.find(end, start_pos)
            if start_pos < 0 or end_pos < 0:
                return None
            return data[start_pos + len(begin):end_pos]

        if len(init_data) > 0:
            self.setBboxFrom2180(init_data['spatialExtent'])
            self.terc = init_data.get('teryt')
            address_layers = list(
                        filter(
                            lambda x: x.get('title') and x['title'].upper() == 'ADRESY I ULICE',
                            init_data.get('map', {}).get('services', [{},])
                        )
                )
        else:
            bbox = extract('"spatialExtent":[', '],"').split(',')
            self.setBboxFrom2180(list(map(float, bbox)))
            self.terc = extract('"teryt":"', '","')
            address_layers = []

        if len(address_layers) == 0:
            self.__log.warning('No information about address layer in init.php')
            self.__log.debug(data)
            url = 'http://%s.punktyadresowe.pl' % (gmina,)
            self.__log.info(url)
            data = urlopen(url).read().decode('utf-8')
            def extract(begin, end):
                start_pos = data.rfind(begin)
                end_pos = data.find(end, start_pos)
                if start_pos < 0 or end_pos < 0:
                    return None
                return data[start_pos + len(begin):end_pos]
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

    def fetchPoint(self, wms_addr, w, s, e, n, pointx, pointy, layer="punkty"):
        params = {
            'VERSION': '1.1.1',
            'SERVICE': 'WMS',
            'REQUEST': 'GetFeatureInfo',
            'LAYERS': layer, # było: ulice,punkty
            'QUERY_LAYERS': layer, # było: ulice, punkty
            'FORMAT': 'image/png',
            'INFO_FORMAT': 'text/html',
            'SRS': 'EPSG:2180',
            'FEATURE_COUNT': '10000000', # wystarczająco dużo, by ogarnąć każdą sytuację
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
            'LAYERS': layer+',ulice',
            'FORMAT': 'image/png',
            'TRANSPARENT': 'true',
        }

        #TODO: do proper URL parsing
        if '?' in wms_addr:
            url = "%s&%s" % (wms_addr, urlencode(params))
            self.__log.warning("JOSM layer: %s&%s&SRS={proj}&WIDTH={width}&HEIGHT={height}&BBOX={bbox}" % (wms_addr, urlencode(josm_wms)))
        else:
            url = "%s?%s" % (wms_addr, urlencode(params))
            self.__log.warning("JOSM layer: %s?%s&SRS={proj}&WIDTH={width}&HEIGHT={height}&BBOX={bbox}" % (wms_addr, urlencode(josm_wms)))
        self.__log.info(url)
        data = urlopen(url).read()
        return data

    def _convertToAddress(self, soup):
        kv = dict(zip(
            map(lambda x: str(x.text), soup.find_all('th')),
            map(lambda x: str(x.text), soup.find_all('td'))
        ))
        try:
            (lon, lat) = map(lambda x: x[2:], kv[str_normalize('GPS (WGS 84)')].split(', ', 1))
            if '(' in kv[str_normalize('Nazwa ulicy(Id GUS)')]:
                (str_name, str_id) = kv[str_normalize('Nazwa ulicy(Id GUS)')].rsplit('(', 1)
            else:
                str_name = kv[str_normalize('Nazwa ulicy(Id GUS)')]
                str_id = ""
            (city_name, city_id) = kv[str_normalize('Miejscowość(Id GUS)')].rsplit('(', 1)

            if float(lon) < 14 or float(lon) > 25 or float(lat) < 49 or float(lat) > 56:
                self.__log.warning("Point out of Polish borders: (%s, %s), %s, %s, %s", lat, lon, city_name, str_name, kv[str_normalize('Numer')])

            return Address.mappedAddress(
                kv[str_normalize('Numer')],
                kv[str_normalize('Kod pocztowy')].strip(),
                str_name.strip(),
                city_name.strip(),
                str_id[:-1], # sym_ul
                city_id[:-1], # simc
                kv.get(str_normalize('Źródło danych'), ''),
                {'lat': lat, 'lon': lon}, # location
                kv.get(str_normalize('idIIP'), ''),
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

    def fetchTiles(self):
        html = self.fetchPoint(
            self.wms,
            *self.getBbox2180(),
            pointx=0, pointy=0 # sprawdź punkt (0,0) i tak powinno zostać zwrócone wszystko
        )
        ret = list(map(self._convertToAddress, BeautifulSoup(html).find_all('table')))
        return ret

class GUGiK(AbstractImport):
    # parametry do EPSG 2180
    __MAX_BBOX_X = 20000
    __MAX_BBOX_Y = 45000
    __PRECISION = 10
    __base_url = "http://emuia1.gugik.gov.pl/wmsproxy/emuia/wms?SERVICE=WMS&FORMAT=application/vnd.google-earth.kml+xml&VERSION=1.1.1&SERVICE=WMS&REQUEST=GetMap&LAYERS=emuia:layer_adresy_labels&STYLES=&SRS=EPSG:2180&WIDTH=16000&HEIGHT=16000&BBOX="
    __log = logging.getLogger(__name__).getChild('GUGiK')

    def __init__(self, terc):
        super(GUGiK, self).__init__(terc=terc)
        self.terc = terc

    @staticmethod
    def divideBbox(minx, miny, maxx, maxy):
        """divides bbox to tiles of maximum supported size by EMUiA WMS"""
        return [
            (x / GUGiK.__PRECISION,
             y / GUGiK.__PRECISION,
            min(x / GUGiK.__PRECISION + GUGiK.__MAX_BBOX_X, maxx),
            min(y / GUGiK.__PRECISION + GUGiK.__MAX_BBOX_Y, maxy))
            for x in range(math.floor(minx * GUGiK.__PRECISION), math.ceil(maxx * GUGiK.__PRECISION), GUGiK.__MAX_BBOX_X * GUGiK.__PRECISION)
            for y in range(math.floor(miny * GUGiK.__PRECISION), math.ceil(maxy * GUGiK.__PRECISION), GUGiK.__MAX_BBOX_Y * GUGiK.__PRECISION)
        ]

    def _convertToAddress(self, soup):
        desc_soup = lxml.html.fromstring(str(soup.find('{http://www.opengis.net/kml/2.2}description').text))
        addr_kv = dict(
            (
             str(x.find('strong').find('span').text),
             str(x.find('span').text)
            ) for x in desc_soup.find('ul').iterchildren()
        )

        coords = soup.find('{http://www.opengis.net/kml/2.2}Point').find('{http://www.opengis.net/kml/2.2}coordinates').text.split(',')
        ret = Address.mappedAddress(
                addr_kv[str_normalize('NUMER_PORZADKOWY')],
                addr_kv.get(str_normalize('KOD_POCZTOWY')),
                addr_kv.get(str_normalize('NAZWA_ULICY')),
                addr_kv[str_normalize('NAZWA_MIEJSCOWOSCI')],
                addr_kv.get(str_normalize('TERYT_ULICY')),
                addr_kv.get(str_normalize('TERYT_MIEJSCOWOSCI')),
                'emuia.gugik.gov.pl',
                {'lat': coords[1], 'lon': coords[0]},
                addr_kv.get(str_normalize('IDENTYFIKATOR_PUNKTU'))
        )
        ret.status = addr_kv[str_normalize('STATUS')]
        ret.wazny_do = addr_kv.get(str_normalize('WAZNY_DO'))
        ret.status_budynku = addr_kv.get(str_normalize('STATUS_BUDYNKU'))
        if not ret.wazny_do:
            ret.wazny_do = addr_kv.get(str_normalize('WERSJA_DO'))
        return ret

    def _isEligible(self, addr):
        # TODO: check status?
        if addr.status.upper() != 'ZATWIERDZONY':
            self.__log.debug('Ignoring address %s, because status %s is not ZATWIERDZONY', addr, addr.status.upper())
            return False
        if addr.wazny_do:
            self.__log.debug('Ignoring address %s, because it has set WAZNY_DO=%s', addr, addr.wazny_do)
            return False
        if '?' in addr.housenumber or 'bl' in addr.housenumber:
            self.__log.debug('Ignoring address %s because has strange housenumber: %s', addr, addr.housenumber)
            return False
        if addr.status_budynku and addr.status_budynku.upper() == 'PROGNOZOWANY':
            self.__log.debug('Ignoring address %s because STATUS_BUDYNKU = %s', addr, addr.status_budynku)
            return False
        if not addr.get_point().within(self.shape):
            # do not report anything about this, this is normal
            return False
        return True

    def fetchTiles(self):
        bbox = self.getBbox2180()
        ret = []
        for i in self.divideBbox(*bbox):
            url = GUGiK.__base_url+",".join(map(str, i))
            self.__log.info("Fetching from EMUIA: %s", url)

            opener = get_ssl_no_verify_opener()

            soup = lxml.etree.fromstring(opener.open(url).read())
            doc = soup.find('{http://www.opengis.net/kml/2.2}Document') # be namespace aware
            if doc is not None:
                ret.extend(filter(
                    self._isEligible,
                    map(self._convertToAddress, doc.iterchildren('{http://www.opengis.net/kml/2.2}Placemark'))
                    )
                )
            else:
                raise ValueError('No data returned from GUGiK possibly to wrong scale. Check __MAX_BBOX_X, __MAX_BBOX_Y, HEIGHT and WIDTH')
        # take latest version for each point (version is last element after dot in id_)
        ret = [max(v, key=lambda z: z.id_) for  v in groupby(ret, lambda z: z.id_.rsplit('.', 1)[0]).values()]
        return ret

class GISNET(AbstractImport):
    # parametry do EPSG 2180
    __MAX_BBOX_X = 20000
    __MAX_BBOX_Y = 45000
    __MAX_BBOX_X = 1000
    __MAX_BBOX_Y = 1000
    __PRECISION = 10
    __base_url = "http://%s.gis-net.pl/geoserver-%s/wms?SERVICE=WMS&FORMAT=application/vnd.google-earth.kml+xml&VERSION=1.1.1&SERVICE=WMS&REQUEST=GetMap&LAYERS=Punkty_Adresowe&STYLES=&SRS=EPSG:2180&WIDTH=1000&HEIGHT=1000&BBOX="
    __log = logging.getLogger(__name__).getChild('GISNET')

    def __init__(self, gmina, terc):
        super(GISNET, self).__init__(terc=terc)
        self.terc = terc
        self.gmina = gmina

    @staticmethod
    def divideBbox(minx, miny, maxx, maxy):
        """divides bbox to tiles of maximum supported size by EMUiA WMS"""
        return [
            (x / GISNET.__PRECISION,
             y / GISNET.__PRECISION,
            min(x / GISNET.__PRECISION + GISNET.__MAX_BBOX_X, maxx),
            min(y / GISNET.__PRECISION + GISNET.__MAX_BBOX_Y, maxy))
            for x in range(math.floor(minx * GISNET.__PRECISION), math.ceil(maxx * GISNET.__PRECISION), GISNET.__MAX_BBOX_X * GISNET.__PRECISION)
            for y in range(math.floor(miny * GISNET.__PRECISION), math.ceil(maxy * GISNET.__PRECISION), GISNET.__MAX_BBOX_Y * GISNET.__PRECISION)
        ]


    def _convertToAddress(self, soup):
        desc_soup = lxml.html.fromstring(str(soup.find('{http://www.opengis.net/kml/2.2}description').text))
        addr_kv = dict(
            (
             str(x.find('strong').find('span').text),
             str(x.find('span').text)
            ) for x in desc_soup.find('ul').iterchildren()
        )

        coords = soup.find('{http://www.opengis.net/kml/2.2}Point').find('{http://www.opengis.net/kml/2.2}coordinates').text.split(',')
        ret = Address.mappedAddress(
                addr_kv[str_normalize('numer_adr')],
                addr_kv.get(str_normalize('KOD_POCZTOWY')),
                addr_kv.get(str_normalize('nazwa_ulicy')),
                addr_kv[str_normalize('miejscowosc')],
                addr_kv.get(str_normalize('TERYT_ULICY')),
                addr_kv.get(str_normalize('TERYT_MIEJSCOWOSCI')),
                '%s.gis-net.pl' % (self.gmina,),
                {'lat': coords[1], 'lon': coords[0]},
                addr_kv.get(str_normalize('id_adres'))
        )
        ret.status = addr_kv[str_normalize('status')]
        return ret

    def _isEligible(self, addr):
        # TODO: check status?
        if addr.status.upper() != 'POGLĄDOWE':
            self.__log.debug('Ignoring address %s, because status %s is not ZATWIERDZONY', addr, addr.status.upper())
            return False
        if not addr.get_point().within(self.shape):
            # do not report anything about this, this is normal
            return False
        return True

    def fetchTiles(self):
        bbox = self.getBbox2180()
        ret = []
        for i in self.divideBbox(*bbox):
            url = GISNET.__base_url % (self.gmina, self.gmina) + ",".join(map(str, i))
            self.__log.info("Fetching from GISNET: %s", url)
            opener = get_ssl_no_verify_opener()

            data = opener.open(url).read()
            self.__log.debug("Reponse size: %d", len(data))
            soup = lxml.etree.fromstring(data)
            doc = soup.find('{http://www.opengis.net/kml/2.2}Document') # be namespace aware
            if doc is not None:
                ret.extend(filter(
                    self._isEligible,
                    map(self._convertToAddress, doc.iterchildren('{http://www.opengis.net/kml/2.2}Placemark'))
                    )
                )
            else:
                raise ValueError('No data returned from GISNET possibly to wrong scale. Check __MAX_BBOX_X, __MAX_BBOX_Y, HEIGHT and WIDTH')
        # take latest version for each point (version is last element after dot in id_)
        ret = [max(v, key=lambda z: z.id_) for  v in groupby(ret, lambda z: z.id_.rsplit('.', 1)[0]).values()]
        return ret

class WarszawaUM(AbstractImport):
    __base_url = "http://mapa.um.warszawa.pl/mapviewer/foi"
    # request zawiera odpytanie o obszar Warszawy w EPSG:2178
    __base_data = "request=getfoi&version=1.0&bbox=7489837.24855:5773796.99219:7518467.53701:5803895.93273&width=1&height=1&theme=dane_wawa.R_PUNKTY_ADRESOWE_TOOLTIP&clickable=yes&area=yes&dstsrid=2178&cachefoi=yes&tid=104_75201&aw=no"
    # request zawiera odpytanie o obszar Warszawy w EPSG:4326
    __base_data = "request=getfoi&version=1.0&bbox=20.8516882:52.0978507:21.2711512:52.3681531&width=1&height=1&theme=dane_wawa.R_PUNKTY_ADRESOWE_TOOLTIP&clickable=yes&area=yes&dstsrid=4326&cachefoi=yes&tid=104_75201&aw=no"
    __base_data = "request=getfoi&version=1.0&bbox=%s:%s:%s:%s&width=1&height=1&theme=dane_wawa.R_PUNKTY_ADRESOWE_TOOLTIP&clickable=yes&area=yes&dstsrid=4326&cachefoi=yes&tid=104_75201&aw=no"
    __log = logging.getLogger(__name__).getChild('WarszawaUM')

    def __init__(self, gmina, terc):
        super(WarszawaUM, self).__init__(terc=terc)
        self.terc = terc
        self.gmina = gmina
        self.gugik = GUGiK(terc)

    def _findNearest(self, point, street, housenumber):
        lst = list(
                map(self.gugik_data.get, self.gugik_index.nearest(point*2, 10))
            )
        for addr in lst:
            if addr.housenumber == housenumber:
                if street in addr.street:
                    return addr
                for street_part in street.split(' '):
                    if len(street_part) > 3 and street_part in addr.street:
                        #self.__log.debug("Found candidate %d m away. Street names: %s and %s", distance(point, (addr.location['lat'], addr.location['lon'])), street, addr.street)
                        return addr
                if len(street) > 7 and street[4:] in addr.street:
                    self.__log.debug("Found candidate %d m away. Street names: %s and %s", distance(point, (addr.location['lat'], addr.location['lon'])), street, addr.street)
                    return addr
                        
        ret = lst[0]
        if distance(point, ret.get_point()) > 100:
            self.__log.warn("Distance between address: %s, %s and nearest GUGiK: %s is %d. Not merging with GUGIK", street, housenumber, ret, distance(point, ret.get_point()))
            return None
        if ret.street != street:
            self.__log.debug("Different street in GUGiK than in mapa.um.warszawa.pl. GUGiK: %s, mapa: %s. Housenumber: %s", ret.street, street, housenumber)
            return None
        if ret.housenumber != housenumber:
            self.__log.debug("Different housenumber in GUGiK than in mapa.um.warszawa.pl. GUGiK: %s, mapa: %s, street: %s", ret.housenumber, housenumber, street)
        return ret

    def _convertToAddress(self, entry):
        desc_soup = entry['name'] 
        addr_kv = dict(x.split(': ', 2) for x in desc_soup.split('\n'))
        (street, housenumber) = addr_kv[str_normalize('Adres')].rsplit(' ',1)
        street = street.strip()
        if street.startswith('ul. '):
            street = street[4:]
        point = (float(entry['y']), float(entry['x']))
        if Point(reversed(point)).within(self.shape):
            nearest = self._findNearest(point, street, housenumber)
        else:
            nearest = None

        ret = Address.mappedAddress_kpc(
                housenumber,
                addr_kv.get(str_normalize('Kod pocztowy')),
                street,
                'Warszawa',
                nearest.sym_ul if nearest else None,
                nearest.simc if nearest else None, 
                'mapa.um.warszawa.pl',
                {'lat': entry['y'], 'lon': entry['x']},
                entry['id']
        )
        return ret

    def _isEligible(self, addr):
        if not addr.get_point().within(self.shape):
            # do not report anything about this, this is normal
            return False
        return True

    def fetchTiles(self):
        opener = get_ssl_no_verify_opener()
        data = opener.open(WarszawaUM.__base_url, (WarszawaUM.__base_data % self.getBbox()).encode('utf-8')).read().decode('utf-8')
        self.__log.debug("Reponse size: %d", len(data))
        return self.convertData(data)

    def convertData(self, data):
        d = re.sub(r"{(foiarray|id)", r'{"\1"', data)
        d = re.sub(r",(name|gtype|imgurl|x|y|width|height|attrnames|themeMBR|isWholeImg):", r',"\1":', d)
        parsed = json.loads(d)
        self.gugik_data = {}
        self.gugik_index = rtree.index.Index()
        for key, addr in enumerate(self.gugik.fetchTiles()):
            self.gugik_data[key] = addr
            self.gugik_index.insert(key,  (float(addr.location['lat']), float(addr.location['lon'])))
        return list(filter(self._isEligible, map(self._convertToAddress, parsed['foiarray'])))

class GUGiK_GML(AbstractImport):
    __log = logging.getLogger(__name__).getChild('GUGiK_GML')
    __GML_NS = "http://www.opengis.net/gml/3.2"
    __MUA = "urn:gugik:specyfikacje:gmlas:ewidencjaMiejscowosciUlicAdresow:1.0"
    __XLINK_HREF = "{http://www.w3.org/1999/xlink}href"

    def __init__(self, fname):
        self.soup = lxml.etree.fromstring(open(fname, 'rb').read())
        terc = max(
            map(
                lambda x: x.text, 
                self.soup.find('{%s}featureMembers' % self.__GML_NS).findall(
                    '{%s}AD_JednostkaAdministracyjna/{%s}idTERYT' % (self.__MUA, self.__MUA)
                )),
            key=len
        )
        super(GUGiK_GML, self).__init__(terc=terc)
        self.terc = terc

    def _convertToAddress(self, soup, ulic, miejsc):
        coords = soup.find('{%s}pozycja/{%s}Point' % (self.__MUA, self.__GML_NS))
        srs = coords.get('srsName')
        coords = coords.find('{%s}coordinates' % (self.__GML_NS))
        coords = srs_to_wgs(srs, *map(float,coords.text.split(coords.get('cs'))))

        ulica = ulic[soup.find('{%s}ulica2' % self.__MUA).get(self.__XLINK_HREF)]
        miejscowosc = miejsc[soup.find('{%s}miejscowosc' %self.__MUA).get(self.__XLINK_HREF)]

        ret = Address.mappedAddress(
                soup.find('{%s}numerPorzadkowy' % self.__MUA).text,
                soup.find('{%s}kodPocztowy' % self.__MUA).text,
                ulica[1],
                miejscowosc[1],
                ulica[0],
                miejscowosc[0],
                'emuia.gugik.gov.pl',
                {'lat': coords[1], 'lon': coords[0]},
                None,
        )
        ret.status = soup.find('{%s}status' % (self.__MUA)).text
        return ret

    def _isEligible(self, addr):
        # TODO: check status?
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

    def fetchTiles(self):
        doc = self.soup.find('{%s}featureMembers' % self.__GML_NS)
        miejsc = {}
        for miejscowosc in doc.iterchildren('{%s}AD_Miejscowosc' % self.__MUA):
            miejsc[miejscowosc.get('{%s}id' % self.__GML_NS)] = (
                miejscowosc.find('{%s}idTERYT' % self.__MUA).text,
                miejscowosc.find('{{{0}}}nazwa/{{{0}}}AD_EndonimStandaryzowany[{{{0}}}jezyk="pol"]/{{{0}}}nazwa'.format(self.__MUA)).text
            )

        ulic = {}
        for ulica in doc.iterchildren('{%s}AD_Ulica' % self.__MUA):
            nazwa_ulicy = ulica.find('{{{0}}}nazwa/{{{0}}}AD_NazwaUlicy'.format(self.__MUA))
            ulic[ulica.get('{%s}id' % self.__GML_NS)] = (
                nazwa_ulicy.find('{%s}idTERYT' % self.__MUA).text,
                nazwa_ulicy.find('{%s}nazwaGlownaCzesc' % self.__MUA).text
            )

        ret = list(filter(
            self._isEligible,
            map(partial(self._convertToAddress, ulic=ulic, miejsc=miejsc), doc.iterchildren('{%s}AD_PunktAdresowy' % self.__MUA))
        ))

        return ret

class AddressEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Address):
            return obj.to_JSON()
        return json.JSONEncoder.default(self, obj)

def get_ssl_no_verify_opener():

    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    https_handler = urllib.request.HTTPSHandler(context=ssl_ctx, check_hostname=False)
    return urllib.request.build_opener(https_handler)

def main():
    parser = argparse.ArgumentParser(description="Downloads data from iMPA and saves in OSM or JSON format. CC-BY-SA 3.0 @ WiktorN. Filename is <gmina>.osm or <gmina>.json")
    parser.add_argument('--output-format', choices=['json', 'osm'],  help='output file format - "json" or "osm", default: osm', default="osm", dest='output_format')
    parser.add_argument('--source', choices=['impa', 'gugik', 'gugik_gml', 'gisnet', 'warszawa'],  help='input source: "gugik", "impa", "gisnet" or "warszawa". Gugik, gisnet and warszawa requires providing teryt:terc code. gugik_gml requires to provide a filename as gmina. Defaults to "impa"', default="impa", dest='source')
    parser.add_argument('--log-level', help='Set logging level (debug=10, info=20, warning=30, error=40, critical=50), default: 20', dest='log_level', default=20, type=int)
    parser.add_argument('--no-mapping', help='Disable mapping of streets and cities', dest='no_mapping', default=False, action='store_const', const=True)
    parser.add_argument('--wms', help='Override WMS address with address points', dest='wms', default=None)
    parser.add_argument('--terc', help='teryt:terc code which defines area of operation', dest='terc', default=None)
    parser.add_argument('gmina', nargs='*',  help='list of iMPA services to download, it will use at most 4 concurrent threads to download and analyse')
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    if args.no_mapping:
        global mapstreet, mapcity
        mapstreet = lambda x, y: x
        mapcity = lambda x, y: x
    if args.source == "impa":
        imp_gen = partial(iMPA, wms=args.wms, terc=args.terc)
    elif args.source == "gugik":
        imp_gen = partial(GUGiK, terc=args.terc)
    elif args.source == "gisnet":
        imp_gen = partial(GISNET, terc=args.terc)
        if not args.gmina:
            raise Exception("You need to provide service name")
    elif args.source == 'warszawa':
        imp_gen = partial(WarszawaUM, terc=args.terc)
    elif args.source == 'gugik_gml':
        imp_gen = partial(GUGiK_GML)
    else:
        raise Exception("Source not supported")
    if args.gmina:
        #rets = parallel_execution(*map(lambda x: lambda: imp_gen(x).getAddresses(), args.gmina))
        rets = list(map(lambda x: imp_gen(x).getAddresses(), args.gmina)) # usefull for debugging
    else:
        rets = [imp_gen().getAddresses(),]
    if args.output_format == 'json':
        write_conv_func = lambda x: json.dumps(list(x), cls=AddressEncoder)
        file_suffix = '.json'
    else:
        write_conv_func = convertToOSM
        file_suffix = '.osm'

    if args.gmina:
        for (ret, gmina) in zip(rets, args.gmina):
            with open(gmina+file_suffix, "w+", encoding='utf-8') as f:
                f.write(write_conv_func(ret))
    else:
        fname = 'result.osm'
        if args.terc:
            fname = '%s.osm' % (args.terc,)
        with open(fname, 'w+', encoding='utf-8') as f:
            f.write(write_conv_func(rets[0]))

if __name__ == '__main__':
    main()
