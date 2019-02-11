#!/usr/bin/env python3.7

import argparse
import io
import logging
import lxml
import lxml.etree

from converter import osm_to_json
from merger import Merger, OsmAddress


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Merge osm file with address nodes with buildings in specified area as terc code"""
    )
    parser.add_argument('--addr', help='File with address nodes to merge', required=True)
    parser.add_argument('--building', help='File with buildings to merge', required=True)
    parser.add_argument('--output', help='output file with merged data (default: result.osm)')
    parser.add_argument('--terc', help='Teryt TERC code for area processed')
    parser.add_argument('--log-level', help='Set logging level (debug=10, info=20, warning=30, error=40, critical=50), default: 20', dest='log_level', default=20, type=int)

    args = parser.parse_args()

    log_stderr = logging.StreamHandler()
    log_stderr.setLevel(args.log_level)
    logIO = io.StringIO()
    logging.basicConfig(level=10, handlers=[log_stderr, logging.StreamHandler(logIO)])

    if args.output:
        output = open(args.output, "wb")
    else:
        parts = args.input.rsplit('.', 1)
        parts[0] += '-merged'
        output = open('.'.join(parts), "xb")
        print("Output filename: %s" % ('.'.join(parts),))

    data = [OsmAddress.from_soup(x) for x in osm_to_json(lxml.etree.parse(open(args.addr)))['elements']]

    addr = osm_to_json(open(args.building))

    m = Merger(data, addr, args.terc)
    for i in data:
        m._do_merge_create_point(i)
    m.create_index()
    m.merge_addresses()
    output.write(m.get_incremental_result(logIO))


if __name__ == '__main__':
    main()
