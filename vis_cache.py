import colorsys
import json
import string

import mercantile
import shapely.geometry


saturations = [0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]
brightness = [0.5, 0.65, 0.8, 0.95]
base = len(saturations)
offset = 1
sv = {i: (saturations[(i + offset) % base], brightness[(i + offset) // base])
       for i, _ in enumerate(string.ascii_uppercase)}
color_base = 255
hue_stretch = 0.5

color_map = {
    '??': '#00F',
    'AQ': '#000',
}


def get_color(*countries):
    rr, rg, rb = 0, 0, 0
    for country in countries:
        if '+' in country:
            r, g, b = get_color(*country.split('+'))
        elif country in color_map:
            r, g, b = [int(c, 16) * 16 + int(c, 16) for c in color_map[country][1:]]
        else:
            h = string.ascii_uppercase.index(country[0]) / len(string.ascii_uppercase) * hue_stretch
            s, v = sv[string.ascii_uppercase.index(country[1])]
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            r, g, b = r * color_base, g * color_base, b * color_base
        rr += r
        rg += g
        rb += b
    return rr // len(countries), rg // len(countries), rb // len(countries)


def tile_to_rect(zoom, x, y, v):
    zoom = int(zoom)
    x = int(x)
    y = int(y)
    box = mercantile.bounds(x, y, zoom)
    return {
        'type': 'Feature',
        'properties': {
            't': '%s/%s/%s' % (zoom, x, y),
            'c': v,
            'k': '#%02X%02X%02X' % get_color(v),
        },
        'geometry': shapely.geometry.mapping(shapely.geometry.box(*box)),
    }


def generate_geojson(zoom):
    cache_zoom, cache = json.load(open('cache_tile.json'))
    cache_trim = {
        'type': 'FeatureCollection',
        'features': [tile_to_rect(*k.split('/'), v=v)
                     for k, v in cache.items()
                     if int(k.split('/')[0]) <= zoom and len(v.split('|')) == 1],
    }
    json.dump(cache_trim, open('cache_tile_%s.geojson' % zoom, 'w'),
              ensure_ascii=False, sort_keys=True)


if __name__ == '__main__':
    generate_geojson(9)
