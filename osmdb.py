import functools
import logging
import typing

import collections
import pyproj
import shapely
import shapely.ops
import shapely.geometry
import tqdm
from rtree import index
from shapely.geometry import Point, Polygon, LineString

import utils
from data.data import LonType, LatType, Location, BBoxType

__multipliers = {
    'node'    : lambda x: x*3,
    'way'     : lambda x: x*3+1,
    'relation': lambda x: x*3+2,
}


def _get_id(soup: dict):
    """Converts overlapping identifiers for node, ways and relations in single integer space"""
    return __multipliers[soup['type']](int(soup['id']))


def get_soup_position(soup: dict) -> BBoxType:
    """Extracts position for way/node as bounding box"""
    if soup['type'] == 'node':
        lon, lat = LonType(soup['lon']), LatType(soup['lat'])
        return BBoxType(minlat=lat, minlon=lon, maxlat=lat, maxlon=lon)

    if soup['type'] in ('way', 'relation'):
        b = soup.get('bounds')
        if b:
            return BBoxType(minlat=LatType(b['minlat']), minlon=LonType(b['minlon']), maxlat=LatType(b['maxlat']),
                            maxlon=LonType(b['maxlon']))
        else:
            raise TypeError("OSM Data doesn't contain bounds for ways and relations!")
    raise TypeError("%s not supported" % (soup['type'],))


def get_soup_center(soup: dict) -> Location:
    # lat, lon
    pos = get_soup_position(soup)
    return Location(lat=(pos.minlat + pos.maxlat)/2, lon=(pos.minlon + pos.maxlon)/2)


__geod = pyproj.Geod(ellps="WGS84")


def distance(a: typing.Union[shapely.geometry.base.BaseGeometry, Location],
             b: typing.Union[shapely.geometry.base.BaseGeometry, Location]):
    """returns distance betwen a and b points in meters"""
    if isinstance(a, shapely.geometry.base.BaseGeometry):
        a = Location.from_geometry(a)
    if isinstance(b, shapely.geometry.base.BaseGeometry):
        b = Location.from_geometry(b)
    return __geod.inv(a.lon, a.lat, b.lon, b.lat)[2]


