--Tiles Helper
CREATE TYPE tile AS (x INTEGER, y INTEGER, z INTEGER);


--Convert a point geometry to tile: x,y tile at zoom level z.
CREATE OR REPLACE FUNCTION point_to_tile(
    _point geometry,
    zoom_level INTEGER
) RETURNS tile
AS $$
DECLARE
    d2r CONSTANT DOUBLE PRECISION := pi() / 180;
    lon CONSTANT DOUBLE PRECISION := st_x(ST_Transform(_point, 4326));
    lat CONSTANT DOUBLE PRECISION := st_y(ST_Transform(_point, 4326));
    _sin CONSTANT DOUBLE PRECISION := sin(lat * d2r);
    t tile;
BEGIN
    t.x = floor((1 << zoom_level) * (lon / 360 + 0.5)) :: integer;
    t.y = floor((1 << zoom_level) * (0.5 - 0.25 * ln((1 + _sin) / (1 - _sin)) / pi())) :: integer;
    t.z = zoom_level;
    RETURN t;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

--Convert x,y,z tiles to a point in Lat/lon (uppper left edge coordinates)
CREATE OR REPLACE FUNCTION tile_to_point(
     Tile tile
)RETURNS geometry 
As $$
DECLARE
    E CONSTANT DOUBLE PRECISION := 2.7182818284;
    z2 CONSTANT DOUBLE PRECISION := pow(2, Tile.z);
    x float;
    sinh float;
    lon_deg double precision;
    lat_deg double precision;
BEGIN
    lon_deg=CAST (Tile.x*360/(z2)-180 as DOUBLE PRECISION);
    x=pi()*(1-Tile.y*2/z2);
    sinh = (1 - power(E, -2*x)) / (2 * power(E, -x));
    lat_deg=degrees(atan(sinh));
    RETURN ST_SetSRID(ST_Point(lon_deg,lat_deg),4326);
END
$$ LANGUAGE plpgsql IMMUTABLE;

--Examples
select * 
from point_to_tile(ST_SetSRID(ST_point(-1,65),4326),2);

select st_x(ST_Transform(tile_to_point, 4326)) as lon, st_y(ST_Transform(tile_to_point, 4326)) as lat from
(
select *
from tile_to_point((2,3,3))
) as x;

