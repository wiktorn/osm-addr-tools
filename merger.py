#!/usr/bin/env python3.4

import argparse
import functools
import io
import itertools
import json
import logging
import sys
import typing
from collections import defaultdict, OrderedDict

import lxml.etree
import rtree
import shapely
import tqdm
from lxml.builder import E
from shapely.geometry import Point

import overpass
import utils.osmshapedb
from data.base import Address
from data.egeoportal import EGeoportal
from data.gisnet import GISNET
from data.gison import GISON
from data.gugik import GUGiK, GUGiK_GML
from data.impa import iMPA
from data.warszawaum import WarszawaUM
from osmdb import OsmDb, OsmDbEntry, get_soup_center, distance, simplified_shape_poland
from utils import osmshapedb

__log = logging.getLogger(__name__)


# depends FreeBSD
# portmaster graphics/py-pyproj devel/py-rtree devel/py-shapely www/py-beautifulsoup devel/py-lxml

# depeds Lubuntu:
# apt-get install python3-pyproj libspatialindex-dev python3-shapely python3-bs4 python3-lxml
# easy_install3 Rtree

# TODO: import admin_level=8 for area, and add addr:city if missing for addresses within that area
#       (needs greater refactoring)
# TODO: check for alone addresses. Look for addresses that have greater minimal distance to greater than ?? avg*5?
#       avg+stddev*3? http://en.wikipedia.org/wiki/Chauvenet%27s_criterion ?
#       http://en.wikipedia.org/wiki/Peirce%27s_criterion ?


def create_property_funcs(field):
    def getx(self):
        return self._soup['tags'][field]

    def setx(self, val):
        self._soup['tags'][field] = val

    def delx(self):
        del self._soup['tags'][field]

    return property(getx, setx, delx, '%s property' % (field,))


class Location(typing.NamedTuple):
    lat: float
    lon: float

