#!/usr/bin/env python3
# coding=utf-8
import sys

from elasticsearch import Elasticsearch

es = Elasticsearch(['http://192.168.2.207:9200'])


insertBody = {


    "country": "",
    "flag6c_grade": 0,
    "replied": 0,
    "unsubscribe": 0,
    "life_max": 0,
    "name": "",
    "today_max": 0,
    "industry": 0,
    "email_valid": 0,
    "customer_id": 0,
    "email": "",
    "products": []

    }

insertBody["country"]='US'
insertBody["name"]='hhz'
insertBody["industry"]=12
insertBody["email_valid"]=2
insertBody["email"]='asdasd'
insertBody["customer_id"]=3333331
try:
    es.index('buyer', 'data', insertBody)
except Exception as e:
    print(3333331)
    print(e,file=sys.stderr)
