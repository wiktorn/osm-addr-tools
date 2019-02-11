from converters import teryt
from utils import mapping
import re


shorts = re.compile(r"(\w+\. )")


def main():
    ulic = teryt.UlicCache().get_cache()
    names_with_dots = []
    objects = []
    for (symul, names) in mapping.get_inconsistent_symul():
        ulic_entry = ulic.get(symul)
        ulic_name = ulic_entry.nazwa if ulic_entry else 'N/A'
        ulic_name = ulic_name[len("Ulica "):] if "ULICA" in ulic_name.upper() else ulic_name
        ulic_name = mapping.mapstreet(ulic_name, '')
        most_popular_osm = max(names.items(), key=lambda x: x[1])[0]
        if ulic_name == most_popular_osm:
            pass
        elif ulic_name in most_popular_osm:
            ulic_name = most_popular_osm
        elif shorts.sub('', ulic_name).replace('  ', ' ') in most_popular_osm:
            ulic_name = most_popular_osm
        if '.' not in ulic_name:
            objects.append("""// TERYT: {teryt} OSM: {osm_names}
      node["addr:street:sym_ul"="{symul}"]["addr:street"!="{street}"];
      way["addr:street:sym_ul"="{symul}"]["addr:street"!="{street}"];
      relation["addr:street:sym_ul"="{symul}"]["addr:street"!="{street}"];
    """.format(
                teryt=ulic_entry.nazwa if ulic_entry else 'N/A',
                osm_names=", ".join(k for k, _ in sorted(names.items(), key=lambda x: x[1], reverse=True)),
                symul=symul,
                street=ulic_name.replace("\"", "\\\"")
            ))
        if '.' in ulic_name:
            names_with_dots.append("{} {:<40s} {}".format(symul, ulic_name, ", ".join(names)))
    print("""
[out:json][timeout:25];
// gather results
(
{}
);
// print results
out body;
>;
out skel qt;
""".format("".join(objects)))
    print("Names with dots:\n" + "\n".join(names_with_dots))
    print(len(names_with_dots))


if __name__ == '__main__':
    main()
