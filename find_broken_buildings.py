import overpass
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import argparse

def get_data_From_area(terc, user, date):
    query = """
[out:json]
[timeout:1200]
;
area
  ["boundary"="administrative"]
  ["admin_level"="9"]
  ["teryt:terc"="%s"]
  ["type"="boundary"]
->.boundryarea;
(
  way
    (changed:"%s")
    (user:"%s")
    (area.boundryarea)
    ["building"];
);
out meta bb qt;
""" % (terc, date, user)
    return json.loads(overpass.query(query))

def xml_to_json(data):
    bs = BeautifulSoup(data)
    way = bs.find('way')
    element = dict(way.attrs)
    element['nodes'] = list(map(lambda x: int(x.get('ref')), way.find_all('nd')))
    element['tags'] = dict((x.get('k'), x.get('v')) for x in way.find_all('tag'))
    return element

def osm_api_get(url):
    url = "https://api.openstreetmap.org/%s" % (url,)
    return xml_to_json(urlopen(url))

def get_history(obj):
    ret = {}
    for i in obj['elements']:
        ret[i['id']] = osm_api_get('/api/0.6/%s/%s/%s' % (i['type'], i['id'], int(i['version']) - 1))
    return ret

def main():
    parser = argparse.ArgumentParser(description="finds buildings with removed nodes")
    parser.add_argument('--terc', help="TERYT terc code for area", required=True)
    parser.add_argument('--user', help="User name doing changes", required=True)
    parser.add_argument('--date', help="Date in ISO format, ex. 2015-10-01T00:00:00Z", required=True)
    args = parser.parse_args()

    ways = get_data_From_area(args.terc, args.user, args.date)
    history = get_history(ways)

    ret = []
    for i in ways['elements']:
        if len(set(i['nodes']).symmetric_difference(set(history[i['id']]['nodes']))) > 0:
            ret.append(i['id'])
    print(",".join(map(str, ret)))

if __name__ == '__main__':
    main()
