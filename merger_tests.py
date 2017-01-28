import unittest
import converter
import os
import merger
import lxml.etree
import json

def osm_xml_to_addresses(filename):
    return osm_xml_etree_to_addresses(lxml.etree.parse(filename))

def osm_xml_etree_to_addresses(e):
    return list(
        map(
            merger.Address.from_osmXML,
            e.getroot().iterchildren()
        )
    )

def get_merger(directory):
    imported = osm_xml_to_addresses(os.path.join(directory, 'imp.xml'))
    osm = converter.osm_to_json(lxml.etree.parse(os.path.join(directory, 'osm.xml')))
    m = merger.Merger(imported, osm, "", "test")
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

def verify(self, expected, actual):
    with open("latest_actual.osm", "wb+") as f:
        f.write(actual)
    expected = sorted_addresses(converter.osm_to_json(lxml.etree.parse(expected))['elements'])
    actual = sorted_addresses(converter.osm_to_json(lxml.etree.ElementTree(lxml.etree.fromstring(actual)))['elements'])
    self.assertEqual(len(expected), len(actual))
    self.assertEqual(
        json.dumps(expected, sort_keys=True),
        json.dumps(actual, sort_keys=True)
    )
    self.assertCountEqual(expected, actual)

    
def make_incremental_test(name, directory):
    def f(self):
        ret = get_merger(directory).get_incremental_result()
        verify(self, os.path.join(directory, 'result_incremental.xml'), ret)
    f.__name__ = name + '_incremental'
    return f

def make_full_test(name, directory):
    def f(self):
        ret = get_merger(directory).get_full_result()
        verify(self, os.path.join(directory, 'result_full.xml'), ret)
    f.__name__ = name + '_full'
    return f



class MergerTests(unittest.TestCase):
    def setUp(self):
        pass
        #self.maxDiff = None

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


for test in os.listdir('tests'):
    setattr(MergerTests, 'test_' + test + '_incremental', make_incremental_test(test, os.path.join('tests', test)))
    setattr(MergerTests, 'test_' + test + '_full', make_full_test(test, os.path.join('tests', test)))

if __name__ == '__main__':
    unittest.main()
