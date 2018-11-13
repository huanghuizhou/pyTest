#!/usr/bin/env python3
# coding=utf-8
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://192.168.2.207:9200'])


searchBody = {
  "query": {
    "term": {
    }
  }
}


upBody = {
      "script": {
        "source": 'ctx._source.country="AU";ctx._source.name="niubi25";ctx._source.industry=0;ctx._source.email="641228102_tester@channel.com";ctx._source.email_valid=0',
        "lang": "painless"
      },
      "query": {
        "term": {
          "customer_id": 74
        }
      }
    }


upBody1 = {'script': {'source': 'ctx._source.country="AU";ctx._source.name="niubi25";ctx._source.industry=0;ctx._source.email="641228102_tester@channel.com";ctx._source.email_valid=0',
                      'lang': 'painless'},
           'query': {'term': {'customer_id': 74}}}
#source="ctx._source.country='{0}';ctx._source.name='{1}';ctx._source.industry='{2}';ctx._source.email='{3}';ctx._source.email_valid='{4}'".format("US","公司2",16,"aasd@qwew.com",1)
# upBody["script"]["source"]=source
# upBody["query"]["term"]["customer_id"]=15
es.update_by_query('buyer', body=upBody1)
print(111)


