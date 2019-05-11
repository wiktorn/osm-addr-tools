import lxml.etree
import pathlib


def generate_bbox():
    directory = pathlib.Path(__file__).parent.parent / "testdata"
    for test in sorted(directory.iterdir()):
        if test.is_dir() and (test / "osm.xml").is_file():
            with open(test / "osm.xml", "r") as f:
                tree = lxml.etree.parse(f)
                if (
                    len(tree.findall("//bounds")) == 0
                    and len(tree.findall("//way")) > 0
                ):
                    print()
                    print(test / "osm.xml")
                    for elem in tree.getroot().iterchildren():
                        if elem.tag == "way":
                            positions = [
                                (node.get("lon"), node.get("lat"))
                                for node in (
                                    tree.find(
                                        '//node[@id="{}"]'.format(node.get("ref"))
                                    )
                                    for node in elem.iterchildren("nd")
                                )
                            ]
                            print("way: {}".format(elem.get("id")))
                            print(
                                """<bounds minlat="{}" minlon="{}" maxlat="{}" maxlon="{}" />""".format(
                                    min(x[1] for x in positions),
                                    min(x[0] for x in positions),
                                    max(x[1] for x in positions),
                                    max(x[0] for x in positions),
                                )
                            )


def main():
    generate_bbox()


if __name__ == "__main__":
    main()
