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



def my_dict_equals(self, first, second, msg=None):
    if first.keys() != second.keys():
        extra_first = first.keys() - second.keys()
        extra_second = second.keys() - first.keys()
        raise self.failureException("Dicts have different keys, extra keys in first: {0}, missing keys in first: {1}".format(extra_first, extra_second))
    
    for key in first.keys():
        first_value = first[key]
        second_value = second[key]
        if type(first_value) != type(second_value):
            raise self.failureException("Values at key {0} have different types: {1} != {2}".format(key, type(first_value), type(second_value)))

        if isinstance(first_value, dict):
            my_dict_equals(self, first_value, second_value, msg)
        elif isinstance(first_value, list):
            my_list_equals(self, first_value, second_value, msg)
        else:
            self.assertEqual(first_value, second_value, msg)


def sorted_addresses(l):
    def sort_key(o):
        return '\127'.join(
            map(lambda x: o.get(x, ''),
                ['addr:city', 'addr:place', 'addr:street', 'addr:housenumber', 'id']
            )
        )
    return sorted(l, key=sort_key) 

def verify(self, expected, actual):
    first = sorted_addresses(converter.osm_to_json(lxml.etree.parse(expected))['elements'])
    second = sorted_addresses(converter.osm_to_json(lxml.etree.ElementTree(lxml.etree.fromstring(actual)))['elements'])
    with open("latest_actual.osm", "wb+") as f:
        f.write(actual)
    self.assertCountEqual(first, second)
    self.assertEqual(
        json.dumps(first, sort_keys=True),
        json.dumps(second, sort_keys=True)
    )

    
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
