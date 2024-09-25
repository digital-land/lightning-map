#!/usr/bin/env python3

import sys
import csv
import re
from urllib.parse import unquote
from datetime import datetime


logfile = sys.argv[1]
outfile = sys.argv[2] or "output.csv"

# CloudFront log columns
columns = ["@timestamp", "@message", "stem", "query", "user_agent"]

# lightning log fields
fieldnames = ["secs", "client", "point"]

point_re = re.compile(r"^.*(POINT|POLYGON)[\(\s\+]*(?P<lon>-?\d{1,2}\.\d{2})\d*[\s,+]+(?P<lat>\d{1,2}\.\d{2}).*$")


def oneof(l, s):
    return bool([e for e in l if (e in s)])


def parse_client(agent):
    if oneof(
        ["google.com", "Google", "bing.com", "applebot", "openai", "semrush"], agent
    ):
        return "spider"

    if oneof([":canary:", "uptimerobot", "amazonbot"], agent):
        return "canary"

    if oneof(["python-requests", "node-fetch"], agent):
        return "code"

    return "browser"


def parse_point(query):
    if not ("POINT" in query or "POLYGON" in query):
        return ""

    query = unquote(unquote(query))
    match = point_re.match(query)

    if (not match):
        print("failed to parse:", query, file=sys.stderr)
        sys.exit(2)

    return match.group("lon") + " " + match.group("lat")


if __name__ == "__main__":

    first = None

    w = csv.DictWriter(open(outfile, "w", newline=""), fieldnames)
    w.writeheader()

    for row in csv.DictReader(open(logfile, newline="")):

        point = parse_point(row["query"])

        if not point:
            continue

        client = parse_client(row["user_agent"])

        # calculate interval
        d = datetime.strptime(row["@timestamp"], "%Y-%m-%dT%H:%M:%S").timestamp()
        if not first:
            first = d
        secs = d - first

        w.writerow(
            {
                "secs": int(abs(secs)),
                "client": client,
                "point": point,
            }
        )
