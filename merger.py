#!/usr/bin/env python3.4

import argparse
import logging
import io
import itertools
import sys
import functools

from osmdb import OsmDb, get_soup_center, distance, prepare_object_pos
import json
from shapely.geometry import Point
import shapely.geometry.base
from punktyadresowe_import import iMPA, GUGiK, Address, GISNET, WarszawaUM, GUGiK_GML
import overpass
from utils import parallel_map
from lxml.builder import E
import lxml.etree
import converter

__log = logging.getLogger(__name__)

# depends FreeBSD
# portmaster graphics/py-pyproj devel/py-rtree devel/py-shapely www/py-beautifulsoup devel/py-lxml

# depeds Lubuntu:
# apt-get install python3-pyproj libspatialindex-dev python3-shapely python3-bs4 python3-lxml
# easy_install3 Rtree

# TODO: import admin_level=8 for area, and add addr:city if missing for addresses within that area (needs greater refactoring)
# TODO: check for alone addresses. Look for addresses that have greater minimal distance to greater than ?? avg*5? avg+stddev*3? http://en.wikipedia.org/wiki/Chauvenet%27s_criterion ? http://en.wikipedia.org/wiki/Peirce%27s_criterion ?

def create_property_funcs(field):
    def getx(self):
        return self._soup['tags'][field]
    def setx(self, val):
        self._soup['tags'][field] = val
    def delx(self):
        del self._soup['tags'][field]
    return property(getx, setx, delx, '%s property' % (field,))

