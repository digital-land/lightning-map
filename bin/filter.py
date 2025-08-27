#!/usr/bin/env python3

import sys
import re
import simplejson as json

pattern = re.compile(sys.argv[1])
e = json.load(open(sys.argv[2]))

e['features'] = [feature for feature in e['features'] if pattern.match(feature['properties']['reference'])]

json.dump(e, sys.stdout)
