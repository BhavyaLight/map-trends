# OpenStreetMap tile usage global map kid analysis and visualisations

## Cache visualisation

![Global Map](cache_global.png)

To detect covered countris for all tiles I need some smart caching. Main idea that if one big tile coverd only one countr then all smaller tiles below this tile allso covered only this country.

Be careful, this pages can kill your browser. Hi FF, I love you, but you are slow.

- http://tbicr.github.io/map-trends/report_9.html
- http://tbicr.github.io/map-trends/report_10.html
- http://tbicr.github.io/map-trends/report_11.html

You can find that France for example not coverd. This because it covered in OSM with several polygins with FR and FX ISO3166-1. See counties list http://overpass-turbo.eu/s/a27.

![White spaces](cache_white_spaces.png)

Europe:

![Europe without tiles](cache_europe_without_tiles.png)
![Europe with tiles](cache_europe_with_tiles.png)
