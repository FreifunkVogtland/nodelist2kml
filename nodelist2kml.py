#!/usr/bin/python3
# -*- coding: utf-8; -*-

import copy
from datetime import datetime
from fastkml import kml
import json
import os
import os.path
import sys
from shapely.geometry import Point


def dump_kml(data, filename):
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        f.write(data.to_string())
        f.flush()
        os.fsync(f.fileno())


def generate_kml(nodelist):
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    d = kml.Document(ns)
    k.append(d)

    for n in nodelist['nodes']:
        if 'position' not in n:
            continue

        if 'lat' not in n['position']:
            continue

        if 'long' not in n['position']:
            continue

        if 'name' not in n:
            continue

        if 'id' not in n:
            continue

        if 'status' not in n:
            continue

        if 'online' not in n['status']:
            continue

        extended = kml.ExtendedData()

        p = kml.Placemark(ns, n['id'], n['name'])
        p.geometry = Point(n['position']['long'], n['position']['lat'])
        d.append(p)

        extended = []

        if n['status']['online']:
            status = "online"
        else:
            status = "offline"

        extended.append(kml.Data(value=status, name='status', display_name='Status'))

        url = 'http://vogtland.freifunk.net/map/#!v:m;n:'+n['id']
        extended.append(kml.Data(value=url, name='url', display_name='URL'))

        p.extended_data = kml.ExtendedData(elements=extended)


    return k


def main():
    if len(sys.argv) != 3:
        print("./nodes2kml.py NODELIST OUTKML")
        sys.exit(1)

    nodelistjson = sys.argv[1]
    outkml = sys.argv[2]
    outkmltmp = outkml + '.tmp'

    # load
    nodelist = json.load(open(nodelistjson))
    data = generate_kml(nodelist)

    # store
    dump_kml(data, outkmltmp)
    os.rename(outkmltmp, outkml)


if __name__ == "__main__":
    main()
