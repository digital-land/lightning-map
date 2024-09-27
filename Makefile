CDN_LOGS=$(wildcard var/cache/logs-insights-results-*.csv)


all: lightning.svg

lightning.svg: var/lightning-o.svg bin/animate.py
	python3 bin/animate.py < var/lightning-o.svg > $@

var/lightning-o.svg: var/lightning.svg svgo.js
	node_modules/svgo/bin/svgo var/lightning.svg --config svgo.js -o $@

var/lightning.svg:  var/lightning.geojson
	svgis draw var/lightning.geojson --id-field reference --crs EPSG:3857 --scale 2000 -o $@

var/lightning.geojson: var/merged.geojson
	ogr2ogr -simplify 0.01 $@ var/merged.geojson

var/merged.geojson: var/cache/border.geojson var/snapshot.geojson bin/merge.py
	python3 bin/merge.py var/cache/border.geojson var/snapshot.geojson > $@

var/snapshot.geojson: data/snapshot.csv bin/log-to-geojson.py
	python3 bin/log-to-geojson.py data/snapshot.csv > $@

data/snapshot.csv: var/cache/snapshot.csv bin/convert-cdn-log.py
	python3 bin/convert-cdn-log.py var/cache/snapshot.csv $@ 86400

# CDN logs are in reverse timestamp order ..
var/cache/snapshot.csv: $(CDN_LOGS) bin/sort.sh
	bin/sort.sh $(CDN_LOGS) > $@


var/cache/border.geojson:
	curl -qfsL 'https://files.planning.data.gov.uk/dataset/border.geojson' > $@

clean::

clobber::

init::
	pip install -r requirements.txt
	npm install svgo

server::
	python3 -m http.server
