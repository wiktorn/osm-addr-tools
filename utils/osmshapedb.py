import typing

import osmium
import shapely.wkb
import shapely.geometry


_wkb_factory = osmium.geom.WKBFactory()


def _common_attributes(o, type_):
    return {
                'type': type_,
                'id': o.id,
                'timestamp': o.timestamp, # todo - convert datetime.datetime to string
                'version': o.version,
                'changeset': o.changeset,
                'user': o.user,
                'uid': o.uid,
                'tags': dict((tag.k, tag.v) for tag in o.tags)
            }

class GeometryHandler(osmium.SimpleHandler):
    def __init__(self):
        super(GeometryHandler, self).__init__()
        self.__geometries = {}  # type: typing.Dict[str, shapely.geometry.base.BaseGeometry
        self.__elements = []

    def way(self, w):
        wkb = _wkb_factory.create_linestring(w)
        shape = shapely.wkb.loads(wkb, hex=True)
        id_ = "way:{}".format(w.id)
        if id_ not in self.__geometries:
            self.__geometries[id_] = shape
        elem = _common_attributes(w, 'way')
        elem.update({
            'nodes': [x.ref for x in w.nodes]
        })
        self.__elements.append(elem)

    def area(self, a):
        wkb = _wkb_factory.create_multipolygon(a)
        shape = shapely.wkb.loads(wkb, hex=True)
        type_ = "way" if a.id % 2 == 0 else "relation:"
        id_ = "{}:{}".format(type_, a.orid_id)
        self.__geometries[id_] = shape

    def node(self, n):
        wkb = _wkb_factory.create_point(n)
        shape = shapely.wkb.loads(wkb, hex=True)
        self.__geometries["node:{}".format(n.id)] = shape
        elem = _common_attributes(n, 'node')
        elem.update({
                'lat': n.location.lat,
                'lon': n.location.lon,
        })
        self.__elements.append(elem)

    def relation(self, r):
        elem = _common_attributes(r, 'relation')
        elem.update({
            'members': [{'type': x.type, 'ref': x.ref, 'role': x.role} for x in r.members ]
        })
        self.__elements.append(elem)
    
    @property
    def geometries(self):
        return self.__geometries

    @property
    def elements(self):
        return self.__elements


def get_geometries(data) -> typing.Dict[str, shapely.geometry.base.BaseGeometry]:
    # use MergeInputReader to sort input, so nodes will come first. Otherwise invalid locations could be passed
    # in ways/relations GeometryHandler
    mir = osmium.MergeInputReader()
    mir.add_buffer(data, "osm")  # Overpass returns data in osm format
    gh = GeometryHandler()
    # use memory index (flex_mem) for node locations cache. Use "sparse_file_array,<filename>" for file backed indices
    mir.apply(gh, idx='flex_mem')
    return gh