class OsmAddress(Address):
    __log = logging.getLogger(__name__).getChild('OsmAddress')

    def __init__(self, soup, *args, **kwargs):
        self._soup = soup
        if 'tags' not in self._soup:
            self._soup['tags'] = {}
        super(OsmAddress, self).__init__(*args, **kwargs)
        self.state = None

    housenumber = create_property_funcs('addr:housenumber')
    postcode = create_property_funcs('addr:postcode')
    street = create_property_funcs('addr:street')
    city = create_property_funcs('addr:city')
    sym_ul = create_property_funcs('addr:street:sym_ul')
    simc = create_property_funcs('addr:city:simc')
    source = create_property_funcs('source:addr')
    id_ = create_property_funcs('ref:addr')

    def __getitem__(self, key):
        return self._soup[key]

    @staticmethod
    def from_soup(obj, obj_loc_cache=None):
        cache = obj.get('tags', {})

        loc = None
        if obj_loc_cache:
            loc = obj_loc_cache.get(obj['type'] + ':' + str(obj['id']))
        if not loc:
            loc = get_soup_center(obj)

        ret = OsmAddress(
            housenumber = cache.get('addr:housenumber', ''),
            postcode    = cache.get('addr:postcode', ''),
            street      = cache.get('addr:street', ''),
            city        = cache.get('addr:place', '') if cache.get('addr:place') else cache.get('addr:city', ''),
            sym_ul      = cache.get('addr:street:sym_ul', ''),
            simc        = cache.get('addr:city:simc', ''),
            source      = cache.get('source:addr', ''),
            location    = dict(zip(('lat', 'lon'), loc)),
            id_         = cache.get('ref:addr', ''),
            soup        = obj
        )

        fixme = cache.get('fixme')
        if fixme:
            ret.addFixme(fixme)
        if obj.get('action'):
            ret.state = obj['action']
        return ret

    def set_state(self, val):
        if val == 'visible' and self.state not in ('modify', 'delete'):
            self.state = val
        elif val == 'modify' and self.state != 'delete':
            self.state = val
        elif val == 'delete':
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

    def _getTagVal(self, key):
        return self._soup.get('tags')

    def _setTagVal(self, key, val):
        """returns True if something was modified"""
        n = self._soup['tags'].get(key)
        if n == val.strip():
            return False
        self._soup['tags'][key] = val.strip()
        return True

    def _removeTag(self, key):
        if key in self._soup['tags']:
            del self._soup['tags'][key]
            return True
        return False

    def shape(self):
        raise NotImplementedError

    @property
    def osmid(self):
        return "%s:%s" % (self.objtype, self._soup['id'])

    def isEMUiAAddr(self):
        ret = False
        if self.source:
            ret |= ('EMUIA' in source.upper())
        source_addr = self._getTagVal('source')
        if source_addr:
            ret |= ('EMUIA' in source_addr.upper())
        return ret

    def only_address_node(self):
        # return true, if its a node, has a addr:housenumber,
        # and consists only of tags listeb below
        if self.objtype != 'node':
            return False
        return self.housenumber and set(self._soup['tags'].keys()).issubset(
                            {'addr:housenumber', 'addr:street', 'addr:street:sym_ul', 'addr:place',
                            'addr:city', 'addr:city:simc', 'addr:postcode', 'addr:country', 'teryt:sym_ul',
                            'teryt:simc', 'source', 'source:addr', 'fixme', 'addr:street:source', 'ref:addr'}
        )

    def is_new(self):
        return self._soup['id'] < 0

    def get_tag_soup(self):
        return dict((k, v) for (k, v) in self._soup['tags'].items() if v)

    def updateFrom(self, entry):
        def update(name):
            old = getattr(self, name)
            new = getattr(entry, name)
            if new and old != new:
                setattr(self, name, new)
                if old:
                    self.__log.debug("Updating %s from %s to %s", name, old, new)
                return True
            return False

        ret = False
        for name in ('street', 'city', 'housenumber', 'postcode'):
            ret |= update(name)
        # update without changing ret status, so adding these fields will not trigger a change in OSM
        # but if there is something else added, this will get updated too
        for name in ('sym_ul', 'simc', 'source', 'id_'):
            update(name)
        if entry.getFixme():
            self.addFixme(entry.getFixme())
            self.set_state('visible')
        if ret:
            self.set_state('modify')
        return ret

    def to_osm_soup(self):
        def _removeTag(tags, key):
            if key in tags:
                del tags[key]
                return True
            return False

        def _setTagVal(tags, key, value):
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
        meta_kv = dict((k, str(v)) for (k, v) in s.items() if k in ('id', 'version', 'timestamp', 'changeset', 'uid', 'user'))
        # do not export ref:addr until the discussion will come to conclusion
        tags = dict((k,v.strip()) for (k,v) in s.get('tags', {}).items() if v.strip() and k != 'ref:addr' and k != 'addr:ref')

        ret = False
        if self.housenumber:
            if self.street:
                ret |= _removeTag(tags, 'addr:place')
            else:
                ret |= _setTagVal(tags, 'addr:place', self.city)
                ret |= _removeTag(tags, 'addr:street')
                ret |= _removeTag(tags, 'addr:city')
            if self.getFixme():
                ret |= _setTagVal(tags, 'fixme', self.getFixme())
            ret |= _setTagVal(tags, 'addr:postcode', self.postcode)
        if ret or self.state == 'modify':
            if bool(tags.get('source')) and (tags['source'] == self.source or 'EMUIA' in tags['source'].upper()):
                _removeTag(tags, 'source')
            meta_kv['action'] = 'modify'
        if self.state in ('delete', 'modify'):
            meta_kv['action'] = self.state

        tags = tuple(map(lambda x: E.tag(k=x[0], v=x[1]), tags.items()))
        if s['type'] == 'node':
            root = E.node(*tags, lat=str(s['lat']), lon=str(s['lon']), **meta_kv)
        elif s['type'] == 'way':
            nodes = map(lambda x: E.nd(ref=str(x)), s['nodes'])
            root = E.way(*itertools.chain(tags, nodes), **meta_kv)
        elif s['type'] == 'relation':
            members = map(lambda x: E.member(ref=str(x['ref']), type=x['type'], role=x.get('role', '')), s['members'])
            root = E.relation(*itertools.chain(tags, members), **meta_kv)
        else:
            raise ValueError("Unsupported objtype: %s" % (s.objtype,))
        return root


