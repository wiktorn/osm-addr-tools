import functools

import collections

import tqdm
from rtree import index
from shapely.geometry import Point, Polygon, LineString
import shapely.ops
import shapely
import utils
import logging
import pyproj


__multipliers = {
    'node'    : lambda x: x*3,
    'way'     : lambda x: x*3+1,
    'relation': lambda x: x*3+2,
}


def _get_id(soup):
    """Converts overlapping identifiers for node, ways and relations in single integer space"""
    return __multipliers[soup['type']](int(soup['id']))


__position_cache = {}


def get_soup_position(soup):
    try:
        return __position_cache[soup['id']]
    except KeyError:
        ret = get_soup_position_cached(soup)
        __position_cache[soup['id']] = ret
        return ret


def get_soup_position_cached(soup):
    """Extracts position for way/node as bounding box"""
    if soup['type'] == 'node':
        return (float(soup['lat']), float(soup['lon'])) * 2

    if soup['type'] in ('way', 'relation'):
        b = soup.get('bounds')
        if b:
            return tuple(
                    map(float,
                        (b['minlat'], b['minlon'], b['maxlat'], b['maxlon'])
                    )
                )
        else:
            raise TypeError("OSM Data doesn't contain bounds for ways and relations!")
    raise TypeError("%s not supported" % (soup['type'],))


def get_soup_center(soup):
    # lat, lon
    pos = get_soup_position(soup)
    return (pos[0] + pos[2])/2, (pos[1] + pos[3])/2


def prepare_object_pos(elem_lst):
    def elem_loc(elm):
        return float(elm['lat']), float(elm['lon'])

    def elem_id(elm):
        return "%s:%s" % (elm['type'], elm['id'])

    obj_cache = dict((elem_id(x), x) for x in elem_lst)

    def bbox(pos):
        return (
            min(x[0] for x in pos),
            min(x[1] for x in pos),
            max(x[0] for x in pos),
            max(x[1] for x in pos)
        )

    def handle_node(elm):
        return bbox([elem_loc(elm),])

    def handle_way(elm):
        pos = [elem_loc(obj_cache.get('node:' + str(x))) for x in elm['nodes']]
        return bbox(pos)

    def handle_relattion(elm):
        ret = [routing[member['type']]((obj_cache["%s:%s" % (member['type'], member['ref'])])) for member in elm['members']]
        return bbox(ret)

    routing = {
        'relation': handle_relattion,
        'way': handle_way,
        'node': handle_node
    }

    def bbox_to_center(pos):
        return (
            (pos[0] + pos[2]) / 2, 
            (pos[1] + pos[3]) / 2
        )

    return dict(
        (
            elem_id(elm), 
            bbox_to_center(routing[elm['type']](elm))
        ) for elm in elem_lst)
    

__geod = pyproj.Geod(ellps="WGS84")