_epsg_2180_to_4326 = functools.partial(pyproj.transform, pyproj.Proj(init='epsg:2180'), pyproj.Proj(init='epsg:4326'))
_epsg_4326_to_2180 = functools.partial(pyproj.transform, pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:2180'))


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


class OsmDbEntry(object):
    def __init__(self, entry, raw, osmdb: 'OsmDb'):
        self._entry = entry
        self._raw = raw
        self._osmdb = osmdb

    @property
    def entry(self):
        return self._entry

    @property
    def shape(self):
        return self._osmdb.get_shape(self._raw)
    
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


V = typing.TypeVar('V')


class OsmDb(typing.Generic[V]):
    __log = logging.getLogger(__name__).getChild('OsmDb')

    def __init__(self, osmdata: typing.Dict[str, typing.Any],
                 valuefunc: typing.Callable[[dict], V] = lambda x: x,
                 indexes: typing.Optional[typing.Dict[str, typing.Callable[[V], typing.Any]]] = None,
                 index_filter: typing.Callable[[dict], bool] = lambda x: True):
        # assume osmdata is a BeautifulSoup object already
        # do it an assert
        if not indexes:
            indexes = {}  # type: typing.Dict[str, typing.Callable[[V], typing.Any]]
        self._osmdata = osmdata
        self.__custom_indexes = dict((x, {}) for x in indexes.keys()
                                     )  # type: typing.Dict[str, typing.Dict[str, typing.Union[OsmDbEntry, V]]]
        self._valuefunc = valuefunc
        self.__custom_indexes_conf = indexes
        self.__cached_shapes = {}  # type: typing.Dict[str, shapely.geometry.base.BaseGeometry]
        self.__index = index.Index()
        self.__index_entries = {}  # type: typing.Dict[str, typing.Union[OsmDbEntry, V]]
        self.__index_filter = index_filter

        def makegetfromindex(index_name: str):
            def getfromindex(key):
                return self.__custom_indexes[index_name].get(key, [])
            return getfromindex

        def makegetallindexed(index_name: str):
            def getallindexed():
                return tuple(self.__custom_indexes[index_name].keys())
            return getallindexed

        for i in indexes.keys():
            setattr(self, 'getby' + i, makegetfromindex(i))
            setattr(self, 'getall' + i, makegetallindexed(i))

        self.__osm_obj = dict(
            (
                (x['type'], int(x['id'])),
                OsmDbEntry(self._valuefunc(x), x, self)
            ) for x in self._osmdata['elements']
        )  # type: typing.Dict[typing.Tuple[str, int], typing.Union[OsmDbEntry, V]]
        self.update_index("[1/14]")

    def update_index(self, message="") -> None:
        self.__log.debug("Recreating index")

        self.__index = index.Index()
        self.__index_entries = {}
        self.__custom_indexes = dict((x, collections.defaultdict(list)) for x in self.__custom_indexes_conf.keys())

        for val in tqdm.tqdm(
                [value for value in self.__osm_obj.values() if self.__index_filter(value)],
                desc="{} Creating index".format(message)
        ):
            try:
                pos = self.get_shape(val._raw).centroid
            except KeyError:
                raise KeyError("Problem with getting shape of {}:{}".format(val.entry['type'], val.entry['id']))
            pos = (pos.y, pos.x)
            if pos:
                _id = _get_id(val._raw)
                self.__index.insert(_id, pos)

                self.__index_entries[_id] = val

                for custom_index_name, custom_index_func in self.__custom_indexes_conf.items():
                    self.__custom_indexes[custom_index_name][custom_index_func(val)].append(val)

    def add_new(self, new) -> typing.Union[V, OsmDbEntry]:
        self._osmdata['elements'].append(new)
        ret = OsmDbEntry(self._valuefunc(new), new, self)
        self.__osm_obj[(new['type'], int(new['id']))] = ret
        return ret

    def get_by_id(self, typ: str, id_: str) -> typing.Union[V, OsmDbEntry]:
        return self.__osm_obj[(typ, int(id_))]

    def get_all_values(self) -> typing.Iterable[typing.Union[V, OsmDbEntry]]:
        return self.__osm_obj.values()

    def nearest(self, point, num_results=1) -> typing.Iterable[typing.Union[V, OsmDbEntry]]:
        if isinstance(point, Point):
            point = (point.y, point.x)
        return map(self.__index_entries.get,
                   self.__index.nearest(point * 2, num_results)
                   )

    def intersects(self, point):
        if isinstance(point, Point):
            point = (point.y, point.x)
        return (self.__index_entries.get(x) for x in self.__index.intersection(point * 2))

    def get_shape(self, soup: dict) -> shapely.geometry.base.BaseGeometry:
        id_ = soup['id']
        ret = self.__cached_shapes.get(id_)
        if not ret:
            ret = self.get_shape_cached(soup)
            self.__cached_shapes[id_] = ret
        return ret

    def get_shape_cached(self, soup: dict) -> shapely.geometry.base.BaseGeometry:
        if soup['type'] == 'node':
            return Point(float(soup['lon']), float(soup['lat']))

        if soup['type'] == 'way':
            nodes = tuple(self.get_by_id('node', y) for y in soup['nodes'])
            if len(nodes) < 3:
                self.__log.warning("Way has less than 3 nodes. Check geometry. way:%s" % (soup['id'],))
                self.__log.warning("Returning geometry as a point")
                return Point(sum(x.center.x for x in nodes)/len(nodes), sum(x.center.y for x in nodes)/len(nodes))
            return Polygon((x.center.x, x.center.y) for x in nodes)

        if soup['type'] == 'relation':
            if soup['tags'].get('type') in ('network', 'level'):
                # shortcut for stupid relations with addresses
                return LineString(
                    map(
                        lambda x: x.center,
                        (self.get_by_id(x['type'], x['ref']) for x in soup['members'])
                    )
                ).centroid

            # handle relation type 'building' properly for 3D buildings
            if soup['tags'].get('type') == 'building':
                outline_members = [x for x in soup['members'] if x['role'] == 'outline']
                if len(outline_members) != 1:
                    raise ValueError("Broken geometry for relation: %s. Missing outline role" % (soup['id'],))
                return self.get_by_id('way', outline_members[0]['ref']).shape

            # returns only outer ways, no exclusion for inner ways
            # multiple outer: terc=1019042
            # inner ways: terc=1014082
            outer = []
            inner = []
            if 'members' not in soup:
                raise ValueError("Broken geometry for relation: %s. Relation without members." % (soup['id'],))
            for member in filter(lambda x: x['type'] == 'way', soup['members']):
                obj = self.get_by_id(member['type'], member['ref'])
                if member['role'] == 'outer' or not member.get('role'):
                    outer.append(obj)
                if member['role'] == 'inner':
                    inner.append(obj)

            if not outer and not inner:
                # handle broken relations without inner / outer
                outer = [
                    self.get_by_id(x['type'], x['ref']) for x in soup['members'] if x['role'] in ('building', 'house')
                ]
            try:
                inner = self.get_closed_ways(inner)
                outer = self.get_closed_ways(outer)
            except ValueError:
                raise ValueError("Broken geometry for relation: %s" % (soup['id'],))
            ret = None
            for out in outer:
                val = out
                for inn in filter(out.contains, inner):
                    val = val.difference(inn)
                if not ret:
                    ret = val
                else:
                    ret = ret.union(val)
            # handle broken (only inner members) relations
            if not ret and len(outer) == 0 and len(inner) > 0:
                for val in inner:
                    if not ret:
                        ret = val
                    else:
                        ret = ret.union(val)
            if not ret:
                # TODO: maybe use bounds of relation instead?
                raise ValueError("Broken geometry for relation: %s" % (soup['id'],))
            return ret

    def get_closed_ways(self, ways: typing.List[typing.Union[V, OsmDbEntry]]) -> typing.List[shapely.geometry.Polygon]:
        if not ways:
            return []
        ways = list(ways)
        way_by_first_node = utils.groupby(ways, lambda x: x._raw['nodes'][0])
        way_by_last_node = utils.groupby(ways, lambda x: x._raw['nodes'][-1])
        ret = []
        cur_elem = ways[0]
        node_ids = []

        def _get_ids(elem):
            return elem['nodes']

        def _get_way(id_, dct):
            if id_ in dct:
                rv = tuple(filter(lambda x: x in ways, dct[id_]))
                if rv:
                    return rv[0]
            return None

        ids = _get_ids(cur_elem)
        while ways:
            node_ids.extend(ids)
            ways.remove(cur_elem)
            if node_ids[0] == node_ids[-1]:
                # full circle, append to Polygons in ret
                ret.append(
                    Polygon(
                        (x.center.x, x.center.y) for x in (self.get_by_id('node', y) for y in node_ids)
                    )
                )
                if ways:
                    cur_elem = ways[0]
                    node_ids = []
                    ids = _get_ids(cur_elem)
            else:
                # not full circle
                if ways:  # check if there is something to work on
                    last_id = node_ids[-1]
                    first_id = node_ids[0]
                    if _get_way(last_id, way_by_first_node):
                        cur_elem = _get_way(last_id, way_by_first_node)
                        ids = _get_ids(cur_elem)

                    elif _get_way(last_id, way_by_last_node):
                        cur_elem = _get_way(last_id, way_by_last_node)
                        ids = list(reversed(_get_ids(cur_elem)))

                    elif _get_way(first_id, way_by_first_node):
                        cur_elem = _get_way(first_id, way_by_first_node)
                        node_ids = list(reversed(node_ids))
                        ids = _get_ids(cur_elem)

                    elif _get_way(first_id, way_by_last_node):
                        cur_elem = _get_way(first_id, way_by_last_node)
                        node_ids = list(reversed(node_ids))
                        ids = list(reversed(_get_ids(cur_elem)))
                    else:
                        raise ValueError
                else:  # if ways
                    raise ValueError
        # end while
        return ret

                
def main():
    odb = OsmDb(open("adresy.osm").read())
    print(list(odb.nearest((53.5880600, 19.5555200), 10)))


if __name__ == '__main__':
    main()
