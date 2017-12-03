import unittest
import lxml.etree

import converter


class ConverterTests(unittest.TestCase):
    def helper(self, xml, json):
        ret = converter.osm_to_json(lxml.etree.fromstring(xml).getroottree())
        self.assertEqual(json, ret)

    def test_node(self):
        self.helper(
            """
            <osm version='0.6' generator='JOSM'>
              <node id='-47432' action='modify' lat='50.5221428704' lon='17.21647412211'>
                <tag k='addr:city:simc' v='0500949' />
                <tag k='addr:housenumber' v='19' />
                <tag k='addr:place' v='Rysiowice' />
                <tag k='source:addr' v='Tests' />
              </node>
            </osm>
            """,
            {
                'version': '0.6',
                'generator': 'JOSM',
                'elements': [
                    {
                        'type': 'node',
                        'id': '-47432',
                        'action': 'modify',
                        'lat': '50.5221428704',
                        'lon': '17.21647412211',
                        'tags': {
                            'addr:city:simc': '0500949',
                            'addr:housenumber': '19',
                            'addr:place': 'Rysiowice',
                            'source:addr': 'Tests'
                        },
                     }
                ]
            }
        )

    def test_relation(self):
        self.helper(
            """
            <osm version='0.6' generator='JOSM'>
            
            <relation id="3776337" version="3" timestamp="2017-12-03T09:17:50Z" changeset="54292108" uid="1879367" user="Zibi-importy">
                <member type="way" ref="284675180" role="outer"/>
                <member type="way" ref="284675179" role="inner"/>
                <tag k="addr:city:simc" v="0500949"/>
                <tag k="addr:housenumber" v="19"/>
                <tag k="addr:place" v="Rysiowice"/>
                <tag k="building" v="yes"/>
                <tag k="source:addr" v="otmuchow.e-mapa.net"/>
                <tag k="type" v="multipolygon"/>
              </relation>
            </osm>
            """,
            {
                'version': '0.6',
                'generator': 'JOSM',
                'elements': [
                    {
                        "type": "relation",
                        "id": "3776337",
                        "timestamp": "2017-12-03T09:17:50Z",
                        "version": "3",
                        "changeset": "54292108",
                        "user": "Zibi-importy",
                        "uid": "1879367",
                        "members": [
                            {
                                "type": "way",
                                "ref": "284675180",
                                "role": "outer"
                            },
                            {
                                "type": "way",
                                "ref": "284675179",
                                "role": "inner"
                            }
                        ],
                        "tags": {
                            "addr:city:simc": "0500949",
                            "addr:housenumber": "19",
                            "addr:place": "Rysiowice",
                            "building": "yes",
                            "source:addr": "otmuchow.e-mapa.net",
                            "type": "multipolygon"
                        }
                    }
                ]
            }
        )

    def test_way(self):
        self.helper(
            """
            <osm version='0.6' generator='JOSM'>
            
            <way id="284675179" version="1" timestamp="2014-05-27T18:40:57Z" changeset="22587047" uid="1246157" user="Jedrzej Pelka">
                <nd ref="2883967600"/>
                <nd ref="2883967613"/>
                <nd ref="2883967616"/>
                <nd ref="2883967603"/>
                <nd ref="2883967600"/>
                <tag k="source:geometry" v="geoportal.gov.pl:ortofoto"/>
            </way>
            </osm>
            """,
            {'version': '0.6',
             'generator': 'JOSM',
             'elements':
                 [
                     {
                         'type': 'way',
                         'tags': {
                             'source:geometry': 'geoportal.gov.pl:ortofoto'
                         },
                         'nodes': [
                             '2883967600',
                             '2883967613',
                             '2883967616',
                             '2883967603',
                             '2883967600'
                         ],
                         'id': '284675179',
                         'version': '1',
                         'timestamp': '2014-05-27T18:40:57Z',
                         'changeset': '22587047',
                         'uid': '1246157',
                         'user': 'Jedrzej Pelka'
                     }
                 ]
             }
        )