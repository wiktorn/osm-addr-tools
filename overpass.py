import io
from urllib.parse import urlencode
import logging

import math
import requests
import tqdm
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


__log = logging.getLogger(__name__)


def requests_retry_session(
    retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


__overpassurl = "http://overpass.osm.rambler.ru/cgi/interpreter"
__overpassurl = "http://overpass-api.de/api/interpreter"
__overpassurl = "http://api.openstreetmap.fr/oapi/interpreter/"
__overpassurl = "http://osm-cdn.vink.pl/api/interpreter"


def get_url_for_query(qry: str):
    return (
        __overpassurl
        + "?"
        + urlencode({"data": qry.replace("\t", "").replace("\n", "")})
    )


def query(qry, desc="") -> bytes:
    # TODO - check if the query succeeded
    __log.debug("Query %s , server: %s", qry, __overpassurl)

    r = requests_retry_session().get(get_url_for_query(qry), timeout=180, stream=True)
    total_size = int(r.headers.get("content-length", 0))
    block_size = 128 * 1024
    wrote = 0
    raw_data = bytearray()
    if desc:
        desc = "(" + desc + ")"
    with tqdm.tqdm(
        total=math.ceil(total_size // block_size),
        unit="B",
        unit_scale=True,
        desc="Downloading from Overpass{}".format(desc),
    ) as progressbar:
        for data in r.iter_content(block_size):
            wrote += len(data)
            progressbar.update(len(data))
            raw_data += data
    if total_size != 0 and wrote != total_size:
        raise RuntimeError("Expected %d but got %d bytes".format(total_size, wrote))

    return raw_data
