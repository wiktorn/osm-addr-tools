import unittest
import converter
import os

import data.base
import merger
import lxml.etree
import pathlib


def osm_xml_to_addresses(filename):
    return osm_xml_etree_to_addresses(lxml.etree.parse(filename))


def osm_xml_etree_to_addresses(e):
    return list(
        map(
            data.base.Address.from_osm_xml,
            e.getroot().iterchildren()
        )
    )


def get_merger(directory: os.PathLike, merge_addresses_with_outlines=True, terc:str = None):
    imported = osm_xml_to_addresses(os.path.join(directory, 'imp.xml'))
    osm = converter.osm_to_json(lxml.etree.parse(os.path.join(directory, 'osm.xml')))
    m = merger.Merger(imported, osm, terc if terc else "", "test")
    if merge_addresses_with_outlines:
        m.post_func.append(m.merge_addresses)
    m.merge()
    return m


def sorted_addresses(l):
    def sort_key(o):
        return '\127'.join(
            map(lambda x: o.get(x, ''),
                ['addr:city', 'addr:place', 'addr:street', 'addr:housenumber', 'id']
                )
        )

    return sorted(l, key=sort_key)


def verify(self, expected, actual: bytes):
    # with open("latest_actual.osm", "wb+") as f:
    #    f.write(actual)
    with open(expected, "r", encoding='utf-8') as f:
        self.assertEqual(f.read(), actual.decode('utf-8'))


def make_incremental_test(directory: pathlib.PurePath, terc: str = None):
    def f(self):
        ret = get_merger(directory, terc=terc).get_incremental_result()
        verify(self, os.path.join(directory, 'result_incremental.xml'), ret)

    f.__name__ = directory.name + '_incremental'
    return f


def make_full_test(directory: pathlib.PurePath, terc: str=None):
    def f(self):
        ret = get_merger(directory, terc=terc).get_full_result()
        verify(self, os.path.join(directory, 'result_full.xml'), ret)

    f.__name__ = directory.name + '_full'
    return f


class MergerTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_sorted_addresses(self):
        test = [
            {
                'addr:city': 'Abe',
                'addr:street': 'Bbe',
                'addr:housenumber': '4'

            },
            {
                'addr:city': 'Aae',
                'addr:street': 'Bbe',
                'addr:housenumber': '4'

            },
            {
                'addr:city': 'Abe',
                'addr:street': 'Bae',
                'addr:housenumber': '4'

            },
            {
                'addr:city': 'Abe',
                'addr:street': 'Bbe',
                'addr:housenumber': '3'

            },
            {
                'addr:city': 'Abe',
                'addr:street': 'Bbe',
                'addr:housenumber': '5'

            }
        ]
        expected = [
            {
                'addr:city': 'Aae',
                'addr:street': 'Bbe',
                'addr:housenumber': '4'

            },
            {
                'addr:city': 'Abe',
                'addr:street': 'Bae',
                'addr:housenumber': '4'

            },
            {
                'addr:city': 'Abe',
                'addr:street': 'Bbe',
                'addr:housenumber': '3'

            },
            {
                'addr:city': 'Abe',
                'addr:street': 'Bbe',
                'addr:housenumber': '4'

            },
            {
                'addr:city': 'Abe',
                'addr:street': 'Bbe',
                'addr:housenumber': '5'

            }
        ]
        self.assertEqual(sorted_addresses(test), expected)

    def test_explicit(self):
        test_name = "different_street_within"
        # terc = "1465188"
        terc = None
        make_incremental_test(pathlib.Path(__file__).parent.parent / "testdata" / test_name, terc)(self)
        # make_full_test(pathlib.Path(__file__).parent.parent / "testdata" / test_name, terc)(self)


def __set_tests():

    directory = pathlib.Path(__file__).parent.parent / "testdata"
    for test in directory.iterdir():  # type: pathlib.Path
        if test.is_dir():
            terc = None
            if (test / "terc").exists():
                with (test / "terc").open("r") as f:
                    terc = "".join(f.readlines()).strip()
            setattr(MergerTests, 'test_' + test.name + '_incremental', make_incremental_test(test, terc))
            setattr(MergerTests, 'test_' + test.name + '_full', make_full_test(test, terc))


__set_tests()

if __name__ == '__main__':
    unittest.main()
