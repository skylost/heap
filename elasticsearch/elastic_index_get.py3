#!/usr/bin/env python

import httplib2
import json
import os

host = os.getenv('ELASTICSEARCH_HOST', "localhost")
port = os.getenv('ELASTICSEARCH_PORT', "5601")

http = httplib2.Http(".cache")
resp, content = http.request("http://"+host+":"port+"/_stats/indexes", "GET")
