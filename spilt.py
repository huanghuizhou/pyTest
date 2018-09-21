#!/usr/bin/env python3
# coding=utf-8

from collections import defaultdict

import jieba

stop_words = {'宁波', '宁波市', '慈溪', '慈溪市', '海曙', '海曙区', '江东', '江东区', '江北', '江北区', '象山', '象山县', '余姚', '余姚市', '宁海', '宁海县',
              '奉化', '奉化市', '有限公司', '浙江', '浙江省', '股份', '新', '开发区','经济','技术'}
csv_data = {}
reversed_index = defaultdict(list)
jieba.load_userdict('G:\\test\\dict.txt')
with open('G:\\test\\a.txt') as f:
    for line in f:
        line = line.strip()
        name = line
        # csv_data[name] = line
        parts = [x for x in jieba.cut(name) if x not in stop_words]
        for part in parts:
            reversed_index[part].append(name)

with open('G:\\test\\b.txt') as f, open('G:\\test\\c.txt', 'w') as out:
    a = 0
    for line in f:
        line = line.strip()
        parts = [x for x in jieba.cut(line) if x not in stop_words]
        i = 0
        hit = reversed_index[parts[i]]
        while len(hit) > 1 and i + 1 < len(parts):
            i += 1
            part = parts[i]
            another_hit = reversed_index[part]
            hit = set(hit) & set(another_hit)
        # for part in parts:
        #     hit += index[part]
        if len(hit) > 0:
            result = '/'.join(hit)
            print(line, '=>', result)
            out.write('%s,%s\n' % (line, result))
        a += 1
        # print(a)
