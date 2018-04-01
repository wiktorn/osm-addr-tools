# # -*- coding: UTF-8 -*-
# TODO:
# - add warning, when street exists as a part of name in sym_ul dictionary or in ULIC
import functools
import json
import logging
import os
import pickle
import tempfile
import threading
import time
from collections import namedtuple

import converters.teryt
import overpass
from .mapping_custom import addr_map

__log = logging.getLogger(__name__)

TerytUlicEntry = namedtuple('TerytUlicEntry', ['sym_ul', 'nazwa', 'cecha'])

__CECHA_MAPPING = {
    'UL.': '',
    'AL.': 'Aleja',
    'PL.': 'Plac',
    'SKWER': 'Skwer',
    'BULW.': 'Bulwar',
    'RONDO': 'Rondo',
    'PARK': 'Park',
    'RYNEK': 'Rynek',
    'SZOSA': 'Szosa',
    'DROGA': 'Droga',
    'OS.': 'Osiedle',
    'OGRÓD': 'Ogród',
    'WYB.': 'Wybrzeże',
    'INNE': ''
}


def get_dict(keyname, valuename, coexitingtags=None):
    __log.info("Updating %s data from OSM, it may take a while", keyname)
    tags = [keyname, valuename]
    if coexitingtags:
        tags.extend(coexitingtags)
    soup = json.loads(overpass.getNodesWaysWithTags(tags, 'json'))
    ret = {}
    for tag in soup['elements']:
        symul = tag['tags'][keyname]
        street = tag['tags'][valuename]
        if street:
            try:
                entry = ret[symul]
            except KeyError:
                entry = {}
                ret[symul] = entry
            try:
                entry[street] += 1
            except KeyError:
                entry[street] = 1
    # ret = dict(symul, dict(street, count))
    inconsistent = dict((x[0], x[1].keys()) for x in filter(lambda x: len(x[1]) > 1, ret.items()))
    for (symul, streetlst) in inconsistent.items():
        __log.info("Inconsitent mapping for %s = %s, values: %s", keyname, symul, ", ".join(streetlst))
    return ret


def stored_dict(fetcher, filename):
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
    except IOError:
        __log.debug("Can't read a file: %s, starting with a new one", filename, exc_info=True)
        data = {
            'time': 0
        }
    if data['time'] < time.time() - 21 * 24 * 60 * 60:
        try:
            new = fetcher()
        except Exception as e:
            __log.warning("Failed to download dictionary: %s", filename, exc_info=True)
            __log.warning("Using dictionary from: %s", time.asctime(time.localtime(data['time'])))
            return data['dct']
        data['dct'] = new
        data['time'] = time.time()
        try:
            with open(filename, "w+b") as f:
                pickle.dump(data, f)
        except:
            __log.debug("Can't write file: %s", filename, exc_info=True)
    return data['dct']


__DB_OSM_TERYT_SYMUL = os.path.join(tempfile.gettempdir(), 'osm_teryt_symul_v2.db')
__DB_OSM_TERYT_SIMC = os.path.join(tempfile.gettempdir(), 'osm_teryt_simc_v2.db')
__DB_OSM_SIMC_POSTCODE = os.path.join(tempfile.gettempdir(), 'osm_teryt_simc_postcode_v1.db')
__mapping_symul = {}
__mapping_simc = {}
__teryt_ulic = {}
__mapping_simc_postcode = {}

__init_lock = threading.Lock()
__is_initialized = False


def __init():
    global __is_initialized, __init_lock, __mapping_symul, __mapping_simc, __teryt_ulic, __mapping_simc_postcode
    if not __is_initialized:
        with __init_lock:
            if not __is_initialized:
                __mapping_symul = stored_dict(lambda: get_dict('addr:street:sym_ul', 'addr:street'),
                                              __DB_OSM_TERYT_SYMUL)
                __mapping_simc = stored_dict(lambda: get_dict('teryt:simc', 'name', ['place']),
                                             __DB_OSM_TERYT_SIMC)  # check based on place names, not addresses
                __teryt_ulic = converters.teryt.UlicCache().get_cache()
                __mapping_simc_postcode = stored_dict(lambda: get_dict('teryt:simc', 'addr:postcode', ['place', ]),
                                                      __DB_OSM_SIMC_POSTCODE)
                __is_initialized = True


