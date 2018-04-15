import functools
import itertools
import json
import logging
import re
import ssl
import urllib.request
import uuid
from urllib import request as urequest

import pyproj
from bs4 import BeautifulSoup
from shapely.geometry import Point

import overpass
from osmdb import OsmDb, distance
from utils.mapping import mapstreet, mapcity, mappostcode
from utils.utils import groupby

__log = logging.getLogger(__name__)
__opener = urequest.build_opener()
__headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
}
# User-Agent dla requestów
__opener.addheaders = __headers.items()

# setup
urequest.install_opener(__opener)

__WGS84 = pyproj.Proj(proj='latlong', datum='WGS84')
__EPSG2180 = pyproj.Proj(init="epsg:2180")


def wgsTo2180(lon, lat):
    # returns lon,lat
    return pyproj.transform(__WGS84, __EPSG2180, lon, lat)


def e2180toWGS(lon, lat):
    # returns lon,lat
    return srs_to_wgs('epsg:2180', lon, lat)


@functools.lru_cache(maxsize=None)
def get_proj(srs):
    return pyproj.Proj(init=srs)


def srs_to_wgs(srs, lon, lat):
    if srs.startswith("urn:ogc:def:crs:"):
        srs = srs[16:].replace('::', ':')
    return pyproj.transform(get_proj(srs), __WGS84, lon, lat)


def _filter_ones(lst):
    return list(filter(lambda x: x > 0, lst))


def convert_to_osm(lst):
    ret = BeautifulSoup("", "xml")
    osm = ret.new_tag('osm', version='0.6', upload='false', generator='punktyadresowe_import.py')
    ret.append(osm)

    for (node_id, val) in enumerate(lst):
        osm.append(val.as_osm_soup(-1 * (node_id + 1)))

    return ret.prettify()


