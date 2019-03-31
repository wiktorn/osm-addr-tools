import functools
import os
import tempfile
import typing

import osmium
import shapely.wkb
import shapely.geometry


_wkb_factory = osmium.geom.WKBFactory()


def _common_attributes(o, type_):
    return {
                'type': type_,
                'id': o.id,
                'timestamp': o.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'version': o.version,
                'changeset': o.changeset,
                'user': o.user,
                'uid': o.uid,
                'tags': dict((tag.k, tag.v) for tag in o.tags)
            }


_REL_TYPE_MAP = {
    'w': 'way',
    'n': 'node',
    'r': 'relation'
}

class GeometryHandler(osmium.SimpleHandler):
    def __init__(self):
        super(GeometryHandler, self).__init__()
        self.__geometries = {}  # type: typing.Dict[str, shapely.geometry.base.BaseGeometry]
        self.__elements = []  # type: typing.List[dict]

    def way(self, w):
        wkb = _wkb_factory.create_linestring(w)
        shape = shapely.wkb.loads(wkb, hex=True)
        id_ = self._get_key("way", w.id)
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
        type_ = "way" if a.id % 2 == 0 else "relation"
        id_ = self._get_key(type_, a.orig_id())
        self.__geometries[id_] = shape

    def node(self, n):
        wkb = _wkb_factory.create_point(n)
        shape = shapely.wkb.loads(wkb, hex=True)
        self.__geometries[self._get_key("node", n.id)] = shape
        elem = _common_attributes(n, 'node')
        elem.update({
                'lat': n.location.lat,
                'lon': n.location.lon,
        })
        self.__elements.append(elem)

    def relation(self, r):
        elem = _common_attributes(r, 'relation')
        elem.update({
            'members': [{'type': _REL_TYPE_MAP[x.type], 'ref': x.ref, 'role': x.role} for x in r.members]
        })
        self.__elements.append(elem)

    @property
    def geometries(self):
        return self.__geometries

    @property
    def elements(self):
        return self.__elements

    def get_geometry_byid(self, type_: str, id_: str) -> shapely.geometry.base.BaseGeometry:
        return self.__geometries[self._get_key(type_, id_)]

    def get_geometry(self, obj: dict):
        return self.__geometries[self._get_obj_key(obj)]

    @staticmethod
    def _get_key(type_: str, id_: str) -> str:
        return "{}:{}".format(type_, id_)

    @staticmethod
    def _get_obj_key(obj: dict) -> str:
        return GeometryHandler._get_key(obj['type'], obj['id'])


def get_geometries(data) -> GeometryHandler:
    # use MergeInputReader to sort input, so nodes will come first. Otherwise invalid locations could be passed
    # in ways/relations GeometryHandler
    mir = osmium.MergeInputReader()
    mir.add_buffer(data, "osm")  # Overpass returns data in osm format
    gh = GeometryHandler()
    # sort to temporary file, then read sorted data from file
    with tempfile.NamedTemporaryFile(suffix='.osm') as temp_osm:
        os.unlink(temp_osm.name)
        wh = osmium.WriteHandler(temp_osm.name)
        mir.apply(wh)
        wh.close()
        # use memory index (flex_mem) for node locations cache. Use "sparse_file_array,<filename>" for file backed indices
        gh.apply_file(temp_osm.name, locations=True, idx='flex_mem')
    # gh.apply_buffer(data, "osm")
    return gh