class Merger(object):
    __log = logging.getLogger(__name__).getChild('Merger')

    def __init__(self, impdata, asis, terc, source_addr, parallel_process_func=lambda func, elems: tuple(map(func, elems))):
        self.impdata = impdata
        self.asis = asis
        obj_loc_cache = prepare_object_pos(asis['elements'])
        from_soup = functools.partial(OsmAddress.from_soup, obj_loc_cache = obj_loc_cache)
        self.osmdb = OsmDb(self.asis, valuefunc=from_soup, indexes={'address': lambda x: x.get_index_key(), 'id': lambda x: x.osmid})
        self._new_nodes = []
        self._updated_nodes = []
        self._node_id = 0
        self.pre_func = []
        self.post_func = []
        self._soup_visible = []
        if terc:
            self._import_area_shape = get_boundary_shape(terc)
        self._state_changes = []
        self._parallel_process_func = parallel_process_func
        self.source_addr = source_addr

    def _create_index(self):
        self.osmdb.update_index()

    def merge(self):
        self.__log.debug("Starting premerger functinos")
        self._pre_merge()
        self._create_index()
        self.__log.debug("Starting merge functinos")
        self._do_merge()
        self.__log.debug("Starting postmerge functinos")
        self._post_merge()

    def set_state(self, node, value):
        self._state_changes.append(node)
        node.set_state(value)

    def _pre_merge(self):
        def process(entry):
            self._fix_similar_addr(entry)
            tuple(map(lambda x: x(self, entry), self.pre_func))
        self._parallel_process_func(process, self.impdata)

    def _fix_similar_addr(self, entry):
        # look for near same address
        # change street names to values from OSM
        # change housenumbers to values from import
        try:
            node = next(filter(lambda x: entry.similar_to(x), self.osmdb.nearest(entry.center, num_results=10)))
            how_far = node.distance(entry)
            if node and node.street and entry.street and node.street != entry.street and \
                ((node.objtype == 'node' and how_far < 5.0) or (node.objtype == 'way' and (node.contains(entry.center) or how_far < 10.0))):
                # there is some similar address nearby but with different street name
                log_level = logging.WARNING
                if max(entry.street.split(' '), key=len) in node.street:
                    # lower the logging level, is the longest string in entry is contained in replacement value
                    log_level = logging.DEBUG
                else:
                    entry.addFixme('Street name in import source: %s' % (entry.street,))
                self.__log.log(log_level, "Changing street name from %s in import to %s as in OSM (%s), distance=%.2fm",
                            entry.street, node.street, node.osmid, how_far)
                # update street name based on OSM data
                entry.street = node.street
                # clear symul after name change
                entry.symul = ""
                self.set_state(node, 'visible') # make this *always* visible, to verify, if OSM value is correct. Hope that entry will eventually get merged with node
                # and fixme will get updated
            if node and node.street == entry.street and node.city == entry.city and node.housenumber != entry.housenumber and \
                ((node.objtype == 'node' and how_far < 5.0) or (node.objtype == 'way' and (node.contains(entry.center) or how_far < 10.0))):
                # there is only difference in housenumber, that is similiar
                if node.housenumber.upper() != entry.housenumber.upper():
                    self.__log.info("Updating housenumber from %s to %s", node.housenumber, entry.housenumber)
                if node.housenumber.upper() != entry.housenumber.upper():
                    # if there are some other differences than in case, then add fixme
                    entry.addFixme('House number in OSM: %s' % (node.housenumber,))
                self.set_state(node, 'visible') # make this *always* visible, to verify, if OSM value is correct. Hope that entry will eventually get merged with node
                node.housenumber = entry.housenumber
        except StopIteration: pass

    def _fix_obsolete_emuia(self, entry):
        existing = self.osmdb.getbyaddress(entry.get_index_key())
        if existing:
            # we have something with this address in db
            # sort by distance
            emuia_nodes = sorted(tuple(filter(lambda x: x.isEMUiAAddr() and x.only_address_node(), existing)), lambda x: x.distance(entry))

            # update location of first node if from EMUiA
            if emuia_nodes:
                emuia_nodes[0].location = entry.location

            # all the others mark for deletion
            if len(emuia_nodes)>1:
                for node in emuia_nodes[1:]:
                    self.set_state(node, 'delete')

    def _do_merge(self):
        self._parallel_process_func(self._do_merge_one, self.impdata)

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
        existing = tuple(filter(lambda x: self._import_area_shape.contains(x.center), self.osmdb.getbyaddress(entry.get_index_key())))
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

            if max(x[0] for x in existing) > 100:
                for (dist, node) in existing:
                    if dist > 100:
                        if not (node.objtype in ( 'way', 'relation') and node.contains(entry.center)):
                            # ignore the distance, if the point is within the node
                            self.__log.warning("Address (id=%s) %s is %d meters from imported point", node.osmid, entry, dist)
                            node.addFixme("Node is %d meters away from imported point"  % dist)
                    self.set_state(node, 'visible')
                if min(x[0] for x in existing) > 50:
                    if any(map(lambda x: x[1].objtype in ('way', 'relation') and x[1].contains(entry.center), existing)):
                        # if any of existing addreses is a way/relation within which we have our address
                        # then skip
                        pass
                    else:
                        self.__log.debug("Creating address node, as closest address is farther than 50m")
                        self._create_point(entry)
                        return True
            # update data only on first duplicate, rest - leave to OSM-ers
            self._update_node(existing[0][1], entry)
            return True
        return False

    def _do_merge_by_within(self, entry):
        # look for building nearby
        candidates = list(self.osmdb.nearest(entry.center, num_results=10))
        candidates_within = list(filter(lambda x: x.objtype in ('way', 'relation') and x.contains(entry.center), candidates))
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
                    if c.similar_to(entry):
                        self.__log.info("Different street names - import: %s, OSM: %s, address: %s, OSM: %s", entry.street, c.street, entry, c.osmid)
                    # address within a building that has different address, add a point, maybe building needs spliting
                    self.__log.debug("Adding new node within building with address: %s", entry)
                    self._create_point(entry)
                    return True
        return False

    def _do_merge_by_nearest(self, entry):
        candidates = list(self.osmdb.nearest(entry.center, num_results=10))
        candidates_same = list(filter(lambda x: x.housenumber == entry.housenumber and \
            x.distance(entry) < 2.0, candidates))
        if len(candidates_same) > 0:
            # same location, both are an address, and have same housenumber, can't be coincidence,
            # probably mapper changed something
            for node in candidates_same:
                found = False
                if node.similar_to(entry):
                    found = True
                    self.__log.debug("Updating near node from: %s to %s", node.entry, entry)
                    self._update_node(node, entry)
                    entry.addFixme("Node updated from nearest node")
                if found:
                    return True
            if any(map(lambda x: x.housenumber and x.city, candidates_same)):
                self.__log.info("Found probably same address node at (%s, %s). Skipping. Import address is: %s, osm addresses: %s",
                    entry.location['lon'], entry.location['lat'], entry, ", ".join(map(lambda x: str(x.entry), candidates_same))
                )
                return True
        return False

    def _do_merge_create_point(self, entry):
        if not self._import_area_shape.contains(entry.center):
            self.__log.warning("Imported address %s outside import borders", entry)
        self._create_point(entry)
        return True

    def _update_node(self, node, entry):
        self.__log.debug("Cheking if there is something to update for node %s, address: %s", node.osmid, node.entry)
        if node.updateFrom(entry):
            self.__log.debug("Updating node %s using %s", node.osmid, entry)
            self._updated_nodes.append(node)

    def _create_point(self, entry):
        self.__log.debug("Creating new point")
        soup =  {
            'type': 'node',
            'id': self._get_node_id(),
            'lat': entry.location['lat'],
            'lon': entry.location['lon'],
        }
        new = self.osmdb.add_new(soup)
        new.updateFrom(entry)
        self._new_nodes.append(new)
        # TODO: check that soup gets address tags
        #self.asis['elements'].append(soup)

    def _mark_soup_visible(self, obj):
        self._soup_visible.append(obj)

    def _get_node_id(self):
        self._node_id -= 1
        return self._node_id

    def _get_all_changed_nodes(self):
        ret = dict((x.osmid,x) for x in self._updated_nodes)
        ret.update(dict((x.osmid, x) for x in self._new_nodes))
        self.__log.info("Modified objects: %d", len(ret))
        ret.update(dict((x.osmid, x) for x in self._state_changes))

        for (_id, i) in ret.items():
            if i in self._updated_nodes:
                self.__log.debug("Processing updated node: %s", str(i.entry))
            elif i in self._new_nodes:
                self.__log.debug("Processing new node: %s", str(i.entry))
            elif i.state in ('modify', 'delete'):
                self.__log.debug("Processing node - changed: %s, %s", i.state, str(i.entry))

        return tuple(ret.values())

    def _get_all_visible(self):
        return tuple(self._soup_visible)

    def _get_all_reffered_by(self, lst):
        ret = set()
        def getbyid(key):
            ret = self.osmdb.getbyid(key)
            if not ret:
                raise ValueError("No object found for key: %s" % (key,))
            return ret
        def get_reffered(node):
            if node['type'] == 'node':
                return set((('node', node['id']),))
            if node['type'] == 'nd':
                return set((('node', node['ref']),))
            if node['type'] == 'way':
                return itertools.chain(
                    itertools.chain.from_iterable(map(get_reffered, (getbyid("node:%s" % (x,))[0] for x in node['nodes']))),
                    (('way', node['id']),)
                )
            if node['type'] == 'member':
                return get_reffered(getbyid("%s:%s" % (node['type'], node['ref']))[0])
            if node['type'] == 'relation':
                return itertools.chain(
                    itertools.chain.from_iterable(map(get_reffered, (getbyid("%s:%s" % (x['type'], x['ref']))[0] for x in node['members']))),
                    (('relation', node['id']),)
                )
            raise ValueError("Unkown node type: %s" % (node.name))

        for i in lst:
            ret = ret.union(get_reffered(i))

        return tuple(map(
            lambda x: getbyid("%s:%s" % (x[0], x[1]))[0],
            ret
        ))

    def _post_merge(self):
        # recreate index
        self._create_index()

        for i in self.post_func:
            i()
        self._create_index()
        self.mark_not_existing()
        self._create_index()

    def mark_not_existing(self):
        imp_addr = set(map(lambda x: x.get_index_key(), self.impdata))
        # from all addresses in OsmDb remove those imported
        to_delete = set(filter(
            lambda x: any(
                map(lambda y: self._import_area_shape.contains(y.center), self.osmdb.getbyaddress(x))
            ),
            self.osmdb.getalladdress())) - imp_addr

        self.__log.debug("Marking %d not existing addresses", len(to_delete))
        for addr in filter(any, to_delete): # at least on addr field is filled in
            for node in filter(lambda x: self._import_area_shape.contains(x.center), self.osmdb.getbyaddress(addr)):
                if self._import_area_shape.contains(node.center) and not ((
                        'e-mapa.net' in self.source_addr and node.source != self.source_addr and 'e-mapa.net' in node.source) or (
                        self.source_addr == 'emuia.gugik.gov.pl' and 'e-mapa.net' in node.source)):
                    # if we are importing from iMPA, and the point is from other iMPA import, then skip it
                    # if we are importing from GUGiK, skip points from iMPA
                    # report only points within area of interest
                    self.__log.debug("Marking node to delete - address %s does not exist: %s, %s", addr, node.osmid, str(node.entry))
                    node.addFixme('Check address existance')
                    self.set_state(node, 'visible')

    def merge_addresses(self):
        self._merge_addresses_buffer(0)
        self._merge_addresses_buffer(2)
        self._merge_addresses_buffer(5)

    def _merge_one_address(self, building, addr):
        # as we merge only address nodes, do not pass anything else
        fixme = building['tags'].get('fixme', '')
        for (key, value) in addr.get_tag_soup():
            oldval = building['tags'][key]
            if oldval and oldval != value:
                self.__log.info('Changing tag: %s from %s to %s for address: %s', key, oldval, value, addr)
            building['tags'][key] = value
        fixme += addr.getFixme()
        building['tags']['fixme'] = fixme
        self.osmdb.getbyid("%s:%s" % (building['type'], building['id']))[0].set_state('modify')
        self.set_state(addr, 'delete')
        self._updated_nodes.append(self.osmdb.getbyid("%s:%s" % (building['type'], building['id']))[0])

    def _merge_addresses_buffer(self, buf=0):
        self.__log.info("Merging building with buffer: %d", buf)
        to_merge = self._prepare_merge_list(buf)
        buildings = dict(
            ("%s:%s" % (x['type'], x['id']), x) for x in self.asis['elements'] if x['type'] in ('way', 'relation')
        )

        self.__log.info("Merging %d addresses with buildings", len(tuple(filter(lambda x: len(x[1]) == 1, to_merge.items()))))

        for (_id, nodes) in to_merge.items():
            building = buildings[_id]
            if len(nodes) > 0:
                self._mark_soup_visible(self.osmdb.getbyid(_id)[0])

            # if there is only one candidate, or all candidates are similiar addresses
            if len(nodes) == 1 or all(map(
                lambda x: x[0].similar_to(x[1]),
                itertools.combinations(nodes, 2)
                )):
                if building['tags'].get('addr:housenumber') and not nodes[0].similar_to(self.osmdb.getbyid("%s:%s" % (building['type'], building['id']))[0]):
                    # if building has different address, than we want to put
                    self.__log.info("Skipping merging address: %s, as building already has an address: %s.", str(nodes[0].entry), OsmAddress.from_soup(building))
                    for node in nodes:
                        self._mark_soup_visible(node)
                else:
                    # if building has similar address, just merge
                    self.__log.debug("Merging address %s with building %s", str(nodes[0].entry), _id)
                    for node in nodes:
                        self._merge_one_address(building, node)

            if len(nodes) > 1:
                for node in nodes:
                    self._mark_soup_visible(node)

    def _prepare_merge_list(self, buf):
        ret = {}
        for node in filter(lambda x: x['type'] == 'node' and x.get('tags', {}).get('addr:housenumber'), self.asis['elements']):
            addr = self.osmdb.getbyid("%s:%s" % (node['type'], node['id']))[0]
            self.__log.debug("Looking for candidates for: %s", str(addr.entry))
            if addr.only_address_node() and addr.state != 'delete' and (not self._import_area_shape or self._import_area_shape.contains(addr.center)):
                candidates = list(self.osmdb.nearest(addr.center, num_results=100)) # need to take into account a large number of candidates, as nodes <-> members of ways are also returned
                candidates_within = list(
                    filter(
                        lambda x: addr.osmid != x.osmid and x.objtype == 'relation' and addr.center.within(buffer(x.shape, buf)),
                        candidates
                    )
                )
                if not candidates_within:
                    candidates_within = list(
                        filter(
                            lambda x: addr.osmid != x.osmid and x.objtype == 'way' and addr.center.within(buffer(x.shape, buf)),
                            candidates
                        )
                   )

                if candidates_within:
                    c = candidates_within[0]
                    if c.housenumber and not addr.similar_to(c):
                        self.set_state(c, 'visible')
                        self.set_state(addr, 'visible')
                    else:
                        try:
                            lst = ret[c.osmid]
                        except KeyError:
                            lst = []
                            ret[c.osmid] = lst
                        lst.append(addr)
                        self.__log.debug("Found: %s", c.osmid)
        return ret

    def _get_osm_xml(self, nodes, logIO=None):
        return E.osm(
                        E.note('The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.' + ('\n' + logIO.getvalue() if logIO else '')),
                        E.meta(osm_base=self.asis['osm3s']['timestamp_osm_base']),
                        *tuple(map(OsmAddress.to_osm_soup, nodes)),
                    version='0.6', generator='import adresy merger.py'
        )

    def get_incremental_result(self, logIO=None):
        changes = self._get_all_changed_nodes()
        self.__log.info("Generated %d changes", len(changes))
        nodes = self._get_all_reffered_by(changes + self._get_all_visible())
        return lxml.etree.tostring(self._get_osm_xml(nodes, logIO), pretty_print=True, xml_declaration=True, encoding='UTF-8')

    def get_full_result(self, logIO=None):
        return lxml.etree.tostring(self._get_osm_xml(self._get_all_changed_nodes(), logIO), pretty_print=True, xml_declaration=True, encoding='UTF-8')


