from urllib.request import urlopen
from urllib.parse import urlencode
import argparse
import logging

__log = logging.getLogger(__name__)


# these below server as documentation
__query_terc = """
<osm-script output="xml" timeout="600">
  <query type="area" into="boundryarea">
    <has-kv k="boundary" v="administrative"/>
    <has-kv k="admin_level" v="7"/> <!-- gmina -->
    <has-kv k="teryt:terc" regv="^%s"/>
    <has-kv k="type" v="boundary"/>
  </query>
  <!-- gather results -->
  <union>
    <query type="node">
      <area-query from="boundryarea" />
      <has-kv k="addr:housenumber" modv="" v="" />
    </query>
    <query type="way">
      <area-query from="boundryarea" />
      <has-kv k="addr:housenumber" modv="" v=""/>
    </query>
    <query type="way">
      <area-query from="boundryarea" />
      <has-kv k="building" modv="" v=""/>
    </query>
    <query type="relation">
      <area-query from="boundryarea" />
      <has-kv k="addr:housenumber" modv="" v=""/>
    </query>
    <query type="relation">
      <area-query from="boundryarea" />
      <has-kv k="building" modv="" v=""/>
    </query>
  </union>
  <!-- print results -->
  <print mode="meta" order="quadtile" geometry="bounds" />
  <recurse type="down" />
  <print mode="meta" order="quadtile" />
</osm-script>
"""

# don't know why Overpass API converter leaves out geometry="bounds" (bb) after conversion
# remember to add it (bb before qt) by hand 
__overpass_ql_terc = """[out:json][timeout:600];area["boundary"="administrative"]["admin_level"="7"]["teryt:terc"~"^%s"]["type"="boundary"]->.boundryarea;(node(area.boundryarea)["addr:housenumber"];way(area.boundryarea)["addr:housenumber"];way(area.boundryarea)["building"];relation(area.boundryarea)["addr:housenumber"];relation(area.boundryarea)["building"];);out meta bb qt;>;out meta bb qt;"""

def getAddresses(terc):
    return query(__overpass_ql_terc % (terc,))


__query_ql_tag = """
[out:%(format)s]
[timeout:2400]
[maxsize:1073741824]
;
area
  ["boundary"="administrative"]
  ["admin_level"="2"]
  ["name"="Polska"]
  ["type"="boundary"]
->.boundryarea;
(
  node
    (area.boundryarea)
    %(tags)s;
  way
    (area.boundryarea)
    %(tags)s;
);
out;
"""

def getNodesWaysWithTags(taglist, format="xml"):
    tags = "\n\t".join(map(lambda x: '["' + x + '"]', taglist))
    return query(__query_ql_tag % {'tags': tags, 'format': format})

def getNodesWaysWithTag(tagname, format="xml"):
    return getNodesWaysWithTags([tagname, ], format)



__overpassurl = "http://overpass.osm.rambler.ru/cgi/interpreter"
__overpassurl = "http://overpass-api.de/api/interpreter"
__overpassurl = "http://api.openstreetmap.fr/oapi/interpreter/"
__overpassurl = "http://osm-cdn.vink.pl/api/interpreter"

def query(qry):
    # TODO - check if the query succeeded
    __log.debug("Query %s , server: %s", qry, __overpassurl)
    url = __overpassurl + '?' + urlencode({'data': qry.replace('\t', '').replace('\n', '')})
    return urlopen(url).read().decode('utf-8')

def main():
    parser = argparse.ArgumentParser(description='Fetches addresses for given teryt:terc from OSM')
    parser.add_argument('--terc', help='teryt:terc code for area', required=True)
    parser.add_argument('--output', default='addresses.osm', help='output file (addresses.osm)', type=argparse.FileType("w+", encoding='UTF-8'))
    args = parser.parse_args()
    ret = getAddresses(args.terc)
    args.output.write(ret)

if __name__ == '__main__':
    main()
