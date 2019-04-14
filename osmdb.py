import collections
import functools
import logging
import typing

import pyproj
import shapely
import shapely.geometry
import shapely.ops
import tqdm
from rtree import index
from shapely.geometry import Point

from utils import osmshapedb

__multipliers = {
    'node'    : lambda x: x*3,
    'way'     : lambda x: x*3+1,
    'relation': lambda x: x*3+2,
}


def _get_id(soup):
    """Converts overlapping identifiers for node, ways and relations in single integer space"""
    return __multipliers[soup['type']](int(soup['id']))


def get_soup_position(soup):
    """Extracts position for way/node as bounding box"""
    if soup['type'] == 'node':
        return (float(soup['lat']), float(soup['lon'])) * 2

    if soup['type'] in ('way', 'relation'):
        b = soup.get('bounds')
        if b:
            return tuple(float(x) for x in (b['minlat'], b['minlon'], b['maxlat'], b['maxlon']))
        else:
            raise TypeError("OSM Data doesn't contain bounds for ways and relations!")
    raise TypeError("%s not supported" % (soup['type'],))


def get_soup_center(soup):
    # lat, lon
    pos = get_soup_position(soup)
    return (pos[0] + pos[2])/2, (pos[1] + pos[3])/2


__geod = pyproj.Geod(ellps="WGS84")