def getAddresses(bbox):
    bbox = ",".join(bbox)
    query = """
[out:json]
[timeout:600]
;
(
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
);
out meta bb qt;
>>;
out meta bb qt;
""" % (bbox, bbox, bbox, bbox, bbox,)
    return json.loads(overpass.query(query))

def get_boundary_shape(terc):
    query = """
[out:json]
[timeout:600];
relation
    ["teryt:terc"~"^%s"];
out meta bb qt;
>;
out meta bb qt;
""" % (terc,)
    soup = json.loads(overpass.query(query))
    osmdb = OsmDb(soup)
    boundaries = tuple(x for x in soup['elements'] if x['type'] == 'relation' and x['tags'].get('teryt:terc', '') == terc)
    if len(boundaries) > 1:
        __log.error("More than one relation found with terc: %s. Names: %s. Fix before continuing", terc, ", ".join(map(lambda x: x['tags'].get('name'), boundaries)))
        sys.exit(1)
    if len(boundaries) == 1:
        rel = boundaries[0]
    else:
        rel = tuple(x for x in soup['elements'] if x['type'] == 'relation' and x['tags'].get('teryt:terc', '').startswith(terc))[0]
    __log.info("Loading shape of import area - relation id: %s, relation name: %s" , rel['id'], rel['tags'].get('name'))
    return osmdb.get_shape(rel)


