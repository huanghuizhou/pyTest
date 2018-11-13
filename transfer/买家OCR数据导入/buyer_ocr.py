#!/usr/bin/env python3
# coding=utf-8


import json
import sys
from typing import TextIO

TITLES = {
    '公司名称':       'company',
    '国家/地区':      'country',
    '国家或地区':      'country',
    '国家':         'country',
    '电话':         'tel',
    'tel':         'tel',
    '联系人':        'contact',
    '传真':         'fax',
    'fax':         'fax',
    '地址':         'address',
    '邮编':         'postcode',
    'e-mail':     'email',
    'email':      'email',
    'emai1':      'email',
    '网址':         'website',
    'web':        'website',
    '职位':         'position',
    '进口产品':       'product',
    '进口商品':       'product',
    '主要进口商品(中文)': 'product',
    '采购产品':       'product'
}


def extract_title(line: str):
    """
    提取title，如果找不到，返回None
    :param line:
    :return:
    """
    for title in TITLES.keys():
        if line.lower().startswith(title):
            return title
    return None


def extract_title_data(line: str):
    for title in TITLES.keys():
        if line.lower().startswith(title):
            tmp_title = title
            tmp_data = line[len(tmp_title):]
            return tmp_title.strip(), tmp_data.strip(' :')
    return None, line


def store_obj(obj, title, data):
    if title in TITLES:
        title = TITLES[title]
        obj[title] = data
    else:
        tmp_title, tmp_data = handle_error_field(title, data)
        if tmp_title:
            title, data = tmp_title, tmp_data
            title = TITLES[title]
            obj[title] = data
        else:
            if 'error' not in obj:
                obj['error'] = {}
            obj['error'][title] = data


def handle_error_field(title, data):
    tmp_title = extract_title(title)
    if not tmp_title:
        return None, None
    tmp_data = title[len(tmp_title):] + data
    return tmp_title, tmp_data


def parse_object(fp: TextIO):
    """
    解析title和数据，数据可能跨行
    :return:
    """
    obj = {}
    title, data = '', ''
    while True:
        pre_position = fp.tell()
        line = fp.readline()
        if not line:
            break
        if title and line.startswith('公司名称'):
            store_obj(obj, title, data)
            fp.seek(pre_position)
            return obj
        line = line.strip(' \n\r\t')

        tmp_title, tmp_data = extract_title_data(line)
        if not tmp_title:
            data += tmp_data
            continue

        if not title:
            # 没有title，说明新的一行
            title = tmp_title.strip().lower()
            data = tmp_data.strip()
        elif tmp_title:
            # 已经解析到title，并且解析到新的title，需要保存解析到的title和data，并且用新title和data进行下一轮解析
            # 除了文件第一行，后面的数据都在这个逻辑里
            if tmp_title not in TITLES:
                # 可能由于OCR问题导致断行内有空格
                # title不在给定范围内就整行当数据处理
                data += (' ' + line)
                continue
            store_obj(obj, title, data)
            title = tmp_title.strip().lower()
            data = tmp_data.strip()
    if title:
        store_obj(obj, title, data)
    return obj


def main():
    if len(sys.argv) != 3:
        print('usage buyer_ocr.py 行业代码 备注')
        return

    industry = int(sys.argv[1])
    remark = sys.argv[2]

    fp = open('data.txt')
    head = fp.read(1)
    if head != '\ufeff':
        fp.seek(0)
    datas = []
    while True:
        obj = parse_object(fp)
        if not obj:
            break
        obj['industry'] = industry
        obj['requirement_remark'] = remark
        datas.append(obj)
    # print(datas)
    fp.close()

    json.dump(datas, open('data.json', 'w'), indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
