from flask import Flask, make_response as _make_response
import io
import logging
import json

from merger import Merger, get_addresses
from punktyadresowe_import import iMPA
import overpass
import utils

app = Flask(__name__)

def make_response(ret, code):
    resp = _make_response(ret, code)
    resp.mimetype ='text/xml; charset=utf-8'
    return resp

def get_IMPA_Merger(name):
    imp = iMPA(name)
    terc = imp.terc
    data = imp.getAddresses()
    s = min(map(lambda x: x.center.y, data))
    w = min(map(lambda x: x.center.x, data))
    n = max(map(lambda x: x.center.y, data))
    e = max(map(lambda x: x.center.x, data))
    addr =  get_addresses(map(str, (s, w, n, e)))

    
    m = Merger(data, addr, terc, "%s.e-mapa.net" % name)
    m.post_func.append(m.merge_addresses)
    m.merge()
    return m

@app.route("/osm/adresy/iMPA/<name>.osm", methods=["GET", ])
def differentialImport(name):
    m = get_IMPA_Merger(name)
    ret = m.get_incremental_result()
    
    return make_response(ret, 200)

@app.route("/osm/adresy/iMPA_full/<name>.osm", methods=["GET", ])
def fullImport(name):
    m = get_IMPA_Merger(name)
    ret = m.get_full_result()
    return make_response(ret, 200)


@app.route("/osm/adresy/merge-addr/<terc>.osm", methods=["GET", ])
def merge_addr(terc):
    log_io = io.StringIO()
    logging.basicConfig(level=10, handlers=[logging.StreamHandler(log_io),])
    addr = json.loads(overpass.getAddresses(terc))
    m = Merger([], addr, terc, "emuia.gugik.gov.pl")
    m._create_index()
    m.merge_addresses()
    return make_response(m.get_incremental_result(log_io), 200)

if __name__ == '__main__':
    ADMINS = ['logi-osm@vink.pl']
    if not app.debug:
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1',
                                   'server-error@vink.pl',
                                   ADMINS, 'OSM Rest-Server Failed')
        mail_handler.setLevel(logging.INFO)
        app.logger.addHandler(mail_handler)
    app.run(host='0.0.0.0', port=5001, debug=False)
