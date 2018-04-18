import json
import unittest

import merger
import osmdb
import overpass


class OsmDbTests(unittest.TestCase):
    def test_1(self):
        ret = json.loads(overpass.query(merger.get_referenced_objects("node(2109698537);")))
        db = osmdb.OsmDb(ret)
        self.assertTrue(any(
            x for x in db.get_all_values() if
            x.entry['type'] == 'node' and
            x.entry['id'] == 2109698537
        ))

    def test_2(self):
        ret = json.loads(overpass.query(merger.get_referenced_objects("node(319997075);")))
        db = osmdb.OsmDb(ret)
        self.assertTrue(any(
            x for x in db.get_all_values() if
            x.entry['type'] == 'node' and
            x.entry['id'] == 319997075
        ))

    def test_3(self):
        ret = json.loads(overpass.query(merger.get_referenced_objects("relation(5128693);")))
        db = osmdb.OsmDb(ret)
        self.assertTrue(any(
            x for x in db.get_all_values() if
            x.entry['type'] == 'relation' and
            x.entry['id'] == 5128693
        ))

    def test_4(self):
        ret = json.loads(overpass.query(merger.get_referenced_objects("way(292154964);")))
        db = osmdb.OsmDb(ret)
        self.assertTrue(any(
            x for x in db.get_all_values() if
            x.entry['type'] == 'way' and
            x.entry['id'] == 292154964
        ))
