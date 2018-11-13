#!/usr/bin/env python3
# coding=utf-8

import json
import sys

from elasticsearch import Elasticsearch, helpers

if len(sys.argv) != 4:
    print('usage: es_importer.py host_port index json_file')
    quit()

host = sys.argv[1]
index = sys.argv[2]
json_file = sys.argv[3]

es = Elasticsearch(['http://' + host])
data = json.load(open(json_file))
actions = ({'_index': index, '_type': 'data', '_source': x} for x in data)
helpers.bulk(es, actions)