class Address(object):
    __POSTCODE = re.compile('^[0-9]{2}-[0-9]{3}$')
    __NUMERIC = re.compile('^[0-9]*$')

    def __init__(self, housenumber='', postcode='', street='', city='', sym_ul='', simc='', source='', location={},
                 id_='', last_change=''):
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
        self.extra_tags = {}
        assert all(map(lambda x: isinstance(getattr(self, x, ''), str),
                       ('housenumber', 'postcode', 'street', 'city', 'sym_ul', 'simc', 'source')))
        assert isinstance(self.location, dict)
        assert 'lon' in self.location
        assert 'lat' in self.location
        assert not street or street == street.strip()

    @staticmethod
    def mapped_address(*args, **kwargs):
        ret = Address.mapped_address_kpc(*args, **kwargs)
        ret.postcode = mappostcode('', ret.simc)
        return ret

    @staticmethod
    def mapped_address_kpc(*args, **kwargs):
        ret = Address(*args, **kwargs)
        ret.housenumber = ret.housenumber.strip()
        if ret.street:
            assert ret.street == ret.street.strip()
            newstreet = mapstreet(re.sub(' +', ' ', ret.street), ret.sym_ul)
            assert newstreet == newstreet.strip()
            ret.street = newstreet
        ret.city = mapcity(ret.city, ret.simc)
        return ret

    def add_fixme(self, value):
        self._fixme.append(value)

    @property
    def fixmes(self):
        return self._fixme

    def get_fixme(self):
        return ", ".join(self._fixme)

    def clear_fixme(self):
        self._fixme = []

    def as_osm_soup(self, node_id):
        ret = BeautifulSoup("", "xml")
        node = ret.new_tag('node', id=node_id, action='modify', visible='true', lat=self.location['lat'],
                           lon=self.location['lon'])

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
            addTag('fixme', self.get_fixme())
        if self.extra_tags:
            for key, value in self.extra_tags:
                addTag(key, value)
        return node

    def as_osm_xml(self, node_id):
        return self.as_osm_soup().prettify()

    def get_lat_lon(self):
        return tuple(map(float, (self.location['lat'], self.location['lon'])))

    def get_point(self):
        return Point(reversed(self.get_lat_lon()))

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
        #if self.sym_ul and other.sym_ul:
        #    ret &= (self.sym_ul == other.sym_ul)
        # skip compare by streets, callers should do this by themselvs
        return ret

    def __str__(self):
        if self.street:
            return "%s, %s, %s" % (self.city, self.street, self.housenumber)
        return "%s, %s" % (self.city, self.housenumber)

    def __repr__(self):
        return type(self).__name__ + "(" + ", ".join(
            "%s=%s" % (x, getattr(self, x)) for x in (
                'housenumber', 'postcode',
                'street', 'city', 'sym_ul',
                'simc', 'source', 'location')
        ) + ")"

    def get_index_key(self):
        return tuple(map(str.upper, (self.city.strip(), self.street.strip(), self.housenumber.replace(' ', ''))))

    def to_json(self):
        ret = self.extra_tags.copy()
        ret.update({
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
        })
        return ret

    def to_geo_json(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.location['lon'], self.location['lat']]
            },
            "properties": self.to_json()
        }

    def add_extra_tag(self, key, value):
        if key in ['addr:housenumber', 'addr:postcode', 'addr:street', 'addr:city',
                   'addr:street:sym_ul', 'addr:city:simc', 'source:addr', 'addr:place', 'fixme']:
            raise KeyError("Can't use {0} as extra key".format(key))
        self.extra_tags[key] = value

    @staticmethod
    def from_json(obj):
        ret = Address(
            housenumber=obj['addr:housenumber'],
            postcode=obj.get('addr:postcode'),
            street=obj.get('addr:street'),
            city=obj.get('addr:city'),
            sym_ul=obj.get('addr:street:sym_ul'),
            simc=obj.get('addr:city:simc'),
            source=obj['source:addr'],
            location=obj['location'],
            id_=obj['id'],
        )
        if obj.get('fixme'):
            ret.add_fixme(obj['fixme'])
        return ret

    @staticmethod
    def from_osm_xml(elem):
        tags = dict(
            (x.get('k'), x.get('v')) for x in elem if x.tag == 'tag'
        )
        if 'addr:place' in tags and 'addr:city' not in tags:
            tags['addr:city'] = tags['addr:place']
        tags['location'] = {
            'lon': elem.get('lon'),
            'lat': elem.get('lat')
        }
        tags['id'] = elem.get('id')
        return Address.from_json(tags)


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
                relation = tuple(x for x in data['elements'] if x['type'] == 'relation')[0]
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

    def get_bbox(self):
        """
        this functions returns bbox of imported area using WGS84 lonlat as tuple:
        (minlon, minlat, maxlon, maxlat)
        """
        return self.bbox

    def get_bbox_2180(self):
        return wgsTo2180(*self.bbox[:2]) + wgsTo2180(*self.bbox[2:])

    def set_bbox_from_2180(self, bbox):
        self.bbox = e2180toWGS(*bbox[:2]) + e2180toWGS(*bbox[2:])

    def fetch_tiles(self):
        """
        this function returns list of Address'es of imported area
        """
        raise NotImplementedError("")

    def _check_duplicates_in_import(self, data):
        addr_index = groupby(data, lambda x: (x.city, x.simc, x.housenumber.replace(' ', '').upper(), x.street))
        # remove duplicates closer than 2m
        for (addr, occurances) in sorted(
                filter(lambda x: len(x[1]) > 1, addr_index.items()),
                key=lambda x: str(x[1][0])
        ):
            for (a, b) in filter(lambda x: distance(x[0].center, x[1].center) < 10,
                                 itertools.combinations(occurances, 2)):
                # if any two duplicates are closer than 2m, remove from data
                self.__log.info("Removing duplicate address: %s", a)
                try:
                    data.remove(a)
                except ValueError:
                    pass  # element might have been removed already

        # mark duplicates
        addr_index = groupby(data, lambda x: (x.city, x.simc, x.housenumber.replace(' ', '').upper(), x.street))
        for (addr, occurances) in sorted(
                filter(lambda x: len(x[1]) > 1, addr_index.items()),
                key=lambda x: str(x[1][0])
        ):
            self.__log.warning("Duplicate addresses in import: %s", occurances[0])
            uid = uuid.uuid4()
            for i in occurances:
                i.add_fixme('Duplicate address in import (id: %s)' % (uid,))
            if any(
                    map(
                        lambda x: distance(x[0].center, x[1].center) > 100,
                        itertools.combinations(occurances, 2)
                    )
            ):
                self.__log.warning("Address points doesn't fit into 100m circle. Points count: %d", len(occurances))
                for i in occurances:
                    i.add_fixme('(distance over 100m, points: %d)' % (len(occurances),))

    def _check_mixed_scheme(self, data):
        dups = groupby((x for x in data if x.simc), lambda x: x.simc, lambda x: bool(x.street))

        dups_count = dict((k, len(_filter_ones(v))) for k, v in dups.items())
        dups = dict((k, len(_filter_ones(v)) / len(v)) for k, v in dups.items())
        dups = dict((k, v) for k, v in filter(lambda x: 0 < x[1] and x[1] < 1, dups.items()))

        for i in filter(
                lambda x: not bool(x.street) and x.simc in dups.keys(),
                data
        ):
            i.add_fixme('Mixed addressing scheme in city - with streets and without. %.1f%% (%d) with streets.' % (
                dups[i.simc] * 100, dups_count[i.simc]))

    def get_addresses(self):
        data = list(sorted(self.fetch_tiles(), key=lambda x: str(x)))
        self._check_duplicates_in_import(data)
        self._check_mixed_scheme(data)
        return data


class AddressEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Address):
            return obj.to_json()
        return json.JSONEncoder.default(self, obj)


def get_ssl_no_verify_opener():
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    https_handler = urllib.request.HTTPSHandler(context=ssl_ctx, check_hostname=False)
    return urllib.request.build_opener(https_handler)