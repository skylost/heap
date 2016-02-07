#!/usr/bin/python

import rados, sys

# sudo rados lspools

try:
  cluster = rados.Rados(conffile = '/etc/ceph/ceph.conf', conf = dict (keyring = '/etc/ceph/ceph.client.admin.keyring'))
except TypeError as e:
  print 'Argument validation error: ', e
  raise e

try:
  cluster.connect()
except Exception as e:
  print "connection error: ", e
  raise e

pools = cluster.list_pools()
for pool in pools:
  print pool

cluster.shutdown()
