import unittest

from utils.mapping import mapstreet

import logging

#logging.basicConfig(level=logging.DEBUG)


class TestStreetMapping(unittest.TestCase):
    def test_plac_sloneczny(self):
        self.assertEqual("Plac Słoneczny", mapstreet("Słoneczny", "40187"))

    def test_poniatowskiego(self):
        self.assertEqual("Księcia Józefa Poniatowskiego", mapstreet("Poniatowskiego", "17113"))

    def test_waszyngtona(self):
        self.assertEqual("Aleja Jerzego Waszyngtona", mapstreet("Aleja J. Waszyngtona", "45576"))

    def test_waszyngtona_no_simc(self):
        self.assertEqual("Aleja J. Waszyngtona", mapstreet("Aleja J. Waszyngtona", "xxx"))

    def test_jerozolimskie(self):
        self.assertEqual("Aleje Jerozolimskie", mapstreet("Al. Jerozolimskie", "45207"))
