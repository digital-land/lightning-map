#!/usr/bin/env python3

import sys
import re


secs_re = re.compile(r'^.*id="p\d+-(?P<secs>\d+).*$')

while line := sys.stdin.readline():
    # <circle id="p1-0" cx="-57.886" cy="3396.448" r="1" class="snapshot"/>
    if "<circle " in line:
        match = secs_re.match(line)
        secs = match.group("secs")
        secs = int(secs) / 250
        line = line.replace('r="1"', 'r="0"')
        line = line.replace(
            "/>",
            f'><animate attributeName="r" begin="{secs}s" values="7;5;4;0" dur="2.5s" /></circle>',
        )

    print(line, end="")

    if line.startswith("<svg "):
        print(
            """<style>
  svg {
      background-color: #ffffff;
  }
  circle {
    stroke: #0b0c0c;
    stroke-width: 2px;
    fill-opacity: 0;
  }
  #E92000001 {
    fill: #b1b4b6;
  }
</style>
"""
        )
