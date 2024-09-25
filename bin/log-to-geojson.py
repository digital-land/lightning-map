#!/usr/bin/env python3

import sys
import csv
import simplejson as json
from decimal import Decimal

logfile = sys.argv[1]

e = {"type":"FeatureCollection", "features": []}

n = 0

for row in csv.DictReader(open(logfile, newline="")):
    reference = f'p{n}-{row["secs"]}'
    n = n + 1

    e["features"].append(
        {
            "type": "Feature",
            "geometry": { "type": "Point", "coordinates": [Decimal(n) for n in row["point"].split()]},
            "properties": {
                "secs": row["secs"],
                "client": row["client"],
                "reference": reference,
            }
        }
    )

json.dump(e, sys.stdout)
