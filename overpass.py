from urllib.parse import urlencode
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


__log = logging.getLogger(__name__)


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
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
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


__overpassurl = "http://overpass.osm.rambler.ru/cgi/interpreter"
__overpassurl = "http://overpass-api.de/api/interpreter"
__overpassurl = "http://api.openstreetmap.fr/oapi/interpreter/"
__overpassurl = "http://osm-cdn.vink.pl/api/interpreter"


def get_url_for_query(qry: str):
    return __overpassurl + '?' + urlencode({'data': qry.replace('\t', '').replace('\n', '')})


def query(qry):
    # TODO - check if the query succeeded
    __log.debug("Query %s , server: %s", qry, __overpassurl)
    return requests_retry_session().get(get_url_for_query(qry), timeout=180).content
