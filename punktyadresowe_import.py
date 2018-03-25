#!/usr/bin/env python3.4
# -*- coding: UTF-8 -*-
#
# punktyadresowe_import.py CC-BY-NC-SA 3.0 WiktorN
#
# Based on work by Grzegorz Sapijaszko (http://wiki.openstreetmap.org/wiki/User:Gsapijaszko/punktyadresowe_import)
#
# dependencies:
# Beautiful-Soup (http://www.crummy.com/software/BeautifulSoup/)
#       pip install beautifulsoup4
#       easy_install beautifulsoup4
#       apt-get install python-beautifulsoup4
#       portmaster www/py-beautifulsoup
#
# TODO:
# - add spellchecking for street and city based on TERYT dictionaries
#       - street spellchecking - split into words and look for similar words in dictionary
#       - ideas: http://en.wikipedia.org/wiki/Levenshtein_distance , ngrams (http://en.wikipedia.org/wiki/N-gram),
#                Norvig spell-checker - http://norvig.com/spell-correct.html

import argparse
import json
import logging
from functools import partial

from data.base import convert_to_osm, AddressEncoder
from data.egeoportal import EGeoportal
from data.gisnet import GISNET
from data.gugik import GUGiK, GUGiK_GML
from data.impa import iMPA
from data.warszawaum import WarszawaUM


# stałe
# _EPSG2180 = Proj(init='epsg:2180')


def main():
    parser = argparse.ArgumentParser(
        description="Downloads data from iMPA and saves in OSM or JSON format. CC-BY-SA 3.0 @ WiktorN. Filename is "
                    "<gmina>.osm or <gmina>.json")
    parser.add_argument('--output-format', choices=['json', 'osm'],
                        help='output file format - "json" or "osm", default: osm', default="osm", dest='output_format')
    parser.add_argument('--source', choices=['impa', 'gugik', 'gugik_gml', 'gisnet', 'warszawa', 'e-geoportal'],
                        help='input source: "gugik", "impa", "gisnet" or "warszawa". Gugik, gisnet and warszawa requires'
                             ' providing teryt:terc code. gugik_gml requires to provide a filename as gmina. Defaults to'
                             ' "impa"',
                        default="impa", dest='source')
    parser.add_argument('--log-level',
                        help='Set logging level (debug=10, info=20, warning=30, error=40, critical=50), default: 20',
                        dest='log_level', default=20, type=int)
    parser.add_argument('--no-mapping', help='Disable mapping of streets and cities', dest='no_mapping', default=False,
                        action='store_const', const=True)
    parser.add_argument('--wms', help='Override WMS address with address points', dest='wms', default=None)
    parser.add_argument('--terc', help='teryt:terc code which defines area of operation', dest='terc', default=None)
    parser.add_argument('gmina', nargs='?', help='list of iMPA services to download or e-geoportal layer name')
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    if args.no_mapping:
        global mapstreet, mapcity
        mapstreet = lambda x, y: x
        mapcity = lambda x, y: x
    if args.source == "impa":
        imp_gen = partial(iMPA, wms=args.wms, terc=args.terc)
    elif args.source == "gugik":
        imp_gen = partial(GUGiK, terc=args.terc)
    elif args.source == "gisnet":
        imp_gen = partial(GISNET, terc=args.terc)
        if not args.gmina:
            raise Exception("You need to provide service name")
    elif args.source == 'warszawa':
        imp_gen = partial(WarszawaUM, terc=args.terc)
    elif args.source == 'gugik_gml':
        imp_gen = partial(GUGiK_GML)
    elif args.source == 'e-geoportal':
        imp_gen = partial(EGeoportal, terc=args.terc)
        if not args.gmina:
            raise Exception("You need to provide layer name")
    else:
        raise Exception("Source not supported")
    if args.gmina:
        # rets = parallel_execution(*map(lambda x: lambda: imp_gen(x).getAddresses(), args.gmina))
        ret = imp_gen(args.gmina).get_addresses()
        # rets = list(map(lambda x: imp_gen(x).getAddresses(), args.gmina)) # usefull for debugging
    else:
        ret = imp_gen().get_addresses()
    if args.output_format == 'json':
        write_conv_func = lambda x: json.dumps(list(x), cls=AddressEncoder)
        file_suffix = '.json'
    else:
        write_conv_func = convert_to_osm
        file_suffix = '.osm'

    if args.gmina:
        with open(args.gmina + file_suffix, "w+", encoding='utf-8') as f:
            f.write(write_conv_func(ret))
    else:
        fname = 'result.osm'
        if args.terc:
            fname = '%s.osm' % (args.terc,)
        with open(fname, 'w+', encoding='utf-8') as f:
            f.write(write_conv_func(ret))


if __name__ == '__main__':
    main()
