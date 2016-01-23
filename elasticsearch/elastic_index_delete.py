#!/usr/bin/env python

import httplib
import json
import os

host = os.getenv('ELASTICSEARCH_HOST', "localhost")
port = os.getenv('ELASTICSEARCH_PORT', "5601")

http = httplib.HTTPConnection(host+":"+port)

try:
  http.request("GET", "/_stats/indexes")
except Exception as e:
  print(type(e))
response = http.getresponse()
print response.status, response.reason

json_obj = json.loads(response.read())
json_obj = json_obj["indices"].keys()
json_obj = sorted(json_obj, reverse=False)
json_obj = json_obj[:-1]

for key in json_obj:
  #http.request("DELETE", "/%s?pretty" % key)
  print key
    
response = http.getresponse()
print response.status, response.reason
