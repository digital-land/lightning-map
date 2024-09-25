#!/usr/bin/env python3

import re
import sys
import csv

lpas = {}
for row in csv.DictReader(open("var/organisation.csv")):
    row["class"] = "none"
    lpas[row["local-planning-authority"]] = row


stroke = "#DEE0E2"

counts = {}
for row in legends:
    counts[row["reference"]] = 0

for lpa, l in lpas.items():
    counts[l["class"]] += 1

total = sum(counts.values())

print("""<!doctype html>
<html lang="en-GB">
<head>
<style>
html {
  font-family: sans-serif;
  font-size: 14px;
  color: #0b0c0c;
}
body {
  padding: 5px 10px;
}

.choropleth {
 width: 400px;
 resize: both;
}

.choropleth svg {
 width: 100%;
 fill: 	#0b0c0c;
}

.stacked-chart {
  display: flex;
  width: 99%;
  margin: 1em 0;
}

.stacked-chart .bar {
  display: flex;
  justify-content: left;
  align-items: center;
  height: 2em;
  text-indent: 1em;
  color: #ffffff;
}

ul.key {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

li.key-item {
   border-left: 16px solid;
   margin-bottom: 5px;
   padding-left: 5px;
}
""")

for item in legends:
    (reference, colour) = (item["reference"], item["colour"])
    print(f".stacked-chart .bar.{reference} {{ background-color: {colour}; color: #000 }}")
    print(f".key-item.{reference} {{ border-color: {colour}; }}")
    print(f"svg path.{reference} {{ fill: {colour}; stroke: {stroke}; }}")
print(f"svg path:hover {{ fill: #ffdd00 }}")


print("""
</style>
</head>
<body>
<div class="choropleth">
""")

re_id = re.compile(r"id=\"(?P<lpa>\w+)")

with open("lpa.svg") as f:
    for line in f.readlines():

        line = line.replace(' fill-rule="evenodd"', '')
        line = line.replace('class="polygon ', 'class="')

        match = re_id.search(line)
        if match:
            lpa = match.group("lpa")

            if lpa not in lpas:
                counts["error"] += 1
                name = lpa
                _class = "error"
            else:
                org = lpas[lpa]
                name = org["name"]
                _class = org.get("class", "white")

        if 'class="lpa"' in line:
            line = line.replace('<path', f'<a href="#{lpa}"><path')
            line = line.replace('class="lpa"/>', f'class="lpa {_class}"><title>{name}</title></path></a>')

        print(line, end="")


print("""
</div>
</body>
</html>""")
