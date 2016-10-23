import lxml.etree
import json

def convert_element(elem):
    ret = {
        'type': elem.tag,
        'tags': {},
        'nodes': [],
        'members': []
    }
    ret.update(elem.attrib)
    for n in elem:
        #child tags
        if n.tag == 'tag':
            ret['tags'][n.get('k')] = n.get('v')
        if n.tag == 'nd':
            ret['nodes'].append(n.get('ref'))
        if n.tag == 'member':
            ret['members'].append(n.attrib.copy())
    for i in ('tags', 'nodes', 'members'):
        if len(ret[i]) == 0:
            del ret[i]
    return ret


def osm_to_json(root):
    osm = root.getroot()
    assert osm.tag == 'osm'
    return {
        'version': osm.get('version'),
        'generator': osm.get('generator'),
        'elements': [convert_element(x) for x in osm if x.tag in ['node', 'way', 'relation']]
    }


        

def main():
    root = lxml.etree.parse(open('1205092.osm'))
    print(json.dumps(osm_to_json(root)))


if __name__ == '__main__':
    main()
