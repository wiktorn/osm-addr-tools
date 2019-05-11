import json
import unittest

import merger
import osmdb
import overpass
from utils import osmshapedb


class OsmDbTests(unittest.TestCase):
    def trivial_check(self, typ, id_):
        ret = osmshapedb.get_geometries(
            overpass.query(merger.get_referenced_objects("{}({});".format(typ, id_)))
        )
        db = osmdb.OsmDb(
            ret,
            index_filter=lambda x: x.get("tags", {}).get("building", False)
            or x.get("tags", {}).get("addr:housenumber", False),
        )
        self.assertTrue(
            any(
                x
                for x in db.get_all_values()
                if x.entry["type"] == typ and x.entry["id"] == id_
            )
        )

    def test_1(self):
        self.trivial_check("node", 2109698537)

    @unittest.skip("Node deleted")
    def test_2(self):
        self.trivial_check("node", 319997075)  # deleted

    def test_3(self):
        self.trivial_check("relation", 5128693)

    def test_4(self):
        self.trivial_check("way", 292154964)

    def test_5(self):
        self.trivial_check("way", 196605788)

    @unittest.skip("Not a building, nor a housenumber")
    def test_complicated_relation(self):
        self.trivial_check("relation", 2567398)  # not a building, nor a housenumber

    @unittest.skip("Not a building, nor a housenumber")
    def test_associated_street(self):
        self.trivial_check("relation", 3472746)  # not a building, nor housenumber

    @unittest.skip("Not a building, nor a housenumber")
    def test_building_part(self):
        self.trivial_check("relation", 4609851)  # not a building, nor a housenumber

    @unittest.skip("Not a building, nor a housenumber")
    def test_building_part2(self):
        self.trivial_check("relation", 4096062)  # not a building, nor a housenumber
