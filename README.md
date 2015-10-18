# OpenStreetMap tile usage global map kid analysis and visualisations

## Detect countries for each tile

    python3 fetch2.py | parallel --pipe --recend '' -k xz -9 > all-out.csv.xz

Now out file contains lines similar to next:

    2014-01-01,6,37,21,11270,54.2629207012382,30.9375,??|BY|RU|RU+UA|UA

1. `2014-01-01` - date when log collected;
2. `6` - tile zoom;
3. `27` - tile x;
4. `21` - tile y;
5. `11270` - count of tile fetches;
6. `54.2629207012382` - tile center latitude;
7. `30.9375` - tile center longitude;
8. `??|BY|RU|RU+UA|UA` - countries covered by tile `|` - split countries, `+` split two countries parts with same area in OSM, `??` - unknown counry sea, `BY` - ISO3166 alpha 2 code of country.

See known countries list in OSM: http://overpass-turbo.eu/s/a27.

## Cache visualisation

![Global Map](cache_global.png)

To detect covered countris for all tiles I need some smart caching. Main idea that if one big tile coverd only one country then all smaller tiles below this tile also covered only this country. Sometime one area can be belong to two codes in OSM, for example FR and FX or controversial territories, and this case better also cover to improve caching work.

![White spaces](cache_white_spaces.png)

You can play with prepared maps with visualized cache. Be careful, this pages can kill your browser. Hi FF, I love you, but you are slow.

- http://tbicr.github.io/map-trends/report_9.html
- http://tbicr.github.io/map-trends/report_10.html
- http://tbicr.github.io/map-trends/report_11.html

Europe:

![Europe without tiles](cache_europe_without_tiles.png)
![Europe with tiles](cache_europe_with_tiles.png)

