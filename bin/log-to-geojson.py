#!/usr/bin/env python3

import sys
import csv
import simplejson as json
from decimal import Decimal

logfile = sys.argv[1]

e = {"type":"FeatureCollection", "features": []}

for row in csv.DictReader(open(logfile, newline="")):
    e["features"].append(
        {
            "type": "Feature",
            "geometry": { "type": "Point", "coordinates": [Decimal(n) for n in row["point"].split()]},
            "properties": {
                "secs": row["secs"],
                "client": row["client"],
            }
        }
    )

json.dump(e, sys.stdout)