class OsmAddress(Address):
    __log = logging.getLogger(__name__).getChild('OsmAddress')

    def __init__(self, soup, *args, **kwargs):
        self._soup = soup
        if 'tags' not in self._soup:
            self._soup['tags'] = {}
        super(OsmAddress, self).__init__(*args, **kwargs)
        self.state = None
        self.ref_ways = []
        self.osm_fixme = ""

    # @formatter:off
    housenumber = create_property_funcs('addr:housenumber')
    postcode    = create_property_funcs('addr:postcode')
    street      = create_property_funcs('addr:street')
    city        = create_property_funcs('addr:city')
    sym_ul      = create_property_funcs('addr:street:sym_ul')
    simc        = create_property_funcs('addr:city:simc')
    source      = create_property_funcs('source:addr')
    id_         = create_property_funcs('ref:addr')
    # @formatter:on

    def __getitem__(self, key):
        return self._soup[key]

    @staticmethod
    def from_soup(obj, location: shapely.geometry.Point = None, ways_for_node=None):
        tags = dict(
            (k, v.strip()) for (k, v) in obj.get('tags', {}).items()
        )
        if location is None:
            loc = dict(zip(('lat', 'lon'), get_soup_center(obj)))
        else:
            loc = {'lat': location.y, 'lon': location.x}

        ret = OsmAddress(
            housenumber=tags.get('addr:housenumber', ''),
            postcode=tags.get('addr:postcode', ''),
            street=tags.get('addr:street', ''),
            city=tags.get('addr:place', '') if tags.get('addr:place') else tags.get('addr:city', ''),
            sym_ul=tags.get('addr:street:sym_ul', ''),
            simc=tags.get('addr:city:simc', ''),
            source=tags.get('source:addr', ''),
            location=loc,
            id_=tags.get('ref:addr', ''),
            soup=obj
        )

        ret.osm_fixme = tags.get('fixme', '')
        if obj.get('action'):
            ret.state = obj['action']
        if ways_for_node:
            ret.ref_ways = ways_for_node.get(obj['id'], [])
        if tags.get('addr:place') and tags.get('addr:city'):
            # clear the data in OSM
            ret.set_state('modify')
        if tags.get('addr:city') and not tags.get('addr:street'):
            # clear the data in OSM
            ret.set_state('modify')
        return ret

    def get_fixme(self):
        s1 = super(OsmAddress, self).get_fixme()
        return ", ".join(x for x in (s1, self.osm_fixme) if x)

    def set_state(self, val):
        if val not in ('visible', 'modify', 'delete'):
            raise ValueError('Unknown state %s' % val)
        if val == 'visible' and self.state not in ('modify', 'delete'):
            self.state = val
        elif val == 'modify' and self.state != 'delete':
            self.state = val
        elif val == 'delete':
            if len(self.ref_ways) > 0:
                self.state = 'modify'
                self.housenumber = ''
                self.postcode = ''
                self.street = ''
                self.city = ''
                self.sym_ul = ''
                self.simc = ''
                self.source = ''
                self.id_ = ''
            else:
                self.state = val
        else:
            # mark change
            self.state = self.state

    @property
    def center(self):
        return Point(float(self.location['lon']), float(self.location['lat']))

    def distance(self, other):
        return distance(self.center, other.center)

    @property
    def objtype(self):
        return self._soup['type']

    def _get_tag_val(self, key):
        return self._soup.get('tags').get(key)

    def _set_tag_val(self, key, val):
        """returns True if something was modified"""
        n = self._soup['tags'].get(key)
        if n == val.strip():
            return False
        self._soup['tags'][key] = val.strip()
        return True

    def _remove_tag(self, key):
        if key in self._soup['tags']:
            del self._soup['tags'][key]
            return True
        return False

    def shape(self):
        raise NotImplementedError

    @property
    def osmid(self):
        return "%s:%s" % (self.objtype, self._soup['id'])

    @property
    def osmid_tuple(self):
        return (self.objtype, self._soup['id'])

    def is_emuia_addr(self):
        ret = False
        if self.source:
            ret |= ('EMUIA' in self.source.upper())
        source_addr = self._get_tag_val('source')
        if source_addr:
            ret |= ('EMUIA' in source_addr.upper())
        return ret

    def only_address_node(self):
        # return true, if its a node, has a addr:housenumber,
        # and consists only of tags listed below
        if self.objtype != 'node':
            return False
        return self.housenumber and set(self._soup['tags'].keys()).issubset(
            {'addr:housenumber', 'addr:street', 'addr:street:sym_ul', 'addr:place',
             'addr:city', 'addr:city:simc', 'addr:postcode', 'addr:country', 'teryt:sym_ul',
             'teryt:simc', 'source', 'source:addr', 'fixme', 'addr:street:source', 'ref:addr'}
        )

    def is_new(self):
        return int(self._soup['id']) < 0

    def get_tag_soup(self):
        return dict((k, v) for (k, v) in self._soup['tags'].items() if v)

    def update_from(self, entry):
        def update(tag_name):
            old = getattr(self, tag_name)
            new = getattr(entry, tag_name)
            if new and old != new:
                setattr(self, tag_name, new)
                if old:
                    self.__log.debug("Updating %s from %s to %s", tag_name, old, new)
                return True
            return False

        ret = False
        for name in ('street', 'city', 'housenumber', 'postcode'):
            ret |= update(name)
        # update without changing ret status, so adding these fields will not trigger a change in OSM
        # but if there is something else added, this will get updated too
        for name in ('sym_ul', 'simc', 'source', 'id_'):
            update(name)
        if entry.get_fixme():
            self.add_fixme(entry.get_fixme())
            self.set_state('visible')
        if ret:
            self.set_state('modify')
        return ret

    def to_osm_soup(self):
        def _remove_tag(tags, key):
            if key in tags:
                del tags[key]
                return True
            return False

        def _set_tag_val(tags, key, value):
            n = tags.get(key)
            if n == value.strip():
                return False
            if value.strip():
                tags[key] = value.strip()
                return True
            else:
                if n:
                    del tags[key]
                    return True
                else:
                    return False

        s = self._soup
        meta_kv = OrderedDict((k, str(v)) for (k, v) in sorted(s.items()) if
                              k in ('id', 'version', 'timestamp', 'changeset', 'uid', 'user'))
        # do not export ref:addr until the discussion will come to conclusion
        tags = dict(
            (k, v.strip()) for (k, v) in s.get('tags', {}).items() if
            v.strip() and k != 'ref:addr' and k != 'addr:ref'
        )

        ret = False
        if self.housenumber:
            if self.street:
                ret |= _remove_tag(tags, 'addr:place')
            else:
                ret |= _set_tag_val(tags, 'addr:place', self.city)
                ret |= _remove_tag(tags, 'addr:street')
                # do not change value of ret - this value is always there, as self.city set this
                _remove_tag(tags, 'addr:city')
            if self.get_fixme():
                # presence of only fixme tag is not sufficient to send a change to OSM
                _set_tag_val(tags, 'fixme', self.get_fixme())
            ret |= _set_tag_val(tags, 'addr:postcode', self.postcode)
        if ret or self.state == 'modify':
            if bool(tags.get('source')) and (tags['source'] == self.source or 'EMUIA' in tags['source'].upper()):
                _remove_tag(tags, 'source')
            meta_kv['action'] = 'modify'
        if self.state in ('delete', 'modify'):
            meta_kv['action'] = self.state

        tags = tuple(map(lambda x: lxml.etree.Element('tag', attrib=OrderedDict((
            ('k', x[0]),
            ('v', x[1])
        ))),
                         sorted(tags.items())))
        if s['type'] == 'node':
            root = lxml.etree.Element('node', attrib=OrderedDict((
                                                                     ('lat', "{:0.7f}".format(s['lat'])),
                                                                     ('lon', "{:0.7f}".format(s['lon']))) +
                                                                 tuple(meta_kv.items())
                                                                 ))
            for i in tags:
                root.append(i)
        elif s['type'] == 'way':
            root = lxml.etree.Element('way', attrib=meta_kv)
            for i in tags:
                root.append(i)

            for i in s['nodes']:  # not sorting nodes, as the order defines the way
                root.append(root.makeelement('nd', attrib=OrderedDict({'ref': str(i)})))

        elif s['type'] == 'relation':
            root = lxml.etree.Element('relation', attrib=meta_kv)
            for i in tags:
                root.append(i)

            for i in s['members']:  # not sorting relation memebers, as this might be important
                root.append(root.makeelement('member', attrib=OrderedDict((
                    ('ref', str(i['ref'])),
                    ('type', i['type']),
                    ('role', i.get('role', ''))
                ))))
        else:
            raise ValueError("Unsupported objtype: %s" % (s.objtype,))
        return root