@functools.lru_cache(maxsize=None)
def mapstreet(strname, symul):
    __init()
    teryt_entry = __teryt_ulic.get(symul)

    def check_and_add_cecha(street):
        teryt_nazwa = ""
        if teryt_entry and teryt_entry.cecha:
            teryt_nazwa = teryt_entry.nazwa[5:].strip() if \
                teryt_entry.nazwa.startswith('Ulica') and teryt_entry.cecha.upper() == 'ULICA' \
                else teryt_entry.nazwa
            if street.upper().startswith(teryt_entry.cecha_orig.upper()):
                # remove short version cecha and prepand full version
                street = "%s %s" % (teryt_entry.cecha,
                                    street[len(teryt_entry.cecha_orig):].strip())
                street = street.strip()
            if street.upper().startswith('UL.') and teryt_entry.cecha_orig.upper() == 'UL.':
                street = street[3:].strip()
            if street.upper().startswith('ULICA') and teryt_entry.cecha.upper() == 'ULICA':
                street = street[5:].strip()
            if not street.upper().startswith(teryt_entry.cecha.upper()) and \
                    not street.upper().startswith(__CECHA_MAPPING.get(teryt_entry.cecha_orig, '').upper()):
                __log.debug("Adding TERYT.CECHA=%s to street=%s (addr:street:sym_ul=%s)" % (
                    __CECHA_MAPPING.get(teryt_entry.cecha_orig, ''), street, symul))
                return "%s %s" % (__CECHA_MAPPING.get(teryt_entry.cecha_orig, ''), street)
        else:
            if street.upper().startswith('AL. '):
                return 'Aleja ' + street[4:]
            if street.upper().startswith('PL. '):
                return 'Plac ' + street[4:]
            if street.upper().startswith('UL. '):
                return street[4:]
        return max(street, teryt_nazwa, key=lambda x: len(x))

    try:
        strname = strname.replace('„', '"').replace('”', '"')
        ret = check_and_add_cecha(addr_map[strname])
        log_level = logging.INFO
        if max(strname.split(' '), key=len) in ret:
            # if longest part of strname is in ret, then lower the log message level
            log_level = logging.DEBUG
        __log.log(log_level, "mapping street %s -> %s, TERYT: %s (addr:street:sym_ul=%s) " % (strname,
                                                                                              ret,
                                                                                              teryt_entry.nazwa if
                                                                                              teryt_entry else 'N/A',
                                                                                              symul
                                                                                              )
                  )
        return ret
    except KeyError:
        try:
            ret = __mapping_symul[symul]
            if len(ret) > 1:
                __log.info("Inconsitent mapping for addr:street:sym_ul = %s. Original value: %s, TERYT: %s, "
                           "OSM values: %s. Leaving original value.",
                           symul,
                           strname,
                           teryt_entry.nazwa if teryt_entry else 'N/A',
                           ", ".join(ret))
                return strname
            ret = check_and_add_cecha(next(iter(ret.keys())))  # check and add for first and only key
            if ret != strname:
                log_level = logging.INFO
                if max(strname.split(' '), key=len) in ret:
                    log_level = logging.DEBUG
                __log.log(log_level, "mapping street %s -> %s, TERYT: %s (addr:street:sym_ul=%s) " % (
                    strname,
                    ret,
                    teryt_entry.nazwa if teryt_entry else 'N/A',
                    symul
                )
                          )
            return ret
        except KeyError:
            return check_and_add_cecha(strname)


@functools.lru_cache(maxsize=None)
def mapcity(cityname, simc):
    __init()
    try:
        ret = __mapping_simc[simc]
        if len(ret) > 1:
            __log.info("Inconsitent mapping for addr:city:simc = %s. Original value: %s, OSM values: %s. "
                       "Leaving original value.", simc, cityname, ", ".join(ret))
            return cityname
        ret = next(iter(ret.keys()))  # take first (and the only one) key
        if ret != cityname:
            __log.info("mapping city %s -> %s (addr:city:simc=%s)" % (cityname, ret, simc))
        return ret
    except KeyError:
        return cityname.replace(' - ', '-')


import re

__POSTCODE = re.compile('^[0-9]{2}-[0-9]{3}$')


@functools.lru_cache(maxsize=None)
def mappostcode(postcode, simc):
    __init()
    if postcode:
        return postcode
    try:
        ret = __mapping_simc_postcode[simc]
        if len(ret) > 1:
            __log.info("Inconsistent mapping for teryt:simc = %s to postcode. OSM values: %s", simc, ", ".join(ret))
            return postcode
        ret = next(iter(ret.keys()))  # take first (and the only one) key
        if not __POSTCODE.match(ret):
            __log.info("Postcode for simc: %s doesn't look good: %s", simc, ret)
            return postcode
        if ret != postcode:
            __log.info("Adding postcode %s for teryt:simc=%s", ret, simc)
        return ret
    except KeyError:
        return postcode


def main():
    logging.basicConfig(level=10)
    print(mapstreet('Głowackiego', 'x'))
    print(mapcity('Kostrzyń', 'x'))


if __name__ == '__main__':
    main()