_epsg_2180_to_4326 = functools.partial(pyproj.transform, pyproj.Proj(init='epsg:2180'), pyproj.Proj(init='epsg:4326'))
_epsg_4326_to_2180 = functools.partial(pyproj.transform, pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:2180'))


def distance(a, b):
    """returns distance betwen a and b points in meters"""
    if isinstance(a, shapely.geometry.base.BaseGeometry):
        point_a = a.centroid
        a = (point_a.y, point_a.x)
    if isinstance(b, shapely.geometry.base.BaseGeometry):
        point_b = b.centroid
        b = (point_b.y, point_b.x)
    return __geod.inv(a[1], a[0], b[1], b[0])[2]


def buffered_shape_poland(shape: shapely.geometry.base.BaseGeometry, buffer: int) -> shapely.geometry.base.BaseGeometry:
    """
    :param shape: shape to extend
    :param buffer: buffer in meters -
    :return: object extended in each direction by buffer

    Uses EPSG:2180 (PUWG) to get estimated 1 m = 1 unit, so buffer will actually extend objects by one meter
    Warning: This will work only in Poland
    """
    ret = shapely.ops.transform(_epsg_4326_to_2180, shape).buffer(buffer)
    return shapely.ops.transform(_epsg_2180_to_4326, ret)


def skip_exceptions(gen):
    while True:
        try:
            yield next(gen)
        except StopIteration:
            raise
        except Exception:
            pass


class OsmDbEntry(object):
    def __init__(self, entry, raw, shape: shapely.geometry.base.BaseGeometry):
        self._entry = entry
        self._raw = raw
        self._shape = shape

    @property
    def entry(self):
        return self._entry

    @property
    def shape(self):
        return self._shape

    @property
    def shape_noerror(self):
        return self.shape
    
    @property
    def center(self):
        return self.shape.centroid

    def __getattr__(self, attr):
        return getattr(self.entry, attr)

    def __getitem__(self, attr):
        return self._entry[attr]

    def within(self, other):
        return self.shape.within(other)

    def contains(self, other):
        return self.shape.contains(other)

    def buffered_shape(self, buffer: int) -> shapely.geometry.base.BaseGeometry:
        """
        :param buffer: buffer in meters -
        :return: object extended in each direction by buffer

        Uses EPSG:2180 (PUWG) to get estimated 1 m = 1 unit, so buffer will actually extend objects by one meter
        Warning: This will work only in Poland
        """
        return buffered_shape_poland(self.shape, buffer)


class OsmDb(object):
    __log = logging.getLogger(__name__).getChild('OsmDb')

    def __init__(self, osmdata: osmshapedb.GeometryHandler, valuefunc=lambda x, location: x, indexes=None,
                 index_filter=lambda x: True):
        # assume osmdata is a BeautifulSoup object already
        # do it an assert
        if not indexes:
            indexes = {}
        self._osmdata = osmdata.elements  # type: typing.List[dict]
        self._shapedb = osmdata.geometries  # type: typing.Dict[str, shapely.geometry.base.BaseGeometry]
        self.__custom_indexes = dict((x, {}) for x in indexes.keys())
        self._valuefunc = valuefunc
        self.__custom_indexes_conf = indexes
        self.__cached_shapes = {}
        self.__index = index.Index()
        self.__index_entries = {}
        self.__index_filter = index_filter

        def makegetfromindex(index_name):
            def getfromindex(key):
                return self.__custom_indexes[index_name].get(key, [])
            return getfromindex

        def makegetallindexed(index_name):
            def getallindexed():
                return tuple(self.__custom_indexes[index_name].keys())
            return getallindexed

        for i in indexes.keys():
            setattr(self, 'getby' + i, makegetfromindex(i))
            setattr(self, 'getall' + i, makegetallindexed(i))

        self.__osm_obj: typing.Dict[typing.Tuple[str, int], OsmDbEntry] = dict()
        for x in self._osmdata:
            shape_obj = self._shapedb.get("{}:{}".format(x['type'], x['id']))
            if shape_obj:
                key = (x['type'], int(x['id']))
                self.__osm_obj[key] = OsmDbEntry(self._valuefunc(x, location=shape_obj.centroid), x, shape_obj)
        self.update_index("[1/14]")

    def update_index(self, message=""):
        self.__log.debug("Recreating index")

        self.__index = index.Index()
        self.__index_entries = {}
        self.__custom_indexes = dict((x, collections.defaultdict(list)) for x in self.__custom_indexes_conf.keys())

        for val in tqdm.tqdm(
                [value for value in self.__osm_obj.values() if self.__index_filter(value)],
                desc="{} Creating index".format(message)
        ):
            try:
                # pos = self.get_shape(val._raw).centroid
                pos = self._shapedb["{}:{}".format(val._raw['type'], val._raw['id'])].centroid
            except KeyError:
                raise KeyError("Problem with getting shape of {}:{}".format(val.entry['type'], val.entry['id']))
            pos = (pos.y, pos.x)
            if pos:
                _id = _get_id(val._raw)
                self.__index.insert(_id, pos)

                self.__index_entries[_id] = val

                for custom_index_name, custom_index_func in self.__custom_indexes_conf.items():
                    self.__custom_indexes[custom_index_name][custom_index_func(val)].append(val)

    def add_new(self, new):
        self._osmdata.append(new)
        key = "{}:{}".format(new['type'], new['id'])
        location = shapely.geometry.Point(float(new['lon']), float(new['lat']))
        self._shapedb[key] = location
        ret = OsmDbEntry(self._valuefunc(new, location=location), new, location)
        self.__osm_obj[(new['type'], int(new['id']))] = ret
        return ret

    def get_by_id(self, typ: str, id_: int) -> OsmDbEntry:
        return self.__osm_obj[(typ, int(id_))]

    def get_all_values(self):
        return self.__osm_obj.values()

    def nearest(self, point, num_results=1):
        if isinstance(point, Point):
            point = (point.y, point.x)
        return map(self.__index_entries.get,
                   self.__index.nearest(point * 2, num_results)
                   )

    def intersects(self, point):
        if isinstance(point, Point):
            point = (point.y, point.x)
        return (self.__index_entries.get(x) for x in self.__index.intersection(point * 2))

                
def main():
    odb = OsmDb(osmshapedb.get_geometries(open("adresy.osm").read()))
    print(list(odb.nearest((53.5880600, 19.5555200), 10)))


if __name__ == '__main__':
    main()
