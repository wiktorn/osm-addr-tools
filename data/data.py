import functools
import typing

import pyproj
import shapely.geometry


class _BaseGeoType(float):
    def __new__(cls, o: typing.Union[str, float]):
        if isinstance(o, str):
            return super(_BaseGeoType, cls).__new__(cls, float(o))
        else:
            return super(_BaseGeoType, cls).__new__(cls, o)


class LonType(_BaseGeoType):
    pass


class LatType(_BaseGeoType):
    pass


class XType(_BaseGeoType):
    pass


class YType(_BaseGeoType):
    pass


class BBoxType(typing.NamedTuple):
    minlat: LatType
    minlon: LonType
    maxlat: LatType
    maxlon: LonType


def _coordinate_to_string(v: float) -> str:
    return '{:0.8f}'.format(v)


class Location(typing.NamedTuple):
    """Location with arguments as floats in WGS84 projection"""
    lon: LonType
    lat: LatType

    @staticmethod
    def from_geometry(geom: shapely.geometry.base.BaseGeometry):
        centroid = geom.centroid
        return Location(lat=centroid.y, lon=centroid.x)

    def to_point(self) -> shapely.geometry.Point:
        return shapely.geometry.Point(self.lon, self.lat)

    def to_location_str(self) -> 'LocationStr':
        return LocationStr(lon=_coordinate_to_string(self.lon), lat=_coordinate_to_string(self.lat))


class LocationXY(typing.NamedTuple):
    """Location with argumetns as floats in any projection"""
    x: XType
    y: YType
    projection: str

    def to_location(self) -> Location:
        lon, lat = srs_to_wgs(self.projection, x=self.x, y=self.y)
        return Location(lon=lon, lat=lat)

    def to_location_str(self) -> 'LocationStr':
        lon, lat = srs_to_wgs(self.projection, x=self.x, y=self.y)
        return LocationStr(lon=_coordinate_to_string(lon), lat=_coordinate_to_string(lat))


class LocationStr(typing.NamedTuple):
    """Location with arguments as string with float numbers in WGS84 projection"""
    lon: str
    lat: str

    def to_location(self) -> Location:
        return Location(lat=LatType(float(self.lat)), lon=LonType(float(self.lon)))


@functools.lru_cache(maxsize=None)
def get_proj(srs: str) -> pyproj.Proj:
    return pyproj.Proj(init=srs)


__WGS84 = pyproj.Proj(proj='latlong', datum='WGS84')


def srs_to_wgs(srs: str, x: XType, y: YType) -> typing.Tuple[LonType, LatType]:
    if srs.startswith("urn:ogc:def:crs:"):
        srs = srs[16:].replace('::', ':')
    return pyproj.transform(get_proj(srs), __WGS84, float(x), float(y))


__EPSG2180 = pyproj.Proj(init="epsg:2180")


def wgs_to_2180(lon: LonType, lat: LatType) -> typing.Tuple[XType, YType]:
    # returns lon,lat
    return pyproj.transform(__WGS84, __EPSG2180, lon, lat)


def e2180_to_wgs(x: XType, y: YType) -> typing.Tuple[LonType, LatType]:
    # returns lon,lat
    return srs_to_wgs('epsg:2180', x, y)
