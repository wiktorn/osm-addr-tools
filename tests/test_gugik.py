import unittest
from data.gugik import GUGiK
import json


class GugikTests(unittest.TestCase):
    def test_convert_to_address(self):
        g = GUGiK(terc="1409033")
        sample_addr = json.loads("""
        {
        "cyklZyciaOd": "2016-11-26",
        "pktPrgIIPPn": "PL.PZGIK.200",
        "pktPrgIIPId": "0136b1ba-8573-47ea-8350-9d2b6b0f1110",
        "pktPrgIIPWersja": "2016-11-26T13:30:54+02:00",
        "pktEmuiaIIPPn": "PL.ZIPIN.1549.EMUiA",
        "pktEmuiaIIPId": "30000000000028145728",
        "pktEmuiaIIPWersja": "2",
        "pktNumer": "2",
        "pktStatus": "istniejacy",
        "pktKodPocztowy": "27-300",
        "pktX": 369167.595000001,
        "pktY": 684855.4629,
        "ulIIPPn": "PL.PZGIK.200",
        "ulIIPId": "28dc7a49-6cd7-4caf-8dbe-660885ea72fa",
        "ulIIPWersja": "2016-11-26T13:30:49+02:00",
        "ulNazwaGlowna": "Widok",
        "ulTyp": "ulica",
        "ulIdTeryt": "24011",
        "miejscIIPPn": "PL.PZGIK.200",
        "miejscIIPId": "449b3481-24c4-497b-9103-9a2767539389",
        "miejscIIPWersja": "2016-11-26T13:30:47+02:00",
        "miejscNazwa": "Lipsko",
        "miejscRodzaj": "Miasto",
        "miejscIdTeryt": "0973613",
        "gmNazwa": "Lipsko",
        "gmIdTeryt": "1409033",
        "gmIIPPn": "PL.PZGIK.200",
        "gmIIPId": "427e408a-4f53-4476-a585-ea7ee07625c9",
        "gmIIPWersja": "2012-09-26T21:58:25+02:00",
        "powNazwa": "lipski",
        "powIdTeryt": "1409",
        "powIIPPn": "PL.PZGIK.200",
        "powIIPId": "ba9c16c6-9bb2-4493-ac50-c73cd65030ab",
        "powIIPWersja": "2012-09-27T08:13:53+02:00",
        "wojNazwa": "mazowieckie",
        "wojIdTeryt": "14",
        "wojIIPPn": "PL.PZGIK.200",
        "wojIIPId": "4b6c492a-eb04-441d-a92a-f44359c06de7",
        "wojIIPWersja": "2012-09-27T13:45:13+02:00"
      }
        """)
        addr = g._convert_to_address(sample_addr)
        pos = addr.center
        self.assertAlmostEqual(21.64446755, pos.x, 7)
        self.assertAlmostEqual(51.15934363, pos.y)
        self.assertEqual("Lipsko", addr.city)
        self.assertEqual("Widok", addr.street)
        self.assertEqual("27-300", addr.postcode)
        self.assertEqual("2", addr.housenumber)
        self.assertEqual("24011", addr.sym_ul)
        self.assertEqual("0973613", addr.simc)

    def test_convert_no_street(self):
        g = GUGiK(terc="1409033")
        sample_addr = json.loads("""
        {
        "cyklZyciaOd": "2016-11-26",
        "pktPrgIIPPn": "PL.PZGIK.200",
        "pktPrgIIPId": "639a1363-a8f7-4260-992f-9c61e8f65e32",
        "pktPrgIIPWersja": "2016-11-26T13:31:53+02:00",
        "pktEmuiaIIPPn": "PL.ZIPIN.1549.EMUiA",
        "pktEmuiaIIPId": "30000000000031356054",
        "pktEmuiaIIPWersja": "2",
        "pktNumer": "1",
        "pktStatus": "istniejacy",
        "pktKodPocztowy": "27-300",
        "pktX": 366020.5899,
        "pktY": 683390.1556,
        "miejscIIPPn": "PL.PZGIK.200",
        "miejscIIPId": "bc09f8c9-6595-4b53-aa1d-d99c88102284",
        "miejscIIPWersja": "2016-11-26T13:30:46+02:00",
        "miejscNazwa": "Gruszczyn",
        "miejscRodzaj": "Wieś",
        "miejscIdTeryt": "0628046",
        "gmNazwa": "Lipsko",
        "gmIdTeryt": "1409033",
        "gmIIPPn": "PL.PZGIK.200",
        "gmIIPId": "427e408a-4f53-4476-a585-ea7ee07625c9",
        "gmIIPWersja": "2012-09-26T21:58:25+02:00",
        "powNazwa": "lipski",
        "powIdTeryt": "1409",
        "powIIPPn": "PL.PZGIK.200",
        "powIIPId": "ba9c16c6-9bb2-4493-ac50-c73cd65030ab",
        "powIIPWersja": "2012-09-27T08:13:53+02:00",
        "wojNazwa": "mazowieckie",
        "wojIdTeryt": "14",
        "wojIIPPn": "PL.PZGIK.200",
        "wojIIPId": "4b6c492a-eb04-441d-a92a-f44359c06de7",
        "wojIIPWersja": "2012-09-27T13:45:13+02:00"
      }""")
        g._convert_to_address(sample_addr)
        addr = g._convert_to_address(sample_addr)
        pos = addr.center
        self.assertAlmostEqual(21.621925429, pos.x, 7)
        self.assertAlmostEqual(51.13153787, pos.y, 7)
        self.assertEqual("1", addr.housenumber)
        self.assertEqual("27-300", addr.postcode)
        self.assertEqual("Gruszczyn", addr.city)
        self.assertEqual("", addr.street)
        self.assertEqual("0628046", addr.simc)
        self.assertEqual("", addr.sym_ul)