class Merger(object):
    __log = logging.getLogger(__name__).getChild('Merger')

    def __init__(self, impdata: typing.List[Address], asis: osmshapedb.GeometryHandler, terc: str, source_addr: str):
        self.impdata = impdata
        for entry in self.impdata:
            if not entry.source:
                entry.source = source_addr
        self.asis = asis
        self._import_area_shape = Point(0, 0).buffer(400) if not terc else get_boundary_shape(terc)
        self.imp_obj_by_id = dict(zip(itertools.count(), self.impdata))
        self.imp_index = rtree.index.Index()
        for (key, value) in self.imp_obj_by_id.items():
            self.imp_index.insert(key, (value.center.y, value.center.x))
        self.address_index = dict((x.get_index_key(), x) for x in self.impdata)
        self._new_nodes: typing.List[OsmDbEntry] = []
        self._updated_nodes: typing.List[OsmDbEntry] = []
        self._soup_visible: typing.List[OsmDbEntry] = []
        self._state_changes: typing.List[OsmDbEntry] = []
        self._node_id = 0
        self.pre_func = []
        self.post_func = []
        self.source_addr = source_addr

        ways_for_node = defaultdict(list)
        for way in filter(lambda x: x['type'] == 'way', asis.elements):
            for node in way['nodes']:
                ways_for_node[node].append(way['id'])

        from_soup = functools.partial(OsmAddress.from_soup, ways_for_node=ways_for_node)
        self.osmdb = OsmDb(
            self.asis,
            valuefunc=from_soup,
            indexes={'address': lambda x: x.get_index_key(), 'id': lambda x: x.osmid},
            index_filter=lambda x: (x['tags'].get('building', False)
                                    or x.entry.housenumber) and self._import_area_shape.contains(x.shape)
        )

    def create_index(self, message=""):
        self.osmdb.update_index(message)

    def merge(self):
        self.__log.debug("Starting premerger functinos")
        self._pre_merge()
        self.create_index("[3/14]")
        self.__log.debug("Starting merge functinos")
        self._do_merge()
        self.__log.debug("Starting postmerge functinos")
        self._post_merge()

    def set_state(self, node, value):
        self._state_changes.append(node)
        for i in node.ref_ways:
            self._state_changes.append(self.osmdb.get_by_id('way', i))
        node.set_state(value)

    def _fix_wesola(self, entry):
        if entry.get('tags', {}).get('addr:street', "").endswith(' (W)'):
            entry['tags']['addr:street'] = entry['tags']['addr:street'][:-4]
            self._state_changes.append(self.osmdb.get_by_id(entry['type'], entry['id']))

    def _pre_merge(self):
        # for custom fixes
        # for entry in self.asis['elements']:
        #    self._fix_wesola(entry)
        def process(entry):
            self._fix_similar_addr(entry)
            tuple(map(lambda f: f(entry), self.pre_func))

        for x in tqdm.tqdm(self.impdata, desc="[2/14] Running pre-merge functions"):  # type: Address
            if x.center.within(self._import_area_shape):
                process(x)

    def _fix_similar_addr(self, entry):
        # look for near same address
        # change street names to values from OSM
        # change housenumbers to values from import
        node = next(
            (
                x for x in itertools.islice(
                    (x for x in self.osmdb.nearest(entry.center, num_results=100) if x.housenumber),
                    0,
                    10
                ) if entry.similar_to(x)
            )
            , None
        )
        if not node:
            return
        how_far = node.distance(entry)
        if node and node.street and entry.street and node.street != entry.street and \
                ((node.objtype == 'node' and how_far < 5.0) or (
                        node.objtype == 'way' and (node.contains(entry.center) or how_far < 10.0))):
            # there is some similar address nearby but with different street name
            if node.objtype == 'node':
                node.add_fixme('Street name in OSM: ' + node.street)
                node.entry.street = entry.street
                self.set_state(node, 'modify')

        if node and node.street == entry.street and node.city == entry.city and \
                node.housenumber != entry.housenumber and ((node.objtype == 'node' and how_far < 5.0) or (
                node.objtype == 'way' and (node.contains(entry.center) or how_far < 10.0))):
            # there is only difference in housenumber, that is similiar
            if node.housenumber.upper() != entry.housenumber.upper():
                clean = lambda x: x.upper().replace(' ', '')
                if clean(node.housenumber) == clean(entry.housenumber) and len(node.housenumber) < len(
                        entry.housenumber):
                    # difference only in spaces, no spaces in OSM do not change address in OSM
                    return
                # if there are some other differences than in case, then add fixme
                self.__log.info("Updating housenumber from %s to %s", node.housenumber, entry.housenumber)
                entry.add_fixme('House number in OSM: %s' % (node.housenumber,))
            # make this *always* visible, to verify, if OSM value is correct. Hope that entry will
            # eventually get merged with node
            self.set_state(node, 'modify')
            node.entry.housenumber = entry.housenumber

    def _fix_obsolete_emuia(self, entry):
        existing = self.osmdb.getbyaddress(entry.get_index_key())
        if existing:
            # we have something with this address in db
            # sort by distance
            emuia_nodes = sorted(tuple(filter(lambda x: x.is_emuia_addr() and x.only_address_node(), existing)),
                                 key=lambda x: x.distance(entry))

            # update location of first node if from EMUiA
            if emuia_nodes:
                emuia_nodes[0].location = entry.location

            # all the others mark for deletion
            if len(emuia_nodes) > 1:
                for node in emuia_nodes[1:]:
                    self.set_state(node, 'delete')

    def _do_merge(self):
        for entry in tqdm.tqdm(self.impdata, desc="[4/14] Merging"): # type: Address
            if entry.center.within(self._import_area_shape):
                self._do_merge_one(entry)

    def _do_merge_one(self, entry):
        self.__log.debug("Processing address: %s", entry)
        return any(map(lambda x: x(entry),
                       (
                           # first returning true will stop exection of the chain
                           self._do_merge_by_existing,
                           self._do_merge_by_within,
                           self._do_merge_by_nearest,
                           self._do_merge_create_point,
                       )
                       ))

    def _do_merge_by_existing(self, entry):
        existing = tuple(filter(lambda x: self._import_area_shape.contains(x.center),
                                self.osmdb.getbyaddress(entry.get_index_key())))
        self.__log.debug("Found %d same addresses", len(existing))
        # create tuples (distance, entry) sorted by distance
        existing = sorted(map(lambda x: (x.distance(entry), x), existing), key=lambda x: x[0])
        if existing:
            # report duplicates
            if len(existing) > 1:
                self.__log.warning("More than one address node for %s. %s",
                                   entry,
                                   ", ".join("Id: %s, dist: %sm" % (x[1].osmid, str(x[0])) for x in existing)
                                   )

            if max(x[0] for x in existing) > 50:
                for (dist, node) in existing:
                    if dist > 50:
                        if not (
                                (
                                        node.objtype in ('way', 'relation') and
                                        node.buffered_shape(50).contains(entry.center)
                                ) or (
                                        # if node is within other way/relation with the same address do not mark it if
                                        # the way is not away more than 50 to avoid to many warnings
                                        node.objtype == 'node' and any(
                                            (
                                                    (
                                                            node.within(x.shape) and
                                                            x.buffered_shape(50).contains(entry.center)
                                                    )
                                                    for (_, x) in existing if x.objtype in ('way', 'relation')
                                            )
                                        )
                                )
                        ):
                            # ignore the distance, if the point is within the node
                            self.__log.warning("Address (id=%s) %s is %d meters from imported point",
                                               node.osmid, entry, dist)
                            node.add_fixme("Node is %d meters away from imported point" % dist)
                    self.set_state(node, 'visible')
                if min(x[0] for x in existing) > 50:
                    if any(map(
                            lambda x: x[1].objtype in ('way', 'relation') and x[1].contains(entry.center),
                            existing)):
                        # if any of existing addresses is a way/relation within which we have our address
                        # then skip
                        pass
                    else:
                        self.__log.debug("Creating address node, as closest address is farther than 50m")
                        self._create_point(entry)
                        return True

            building = next(
                (x for (_, x) in existing if x.objtype in ('way', 'relation' and x.contains(entry.center))),
                None
            )

            if building:
                # there is existing building with same address that contains processed entry
                building_center = (building.center.y, building.center.x) * 2

                if len(list(itertools.islice(
                        (
                                x for x in
                                (
                                        self.imp_obj_by_id[x] for x in self.imp_index.nearest(building_center, 20)
                                ) if building.contains(x.center)
                        ),
                        0,
                        2)
                )) > 1:
                    # we have more than one address within this building
                    # clear address from the building and create point
                    self._create_point(entry)
                    building._raw['tags'] = dict(
                        (key, "" if (key.startswith('addr:') or key == 'source:addr') else value)
                        for key, value in building._raw['tags'].items()
                    )
                    building.clear_fixme()
                    self.set_state(building, "modify")
                    return True
            # update data only on first duplicate, rest - leave to OSM-ers
            self._update_node(existing[0][1], entry)
            return True
        return False

    def _do_merge_by_within(self, entry):
        # look for building nearby
        candidates_within = list(
            itertools.islice(
                (
                    x for x in self.osmdb.nearest(entry.center, num_results=100)
                    if x.objtype in ('way', 'relation') and x.contains(entry.center)
                ),
                0,
                10
            )
        )
        self.__log.debug("Found %d buildings containing address", len(candidates_within))

        if candidates_within:
            c = candidates_within[0]
            if not c.housenumber:
                # no address on way/relation -> add address
                # create a point, will be merged with building later
                self.__log.debug("Creating address node as building contains no address")
                self._create_point(entry)
                return True
            else:
                # WARNING - candidate has an address
                if c.similar_to(entry) and c.street == entry.street:
                    self.__log.debug("Updating OSM address: %s with import %s", c.entry, entry)
                    self._update_node(c, entry)
                    return True
                else:
                    c_center = (c.center.y, c.center.x) * 2
                    if len(list(itertools.islice(
                            (
                                    x for x in
                                    (
                                            self.imp_obj_by_id[x] for x in self.imp_index.nearest(c_center, 20)
                                    ) if c.contains(x.center)
                            ),
                            0,
                            2)
                    )) > 1 or not self.handle_one_street_name_change(c, entry):
                        if not c.get_index_key() in self.address_index:
                            # create address point from building only if the address on building is different
                            # than addresses in import
                            new_entry = self.osmdb.add_new({
                                'type': 'node',
                                'id': self._get_node_id(),
                                'lat': c.center.y,
                                'lon': c.center.x,
                                'tags': dict((key, value) for key, value in c._raw['tags'].items()
                                             if key.startswith('addr:') or key == 'source:addr')
                            })
                            self._new_nodes.append(new_entry)
                        # remove address from building
                        c._raw['tags'] = dict(
                            (key, "" if (key.startswith('addr:') or key == 'source:addr') else value)
                            for key, value in c._raw['tags'].items()
                        )
                        c.clear_fixme()
                        self.set_state(c, "modify")
                        self._create_point(entry)
                    return True
        return False

    def _do_merge_by_nearest(self, entry):
        candidates = list(self.osmdb.nearest(entry.center, num_results=10))
        candidates_same = [x for x in candidates if x.housenumber == entry.housenumber and x.distance(entry) < 2.0]
        if len(candidates_same) > 0:
            # same location, both are an address, and have same housenumber, can't be coincidence,
            # probably mapper changed something
            for node in candidates_same:
                found = False
                if node.similar_to(entry):
                    found = True
                    self.__log.debug("Updating near node from: %s to %s", node.entry, entry)
                    # as node.similar_to(entry) only changes in street might happened
                    node.add_fixme("Street name in OSM: " + node.street)
                    self._update_node(node, entry)
                if found:
                    return True
            if any(map(lambda x: x.housenumber and x.city, candidates_same)):
                self.__log.info(
                    "Found probably same address node at (%s, %s). Skipping. Import address is: %s, osm addresses: %s",
                    entry.location['lon'], entry.location['lat'], entry, ", ".join(
                        map(lambda x: str(x.entry), candidates_same))
                )
                return True

        candidates_same = [
            x for x in candidates if all(
                getattr(x, attr) == getattr(entry, attr) for attr in ('city', 'simc', 'street', 'sym_ul')
            ) and x.distance(entry) < 2.0
        ]
        if len(candidates_same) > 0:
            # same location, both are address but different house numbers
            # update house number in osm
            for node in candidates_same:
                self._update_node(node, entry)
            return True
        return False

    def _do_merge_create_point(self, entry):
        if not self._import_area_shape.contains(entry.center):
            self.__log.warning("Imported address %s outside import borders", entry)
        self._create_point(entry)
        return True

    def _update_node(self, node, entry):
        self.__log.debug("Cheking if there is something to update for node %s, address: %s", node.osmid, node.entry)
        if node.update_from(entry):
            self.__log.debug("Updating node %s using %s", node.osmid, entry)
            self._updated_nodes.append(node)

    def _create_point(self, entry):
        self.__log.debug("Creating new point")
        soup = {
            'type': 'node',
            'id': self._get_node_id(),
            'lat': float(entry.location['lat']),
            'lon': float(entry.location['lon']),
        }
        new = self.osmdb.add_new(soup)
        new.update_from(entry)
        self._new_nodes.append(new)
        # TODO: check that soup gets address tags
        # self.asis['elements'].append(soup)

    def _mark_soup_visible(self, obj):
        self._soup_visible.append(obj)

    def _get_node_id(self):
        self._node_id -= 1
        return self._node_id

    def _get_all_changed_nodes(self) -> typing.Tuple[OsmDbEntry]:
        ret: typing.Dict[str, OsmDbEntry] = dict((x.osmid, x) for x in self._updated_nodes)
        ret.update(dict((x.osmid, x) for x in self._new_nodes))
        self.__log.info("Modified objects: %d", len(ret))
        ret.update(dict((x.osmid, x) for x in self._state_changes))
        ret.update(dict((x.osmid, x) for x in self.osmdb.get_all_values() if
                        x.state in ('modify', 'delete') and x.osmid not in ret.keys()))

        for (_id, i) in sorted(ret.items(), key=lambda x: x[0]):
            if i in self._updated_nodes:
                self.__log.debug("Processing updated node: %s", str(i.entry))
            elif i in self._new_nodes:
                self.__log.debug("Processing new node: %s", str(i.entry))
            elif i.state in ('modify', 'delete'):
                self.__log.debug("Processing node - changed: %s, %s", i.state, str(i.entry))

        return tuple(ret.values())

    def _get_all_visible(self):
        ret = dict((x.osmid, x) for x in self._soup_visible)
        ret.update(dict(
            (x.osmid, x) for x in self.osmdb.get_all_values() if x.state == 'visible' and x.osmid not in ret.keys()))
        return tuple(ret.values())

    def _get_all_reffered_by(self, lst: typing.Iterable[OsmDbEntry]) -> typing.Iterable[OsmDbEntry]:
        ret = set()

        __referred_cache = dict()

        def get_referred(node, exclude_ids=()) -> typing.Iterable[typing.Tuple[str, int]]:
            referrers = __referred_cache.get(node.osmid)
            if not referrers:
                referrers = get_referred_cached(node, exclude_ids)
                __referred_cache[node.osmid] = referrers
            return referrers

        def get_referred_cached(node, exclude_ids=()) -> typing.Iterable[typing.Tuple[str, int]]:
            if node.osmid in exclude_ids:
                return set()
            if node['type'] == 'node':
                return set(
                    itertools.chain(
                        itertools.chain.from_iterable(
                            get_referred(self.osmdb.get_by_id('way', x), exclude_ids) for x in node.ref_ways if "way:{}".format(x) not in exclude_ids
                        ),
                        (('node', node['id']),)
                    )
                )
            if node['type'] == 'nd':
                return set(
                    itertools.chain(
                        itertools.chain.from_iterable(
                            get_referred(self.osmdb.get_by_id('way', x), exclude_ids) for x in node.ref_ways
                            if "way:{}".format(x) not in exclude_ids
                        ),
                        (('node', node['ref']),)
                    )
                )
            if node['type'] == 'way':
                return itertools.chain(
                    itertools.chain.from_iterable(
                        get_referred(
                            self.osmdb.get_by_id('node', x),
                            exclude_ids=exclude_ids + ("way:{}".format(node['id']),)
                        ) for x in node['nodes']
                    ),
                    (('way', node['id']),)
                )
            if node['type'] == 'member':
                return get_referred(self.osmdb.get_by_id(node['type'], int(node['ref'])))
            if node['type'] == 'relation':
                return itertools.chain(
                    itertools.chain.from_iterable(
                        get_referred(self.osmdb.get_by_id(x['type'], int(x['ref']))) for x in node['members']
                    ),
                    (('relation', node['id']),)
                )
            raise ValueError("Unknown node type: %s" % node.name)

        for i in tqdm.tqdm(lst, desc="[14/14] Generating output") :
            ret = ret.union(get_referred(i))

        return tuple(map(
            lambda x: self.osmdb.get_by_id(x[0], x[1]),
            sorted(ret, key=lambda x: "%s:%s" % (x[0], x[1]))
        ))

    def _post_merge(self):
        # recreate index
        self.create_index("[5/14]")
        self.handle_street_name_changes()
        self.create_index("[7/14]")
        self.mark_not_existing()
        self.create_index("[9/14]")
        for i in self.post_func:
            i()
        self.create_index("[13/14]")

    def mark_not_existing(self):
        imp_addr = set(map(lambda x: x.get_index_key(), self.impdata))
        # from all addresses in OsmDb remove those imported
        to_delete = set(
            filter(
                lambda x: any(
                    map(lambda y: self._import_area_shape.contains(y.center), self.osmdb.getbyaddress(x))
                ),
                tqdm.tqdm(self.osmdb.getalladdress(), desc="[8/14] Looking for not existing addresses")
            )
        ) - imp_addr

        self.__log.debug("Marking %d not existing addresses", len(to_delete))
        for addr in filter(any, to_delete):  # type: OsmDbEntry
            # at least on addr field is filled in
            for node in filter(
                    lambda x: self._import_area_shape.contains(x.shape),
                    self.osmdb.getbyaddress(addr)
            ):  # type: OsmDbEntry
                if self._import_area_shape.contains(node.shape) and \
                        not (('e-mapa.net' in self.source_addr and node.source != self.source_addr and
                              'e-mapa.net' in node.source)
                             or (self.source_addr == 'emuia.gugik.gov.pl' and 'e-mapa.net' in node.source)):
                    # if we are importing from iMPA, and the point is from other iMPA import, then skip it
                    # if we are importing from GUGiK, skip points from iMPA
                    # report only points within area of interest
                    self.__log.debug("Marking node to delete - address %s does not exist: %s, %s", addr, node.osmid,
                                     str(node.entry))
                    node.add_fixme('Check address existence')
                    self.set_state(node, 'visible')

    def merge_addresses(self):
        self._merge_addresses_buffer(0, "[10/14]")
        self._merge_addresses_buffer(2, "[11/14]")
        self._merge_addresses_buffer(5, "[12/14]")

    def _merge_one_address(self, building: typing.Dict[str, typing.Any], addr: OsmDbEntry):
        # as we merge only address nodes, do not pass anything else
        if addr.get_fixme() and not addr.is_new():
            self.set_state(addr, 'visible')
        else:
            building_obj = self.osmdb.get_by_id(building['type'], building['id'])
            fixme = building_obj.osm_fixme
            for (key, value) in addr.get_tag_soup().items():
                oldval = building['tags'].get(key)
                if oldval and oldval != value:
                    self.__log.info('Changing tag: %s from %s to %s for address: %s', key, oldval, value, addr.entry)
                building['tags'][key] = value
            fixme += addr.get_fixme()
            # TODO
            # building_obj.clear_fixme()
            if fixme or building_obj.get_fixme():
                building_obj.clear_fixme()
                building_obj.add_fixme(fixme)
            building_obj.set_state('modify')
            self.set_state(addr, 'delete')
            self._updated_nodes.append(building_obj)

    def _merge_addresses_buffer(self, buf=0, message=""):
        self.__log.info("Merging building with buffer: %d", buf)
        to_merge = self._prepare_merge_list(buf, message)
        buildings = dict(
            ((x['type'], x['id']), x) for x in self.asis.elements if x['type'] in ('way', 'relation')
        )

        self.__log.info("Merging %d addresses with buildings",
                        len(tuple(filter(lambda x: len(x[1]) == 1, to_merge.items()))))

        for (_id, nodes) in sorted(to_merge.items(), key=lambda x: x[0]):
            building = buildings[_id]
            if len(nodes) > 0:
                self._mark_soup_visible(self.osmdb.get_by_id(*_id))

            self._merge_building_with_addresses(_id, building, nodes)

        self.__log.info("Finished merging addresses with buildings")

    def _merge_building_with_addresses(self, _id: str, building: typing.Dict[str, typing.Any],
                                       nodes: typing.List[OsmDbEntry]):

        def building_tag(tag: str) -> str:
            return building['tags'].get(tag, '')

        if len(nodes) == 1 or all(map(
                lambda x: x[0].similar_to(x[1]) and x[0].street == x[1].street,
                itertools.combinations(nodes, 2)
        )):
            # if there is only one candidate, or all candidates are similar addresses on same street
            if building_tag('addr:housenumber') and not (
                    nodes[0].similar_to(self.osmdb.get_by_id(building['type'], building['id'])) and
                    nodes[0].street == self.osmdb.get_by_id(building['type'], building['id']).street
            ):
                # if building has different address, than we want to put
                self.__log.info("Skipping merging address: %s, as building already has an address: %s.",
                                str(nodes[0].entry), OsmAddress.from_soup(building, location=shapely.geometry.Point(0, 0)))
                # mark only visible, allow for other rules to work - so no return
                for node in nodes:
                    self._mark_soup_visible(node)
            else:
                # if building has similar address, just merge
                self.__log.debug("Merging address %s with building %s", str(nodes[0].entry), _id)
                for node in nodes:
                    self._merge_one_address(building, node)
                return

        if len(nodes) > 1:
            for node in nodes:
                self._mark_soup_visible(node)

    def _prepare_merge_list(self, buf, message="") -> typing.DefaultDict[str, typing.List[OsmAddress]]:
        """

        :param buf: defines how big buffer around buildings to consider when merging
        :param message: message for progress bar
        :return: dictionary with osmid of the building as key and list of nodes with addresses within this building
        """
        ret = defaultdict(list)
        for addr in tqdm.tqdm(
                [
                        x for x in
                        (
                                self.osmdb.get_by_id(x['type'], x['id']) for x in self.asis.elements
                                if x['type'] == 'node' and x.get('tags', {}).get('addr:housenumber')
                        )
                        if x.shape.within(self._import_area_shape)
                ],
                desc="{} Preparing merge list (buf={})".format(message, buf)
        ):  # type: OsmDbEntry
            self.__log.debug("Looking for candidates for: %s", str(addr.entry))
            if addr.only_address_node() and addr.state != 'delete' and (
                    self._import_area_shape.contains(addr.center)):
                # do not use nodes as candidates, as they will never match
                candidates = list(
                    itertools.islice(
                        (
                            x for x in self.osmdb.nearest(addr.center, num_results=1000)
                            if x.objtype in ('way', 'relation')
                        ),
                        0,
                        20
                    )
                )
                candidate_within = next(
                    (
                        x for x in candidates if
                        x.objtype == 'relation' and
                        x.osmid != addr.osmid and
                        addr.center.within(x.buffered_shape(buf) if buf else x.shape)
                    ),
                    None
                )
                if not candidate_within:
                    candidate_within = next(
                        (
                            x for x in candidates if
                            x.objtype == 'way' and
                            x.osmid != addr.osmid and
                            addr.center.within(x.buffered_shape(buf) if buf else x.shape)
                        ),
                        None
                    )
                if candidate_within:
                    if len(list(itertools.islice(
                            (
                                    x for x in
                                    (
                                        self.imp_obj_by_id[x] for x in self.imp_index.nearest(
                                            (candidate_within.center.y, candidate_within.center.x) * 2,
                                            20
                                        )
                                    ) if candidate_within.buffered_shape(buf).contains(x.center)
                            ),
                            0,
                            2
                        ))
                    ) <= 1:
                        # only merge, when there is less than one import address within building + buf
                        ret[candidate_within.osmid_tuple].append(addr)
                        self.__log.debug("Found: %s", candidate_within.osmid)
                    else:
                        candidate_within.set_state('visible')
        return ret

    def _get_osm_xml(self, nodes, log_io=None):
        return E.osm(
            E.note('The data included in this document is from www.openstreetmap.org. '
                   'The data is made available under ODbL.' + ('\n' + log_io.getvalue() if log_io else '')),
            E.meta(osm_base=""),  # self.asis.get('osm3s', {}).get('timestamp_osm_base', '')),
            *tuple(map(OsmAddress.to_osm_soup, nodes)),
            version='0.6', generator='import adresy merger.py'
        )

    def get_incremental_result(self, log_io=None):
        changes = self._get_all_changed_nodes()
        self.__log.info("Generated %d changes", len(changes))
        nodes = self._get_all_reffered_by(changes + self._get_all_visible())
        return lxml.etree.tostring(self._get_osm_xml(nodes, log_io),
                                   pretty_print=True, xml_declaration=True, encoding='UTF-8')

    def get_full_result(self, log_io=None):
        return lxml.etree.tostring(
            self._get_osm_xml(
                sorted(
                    (x for x in self.osmdb.get_all_values() if x.shape.within(self._import_area_shape)),
                    key=lambda x: x.osmid
                ),
                log_io),
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8'
        )

    def handle_one_street_name_change(self, osm_addr, imp_addr) -> bool:
        if osm_addr \
                and osm_addr.housenumber.upper().replace(' ', '') == imp_addr.housenumber.upper().replace(' ', '') \
                and osm_addr.city == imp_addr.city \
                and osm_addr.street != imp_addr.street:
            osm_addr.add_fixme('Street name in OSM: ' + osm_addr.street)
            osm_addr.update_from(imp_addr)
            self._updated_nodes.append(osm_addr)
            return True

    def handle_street_name_changes(self):
        """
            If the imported point is within a building, that has the same housenumber and city, and there is symul
            in imported data, then update the street name from imported point
        """

        for entry in tqdm.tqdm(self.impdata, desc="[6/14] Detecting street name changes"):  # type: Address
            if not entry.center.within(self._import_area_shape):
                continue
            candidate = next(
                (
                    x for x in itertools.chain(
                        itertools.islice(
                            (x for x in self.osmdb.nearest(entry.center, num_results=100) if x.objtype == 'relation'),
                            0,
                            10
                        ),
                        itertools.islice(
                            (x for x in self.osmdb.nearest(entry.center, num_results=100) if x.objtype == 'way'),
                            0,
                            10
                        )
                    ) if x.contains(entry.center)
                ),
                None
            )

            if not self.handle_one_street_name_change(candidate, entry):
                # try to find node
                candidate = next(
                    itertools.takewhile(
                        lambda x: distance(x.center, entry.center) < 10,
                        (
                            x for x in self.osmdb.nearest(entry.center, num_results=1000)
                            if x.objtype == 'node' and x.housenumber
                        )
                    ),
                    None
                )
                self.handle_one_street_name_change(candidate, entry)

    def mark_all_nodes_visible(self):
        for obj in self.osmdb.get_all_values():
            if obj.housenumber and obj.entry['type'] == 'node' and obj.shape.within(self._import_area_shape):
                self._mark_soup_visible(obj)


