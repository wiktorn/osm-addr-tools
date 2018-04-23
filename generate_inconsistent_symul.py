from converters import teryt
from utils import mapping


def main():
    ulic = teryt.UlicCache().get_cache()
    names_with_dots = []
    objects = []
    for symul in mapping.get_inconsistent_symul():
        ulic_entry = ulic.get(symul)
        ulic_name = ulic_entry.nazwa if ulic_entry else 'N/A'
        if '.' not in ulic_name:
            objects.append("""
      node["addr:street:sym_ul"="{symul}"]["addr:street"!="{street}"];
      way["addr:street:sym_ul"="{symul}"]["addr:street"!="{street}"];
      relation["addr:street:sym_ul"="{symul}"]["addr:street"!="{street}"];
    """.format(
                symul=symul,
                street=(ulic_name[len("Ulica "):] if "ULICA" in ulic_name.upper() else ulic_name).replace("\"", "\\\"")
            ))
        if '.' in ulic_name:
            names_with_dots.append(ulic_name)
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


if __name__ == '__main__':
    main()