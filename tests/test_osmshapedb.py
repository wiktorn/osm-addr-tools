import unittest
import requests

import utils.osmshapedb
import overpass
# import merger


class OsmDbTests(unittest.TestCase):

    def test_relation(self):
        # merger.get_boundary_shape("321501")
        pass

    def test_multipolygon(self):
        data = requests.get("https://www.openstreetmap.org/api/0.6/relation/6828290/full").content
        ret = utils.osmshapedb.get_geometries(data)
        self.assertTrue('relation:6828290' in ret.geometries)

    def test_closedway(self):
            data = overpass.query("""
            [out:xml]
    [timeout:600];
    (
        way(310328094);
    )->.a;
    (
      node(w.a);
      node(r.a);
      way(r.a);
      way(bn.a);
      relation(bn.a);
      relation(bw.a);
    )->.b;
    (
      node(w.b);
      node(r.b);
      way(r.b);
    )->.c;
    (
        node(w.c);
    )->.d;
    .a out meta ;
    .b out meta ;
    .c out meta ;
    .d out meta ;
            """)
            ret = utils.osmshapedb.get_geometries(data)
            self.assertTrue('way:310328094' in ret.geometries)

    def test_area(self):
        input = b'<?xml version="1.0" encoding="UTF-8"?>' \
                b'<osm version="0.6" generator="Overpass API 0.7.55.4 3079d8ea">' \
                b'<note>The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.</note>' \
                b'<meta osm_base="2019-03-17T20:10:02Z"/>' \
                b'  <node id="31345520" lat="53.7080210" lon="16.6943922" version="16" timestamp="2017-01-28T18:13:45Z" changeset="45600156" uid="163896" user="Zbigniew_Cz">' \
                b'    <tag k="is_in:county" v="powiat szczecinecki"/>' \
                b'    <tag k="is_in:municipality" v="gmina Szczecinek"/>' \
                b'    <tag k="is_in:province" v="wojew\xc3\xb3dztwo zachodniopomorskie"/>' \
                b'    <tag k="name" v="Szczecinek"/>' \
                b'    <tag k="name:de" v="Neustettin"/>' \
                b'    <tag k="name:lt" v="\xc5\xa0\xc4\x8decinekas"/>' \
                b'    <tag k="name:ru" v="\xd0\xa9\xd0\xb5\xd1\x86\xd0\xb8\xd0\xbd\xd0\xb5\xd0\xba"/>' \
                b'    <tag k="place" v="town"/>' \
                b'    <tag k="population" v="40620"/>' \
                b'    <tag k="source:population" v="http://stat.gov.pl/obszary-tematyczne/ludnosc/ludnosc/powierzchnia-i-ludnosc-w-przekroju-terytorialnym-w-2014-r-,7,11.html"/>' \
                b'    <tag k="teryt:rm" v="96"/>' \
                b'    <tag k="teryt:simc" v="0950262"/>' \
                b'    <tag k="teryt:stan_na" v="2009-01-01"/>' \
                b'    <tag k="teryt:terc" v="3215011"/>' \
                b'    <tag k="teryt:updated_by" v="teryt2osm combine.py v. 49"/>' \
                b'    <tag k="wikidata" v="Q848999"/>' \
                b'    <tag k="wikipedia" v="pl:Szczecinek"/>' \
                b'  </node>' \
                b'  <node id="2038096237" lat="53.6603258" lon="16.7078946" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096240" lat="53.6605333" lon="16.7077016" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096242" lat="53.6606503" lon="16.7084243" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096244" lat="53.6608286" lon="16.7085186" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096246" lat="53.6612382" lon="16.7071674" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096248" lat="53.6613845" lon="16.7074098" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096250" lat="53.6614484" lon="16.7068935" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096252" lat="53.6614510" lon="16.7071719" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096255" lat="53.6618766" lon="16.7099282" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096257" lat="53.6621134" lon="16.7061618" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096264" lat="53.6621905" lon="16.7062157" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096266" lat="53.6626055" lon="16.7055019" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096268" lat="53.6635312" lon="16.7044200" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096270" lat="53.6636748" lon="16.7044155" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096272" lat="53.6644940" lon="16.7133714" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096274" lat="53.6646058" lon="16.7031316" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096276" lat="53.6646244" lon="16.7029880" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096278" lat="53.6647627" lon="16.7150413" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096282" lat="53.6651617" lon="16.7023101" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096284" lat="53.6657761" lon="16.7014617" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096286" lat="53.6669703" lon="16.6999309" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096289" lat="53.6670501" lon="16.7201814" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096292" lat="53.6670740" lon="16.6997244" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096295" lat="53.6679039" lon="16.6986470" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096299" lat="53.6685475" lon="16.7234899" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096303" lat="53.6686512" lon="16.6976234" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096305" lat="53.6688853" lon="16.7243025" version="1" timestamp="2012-11-28T11:57:01Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096306" lat="53.6690448" lon="16.6972104" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096308" lat="53.6692496" lon="16.6969276" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096309" lat="53.6693693" lon="16.6967346" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096310" lat="53.6700023" lon="16.6961375" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096311" lat="53.6705847" lon="16.6956303" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096313" lat="53.6710023" lon="16.6953834" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096316" lat="53.6712124" lon="16.6953205" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096319" lat="53.6714437" lon="16.7292495" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096322" lat="53.6715794" lon="16.6950646" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096325" lat="53.6720102" lon="16.7299812" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096328" lat="53.6722176" lon="16.6948716" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096330" lat="53.6724202" lon="16.7429292" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096333" lat="53.6726165" lon="16.7301653" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096336" lat="53.6727043" lon="16.6947639" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096339" lat="53.6727947" lon="16.7308387" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096342" lat="53.6730340" lon="16.7310811" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096345" lat="53.6732025" lon="16.7439091" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096349" lat="53.6733984" lon="16.7342953" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096352" lat="53.6734223" lon="16.6946786" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096355" lat="53.6734542" lon="16.7311798" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096358" lat="53.6734609" lon="16.7404137" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096361" lat="53.6736768" lon="16.7447277" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096364" lat="53.6740236" lon="16.7391828" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096367" lat="53.6741298" lon="16.7452894" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096371" lat="53.6742289" lon="16.7393501" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096381" lat="53.6742387" lon="16.7348026" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096385" lat="53.6745179" lon="16.6723181" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096388" lat="53.6746289" lon="16.7459825" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096391" lat="53.6746828" lon="16.6726907" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096395" lat="53.6747599" lon="16.7487011" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096398" lat="53.6748625" lon="16.7388960" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096401" lat="53.6748689" lon="16.6948447" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096405" lat="53.6749567" lon="16.6731396" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096408" lat="53.6751244" lon="16.7484024" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096411" lat="53.6751881" lon="16.6732922" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096414" lat="53.6752801" lon="16.7501949" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096417" lat="53.6752872" lon="16.7545985" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096418" lat="53.6753049" lon="16.7544013" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096420" lat="53.6753290" lon="16.7351842" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096422" lat="53.6753297" lon="16.7540368" version="1" timestamp="2012-11-28T11:57:02Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096424" lat="53.6753509" lon="16.7368884" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096426" lat="53.6754114" lon="16.7353323" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096428" lat="53.6757704" lon="16.6713799" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096431" lat="53.6759486" lon="16.6746614" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096433" lat="53.6759752" lon="16.6949210" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096435" lat="53.6760629" lon="16.6949344" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096438" lat="53.6760682" lon="16.6950242" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096440" lat="53.6760789" lon="16.6712946" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096442" lat="53.6763455" lon="16.7549510" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096444" lat="53.6767065" lon="16.7552020" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096447" lat="53.6770122" lon="16.6764346" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096450" lat="53.6770335" lon="16.6950646" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096453" lat="53.6770787" lon="16.6712003" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096456" lat="53.6771239" lon="16.6952442" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096459" lat="53.6772374" lon="16.7557756" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096463" lat="53.6774457" lon="16.6951409" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096466" lat="53.6774457" lon="16.6952621" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096469" lat="53.6778674" lon="16.7582911" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096472" lat="53.6780306" lon="16.6713080" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096475" lat="53.6780838" lon="16.6952038" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096478" lat="53.6781823" lon="16.7581357" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096482" lat="53.6782567" lon="16.7586436" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096485" lat="53.6783019" lon="16.6951724" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096488" lat="53.6785292" lon="16.7591515" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096491" lat="53.6786050" lon="16.6792000" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096494" lat="53.6788071" lon="16.6715684" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096497" lat="53.6791129" lon="16.6954193" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096509" lat="53.6791341" lon="16.6953115" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096512" lat="53.6791926" lon="16.6686011" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096515" lat="53.6792405" lon="16.6683676" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096518" lat="53.6792883" lon="16.6712362" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096521" lat="53.6794107" lon="16.6807487" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096524" lat="53.6794532" lon="16.6808789" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096526" lat="53.6795808" lon="16.6806410" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096528" lat="53.6796127" lon="16.6654856" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096530" lat="53.6796260" lon="16.6954866" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096532" lat="53.6796659" lon="16.6706302" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096534" lat="53.6796739" lon="16.6648706" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096537" lat="53.6797430" lon="16.6954911" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096540" lat="53.6798042" lon="16.6953070" version="1" timestamp="2012-11-28T11:57:03Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096543" lat="53.6798095" lon="16.6639413" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096546" lat="53.6798760" lon="16.6703653" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096549" lat="53.6802828" lon="16.6639234" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096552" lat="53.6803705" lon="16.6823513" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096558" lat="53.6804049" lon="16.7620016" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096561" lat="53.6805912" lon="16.6827778" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096563" lat="53.6807348" lon="16.6827778" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096566" lat="53.6807667" lon="16.6615666" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096569" lat="53.6807906" lon="16.6955988" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096571" lat="53.6808278" lon="16.6954058" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096573" lat="53.6808720" lon="16.7627724" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096575" lat="53.6809315" lon="16.6609336" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096577" lat="53.6810352" lon="16.6619796" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096579" lat="53.6811177" lon="16.6605520" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096581" lat="53.6812825" lon="16.6636989" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096583" lat="53.6813171" lon="16.6603680" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096585" lat="53.6813596" lon="16.6594612" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096588" lat="53.6813729" lon="16.6839091" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096590" lat="53.6813835" lon="16.6589943" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096594" lat="53.6813993" lon="16.7634954" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096597" lat="53.6814154" lon="16.6956437" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096600" lat="53.6814341" lon="16.6601121" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096603" lat="53.6814713" lon="16.6622220" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096606" lat="53.6814819" lon="16.6586935" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096609" lat="53.6815670" lon="16.6586262" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096612" lat="53.6816361" lon="16.6955180" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096615" lat="53.6816893" lon="16.6585544" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096618" lat="53.6818010" lon="16.6585095" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096621" lat="53.6818302" lon="16.6623118" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096636" lat="53.6818381" lon="16.7644812" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096639" lat="53.6818558" lon="16.7639853" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096640" lat="53.6818877" lon="16.7655687" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096641" lat="53.6820429" lon="16.6585948" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096642" lat="53.6822476" lon="16.6587070" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096644" lat="53.6823753" lon="16.6627338" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096646" lat="53.6823965" lon="16.6585140" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096648" lat="53.6824790" lon="16.6583344" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096652" lat="53.6825534" lon="16.6581324" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096655" lat="53.6826411" lon="16.6580067" version="1" timestamp="2012-11-28T11:57:04Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096658" lat="53.6826662" lon="16.7661901" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096661" lat="53.6827342" lon="16.6626081" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096664" lat="53.6827847" lon="16.6957560" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096667" lat="53.6828565" lon="16.6956258" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096670" lat="53.6828679" lon="16.7667936" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096673" lat="53.6829599" lon="16.7669370" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096676" lat="53.6829894" lon="16.6578496" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096679" lat="53.6830187" lon="16.6956886" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096682" lat="53.6830665" lon="16.6624285" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096685" lat="53.6831015" lon="16.7671461" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096688" lat="53.6831702" lon="16.6574051" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096691" lat="53.6833430" lon="16.6621098" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096694" lat="53.6833537" lon="16.6571223" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096697" lat="53.6834093" lon="16.7673791" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096701" lat="53.6834175" lon="16.6956751" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096704" lat="53.6835079" lon="16.6877159" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096707" lat="53.6835265" lon="16.6569428" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096709" lat="53.6835850" lon="16.6884027" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096711" lat="53.6836701" lon="16.6568036" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096713" lat="53.6836754" lon="16.6876620" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096716" lat="53.6838535" lon="16.6565342" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096719" lat="53.6838907" lon="16.6957245" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096722" lat="53.6839040" lon="16.6882232" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096725" lat="53.6839366" lon="16.7679348" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096727" lat="53.6839891" lon="16.6620559" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096729" lat="53.6839997" lon="16.6564938" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096731" lat="53.6840476" lon="16.6632051" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096734" lat="53.6840901" lon="16.6894307" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096736" lat="53.6841247" lon="16.6565522" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096739" lat="53.6841433" lon="16.6957874" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096742" lat="53.6841949" lon="16.7682276" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096754" lat="53.6844464" lon="16.6564445" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096756" lat="53.6846378" lon="16.6960029" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096758" lat="53.6848638" lon="16.6565118" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096760" lat="53.6849911" lon="16.7693091" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096763" lat="53.6850153" lon="16.6912713" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096766" lat="53.6850233" lon="16.6563996" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096769" lat="53.6850366" lon="16.6913880" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096772" lat="53.6850738" lon="16.6911276" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096776" lat="53.6852413" lon="16.6912354" version="1" timestamp="2012-11-28T11:57:05Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096778" lat="53.6854141" lon="16.6560000" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096781" lat="53.6854380" lon="16.6960971" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096783" lat="53.6854405" lon="16.7697512" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096786" lat="53.6856667" lon="16.6919851" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096788" lat="53.6857305" lon="16.6918549" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096791" lat="53.6858793" lon="16.6555107" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096796" lat="53.6860867" lon="16.6551920" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096799" lat="53.6862834" lon="16.6962857" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096802" lat="53.6862888" lon="16.6548643" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096805" lat="53.6866477" lon="16.6964293" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096808" lat="53.6869408" lon="16.7726611" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096811" lat="53.6870305" lon="16.6943284" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096814" lat="53.6873070" lon="16.6542403" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096816" lat="53.6880593" lon="16.6540517" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096819" lat="53.6885165" lon="16.6545321" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096823" lat="53.6887065" lon="16.7748898" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096827" lat="53.6887957" lon="16.6545366" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096830" lat="53.6888904" lon="16.7754276" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096832" lat="53.6893610" lon="16.7765031" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096835" lat="53.6896729" lon="16.6535624" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096838" lat="53.6901677" lon="16.7773396" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096841" lat="53.6905421" lon="16.6535849" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096843" lat="53.6908585" lon="16.6536298" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096845" lat="53.6909223" lon="16.6581458" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096847" lat="53.6909462" lon="16.6578406" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096849" lat="53.6909914" lon="16.6585319" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096852" lat="53.6911159" lon="16.7782956" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096856" lat="53.6912280" lon="16.6565702" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096859" lat="53.6912705" lon="16.6558878" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096862" lat="53.6913370" lon="16.6541460" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096864" lat="53.6913495" lon="16.7785704" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096865" lat="53.6914379" lon="16.7786840" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096866" lat="53.6914839" lon="16.7787915" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096875" lat="53.6914938" lon="16.6550124" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096879" lat="53.6916007" lon="16.7791799" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096882" lat="53.6916820" lon="16.7794069" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096885" lat="53.6919022" lon="16.7798304" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096888" lat="53.6924295" lon="16.6578945" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096891" lat="53.6926606" lon="16.7798560" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096894" lat="53.6927668" lon="16.7771151" version="1" timestamp="2012-11-28T11:57:06Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096897" lat="53.6941226" lon="16.6595240" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096902" lat="53.6942157" lon="16.6597215" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096905" lat="53.6943858" lon="16.6601435" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096908" lat="53.6945187" lon="16.6603725" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096911" lat="53.6947924" lon="16.6607047" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096913" lat="53.6949307" lon="16.6609022" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096915" lat="53.6954623" lon="16.6622444" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096917" lat="53.6963021" lon="16.6623163" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096920" lat="53.6964643" lon="16.6626530" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096923" lat="53.6964669" lon="16.6631468" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096926" lat="53.6966849" lon="16.6637483" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096929" lat="53.6969400" lon="16.6643229" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096932" lat="53.6971447" lon="16.6644396" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096935" lat="53.6972643" lon="16.6645564" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096938" lat="53.6974530" lon="16.6647943" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096941" lat="53.6975673" lon="16.6621591" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096944" lat="53.6978490" lon="16.6632725" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096947" lat="53.6978729" lon="16.6610099" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096950" lat="53.6978942" lon="16.6637932" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096953" lat="53.6979527" lon="16.6641254" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096956" lat="53.6981068" lon="16.6609201" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096960" lat="53.6984178" lon="16.6604847" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096962" lat="53.6987659" lon="16.6596766" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096965" lat="53.6988084" lon="16.6595375" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096968" lat="53.6988696" lon="16.6600178" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096971" lat="53.6989949" lon="16.7778973" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096974" lat="53.6992393" lon="16.7778756" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096976" lat="53.6992742" lon="16.7774262" version="2" timestamp="2012-11-28T12:01:36Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096977" lat="53.6993345" lon="16.7761657" version="2" timestamp="2012-11-28T12:01:36Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096978" lat="53.6993647" lon="16.7752357" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096979" lat="53.6994389" lon="16.7740228" version="2" timestamp="2012-11-28T12:01:36Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096981" lat="53.6995274" lon="16.7740406" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096983" lat="53.6996102" lon="16.7717776" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096985" lat="53.6997530" lon="16.7697218" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096988" lat="53.6999034" lon="16.7672872" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038096999" lat="53.6999539" lon="16.6585184" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097002" lat="53.7000601" lon="16.7673084" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097005" lat="53.7000914" lon="16.7667156" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097008" lat="53.7001320" lon="16.6590661" version="1" timestamp="2012-11-28T11:57:07Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097011" lat="53.7006679" lon="16.7666627" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097014" lat="53.7011003" lon="16.7640905" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097018" lat="53.7013322" lon="16.7626933" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097021" lat="53.7013322" lon="16.7629791" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097024" lat="53.7015765" lon="16.7612325" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097027" lat="53.7016768" lon="16.7604280" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097030" lat="53.7016893" lon="16.7619946" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097033" lat="53.7017520" lon="16.7615924" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097036" lat="53.7019024" lon="16.7591896" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097039" lat="53.7027817" lon="16.7534343" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097049" lat="53.7039295" lon="16.7536249" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097051" lat="53.7044238" lon="16.6493336" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097054" lat="53.7044504" lon="16.6484583" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097057" lat="53.7044690" lon="16.6506579" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097060" lat="53.7045939" lon="16.6568260" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097063" lat="53.7046258" lon="16.6475290" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097067" lat="53.7047533" lon="16.6557935" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097071" lat="53.7048437" lon="16.6559237" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097073" lat="53.7049686" lon="16.6544513" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097076" lat="53.7050563" lon="16.6529743" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097078" lat="53.7050669" lon="16.6468646" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097080" lat="53.7052237" lon="16.6465908" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097082" lat="53.7052688" lon="16.6463888" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097084" lat="53.7054708" lon="16.6458680" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097086" lat="53.7055983" lon="16.7414726" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097088" lat="53.7056171" lon="16.7399695" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097091" lat="53.7056568" lon="16.6454236" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097094" lat="53.7057870" lon="16.6444943" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097097" lat="53.7059513" lon="16.7467294" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097100" lat="53.7060690" lon="16.7394049" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097103" lat="53.7061444" lon="16.7446617" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097106" lat="53.7062667" lon="16.7389277" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097109" lat="53.7065068" lon="16.7359533" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097112" lat="53.7066010" lon="16.7355398" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097114" lat="53.7068034" lon="16.7374326" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097116" lat="53.7071141" lon="16.7365339" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097118" lat="53.7071422" lon="16.6402386" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097120" lat="53.7072647" lon="16.7477553" version="1" timestamp="2012-11-28T11:57:08Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097137" lat="53.7072930" lon="16.7365021" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097141" lat="53.7073730" lon="16.7464590" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097145" lat="53.7073867" lon="16.6408985" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097148" lat="53.7074389" lon="16.7345775" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097152" lat="53.7074436" lon="16.7361203" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097155" lat="53.7074954" lon="16.7354364" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097158" lat="53.7077260" lon="16.7343389" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097162" lat="53.7078862" lon="16.6382320" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097166" lat="53.7079765" lon="16.6389009" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097170" lat="53.7082555" lon="16.6394126" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097174" lat="53.7083193" lon="16.6377202" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097179" lat="53.7083273" lon="16.6392869" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097183" lat="53.7087763" lon="16.6378010" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097187" lat="53.7089219" lon="16.7543055" version="2" timestamp="2014-09-09T21:36:14Z" changeset="25337938" uid="1403931" user="__Daniel__"/>' \
                b'  <node id="2038097191" lat="53.7090143" lon="16.7513902" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097195" lat="53.7090633" lon="16.6385058" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097199" lat="53.7091669" lon="16.6188568" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097205" lat="53.7092127" lon="16.7489255" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097208" lat="53.7093722" lon="16.7473547" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097211" lat="53.7095044" lon="16.6191621" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097214" lat="53.7095921" lon="16.6212540" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097216" lat="53.7095947" lon="16.6196065" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097219" lat="53.7102032" lon="16.6223718" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097222" lat="53.7102324" lon="16.6205851" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097225" lat="53.7102643" lon="16.6182418" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097229" lat="53.7103546" lon="16.6234043" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097234" lat="53.7103599" lon="16.6207916" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097238" lat="53.7103918" lon="16.6234717" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097242" lat="53.7106350" lon="16.7353807" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097246" lat="53.7106974" lon="16.6365037" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097250" lat="53.7107104" lon="16.7345536" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097254" lat="53.7107346" lon="16.6237904" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097257" lat="53.7108462" lon="16.6238936" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097259" lat="53.7109365" lon="16.6179186" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097261" lat="53.7111650" lon="16.6361086" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097264" lat="53.7112660" lon="16.6182822" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097266" lat="53.7114812" lon="16.6270854" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097269" lat="53.7115582" lon="16.6250563" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097272" lat="53.7115635" lon="16.6265647" version="1" timestamp="2012-11-28T11:57:09Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097275" lat="53.7116167" lon="16.6362972" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097278" lat="53.7116592" lon="16.6253212" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097294" lat="53.7116964" lon="16.6170656" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097300" lat="53.7118744" lon="16.6156785" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097303" lat="53.7118956" lon="16.6154630" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097306" lat="53.7119302" lon="16.6365620" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097309" lat="53.7121640" lon="16.6367910" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097312" lat="53.7121985" lon="16.6284726" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097315" lat="53.7122384" lon="16.6367865" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097319" lat="53.7123606" lon="16.6366742" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097322" lat="53.7124403" lon="16.6365216" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097325" lat="53.7124987" lon="16.6143811" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097328" lat="53.7125147" lon="16.6362702" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097331" lat="53.7125811" lon="16.6358437" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097334" lat="53.7126050" lon="16.6347439" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097336" lat="53.7126475" lon="16.6345778" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097338" lat="53.7126502" lon="16.6294332" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097340" lat="53.7127405" lon="16.6297161" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097342" lat="53.7128567" lon="16.7349274" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097344" lat="53.7128787" lon="16.6138200" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097347" lat="53.7131789" lon="16.6296757" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097350" lat="53.7132427" lon="16.6135596" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097353" lat="53.7133702" lon="16.6135596" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097357" lat="53.7135907" lon="16.6335273" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097362" lat="53.7138006" lon="16.6294377" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097366" lat="53.7138378" lon="16.6137796" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097369" lat="53.7140344" lon="16.6140938" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097375" lat="53.7141035" lon="16.6324634" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097379" lat="53.7141964" lon="16.6293435" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097382" lat="53.7144249" lon="16.6294243" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097385" lat="53.7145099" lon="16.6132588" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097388" lat="53.7145976" lon="16.6322120" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097393" lat="53.7146826" lon="16.6126573" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097396" lat="53.7146853" lon="16.6128728" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097400" lat="53.7148553" lon="16.6313142" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097404" lat="53.7150067" lon="16.6301291" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097408" lat="53.7150439" lon="16.6095149" version="1" timestamp="2012-11-28T11:57:10Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097411" lat="53.7152382" lon="16.7304818" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097414" lat="53.7152665" lon="16.7310862" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097417" lat="53.7152759" lon="16.7295275" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097420" lat="53.7153362" lon="16.6119211" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097422" lat="53.7153935" lon="16.7321121" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097424" lat="53.7155065" lon="16.7294798" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097433" lat="53.7158077" lon="16.7340129" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097436" lat="53.7160827" lon="16.6093667" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097438" lat="53.7171113" lon="16.7254079" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097440" lat="53.7171852" lon="16.6099144" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097442" lat="53.7173420" lon="16.7260282" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097444" lat="53.7175067" lon="16.7265929" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097446" lat="53.7179349" lon="16.7277779" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097447" lat="53.7181468" lon="16.6102466" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097448" lat="53.7194963" lon="16.6161498" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097449" lat="53.7195209" lon="16.7237299" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097450" lat="53.7200150" lon="16.7205249" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097451" lat="53.7201421" lon="16.7183617" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097452" lat="53.7203585" lon="16.7208191" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097454" lat="53.7206067" lon="16.6094251" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097456" lat="53.7210832" lon="16.7209862" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097458" lat="53.7221608" lon="16.7195865" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097460" lat="53.7222879" lon="16.7130890" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097462" lat="53.7223538" lon="16.7119120" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097464" lat="53.7224808" lon="16.7133912" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097470" lat="53.7227146" lon="16.6318862" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097474" lat="53.7228114" lon="16.6314917" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097481" lat="53.7231302" lon="16.7093353" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097483" lat="53.7231349" lon="16.7091762" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097485" lat="53.7232055" lon="16.7133833" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097488" lat="53.7234784" lon="16.7150056" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097490" lat="53.7236149" lon="16.7139559" version="1" timestamp="2012-11-28T11:57:11Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097497" lat="53.7237184" lon="16.7088184" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097500" lat="53.7237466" lon="16.7081742" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097514" lat="53.7240533" lon="16.6197413" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097517" lat="53.7240964" lon="16.6197549" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097520" lat="53.7241043" lon="16.7166042" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097539" lat="53.7241273" lon="16.6188752" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097545" lat="53.7242548" lon="16.7194274" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097547" lat="53.7242981" lon="16.6176146" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097553" lat="53.7243715" lon="16.6310105" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097557" lat="53.7244383" lon="16.7168587" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097563" lat="53.7245183" lon="16.7190298" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097566" lat="53.7245230" lon="16.7074028" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097574" lat="53.7246266" lon="16.7177414" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097592" lat="53.7249842" lon="16.7181152" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097595" lat="53.7249936" lon="16.7070449" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097601" lat="53.7250359" lon="16.7083492" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097608" lat="53.7256012" lon="16.6308950" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097611" lat="53.7256617" lon="16.7077527" version="1" timestamp="2012-11-28T11:57:12Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097614" lat="53.7257794" lon="16.7064882" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097618" lat="53.7261746" lon="16.7032116" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097621" lat="53.7263722" lon="16.7014779" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097624" lat="53.7263816" lon="16.7046909" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097627" lat="53.7266687" lon="16.7040864" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097630" lat="53.7267533" lon="16.7003407" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097634" lat="53.7269839" lon="16.7001896" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097637" lat="53.7270592" lon="16.7002055" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097640" lat="53.7278685" lon="16.7006508" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097643" lat="53.7279298" lon="16.6287780" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097646" lat="53.7283625" lon="16.7007224" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097649" lat="53.7288236" lon="16.7006031" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097652" lat="53.7292047" lon="16.7009212" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097655" lat="53.7292676" lon="16.6281621" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097666" lat="53.7293035" lon="16.7009371" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097668" lat="53.7296657" lon="16.7007940" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097671" lat="53.7300986" lon="16.7008815" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097674" lat="53.7305941" lon="16.6282872" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097677" lat="53.7306726" lon="16.7007781" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097680" lat="53.7310725" lon="16.7008178" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097683" lat="53.7311525" lon="16.7008735" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097687" lat="53.7313797" lon="16.6284989" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097690" lat="53.7318629" lon="16.7023130" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097693" lat="53.7319334" lon="16.7024164" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097696" lat="53.7320685" lon="16.6287203" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097698" lat="53.7321216" lon="16.7025277" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097700" lat="53.7321766" lon="16.6287395" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097702" lat="53.7324650" lon="16.6603301" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097705" lat="53.7324886" lon="16.6600120" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097707" lat="53.7326297" lon="16.7032196" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097710" lat="53.7326438" lon="16.6603381" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097713" lat="53.7326532" lon="16.6692691" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097716" lat="53.7326776" lon="16.6291725" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097719" lat="53.7330343" lon="16.6579284" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097722" lat="53.7331848" lon="16.6673922" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097725" lat="53.7335753" lon="16.6642906" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097729" lat="53.7337305" lon="16.6634317" version="1" timestamp="2012-11-28T11:57:13Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097733" lat="53.7337447" lon="16.6298311" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097736" lat="53.7344738" lon="16.7036809" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097739" lat="53.7345444" lon="16.6695554" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097742" lat="53.7346996" lon="16.6529658" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097745" lat="53.7348784" lon="16.6305548" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097748" lat="53.7348784" lon="16.6525523" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097751" lat="53.7349772" lon="16.6522024" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097754" lat="53.7351606" lon="16.6692214" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097758" lat="53.7354711" lon="16.6510810" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097761" lat="53.7357440" lon="16.6502221" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097764" lat="53.7357816" lon="16.7062735" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097767" lat="53.7358004" lon="16.6310558" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097770" lat="53.7358428" lon="16.7048976" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097773" lat="53.7358522" lon="16.7050965" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097776" lat="53.7358663" lon="16.7054623" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097778" lat="53.7360168" lon="16.6496893" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097780" lat="53.7360686" lon="16.7039672" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097782" lat="53.7363132" lon="16.7040467" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097792" lat="53.7363978" lon="16.6680841" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097796" lat="53.7366236" lon="16.6480351" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097799" lat="53.7367459" lon="16.7040228" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097802" lat="53.7367977" lon="16.6477011" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097806" lat="53.7367977" lon="16.7039672" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097810" lat="53.7368682" lon="16.6474625" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097813" lat="53.7370564" lon="16.6468740" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097816" lat="53.7373198" lon="16.6463332" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097819" lat="53.7374986" lon="16.6458719" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097822" lat="53.7375550" lon="16.6456572" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097825" lat="53.7376491" lon="16.6453948" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097828" lat="53.7377996" lon="16.6450846" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097831" lat="53.7378702" lon="16.6666526" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097834" lat="53.7379078" lon="16.7002771" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097837" lat="53.7379690" lon="16.6445677" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097842" lat="53.7383406" lon="16.6437406" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097847" lat="53.7384158" lon="16.6434463" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097851" lat="53.7384911" lon="16.6323919" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097855" lat="53.7387639" lon="16.6303162" version="1" timestamp="2012-11-28T11:57:14Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097859" lat="53.7387922" lon="16.6425874" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097862" lat="53.7387969" lon="16.6422136" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097866" lat="53.7389615" lon="16.6316444" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097869" lat="53.7391496" lon="16.6306423" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097872" lat="53.7391543" lon="16.6412911" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097875" lat="53.7392249" lon="16.6411559" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097878" lat="53.7394131" lon="16.6409809" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097881" lat="53.7394507" lon="16.6408855" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097884" lat="53.7395401" lon="16.6406231" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097888" lat="53.7397141" lon="16.6402016" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097891" lat="53.7397517" lon="16.6639168" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097894" lat="53.7397705" lon="16.6938989" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097897" lat="53.7397847" lon="16.6937160" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097899" lat="53.7398646" lon="16.6935569" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097901" lat="53.7398740" lon="16.6397801" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097903" lat="53.7399117" lon="16.6396290" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097905" lat="53.7399681" lon="16.6934217" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097907" lat="53.7399916" lon="16.6331713" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097909" lat="53.7400245" lon="16.6870515" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097913" lat="53.7400904" lon="16.6320738" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097916" lat="53.7401609" lon="16.6933184" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097919" lat="53.7401986" lon="16.6866062" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097922" lat="53.7404385" lon="16.6362808" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097937" lat="53.7404808" lon="16.6858030" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097941" lat="53.7404902" lon="16.6361456" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097944" lat="53.7405466" lon="16.6899702" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097947" lat="53.7405466" lon="16.6901293" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097950" lat="53.7405796" lon="16.6930798" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097953" lat="53.7405843" lon="16.6903758" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097958" lat="53.7406548" lon="16.6857552" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097961" lat="53.7406548" lon="16.6905985" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097964" lat="53.7406736" lon="16.6891988" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097967" lat="53.7406736" lon="16.6929764" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097969" lat="53.7408665" lon="16.6365274" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097971" lat="53.7409041" lon="16.6839897" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097973" lat="53.7409041" lon="16.6882922" version="1" timestamp="2012-11-28T11:57:15Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097975" lat="53.7409512" lon="16.6878548" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097978" lat="53.7410076" lon="16.6912983" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097981" lat="53.7410311" lon="16.6917516" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097984" lat="53.7410405" lon="16.6367819" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097987" lat="53.7410452" lon="16.6915528" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097990" lat="53.7410970" lon="16.6362013" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097993" lat="53.7412146" lon="16.6841249" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097996" lat="53.7412193" lon="16.6359230" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038097999" lat="53.7415062" lon="16.6340063" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038098003" lat="53.7416144" lon="16.6844828" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038098005" lat="53.7426068" lon="16.6857870" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038098007" lat="53.7429736" lon="16.6800610" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038098009" lat="53.7431900" lon="16.6730307" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038098011" lat="53.7431947" lon="16.6617378" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038098013" lat="53.7432511" lon="16.6723389" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038098015" lat="53.7434581" lon="16.6710823" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038098017" lat="53.7440037" lon="16.6573717" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038098020" lat="53.7451795" lon="16.6623740" version="1" timestamp="2012-11-28T11:57:16Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038107025" lat="53.6995818" lon="16.7723209" version="1" timestamp="2012-11-28T12:01:33Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2038107026" lat="53.6995873" lon="16.7732346" version="1" timestamp="2012-11-28T12:01:33Z" changeset="14072144" uid="116241" user="gsapijaszko"/>' \
                b'  <node id="2057191701" lat="53.7115866" lon="16.6272718" version="2" timestamp="2015-02-16T20:19:57Z" changeset="28894544" uid="2356123" user="Vercyngetorix"/>' \
                b'  <node id="2295006590" lat="53.7099576" lon="16.6374101" version="1" timestamp="2013-05-07T18:32:25Z" changeset="16016445" uid="1403931" user="__Daniel__"/>' \
                b'  <node id="3008897776" lat="53.7404132" lon="16.6859953" version="1" timestamp="2014-08-10T16:09:09Z" changeset="24658134" uid="1772132" user="gethiox"/>' \
                b'  <node id="3164883859" lat="53.7328365" lon="16.6692969" version="4" timestamp="2017-04-28T08:34:32Z" changeset="48220796" uid="2578506" user="seba020"/>' \
                b'  <node id="3165578288" lat="53.7368013" lon="16.6676918" version="2" timestamp="2015-01-01T14:49:20Z" changeset="27841499" uid="67099" user="marcin_b"/>' \
                b'  <node id="3354754671" lat="53.7126675" lon="16.6294875" version="1" timestamp="2015-02-16T20:19:46Z" changeset="28894544" uid="2356123" user="Vercyngetorix"/>' \
                b'  <node id="3363121455" lat="53.7051644" lon="16.6466610" version="1" timestamp="2015-02-21T11:16:18Z" changeset="28996296" uid="2356123" user="Vercyngetorix"/>' \
                b'  <node id="3561942839" lat="53.7118080" lon="16.6262863" version="1" timestamp="2015-05-31T20:52:45Z" changeset="31619048" uid="2356123" user="Vercyngetorix"/>' \
                b'  <node id="3854890106" lat="53.7106380" lon="16.7353569" version="1" timestamp="2015-11-23T17:40:54Z" changeset="35535144" uid="2356123" user="Vercyngetorix"/>' \
                b'  <node id="3998599660" lat="53.7200663" lon="16.6125588" version="1" timestamp="2016-02-10T07:30:35Z" changeset="37118341" uid="2356123" user="Vercyngetorix"/>' \
                b'  <node id="5924318399" lat="53.6653669" lon="16.7020268" version="1" timestamp="2018-09-23T16:27:45Z" changeset="62855358" uid="1537441" user="Perimex"/>' \
                b'  <node id="6168973180" lat="53.6794927" lon="16.7606155" version="1" timestamp="2018-12-28T18:07:35Z" changeset="65849043" uid="7692914" user="Qitay"/>' \
                b'  <node id="6168973184" lat="53.6801251" lon="16.7615765" version="1" timestamp="2018-12-28T18:07:35Z" changeset="65849043" uid="7692914" user="Qitay"/>' \
                b'  <node id="6168974494" lat="53.6807831" lon="16.7626257" version="1" timestamp="2018-12-28T18:07:35Z" changeset="65849043" uid="7692914" user="Qitay"/>' \
                b'  <node id="6168974495" lat="53.6802967" lon="16.7618371" version="1" timestamp="2018-12-28T18:07:35Z" changeset="65849043" uid="7692914" user="Qitay"/>' \
                b'  <way id="1" version="16" timestamp="2018-12-28T18:07:48Z" changeset="65849043" uid="7692914" user="Qitay">' \
                b'    <nd ref="2038097120"/>' \
                b'    <nd ref="2038097208"/>' \
                b'  </way>' \
                b'  <way id="193299964" version="16" timestamp="2018-12-28T18:07:48Z" changeset="65849043" uid="7692914" user="Qitay">' \
                b'    <nd ref="2038097208"/>' \
                b'    <nd ref="2038097205"/>' \
                b'    <nd ref="2038097191"/>' \
                b'    <nd ref="2038097187"/>' \
                b'    <nd ref="2038097049"/>' \
                b'    <nd ref="2038097039"/>' \
                b'    <nd ref="2038097036"/>' \
                b'    <nd ref="2038097027"/>' \
                b'    <nd ref="2038097024"/>' \
                b'    <nd ref="2038097033"/>' \
                b'    <nd ref="2038097030"/>' \
                b'    <nd ref="2038097018"/>' \
                b'    <nd ref="2038097021"/>' \
                b'    <nd ref="2038097014"/>' \
                b'    <nd ref="2038097011"/>' \
                b'    <nd ref="2038097005"/>' \
                b'    <nd ref="2038097002"/>' \
                b'    <nd ref="2038096988"/>' \
                b'    <nd ref="2038096985"/>' \
                b'    <nd ref="2038096983"/>' \
                b'    <nd ref="2038107025"/>' \
                b'    <nd ref="2038107026"/>' \
                b'    <nd ref="2038096981"/>' \
                b'    <nd ref="2038096979"/>' \
                b'    <nd ref="2038096978"/>' \
                b'    <nd ref="2038096977"/>' \
                b'    <nd ref="2038096976"/>' \
                b'    <nd ref="2038096974"/>' \
                b'    <nd ref="2038096971"/>' \
                b'    <nd ref="2038096894"/>' \
                b'    <nd ref="2038096891"/>' \
                b'    <nd ref="2038096885"/>' \
                b'    <nd ref="2038096882"/>' \
                b'    <nd ref="2038096879"/>' \
                b'    <nd ref="2038096866"/>' \
                b'    <nd ref="2038096865"/>' \
                b'    <nd ref="2038096864"/>' \
                b'    <nd ref="2038096852"/>' \
                b'    <nd ref="2038096838"/>' \
                b'    <nd ref="2038096832"/>' \
                b'    <nd ref="2038096830"/>' \
                b'    <nd ref="2038096823"/>' \
                b'    <nd ref="2038096808"/>' \
                b'    <nd ref="2038096783"/>' \
                b'    <nd ref="2038096760"/>' \
                b'    <nd ref="2038096742"/>' \
                b'    <nd ref="2038096725"/>' \
                b'    <nd ref="2038096697"/>' \
                b'    <nd ref="2038096685"/>' \
                b'    <nd ref="2038096673"/>' \
                b'    <nd ref="2038096670"/>' \
                b'    <nd ref="2038096658"/>' \
                b'    <nd ref="2038096640"/>' \
                b'    <nd ref="2038096636"/>' \
                b'    <nd ref="2038096639"/>' \
                b'    <nd ref="2038096594"/>' \
                b'    <nd ref="2038096573"/>' \
                b'    <nd ref="6168974494"/>' \
                b'    <nd ref="2038096558"/>' \
                b'    <nd ref="6168974495"/>' \
                b'    <nd ref="6168973184"/>' \
                b'    <nd ref="6168973180"/>' \
                b'    <nd ref="2038096488"/>' \
                b'    <nd ref="2038096482"/>' \
                b'    <nd ref="2038096478"/>' \
                b'    <nd ref="2038096469"/>' \
                b'    <nd ref="2038096459"/>' \
                b'    <nd ref="2038096444"/>' \
                b'    <nd ref="2038096442"/>' \
                b'    <nd ref="2038096417"/>' \
                b'    <nd ref="2038096418"/>' \
                b'    <nd ref="2038096422"/>' \
                b'    <nd ref="2038096414"/>' \
                b'    <nd ref="2038096408"/>' \
                b'    <nd ref="2038096395"/>' \
                b'    <nd ref="2038096388"/>' \
                b'    <nd ref="2038096367"/>' \
                b'    <nd ref="2038096361"/>' \
                b'    <nd ref="2038096345"/>' \
                b'    <nd ref="2038096330"/>' \
                b'    <nd ref="2038096358"/>' \
                b'    <nd ref="2038096364"/>' \
                b'    <nd ref="2038096371"/>' \
                b'    <nd ref="2038096398"/>' \
                b'    <nd ref="2038096424"/>' \
                b'    <nd ref="2038096426"/>' \
                b'    <nd ref="2038096420"/>' \
                b'    <nd ref="2038096381"/>' \
                b'    <nd ref="2038096349"/>' \
                b'    <nd ref="2038096355"/>' \
                b'    <nd ref="2038096342"/>' \
                b'    <nd ref="2038096339"/>' \
                b'    <nd ref="2038096333"/>' \
                b'    <nd ref="2038096325"/>' \
                b'    <nd ref="2038096319"/>' \
                b'    <nd ref="2038096305"/>' \
                b'    <nd ref="2038096299"/>' \
                b'    <nd ref="2038096289"/>' \
                b'    <nd ref="2038096278"/>' \
                b'    <nd ref="2038096272"/>' \
                b'    <nd ref="2038096255"/>' \
                b'    <nd ref="2038096244"/>' \
                b'    <nd ref="2038096242"/>' \
                b'    <nd ref="2038096237"/>' \
                b'    <nd ref="2038096240"/>' \
                b'    <nd ref="2038096246"/>' \
                b'    <nd ref="2038096248"/>' \
                b'    <nd ref="2038096252"/>' \
                b'    <nd ref="2038096250"/>' \
                b'    <nd ref="2038096257"/>' \
                b'    <nd ref="2038096264"/>' \
                b'    <nd ref="2038096266"/>' \
                b'    <nd ref="2038096268"/>' \
                b'    <nd ref="2038096270"/>' \
                b'    <nd ref="2038096274"/>' \
                b'    <nd ref="2038096276"/>' \
                b'    <nd ref="2038096282"/>' \
                b'    <nd ref="5924318399"/>' \
                b'    <nd ref="2038096284"/>' \
                b'    <nd ref="2038096286"/>' \
                b'    <nd ref="2038096292"/>' \
                b'    <nd ref="2038096295"/>' \
                b'    <nd ref="2038096303"/>' \
                b'    <nd ref="2038096306"/>' \
                b'    <nd ref="2038096308"/>' \
                b'    <nd ref="2038096309"/>' \
                b'    <nd ref="2038096310"/>' \
                b'    <nd ref="2038096311"/>' \
                b'    <nd ref="2038096313"/>' \
                b'    <nd ref="2038096316"/>' \
                b'    <nd ref="2038096322"/>' \
                b'    <nd ref="2038096328"/>' \
                b'    <nd ref="2038096336"/>' \
                b'    <nd ref="2038096352"/>' \
                b'    <nd ref="2038096401"/>' \
                b'    <nd ref="2038096433"/>' \
                b'    <nd ref="2038096435"/>' \
                b'    <nd ref="2038096438"/>' \
                b'    <nd ref="2038096450"/>' \
                b'    <nd ref="2038096456"/>' \
                b'    <nd ref="2038096466"/>' \
                b'    <nd ref="2038096463"/>' \
                b'    <nd ref="2038096475"/>' \
                b'    <nd ref="2038096485"/>' \
                b'    <nd ref="2038096509"/>' \
                b'    <nd ref="2038096497"/>' \
                b'    <nd ref="2038096530"/>' \
                b'    <nd ref="2038096537"/>' \
                b'    <nd ref="2038096540"/>' \
                b'    <nd ref="2038096571"/>' \
                b'    <nd ref="2038096569"/>' \
                b'    <nd ref="2038096597"/>' \
                b'    <nd ref="2038096612"/>' \
                b'    <nd ref="2038096664"/>' \
                b'    <nd ref="2038096667"/>' \
                b'    <nd ref="2038096679"/>' \
                b'    <nd ref="2038096701"/>' \
                b'    <nd ref="2038096719"/>' \
                b'    <nd ref="2038096739"/>' \
                b'    <nd ref="2038096756"/>' \
                b'    <nd ref="2038096781"/>' \
                b'    <nd ref="2038096799"/>' \
                b'    <nd ref="2038096805"/>' \
                b'    <nd ref="2038096811"/>' \
                b'    <nd ref="2038096786"/>' \
                b'    <nd ref="2038096788"/>' \
                b'    <nd ref="2038096776"/>' \
                b'    <nd ref="2038096769"/>' \
                b'    <nd ref="2038096763"/>' \
                b'    <nd ref="2038096772"/>' \
                b'    <nd ref="2038096734"/>' \
                b'    <nd ref="2038096709"/>' \
                b'    <nd ref="2038096722"/>' \
                b'    <nd ref="2038096704"/>' \
                b'    <nd ref="2038096713"/>' \
                b'    <nd ref="2038096588"/>' \
                b'    <nd ref="2038096563"/>' \
                b'    <nd ref="2038096561"/>' \
                b'    <nd ref="2038096552"/>' \
                b'    <nd ref="2038096524"/>' \
                b'    <nd ref="2038096521"/>' \
                b'    <nd ref="2038096526"/>' \
                b'    <nd ref="2038096491"/>' \
                b'    <nd ref="2038096447"/>' \
                b'    <nd ref="2038096431"/>' \
                b'    <nd ref="2038096411"/>' \
                b'    <nd ref="2038096405"/>' \
                b'    <nd ref="2038096391"/>' \
                b'    <nd ref="2038096385"/>' \
                b'    <nd ref="2038096428"/>' \
                b'    <nd ref="2038096440"/>' \
                b'    <nd ref="2038096453"/>' \
                b'    <nd ref="2038096472"/>' \
                b'    <nd ref="2038096494"/>' \
                b'    <nd ref="2038096518"/>' \
                b'    <nd ref="2038096532"/>' \
                b'    <nd ref="2038096546"/>' \
                b'    <nd ref="2038096512"/>' \
                b'    <nd ref="2038096515"/>' \
                b'    <nd ref="2038096528"/>' \
                b'    <nd ref="2038096534"/>' \
                b'    <nd ref="2038096543"/>' \
                b'    <nd ref="2038096549"/>' \
                b'    <nd ref="2038096581"/>' \
                b'    <nd ref="2038096731"/>' \
                b'    <nd ref="2038096727"/>' \
                b'    <nd ref="2038096691"/>' \
                b'    <nd ref="2038096682"/>' \
                b'    <nd ref="2038096661"/>' \
                b'    <nd ref="2038096644"/>' \
                b'    <nd ref="2038096621"/>' \
                b'    <nd ref="2038096603"/>' \
                b'    <nd ref="2038096577"/>' \
                b'    <nd ref="2038096566"/>' \
                b'    <nd ref="2038096575"/>' \
                b'    <nd ref="2038096579"/>' \
                b'    <nd ref="2038096583"/>' \
                b'    <nd ref="2038096600"/>' \
                b'    <nd ref="2038096585"/>' \
                b'    <nd ref="2038096590"/>' \
                b'    <nd ref="2038096606"/>' \
                b'    <nd ref="2038096609"/>' \
                b'    <nd ref="2038096615"/>' \
                b'    <nd ref="2038096618"/>' \
                b'    <nd ref="2038096641"/>' \
                b'    <nd ref="2038096642"/>' \
                b'    <nd ref="2038096646"/>' \
                b'    <nd ref="2038096648"/>' \
                b'    <nd ref="2038096652"/>' \
                b'    <nd ref="2038096655"/>' \
                b'    <nd ref="2038096676"/>' \
                b'    <nd ref="2038096688"/>' \
                b'    <nd ref="2038096694"/>' \
                b'    <nd ref="2038096707"/>' \
                b'    <nd ref="2038096711"/>' \
                b'    <nd ref="2038096716"/>' \
                b'    <nd ref="2038096729"/>' \
                b'    <nd ref="2038096736"/>' \
                b'    <nd ref="2038096754"/>' \
                b'    <nd ref="2038096758"/>' \
                b'    <nd ref="2038096766"/>' \
                b'    <nd ref="2038096778"/>' \
                b'    <nd ref="2038096791"/>' \
                b'    <nd ref="2038096796"/>' \
                b'    <nd ref="2038096802"/>' \
                b'    <nd ref="2038096814"/>' \
                b'    <nd ref="2038096816"/>' \
                b'    <nd ref="2038096819"/>' \
                b'    <nd ref="2038096827"/>' \
                b'    <nd ref="2038096835"/>' \
                b'    <nd ref="2038096841"/>' \
                b'    <nd ref="2038096843"/>' \
                b'    <nd ref="2038096862"/>' \
                b'    <nd ref="2038096875"/>' \
                b'    <nd ref="2038096859"/>' \
                b'    <nd ref="2038096856"/>' \
                b'    <nd ref="2038096847"/>' \
                b'    <nd ref="2038096845"/>' \
                b'    <nd ref="2038096849"/>' \
                b'    <nd ref="2038096888"/>' \
                b'    <nd ref="2038096897"/>' \
                b'    <nd ref="2038096902"/>' \
                b'    <nd ref="2038096905"/>' \
                b'    <nd ref="2038096908"/>' \
                b'    <nd ref="2038096911"/>' \
                b'    <nd ref="2038096913"/>' \
                b'    <nd ref="2038096915"/>' \
                b'    <nd ref="2038096917"/>' \
                b'    <nd ref="2038096920"/>' \
                b'    <nd ref="2038096923"/>' \
                b'    <nd ref="2038096926"/>' \
                b'    <nd ref="2038096929"/>' \
                b'    <nd ref="2038096932"/>' \
                b'    <nd ref="2038096935"/>' \
                b'    <nd ref="2038096938"/>' \
                b'    <nd ref="2038096953"/>' \
                b'    <nd ref="2038096950"/>' \
                b'    <nd ref="2038096944"/>' \
                b'    <nd ref="2038096941"/>' \
                b'    <nd ref="2038096947"/>' \
                b'    <nd ref="2038096956"/>' \
                b'    <nd ref="2038096960"/>' \
                b'    <nd ref="2038096962"/>' \
                b'    <nd ref="2038096965"/>' \
                b'    <nd ref="2038096968"/>' \
                b'    <nd ref="2038096999"/>' \
                b'    <nd ref="2038097008"/>' \
                b'    <nd ref="2038097060"/>' \
                b'    <nd ref="2038097071"/>' \
                b'    <nd ref="2038097067"/>' \
                b'    <nd ref="2038097073"/>' \
                b'    <nd ref="2038097076"/>' \
                b'    <nd ref="2038097057"/>' \
                b'    <nd ref="2038097051"/>' \
                b'    <nd ref="2038097054"/>' \
                b'    <nd ref="2038097063"/>' \
                b'    <nd ref="2038097078"/>' \
                b'    <nd ref="3363121455"/>' \
                b'    <nd ref="2038097080"/>' \
                b'    <nd ref="2038097082"/>' \
                b'    <nd ref="2038097084"/>' \
                b'    <nd ref="2038097091"/>' \
                b'    <nd ref="2038097094"/>' \
                b'    <nd ref="2038097145"/>' \
                b'    <nd ref="2038097118"/>' \
                b'    <nd ref="2038097166"/>' \
                b'    <nd ref="2038097170"/>' \
                b'    <nd ref="2038097179"/>' \
                b'    <nd ref="2038097162"/>' \
                b'    <nd ref="2038097174"/>' \
                b'    <nd ref="2038097183"/>' \
                b'    <nd ref="2038097195"/>' \
                b'    <nd ref="2295006590"/>' \
                b'    <nd ref="2038097246"/>' \
                b'    <nd ref="2038097261"/>' \
                b'    <nd ref="2038097275"/>' \
                b'    <nd ref="2038097306"/>' \
                b'    <nd ref="2038097309"/>' \
                b'    <nd ref="2038097315"/>' \
                b'    <nd ref="2038097319"/>' \
                b'    <nd ref="2038097322"/>' \
                b'    <nd ref="2038097328"/>' \
                b'    <nd ref="2038097331"/>' \
                b'    <nd ref="2038097334"/>' \
                b'    <nd ref="2038097336"/>' \
                b'    <nd ref="2038097357"/>' \
                b'    <nd ref="2038097375"/>' \
                b'    <nd ref="2038097388"/>' \
                b'    <nd ref="2038097400"/>' \
                b'    <nd ref="2038097404"/>' \
                b'    <nd ref="2038097382"/>' \
                b'    <nd ref="2038097379"/>' \
                b'    <nd ref="2038097362"/>' \
                b'    <nd ref="2038097347"/>' \
                b'    <nd ref="2038097340"/>' \
                b'    <nd ref="3354754671"/>' \
                b'    <nd ref="2038097338"/>' \
                b'    <nd ref="2038097312"/>' \
                b'    <nd ref="2057191701"/>' \
                b'    <nd ref="2038097266"/>' \
                b'    <nd ref="2038097272"/>' \
                b'    <nd ref="3561942839"/>' \
                b'    <nd ref="2038097278"/>' \
                b'    <nd ref="2038097269"/>' \
                b'    <nd ref="2038097257"/>' \
                b'    <nd ref="2038097254"/>' \
                b'    <nd ref="2038097238"/>' \
                b'    <nd ref="2038097229"/>' \
                b'    <nd ref="2038097219"/>' \
                b'    <nd ref="2038097234"/>' \
                b'    <nd ref="2038097222"/>' \
                b'    <nd ref="2038097214"/>' \
                b'    <nd ref="2038097216"/>' \
                b'    <nd ref="2038097211"/>' \
                b'    <nd ref="2038097199"/>' \
                b'    <nd ref="2038097225"/>' \
                b'    <nd ref="2038097259"/>' \
                b'    <nd ref="2038097264"/>' \
                b'    <nd ref="2038097294"/>' \
                b'    <nd ref="2038097300"/>' \
                b'    <nd ref="2038097303"/>' \
                b'    <nd ref="2038097325"/>' \
                b'    <nd ref="2038097344"/>' \
                b'    <nd ref="2038097350"/>' \
                b'    <nd ref="2038097353"/>' \
                b'    <nd ref="2038097366"/>' \
                b'    <nd ref="2038097369"/>' \
                b'    <nd ref="2038097385"/>' \
                b'    <nd ref="2038097396"/>' \
                b'    <nd ref="2038097393"/>' \
                b'    <nd ref="2038097420"/>' \
                b'    <nd ref="2038097408"/>' \
                b'    <nd ref="2038097436"/>' \
                b'    <nd ref="2038097440"/>' \
                b'    <nd ref="2038097447"/>' \
                b'    <nd ref="2038097454"/>' \
                b'    <nd ref="3998599660"/>' \
                b'    <nd ref="2038097448"/>' \
                b'    <nd ref="2038097547"/>' \
                b'    <nd ref="2038097539"/>' \
                b'    <nd ref="2038097514"/>' \
                b'    <nd ref="2038097517"/>' \
                b'    <nd ref="2038097474"/>' \
                b'    <nd ref="2038097470"/>' \
                b'    <nd ref="2038097553"/>' \
                b'    <nd ref="2038097608"/>' \
                b'    <nd ref="2038097643"/>' \
                b'    <nd ref="2038097655"/>' \
                b'    <nd ref="2038097674"/>' \
                b'    <nd ref="2038097687"/>' \
                b'    <nd ref="2038097696"/>' \
                b'    <nd ref="2038097700"/>' \
                b'    <nd ref="2038097716"/>' \
                b'    <nd ref="2038097733"/>' \
                b'    <nd ref="2038097745"/>' \
                b'    <nd ref="2038097767"/>' \
                b'    <nd ref="2038097851"/>' \
                b'    <nd ref="2038097855"/>' \
                b'    <nd ref="2038097869"/>' \
                b'    <nd ref="2038097866"/>' \
                b'    <nd ref="2038097913"/>' \
                b'    <nd ref="2038097907"/>' \
                b'    <nd ref="2038097999"/>' \
                b'    <nd ref="2038097996"/>' \
                b'    <nd ref="2038097990"/>' \
                b'    <nd ref="2038097941"/>' \
                b'    <nd ref="2038097922"/>' \
                b'    <nd ref="2038097969"/>' \
                b'    <nd ref="2038097984"/>' \
                b'    <nd ref="2038097903"/>' \
                b'    <nd ref="2038097901"/>' \
                b'    <nd ref="2038097888"/>' \
                b'    <nd ref="2038097884"/>' \
                b'    <nd ref="2038097881"/>' \
                b'    <nd ref="2038097878"/>' \
                b'    <nd ref="2038097875"/>' \
                b'    <nd ref="2038097872"/>' \
                b'    <nd ref="2038097862"/>' \
                b'    <nd ref="2038097859"/>' \
                b'    <nd ref="2038097847"/>' \
                b'    <nd ref="2038097842"/>' \
                b'    <nd ref="2038097837"/>' \
                b'    <nd ref="2038097828"/>' \
                b'    <nd ref="2038097825"/>' \
                b'    <nd ref="2038097822"/>' \
                b'    <nd ref="2038097819"/>' \
                b'    <nd ref="2038097816"/>' \
                b'    <nd ref="2038097813"/>' \
                b'    <nd ref="2038097810"/>' \
                b'    <nd ref="2038097802"/>' \
                b'    <nd ref="2038097796"/>' \
                b'    <nd ref="2038097778"/>' \
                b'    <nd ref="2038097761"/>' \
                b'    <nd ref="2038097758"/>' \
                b'    <nd ref="2038097751"/>' \
                b'    <nd ref="2038097748"/>' \
                b'    <nd ref="2038097742"/>' \
                b'    <nd ref="2038097719"/>' \
                b'    <nd ref="2038097705"/>' \
                b'    <nd ref="2038097702"/>' \
                b'    <nd ref="2038097710"/>' \
                b'    <nd ref="2038097729"/>' \
                b'    <nd ref="2038097725"/>' \
                b'    <nd ref="2038097722"/>' \
                b'    <nd ref="2038097713"/>' \
                b'    <nd ref="3164883859"/>' \
                b'    <nd ref="2038097739"/>' \
                b'    <nd ref="2038097754"/>' \
                b'    <nd ref="2038097792"/>' \
                b'    <nd ref="3165578288"/>' \
                b'    <nd ref="2038097831"/>' \
                b'    <nd ref="2038097891"/>' \
                b'    <nd ref="2038098017"/>' \
                b'    <nd ref="2038098011"/>' \
                b'    <nd ref="2038098020"/>' \
                b'    <nd ref="2038098015"/>' \
                b'    <nd ref="2038098013"/>' \
                b'    <nd ref="2038098009"/>' \
                b'    <nd ref="2038098007"/>' \
                b'    <nd ref="2038098005"/>' \
                b'    <nd ref="2038098003"/>' \
                b'    <nd ref="2038097993"/>' \
                b'    <nd ref="2038097971"/>' \
                b'    <nd ref="2038097958"/>' \
                b'    <nd ref="2038097937"/>' \
                b'    <nd ref="3008897776"/>' \
                b'    <nd ref="2038097919"/>' \
                b'    <nd ref="2038097909"/>' \
                b'    <nd ref="2038097975"/>' \
                b'    <nd ref="2038097973"/>' \
                b'    <nd ref="2038097964"/>' \
                b'    <nd ref="2038097944"/>' \
                b'    <nd ref="2038097947"/>' \
                b'    <nd ref="2038097953"/>' \
                b'    <nd ref="2038097961"/>' \
                b'    <nd ref="2038097978"/>' \
                b'    <nd ref="2038097987"/>' \
                b'    <nd ref="2038097981"/>' \
                b'    <nd ref="2038097967"/>' \
                b'    <nd ref="2038097950"/>' \
                b'    <nd ref="2038097916"/>' \
                b'    <nd ref="2038097905"/>' \
                b'    <nd ref="2038097899"/>' \
                b'    <nd ref="2038097897"/>' \
                b'    <nd ref="2038097894"/>' \
                b'    <nd ref="2038097834"/>' \
                b'    <nd ref="2038097806"/>' \
                b'    <nd ref="2038097799"/>' \
                b'    <nd ref="2038097782"/>' \
                b'    <nd ref="2038097780"/>' \
                b'    <nd ref="2038097770"/>' \
                b'    <nd ref="2038097773"/>' \
                b'    <nd ref="2038097776"/>' \
                b'    <nd ref="2038097764"/>' \
                b'    <nd ref="2038097736"/>' \
                b'    <nd ref="2038097707"/>' \
                b'    <nd ref="2038097698"/>' \
                b'    <nd ref="2038097693"/>' \
                b'    <nd ref="2038097690"/>' \
                b'    <nd ref="2038097683"/>' \
                b'    <nd ref="2038097680"/>' \
                b'    <nd ref="2038097677"/>' \
                b'    <nd ref="2038097671"/>' \
                b'    <nd ref="2038097668"/>' \
                b'    <nd ref="2038097666"/>' \
                b'    <nd ref="2038097652"/>' \
                b'    <nd ref="2038097649"/>' \
                b'    <nd ref="2038097646"/>' \
                b'    <nd ref="2038097640"/>' \
                b'    <nd ref="2038097637"/>' \
                b'    <nd ref="2038097634"/>' \
                b'    <nd ref="2038097630"/>' \
                b'    <nd ref="2038097621"/>' \
                b'    <nd ref="2038097618"/>' \
                b'    <nd ref="2038097627"/>' \
                b'    <nd ref="2038097624"/>' \
                b'    <nd ref="2038097614"/>' \
                b'    <nd ref="2038097611"/>' \
                b'    <nd ref="2038097601"/>' \
                b'    <nd ref="2038097595"/>' \
                b'    <nd ref="2038097566"/>' \
                b'    <nd ref="2038097500"/>' \
                b'    <nd ref="2038097497"/>' \
                b'    <nd ref="2038097483"/>' \
                b'    <nd ref="2038097481"/>' \
                b'    <nd ref="2038097462"/>' \
                b'    <nd ref="2038097460"/>' \
                b'    <nd ref="2038097464"/>' \
                b'    <nd ref="2038097485"/>' \
                b'    <nd ref="2038097490"/>' \
                b'    <nd ref="2038097488"/>' \
                b'    <nd ref="2038097520"/>' \
                b'    <nd ref="2038097557"/>' \
                b'    <nd ref="2038097574"/>' \
                b'    <nd ref="2038097592"/>' \
                b'    <nd ref="2038097563"/>' \
                b'    <nd ref="2038097545"/>' \
                b'    <nd ref="2038097458"/>' \
                b'    <nd ref="2038097451"/>' \
                b'    <nd ref="2038097450"/>' \
                b'    <nd ref="2038097452"/>' \
                b'    <nd ref="2038097456"/>' \
                b'    <nd ref="2038097449"/>' \
                b'    <nd ref="2038097438"/>' \
                b'    <nd ref="2038097442"/>' \
                b'    <nd ref="2038097444"/>' \
                b'    <nd ref="2038097446"/>' \
                b'    <nd ref="2038097424"/>' \
                b'    <nd ref="2038097417"/>' \
                b'    <nd ref="2038097411"/>' \
                b'    <nd ref="2038097414"/>' \
                b'    <nd ref="2038097422"/>' \
                b'    <nd ref="2038097433"/>' \
                b'    <nd ref="2038097342"/>' \
                b'    <nd ref="2038097250"/>' \
                b'    <nd ref="3854890106"/>' \
                b'    <nd ref="2038097242"/>' \
                b'    <nd ref="2038097158"/>' \
                b'    <nd ref="2038097148"/>' \
                b'    <nd ref="2038097155"/>' \
                b'    <nd ref="2038097152"/>' \
                b'    <nd ref="2038097137"/>' \
                b'    <nd ref="2038097116"/>' \
                b'    <nd ref="2038097112"/>' \
                b'    <nd ref="2038097109"/>' \
                b'    <nd ref="2038097114"/>' \
                b'    <nd ref="2038097106"/>' \
                b'    <nd ref="2038097100"/>' \
                b'    <nd ref="2038097088"/>' \
                b'    <nd ref="2038097086"/>' \
                b'    <nd ref="2038097103"/>' \
                b'    <nd ref="2038097097"/>' \
                b'    <nd ref="2038097141"/>' \
                b'    <nd ref="2038097120"/>' \
                b'    <tag k="boundary" v="administrative"/>' \
                b'  </way>' \
                b'<relation id="2603218" version="10" timestamp="2016-12-01T06:33:32Z" changeset="44077720" uid="339581" user="nyuriks">' \
                b'    <member type="relation" ref="2613088" role="subarea"/>' \
                b'    <member type="way" ref="193299964" role="outer"/>' \
                b'    <member type="way" ref="1" role="outer"/>' \
                b'    <member type="node" ref="31345520" role="admin_centre"/>' \
                b'    <tag k="admin_level" v="7"/>' \
                b'    <tag k="boundary" v="administrative"/>' \
                b'    <tag k="name" v="Szczecinek"/>' \
                b'    <tag k="name:de" v="Neustettin"/>' \
                b'    <tag k="name:prefix" v="gmina miejska"/>' \
                b'    <tag k="population" v="40620"/>' \
                b'    <tag k="source" v="Pa\xc5\x84stwowy Rejestr Granic"/>' \
                b'    <tag k="source:population" v="http://stat.gov.pl/obszary-tematyczne/ludnosc/ludnosc/ludnosc-stan-i-struktura-ludnosci-oraz-ruch-naturalny-w-przekroju-terytorialnym-w-2013-r-stan-w-dniu-31-xii,6,12.html"/>' \
                b'    <tag k="teryt:terc" v="3215011"/>' \
                b'    <tag k="type" v="boundary"/>' \
                b'    <tag k="wikidata" v="Q848999"/>' \
                b'    <tag k="wikipedia" v="pl:Szczecinek"/>' \
                b'  </relation>' \
                b'' \
                b'</osm>' \
                b''

        ret = utils.osmshapedb.get_geometries(input)
        self.assertTrue('relation:2603218' in ret.geometries.keys())