def get_referenced_objects(query, prefix=""):
    return """
[out:xml]
[timeout:600];
%s
(
    %s
)->.a;
(
  node(w.a);
  node(r.a);
  way(r.a);
  way(bn.a);
  relation(bn.a);
  relation(bw.a);
)->.b;
(
  node(w.b);
  node(r.b);
  way(r.b);
)->.c;
(
    node(w.c);
)->.d;
.a out meta ;
.b out meta ;
.c out meta ;
.d out meta ;
    """ % (prefix, query)


def get_addresses(bbox):
    bbox = ",".join(bbox)
    query = """
  node
    (%s)
    ["addr:housenumber"]
    ["amenity"!~"."]
    ["shop"!~"."]
    ["tourism"!~"."]
    ["emergency"!~"."]
    ["company"!~"."];
  way
    (%s)
    ["addr:housenumber"];
  way
    (%s)
    ["building"];
  relation
    (%s)
    ["addr:housenumber"];
  relation
    (%s)
    ["building"];
""" % (bbox, bbox, bbox, bbox, bbox,)
    index = utils.osmshapedb.get_geometries(overpass.query(get_referenced_objects(query), desc="get_addresses"))
    return index


def get_addresses_terc(terc):
    prefix = """
    area["boundary"="administrative"]
        ["admin_level"="7"]
        ["teryt:terc"~"^%s"]
        ["type"="boundary"]->.boundary_area;    
    """ % (terc, )
    query = """
    (
        node(area.boundary_area)["addr:housenumber"];
        way(area.boundary_area)["addr:housenumber"];
        way(area.boundary_area)["building"];
        relation(area.boundary_area)["addr:housenumber"];
        relation(area.boundary_area)["building"];
    );
    """
    return utils.osmshapedb.get_geometries(overpass.query(get_referenced_objects(query, prefix), desc="get_addresses"))


