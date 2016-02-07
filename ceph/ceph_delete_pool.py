#!/usr/bin/python

import rados, sys

# sudo rados rmpool $1 --yes-i-really-really-mean-it

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

if not cluster.pool_exists(sys.argv[1]):
  raise RuntimeError("Pool %s not exists" % sys.argv[1])

try:
  print "\nDelete %s Pool" % sys.argv[1]
  print "------------------"
  cluster.delete_pool(sys.argv[1])
  if not cluster.pool_exists(sys.argv[1]):
    print "Pool named %s deleted\n" % sys.argv[1]
except Exception as e:
  print "error: ", e
  raise e 

cluster.shutdown()
