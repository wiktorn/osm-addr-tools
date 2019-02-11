import unittest
import data.base


class BaseTests(unittest.TestCase):
    def test_e2180_to_wgs(self):
        lat, lon = data.base.LatType(52.1800994), data.base.LonType(21.069666)
        x, y = data.base.XType(641462.7269700456), data.base.YType(481353.3555923067)

        ret_lon, ret_lat = data.base.e2180_to_wgs(x, y)
        self.assertAlmostEqual(ret_lon, lon)
        self.assertAlmostEqual(ret_lat, lat)


    def test_wgs_to_2180(self):
        lat, lon = data.base.LatType(52.1800994), data.base.LonType(21.069666)
        x, y = data.base.XType(641462.7269700456), data.base.YType(481353.3555923067)

        ret_x, ret_y = data.base.wgs_to_2180(lon, lat)
        self.assertAlmostEqual(ret_x, x)
        self.assertAlmostEqual(ret_y, ret_y)

    def test_symmetry_e2180_to_wgs(self):
        lat, lon = data.base.LatType(52.1800994), data.base.LonType(21.069666)
        x, y = data.base.XType(641462.7269700456), data.base.YType(481353.3555923067)

        ret_lon, ret_lat = data.base.e2180_to_wgs(x, y)
        ret_x, ret_y = data.base.wgs_to_2180(ret_lon, ret_lat)
        self.assertAlmostEqual(ret_x, x, places=4)
        self.assertAlmostEqual(ret_y, y, places=4)

    def test_symmetry_wgs_to_2180(self):
        lat, lon = data.base.LatType(52.1800994), data.base.LonType(21.069666)
        x, y = data.base.XType(641462.7269700456), data.base.YType(481353.3555923067)

        ret_x, ret_y = data.base.wgs_to_2180(lon, lat)
        ret_lon, ret_lat = data.base.e2180_to_wgs(ret_x, ret_y)
        self.assertAlmostEqual(ret_lon, lon)
        self.assertAlmostEqual(ret_lat, lat)
