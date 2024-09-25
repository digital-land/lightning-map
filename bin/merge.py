#!/usr/bin/env python3

import sys
import simplejson as json

e = json.load(open(sys.argv[1]))
e2 = json.load(open(sys.argv[2]))

e["features"] = e["features"] + e2["features"]

json.dump(e, sys.stdout)
