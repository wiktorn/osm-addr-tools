#!/usr/bin/env python3.4

from bs4 import BeautifulSoup
import sys


def getTag(node, tag):
    n = node.find("tag", k=tag)
    if n:
        return n.get("v")
    else:
        return None


def makeEntry(soup):
    return {
        "soup": soup,
        "addr:city": getTag(soup, "addr:city"),
        "addr:place": getTag(soup, "addr:place"),
        "addr:street": getTag(soup, "addr:street"),
        "addr:housenumber": getTag(soup, "addr:housenumber"),
    }


def makeKey(dct):
    return (
        dct.get("addr:city"),
        dct.get("addr:place"),
        dct.get("addr:street"),
        dct.get("addr:housenumber"),
    )


def markDuplicate(soup, lst):
    print("marking dups")
    value = "Duplicate (first)"
    while lst:
        dct = lst.pop()
        node = dct["soup"]
        nt = soup.new_tag("tag", k="fixme", v=value)
        node.append(nt)
        value = "Duplicate"


def main():
    with open(sys.argv[1]) as f:
        soup = BeautifulSoup(f)

        ret = {}
        for i in soup.osm.find_all(
            lambda x: int(x.get("id", 1)) < 0 and x.find("tag", k="addr:housenumber"),
            recursive=False,
        ):
            entry = makeEntry(i)
            key = makeKey(entry)
            try:
                lst = ret[key]
            except KeyError:
                lst = []
                ret[key] = lst
            lst.append(entry)

        for i in filter(lambda x: len(x) > 1, ret.values()):
            markDuplicate(soup, i)

    with open("output.osm", "w+") as f:
        f.write(soup.prettify())


if __name__ == "__main__":
    main()