def buffer(shp, meters=0):
    # 0.0000089831528 is the 1m length in arc degrees of great circle
    return shp.buffer(meters*0.0000089831528)

def main():
    # TODO: create mode where no unchanged data are returned (as addresses to be merged with buildings)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""Merge data from WMS with OSM data. Generate output OSM file for JOSM. You need to provide one of:
    1. --impa with service name
    2. --import-file and --addresses-file
    3. --import-file and --terc """)
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('--impa', help='name of iMPA service, use "milawa" when the address is milawa.e-mapa.net')
    source_group.add_argument('--import-file', type=argparse.FileType("r", encoding='UTF-8'), help='JSON file generated by punktyadresowe_import.py for the area', dest='import_file')
    source_group.add_argument('--gugik', action='store_const', const=True, dest='gugik', default=False, help='Import address data from gugik. Select area by providing terc option')
    source_group.add_argument('--gugik_gml', help='Import address data from gugik. Provide filename as argument.')
    source_group.add_argument('--gisnet', help='Import address data from GIS-NET. Use "nowosolna" when the address is nowosolna.gis-net.pl. You need to provide also terc option')
    source_group.add_argument('--warszawa', action='store_const', const=True, dest='warszawa', default=False, help='Import address data from UM Warszawa. You need to provide terc option')
    address_group = parser.add_argument_group()
    address_group.add_argument('--addresses-file', type=argparse.FileType("r", encoding='UTF-8'), help='OSM file with addresses and buildings for imported area', dest='addresses_file')
    address_group.add_argument('--terc', help='teryt:terc code, for which to download addresses from OSM using Overpass API')
    parser.add_argument('--output', type=argparse.FileType('w+b'), help='output file with merged data (default: result.osm)', default='result.osm')
    parser.add_argument('--full', help='Use to output all address data for region, not only modified address data as per default', action='store_const', const=True, dest='full_mode', default=False)
    parser.add_argument('--no-merge', help='Do not merger addresses with buildings', action='store_const', const=True, dest='no_merge', default=False)
    parser.add_argument('--log-level', help='Set logging level (debug=10, info=20, warning=30, error=40, critical=50), default: 20', dest='log_level', default=20, type=int)
    parser.add_argument('--import-wms', help='WMS address for address layer, ex: ' +
        'http://www.punktyadresowe.pl/cgi-bin/mapserv?map=/home/www/impa2/wms/luban.map . Bounding box is still fetched via iMPA', dest='wms')

    args = parser.parse_args()

    log_stderr = logging.StreamHandler()
    log_stderr.setLevel(args.log_level)

    logIO = io.StringIO()

    logging.basicConfig(level=10, handlers=[log_stderr, logging.StreamHandler(logIO)])

    dataFunc = None
    if args.impa:
        imp = iMPA(args.impa, wms=args.wms)
        terc = imp.terc
        dataFunc = lambda: imp.getAddresses()
        source_addr = args.impa + '.e-mapa.net'
    elif args.gisnet:
        imp = GISNET(args.gisnet, args.terc)
        terc = args.terc
        dataFunc = lambda: imp.getAddresses()
        source_addr = args.gisnet + '.gis-net.pl'
    elif args.warszawa:
        imp = WarszawaUM('Warszawa', args.terc)
        terc = args.terc
        dataFunc = lambda: imp.getAddresses()
        source_addr = 'mapa.um.warszawa.pl'
    elif args.gugik_gml:
        imp = GUGiK_GML(args.gugik_gml)
        terc = imp.terc
        dataFunc = lambda: imp.getAddresses()
        source_addr = 'emuia.gugik.gov.pl'
    else:
        imp = GUGiK(args.terc)
        dataFunc = lambda: imp.getAddresses()
        source_addr = 'emuia.gugik.gov.pl'

    if args.import_file:
        dataFunc = lambda: list(map(lambda x: Address.from_JSON(x), json.load(args.import_file)))

    data = dataFunc()

    if args.terc:
        terc = args.terc

    __log.info("Working with TERC: %s", terc)
    if args.addresses_file:
        addrFunc = lambda: converter.osm_to_json(lxml.etree.parse(args.addresses_file))
    else:
        # union with bounds of administrative boundary
        s = min(map(lambda x: x.center.y, data))
        w = min(map(lambda x: x.center.x, data))
        n = max(map(lambda x: x.center.y, data))
        e = max(map(lambda x: x.center.x, data))
        addrFunc = lambda: getAddresses(map(str,(s, w, n, e)))

    addr = addrFunc()

    if len(data) < 1:
        __log.warning("Warning - import data is empty. Check your import")
    __log.info('Processing %d addresses', len(data))

    if len(addr['elements']) == 0:
        __log.warning("Warning - address data is empty. Check your file/terc code")

    #m = Merger(data, addr, terc, parallel_process_func=parallel_map)
    m = Merger(data, addr, terc, source_addr)
    if not args.no_merge:
        m.post_func.append(m.merge_addresses)
    m.merge()

    if args.full_mode:
        ret = m.get_full_result(logIO)
    else:
        ret = m.get_incremental_result(logIO)

    args.output.write(ret)

if __name__ == '__main__':
    main()
