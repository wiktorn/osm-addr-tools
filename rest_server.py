import os

from flask import Flask, request, make_response as _make_response
import io
import logging

from merger import Merger, get_addresses, get_addresses_terc
from data.impa import iMPA
from converters import tools

app = Flask(__name__)


def make_response(ret, code):
    resp = _make_response(ret, code)
    resp.mimetype = "text/xml; charset=utf-8"
    return resp


def get_impa_merger(name):
    imp = iMPA(name)
    terc = imp.terc
    data = imp.get_addresses()
    s = min(map(lambda x: x.center.y, data))
    w = min(map(lambda x: x.center.x, data))
    n = max(map(lambda x: x.center.y, data))
    e = max(map(lambda x: x.center.x, data))
    addr = get_addresses(map(str, (s, w, n, e)))

    m = Merger(data, addr, terc, "%s.e-mapa.net" % name)
    m.post_func.append(m.merge_addresses)
    m.merge()
    return m


@app.route("/osm/adresy/iMPA/<name>.osm", methods=["GET"])
def differential_import(name):
    m = get_impa_merger(name)
    ret = m.get_incremental_result()

    return make_response(ret, 200)


@app.route("/osm/adresy/test.osm", methods=["GET"])
def test_exception():
    raise ValueError("message")


@app.route("/osm/adresy/iMPA_full/<name>.osm", methods=["GET"])
def full_import(name):
    m = get_impa_merger(name)
    ret = m.get_full_result()
    return make_response(ret, 200)


@app.route("/osm/adresy/merge-addr/<terc>.osm", methods=["GET"])
def merge_addr(terc):
    log_io = io.StringIO()
    logging.basicConfig(level=10, handlers=[logging.StreamHandler(log_io)])
    addr = get_addresses_terc(terc)
    m = Merger([], addr, terc, "emuia.gugik.gov.pl")
    m.create_index()
    m.merge_addresses()
    return make_response(m.get_incremental_result(log_io), 200)


@app.errorhandler(Exception)
def report_exception(e):
    app.logger.error(
        "{0}: {1}".format(request.path, e), exc_info=(type(e), e, e.__traceback__)
    )
    return make_response(
        """<?xml version='1.0' encoding='UTF-8'?>
    <osm version="0.6" generator="import adresy merger.py">
    <node id="-1" lon="19" lat="52">
        <tag k="fixme" v="%s" />
    </node>
    </osm>"""
        % repr(e),
        200,
    )


if __name__ == "__main__":
    ADMINS = ["logi-osm@vink.pl"]
    if False:
        from logging.handlers import SMTPHandler

        mail_handler = SMTPHandler(
            "127.0.0.1", "server-error@vink.pl", ADMINS, "OSM Rest-Server Failed"
        )
        mail_handler.setLevel(logging.INFO)
        app.logger.addHandler(mail_handler)

    port = os.environ.get("PORT", 5001)
    app.run(host="0.0.0.0", port=port, debug=False)
