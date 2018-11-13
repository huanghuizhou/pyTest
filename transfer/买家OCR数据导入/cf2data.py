#!/usr/bin/env python3
# coding=utf-8

import json

# cf.json是广交会数据，要做公司合并处理
with open('cf.json') as f:
    cfs = json.load(f)

cf_dict = {}
for cf in cfs:
    name = cf['company']
    if name not in cf_dict:
        cf_dict[name] = cf
    target = cf_dict[name]
    if 'products' not in target:
        target['products'] = []
    target['products'].append(cf['product'])
    if 'extra_data' not in target:
        target['extra_data'] = {
            'industries': [],
        }
    target['extra_data']['industries'].append(int(cf['industry']))

with open('data.json', 'w') as f:
    json.dump(list(cf_dict.values()), f, ensure_ascii=False, indent=4)