_epsg_2180_to_4326 = functools.partial(pyproj.transform, pyproj.Proj(init='epsg:2180'), pyproj.Proj(init='epsg:4326'))
_epsg_4326_to_2180 = functools.partial(pyproj.transform, pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:2180'))

def distance(a, b):
    """returns distance betwen a and b points in meters"""
    if isinstance(a, shapely.geometry.base.BaseGeometry):
        a = (a.y, a.x)
    if isinstance(b, shapely.geometry.base.BaseGeometry):
        b = (b.y, b.x)
    return __geod.inv(a[1], a[0], b[1], b[0])[2]


class OsmDbEntry(object):
    def __init__(self, entry, raw, osmdb):
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
        ret = shapely.ops.transform(_epsg_4326_to_2180, self.shape).buffer(buffer)
        return shapely.ops.transform(_epsg_2180_to_4326, ret)



class OsmDb(object):
    __log = logging.getLogger(__name__).getChild('OsmDb')

    def __init__(self, osmdata, valuefunc=lambda x: x, indexes=None):
        # assume osmdata is a BeautifulSoup object already
        # do it an assert
        if not indexes:
            indexes = {}
        self._osmdata = osmdata
        self.__custom_indexes = dict((x, {}) for x in indexes.keys())
        self._valuefunc = valuefunc
        self.__custom_indexes_conf = indexes
        self.__cached_shapes = {}
        self.__index = index.Index()
        self.__index_entries = {}


        def makegetfromindex(i):
            def getfromindex(key):
                return self.__custom_indexes[i].get(key, [])
            return getfromindex

        def makegetallindexed(i):
            def getallindexed():
                return tuple(self.__custom_indexes[i].keys())
            return getallindexed

        for i in indexes.keys():
            setattr(self, 'getby' + i, makegetfromindex(i))
            setattr(self, 'getall' + i, makegetallindexed(i))

        self.__osm_obj = dict(
            (
                (x['type'], x['id']),
                OsmDbEntry(self._valuefunc(x), x, self)
            ) for x in self._osmdata['elements']
        )
        self.update_index("[1/10]")

    def update_index(self, message=""):
        self.__log.debug("Recreating index")

        self.__index = index.Index()
        self.__index_entries = {}
        self.__custom_indexes = dict((x, collections.defaultdict(list)) for x in self.__custom_indexes_conf.keys())

        for (key, val) in tqdm.tqdm(self.__osm_obj.items(), desc="{} Creating index".format(message)):
            pos = self.get_shape(val._raw).centroid
            pos = (pos.y, pos.x)
            if pos:
                _id = _get_id(val._raw)
                self.__index.insert(_id, pos)

                self.__index_entries[_id] = val

                for custom_index_name, custom_index_func in self.__custom_indexes_conf.items():
                    self.__custom_indexes[custom_index_name][custom_index_func(val)].append(val)

    def add_new(self, new):
        self._osmdata['elements'].append(new)
        ret = OsmDbEntry(self._valuefunc(new), new, self)
        self.__osm_obj[(new['type'], new['id'])] = ret
        return ret

    def get_all_values(self):
        return self.__index_entries.values()

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

    def get_shape(self, soup):
        id_ = soup['id']
        ret = self.__cached_shapes.get(id_)
        if not ret:
            ret = self.get_shape_cached(soup)
            self.__cached_shapes[id_] = ret
        return ret

    def get_shape_cached(self, soup):
        if soup['type'] == 'node':
            return Point(float(soup['lon']), float(soup['lat']))

        if soup['type'] == 'way':
            nodes = tuple(self.__osm_obj[('node', y)] for y in soup['nodes'])
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
                        (self.__osm_obj[(x['type'], x['ref'])] for x in soup['members'])
                    )
                ).centroid

            # handle relation type 'building' properly for 3D buildings
            if soup['tags'].get('type') == 'building':
                outline_members = [x for x in soup['members'] if x['role'] == 'outline']
                if len(outline_members) != 1:
                    raise ValueError("Broken geometry for relation: %s. Missing outline role" % (soup['id'],))
                return self.__osm_obj[('way', outline_members[0]['ref'])].shape

            # returns only outer ways, no exclusion for inner ways
            # hardest one
            # outer ways
            # TODO: handle multiple outer ways, and inner ways
            # multiple outer: terc=1019042
            # inner ways: terc=1014082
            outer = []
            inner = []
            if 'members' not in soup:
                raise ValueError("Broken geometry for relation: %s. Relation without members." % (soup['id'],))
            for member in filter(lambda x: x['type'] == 'way', soup['members']):
                obj = self.__osm_obj[(member['type'], member['ref'])]
                if member['role'] == 'outer' or not member.get('role'):
                    outer.append(obj)
                if member['role'] == 'inner':
                    inner.append(obj)

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
                raise ValueError("Broken geometry for relation: %s" % (soup['id'],))
            return ret

    def get_closed_ways(self, ways):
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
                ret = tuple(filter(lambda x: x in ways, dct[id_]))
                if ret:
                    return ret[0]
            return None

        ids = _get_ids(cur_elem)
        while ways:
            node_ids.extend(ids)
            ways.remove(cur_elem)
            if node_ids[0] == node_ids[-1]:
                # full circle, append to Polygons in ret
                ret.append(
                    Polygon(
                        (x.center.x, x.center.y) for x in (self.__osm_obj[('node', y)] for y in node_ids)
                    )
                )
                if ways:
                    cur_elem = ways[0]
                    node_ids = []
                    ids = _get_ids(cur_elem)
            else:
                # not full circle
                if ways: # check if there is something to work on
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
                else: # if ways
                    raise ValueError
        # end while
        return ret

                
def main():
    odb = OsmDb(open("adresy.osm").read())
    print(list(odb.nearest((53.5880600, 19.5555200), 10)))


if __name__ == '__main__':
    main()