def get_boundary_shape(terc):
    query = """
[out:xml]
[timeout:600];
relation
    ["teryt:terc"~"^%s"];
out meta ;
>;
out meta ;
""" % (terc,)
    soup = overpass.query(query, desc="get_boundary")
    index = utils.osmshapedb.get_geometries(soup)

    boundaries = tuple(x for x in index.elements if x['type'] == 'relation' and
                       x['tags'].get('teryt:terc', '') == terc)
    if len(boundaries) > 1:
        __log.error("More than one relation found with terc: %s. Names: %s. Fix before continuing",
                    terc, ", ".join(map(lambda x: x['tags'].get('name'), boundaries)))
        sys.exit(1)
    if len(boundaries) == 1:
        rel = boundaries[0]
    else:
        rel = tuple(x for x in index.elements if x['type'] == 'relation' and
                    x['tags'].get('teryt:terc', '').startswith(terc))[0]
    __log.info("Loading shape of import area - relation id: %s, relation name: %s", rel['id'], rel['tags'].get('name'))
    ret = index.geometries["{}:{}".format(rel['type'], rel['id'])]
    return simplified_shape_poland(ret, tolerance=5)


def main():
    # TODO: create mode where no unchanged data are returned (as addresses to be merged with buildings)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="""Merge data from WMS with OSM data. Generate output OSM file for """
                                                 """JOSM. You need to provide one of:
    1. --impa with service name
    2. --import-file and --addresses-file
    3. --import-file and --terc """)
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('--impa', help='name of iMPA service, use "milawa" when the address is milawa.e-mapa.net')
    source_group.add_argument('--import-file', type=argparse.FileType("r", encoding='UTF-8'), dest='import_file',
                              help='JSON file generated by punktyadresowe_import.py for the area')
    source_group.add_argument('--gugik', action='store_const', const=True, dest='gugik', default=False,
                              help='Import address data from gugik. Select area by providing terc option')
    source_group.add_argument('--gugik_gml', help='Import address data from gugik. Provide filename as argument.')
    source_group.add_argument('--gisnet',
                              help='Import address data from GIS-NET. Use "nowosolna" when the address is '
                                   'nowosolna.gis-net.pl. You need to provide also terc option')
    source_group.add_argument('--warszawa', action='store_const', const=True, dest='warszawa', default=False,
                              help='Import address data from UM Warszawa. You need to provide terc option')
    source_group.add_argument('--gison',
                              help='Import address data from GISON. Use "brzeznica" when the address is '
                                   'http://portal.gison.pl/brzeznica/. You need to provide also terc option')
    source_group.add_argument('--egeoportal',
                              help='Import address data from E-Geoportal. You need to provide terc option as well')
    address_group = parser.add_argument_group()
    address_group.add_argument('--addresses-file', type=argparse.FileType("r", encoding='UTF-8'), dest='addresses_file',
                               help='OSM file with addresses and buildings for imported area')
    address_group.add_argument('--terc',
                               help='teryt:terc code, for which to download addresses from OSM using Overpass API')

    parser.add_argument('--output', type=argparse.FileType('w+b'), default='result.osm',
                        help='output file with merged data (default: result.osm)')
    parser.add_argument('--full', action='store_const', const=True, dest='full_mode', default=False,
                        help='Use to output all address data for region, not only modified address data as per default')
    parser.add_argument('--no-merge', action='store_const', const=True, dest='no_merge', default=False,
                        help='Do not merger addresses with buildings')
    parser.add_argument('--log-level', dest='log_level', default=20, type=int,
                        help='Set logging level (debug=10, info=20, warning=30, error=40, critical=50), default: 20')
    parser.add_argument('--import-wms', dest='wms',
                        help='WMS address for address layer, ex: '
                             'http://www.punktyadresowe.pl/cgi-bin/mapserv?map=/home/www/impa2/wms/luban.map . '
                             'Bounding box is still fetched via iMPA')

    args = parser.parse_args()

    log_stderr = logging.StreamHandler()
    log_stderr.setLevel(args.log_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(module)s] %(name)s  - %(funcName)s(): %(message)s')
    log_stderr.setFormatter(formatter)

    log_io = io.StringIO()
    log_io_ch = logging.StreamHandler(log_io)
    log_io_ch.setLevel(logging.DEBUG)
    log_io_ch.setFormatter(formatter)

    logging.basicConfig(level=10, handlers=[log_stderr, log_io_ch])
    logging.getLogger("converters").setLevel(logging.INFO)

    terc = None
    if args.impa:
        imp = iMPA(args.impa, wms=args.wms)
        terc = imp.terc
        source_addr = args.impa + '.e-mapa.net'
    elif args.gisnet:
        imp = GISNET(args.gisnet, args.terc)
        terc = args.terc
        source_addr = args.gisnet + '.gis-net.pl'
    elif args.warszawa:
        imp = WarszawaUM('Warszawa', args.terc)
        terc = args.terc
        source_addr = 'mapa.um.warszawa.pl'
    elif args.gugik_gml:
        imp = GUGiK_GML(args.gugik_gml)
        terc = imp.terc
        source_addr = 'emuia.gugik.gov.pl'
    elif args.gison:
        imp = GISON(args.gison, args.terc)
        terc = args.terc
        source_addr = 'portal.gison.pl/' + args.gison
    elif args.egeoportal:
        imp = EGeoportal(args.egeoportal, args.terc)
        terc = args.terc
        source_addr = 'e-geportal.pl/' + args.egeoportal
    else:
        imp = GUGiK(args.terc)
        source_addr = 'emuia.gugik.gov.pl'

    if args.import_file:
        data_func = lambda: list(map(lambda x: Address.from_json(x), json.load(args.import_file)))
    else:
        data_func = lambda: imp.get_addresses()

    data = data_func()
    if len(data) == 0:
        raise ValueError("No data to import! Check your source")

    if args.terc:
        terc = args.terc
    __log.info("Working with TERC: %s", terc)

    if args.addresses_file:
        def addr_func():
            return lxml.etree.parse(args.addresses_file)
    else:
        # union with bounds of administrative boundary
        s = min(map(lambda x: x.center.y, data))
        w = min(map(lambda x: x.center.x, data))
        n = max(map(lambda x: x.center.y, data))
        e = max(map(lambda x: x.center.x, data))

        def addr_func():
            return get_addresses(map(str, (s, w, n, e)))

    addr = addr_func()

    if len(data) < 1:
        __log.warning("Warning - import data is empty. Check your import")
    __log.info('Processing %d addresses', len(data))

    if len(addr.elements) == 0:
        __log.warning("Warning - no data fetched from OSM. Check your file/terc code")

    # m = Merger(data, addr, terc, parallel_process_func=parallel_map)
    m = Merger(data, addr, terc, source_addr)
    if not args.no_merge:
        m.post_func.append(m.merge_addresses)
    m.merge()

    if args.full_mode:
        ret = m.get_full_result(log_io)
    else:
        ret = m.get_incremental_result(log_io)

    args.output.write(ret)


if __name__ == '__main__':
    main()
