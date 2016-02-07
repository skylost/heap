#!/usr/bin/python

import rados, sys

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

if cluster.pool_exists(sys.argv[1]):
  raise RuntimeError("Pool %s already exists" % sys.argv[1])

try:
  print "\nCreate %s Pool" % sys.argv[1]
  print "------------------"
  cluster.create_pool(sys.argv[1])
  if cluster.pool_exists(sys.argv[1]):
    print "Pool named %s created\n" % sys.argv[1]
except Exception as e:
  print "error: ", e
  raise e 

cluster.shutdown()
