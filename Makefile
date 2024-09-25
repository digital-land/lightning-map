CDN_LOGS=$(wildcard var/cache/logs-insights-results-*.csv)

var/lightning.svg:  var/lightning.geojson Makefile
	svgis draw var/lightning.geojson --crs EPSG:3857 --scale 2000 -o $@

var/lightning.geojson: var/snapshot.geojson
	ogr2ogr -simplify 0.01 $@ var/snapshot.geojson

var/snapshot.geojson: data/snapshot.csv bin/log-to-geojson.py
	python3 bin/log-to-geojson.py data/snapshot.csv > $@

data/snapshot.csv: var/cache/snapshot.csv bin/convert-cdn-log.py
	python3 bin/convert-cdn-log.py var/cache/snapshot.csv $@

# CDN logs are in reverse timestamp order ..
var/cache/snapshot.csv: $(CDN_LOGS) bin/sort.sh
	bin/sort.sh $(CDN_LOGS) > $@

clean::

clobber::

init::
	pip install -r requirements.txt
	npm install svgo

server::
	python3 -m http.server
