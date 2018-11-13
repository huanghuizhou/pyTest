#!/usr/bin/env python3
# coding=utf-8
import json
import sys

import pymysql
from elasticsearch import Elasticsearch
from pymysql.connections import Connection

# MYSQL_HOST = '192.168.2.203'
# MYSQL_PORT = 3306
# MYSQL_USER = 'gt_user'
# MYSQL_PASSWD = 'greatTao1314!@#$'
#

MYSQL_HOST = '192.168.2.203'
MYSQL_PORT = 3306
MYSQL_USER = 'greatTao'
MYSQL_PASSWD = 'greatTao.1314'

ES_HOST = '192.168.2.207:9200'


# MYSQL_HOST = 'localhost'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# MYSQL_PASSWD = '123456'

es = Elasticsearch([ES_HOST])

def new_mysql_conn() -> Connection:
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWD,
        db='gttown_crm',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


# 根据条件更新示例


def doUpdtae(buyer):
    customer_id = buyer['id']
    company = buyer['company']
    country = buyer['country']
    industry = buyer['industry']
    email = buyer['email']
    products = buyer['products']
    extra_data = json.loads(buyer['extra_data']) if buyer['extra_data'] else {}
    industries = extra_data['industries'] if 'industries' in extra_data else [industry]

    searchBody = {
        "query": {
            "term": {
            }
        }
    }
    searchBody["query"]["term"] = {"customer_id": customer_id}
    searchResult = es.search("buyer", "data", body=searchBody)

    if searchResult["hits"]["total"] > 0:
        oldDatas = searchResult["hits"]["hits"]
        for oldData in oldDatas:
            id = oldData['_id']
            # 删除old
            try:
                es.delete("buyer", "data", id=id)
            except Exception as e:
                print(e)
                return

        oldData = searchResult["hits"]["hits"][0]['_source']

        oldData["country"] = country
        oldData["name"] = company
        oldData["industry"] = industries
        oldData["email"] = email
        oldData["products"] = products
        try:
            es.index('buyer', 'data', oldData)
        except Exception as e:
            print(customer_id)
            print(e, file=sys.stderr)


    else:
        insertBody = {
            "country": "",
            "flag6c_grade": 0,
            "replied": 0,
            "unsubscribe": 0,
            "life_max": 0,
            "name": "",
            "today_max": 0,
            "industry": [],
            "email_valid": 0,
            "customer_id": 0,
            "email": "",
            "products": []
        }

        insertBody["country"] = country
        insertBody["name"] = company
        insertBody["industry"] = industries
        insertBody["email"] = email
        insertBody["customer_id"] = customer_id
        insertBody["products"] = products
        try:
            es.index('buyer', 'data', insertBody)
        except Exception as e:
            print(customer_id)
            print(e, file=sys.stderr)

    print(customer_id, " update success")

    # # 插入
    # if searchResult["hits"]["total"] == 0:
    #     insertBody = {
    #         "country": "",
    #         "flag6c_grade": 0,
    #         "replied": 0,
    #         "unsubscribe": 0,
    #         "life_max": 0,
    #         "name": "",
    #         "today_max": 0,
    #         "industry": 0,
    #         "email_valid": 0,
    #         "customer_id": 0,
    #         "email": "",
    #         "products": []
    #     }
    #
    #     insertBody["country"] = country
    #     insertBody["name"] = company
    #     insertBody["industry"] = industry
    #     insertBody["email_valid"] = email_status
    #     insertBody["email"] = email
    #     insertBody["customer_id"] = customer_id
    #     try:
    #         es.index('buyer', 'data', insertBody)
    #     except Exception as e:
    #         print(customer_id)
    #         print(e, file=sys.stderr)
    # # 更新
    # else:
    #     upBody = {
    #         "script": {
    #             "source": "ctx._source.email_valid=1;ctx._source.life_max=2",
    #             "lang": "painless"
    #         },
    #         "query": {
    #             "term": {
    #                 "customer_id": 0
    #             }
    #         }
    #     }
    #     source = 'ctx._source.country="{0}";ctx._source.name="{1}";ctx._source.industry={2};ctx._source.email="{3}";ctx._source.email_valid={4}'.format(
    #         country, company, industry, email, email_status)
    #     upBody["script"]["source"] = source
    #     upBody["query"]["term"]["customer_id"] = customer_id
    #     try:
    #         es.update_by_query('buyer', 'data', body=upBody, params={'conflicts': 'proceed'})
    #         # global count
    #         # count +=1
    #         # if(count %20==0):
    #         #     sleep(2)
    #         #     print(count)
    #     except Exception as e:
    #         print(customer_id)
    #         print(e, file=sys.stderr)
    #         sleep(2)


def main():
    conn = new_mysql_conn()
    with conn.cursor() as cursor:
        cursor.execute(
            "select cc.id,cc.company,cc.country,cc.industry,cc.role,cd.customer_id,cd.email,cd.email_status,cc.extra_data from channel_customer cc left join channel_contact cd on cc.id=cd.customer_id  where cc.role=1 GROUP BY cc.id")
        buyers = cursor.fetchall()

    for buyer in buyers:
        id = buyer['id']
        with conn.cursor() as productCursor:
            productCursor.execute(
                "select product_content from channel_product where customer_id=%s", id)
            products = productCursor.fetchall()
            if (len(products) > 0):
                productList = []
                for product in products:
                    productList.append(product['product_content'])
                buyer['products'] = productList
            else:
                buyer['products'] = []
        doUpdtae(buyer)


if __name__ == '__main__':
    main()
