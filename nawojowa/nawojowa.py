import itertools
import json
import lxml.etree as ET


import requests
from bs4 import BeautifulSoup
from overpy import Overpass


def get_number(housenumber):
    res = requests.post(
        "http://hosting18.vpo9.iat.pl/adres1.php",
        data={"op1": housenumber.replace(" ", ""), "Submit": "szukaj"},
    )
    res.encoding = "UTF-8"
    soup = BeautifulSoup(res.text)
    text = soup.find("div", attrs={"id": "adres"}).find("span").text
    if text.startswith("ul. "):
        text = text[4:]
    try:
        street, number = text.rsplit(" ", 1)
        return {
            "addr:street": street,
            "addr:housenumber": number,
            "addr:city": "Nawojowa",
        }
    except ValueError:
        return {}


def get():
    res = Overpass().query(
        """[out:xml][timeout:300];
area["boundary"="administrative"]["wikidata"="Q6982957"]->.granica;
(
	node(area.granica)["addr:housenumber"];
	way(area.granica)["addr:housenumber"];
);
out meta;
>>;
out meta;"""
    )
    rv = dict(
        (x, get_number(x))
        for x in (
            x.tags["addr:housenumber"]
            for x in itertools.chain(res.get_nodes(), res.get_ways())
            if "addr:housenumber" in x.tags
        )
    )
    with open("nawojowa.json", "w+") as f:
        json.dump(rv, f)


def main():
    res = requests.get(
        "https://overpass-api.de/api/interpreter?data=%5Bout%3Axml%5D%5Btimeout%3A300%5D%3B%0Aarea%5B%22boundary%22%3D%22administrative%22%5D%5B%22wikidata%22%3D%22Q6982957%22%5D-%3E.granica%3B%0A%28%0A%09node%28area.granica%29%5B%22addr%3Ahousenumber%22%5D%3B%0A%09way%28area.granica%29%5B%22addr%3Ahousenumber%22%5D%3B%20%20%20%20%0A%29%3B%0Aout%20meta%20center%3B%0A%3E%3E%3B%0Aout%20meta%3B"
    )

    id_gen = itertools.count(start=-1, step=-1)

    with open("nawojowa.json", "r") as f:
        mapping = json.load(f)

    et = ET.fromstring(res.text.encode("utf-8"))
    nodes_to_add = []
    for node in itertools.chain(et.iter("node"), et.iter("way")):
        housenumber = node.find("tag[@k='addr:housenumber']")
        new = None
        if housenumber is not None:
            new = mapping.get(housenumber.get("v"))
        try:
            if new and new["addr:street"] and new["addr:housenumber"]:
                new_node = ET.Element("node")
                nodes_to_add.append(new_node)
                new_node.set("id", str(next(id_gen)))
                if node.get("lat"):
                    new_node.set("lat", str(float(node.get("lat")) + 0.0000075))
                    new_node.set("lon", str(float(node.get("lon")) + 0.000025))
                else:
                    center = node.find("center")
                    new_node.set("lat", str(float(center.get("lat"))))
                    new_node.set("lon", str(float(center.get("lon"))))

                for i in (
                    "addr:place",
                    "addr:housenumber",
                    "source:addr",
                    "addr:postcode",
                ):
                    found = node.find("tag[@k='{0}']".format(i))
                    if found is not None:
                        tag = ET.SubElement(new_node, "tag")
                        tag.set("k", i)
                        tag.set("v", found.get("v"))
                node.find("tag[@k='addr:place']").set("k", "addr:city")
                node.find("tag[@k='addr:housenumber']").set(
                    "v", new["addr:housenumber"]
                )
                node.set("action", "modify")
                source = node.find("tag[@k='source:addr']")
                if source is None:
                    source = ET.SubElement(node, "tag")
                    source.set("k", "source:addr")
                source.set("v", "http://hosting18.vpo9.iat.pl/")
                street = ET.SubElement(node, "tag")
                street.set("k", "addr:street")
                street.set("v", new["addr:street"])
        except:
            pass
    for i in nodes_to_add:
        et.append(i)
    with open("output.osm", "wb+") as f:
        f.write(ET.tostring(et, encoding="utf-8", method="xml"))


if __name__ == "__main__":
    main()
