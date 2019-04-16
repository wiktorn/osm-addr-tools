import unittest

from utils.mapping import mapstreet

import logging


class TestStreetMapping(unittest.TestCase):
    def test_plac_sloneczny(self):
        self.assertEqual("Plac Słoneczny", mapstreet("Słoneczny", "40187"))

    def test_poniatowskiego(self):
        self.assertEqual("Księcia Józefa Poniatowskiego", mapstreet("Poniatowskiego", "17113"))

    def test_waszyngtona(self):
        self.assertEqual("Aleja Jerzego Waszyngtona", mapstreet("Aleja J. Waszyngtona", "45576"))

    def test_jerozolimskie(self):
        self.assertEqual("Aleje Jerozolimskie", mapstreet("Al. Jerozolimskie", "45207"))

    def test_jerozolimskie2(self):
        self.assertEqual("Aleje Jerozolimskie", mapstreet("Aleja Jerozolimskie", "45207"))

    def test_jerozolimskie3(self):
        self.assertEqual("Aleje Jerozolimskie", mapstreet("Jerozolimskie", "45207"))

    def test_jerozolimskie(self):
        self.assertEqual("Aleje Jerozolimskie", mapstreet("Al. Jerozolimskie", ""))

    def test_sloneczny_sto_case(self):
        self.assertEqual("Słoneczny Stok", mapstreet("SŁONECZNY STOK", "20264"))


