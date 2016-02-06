#!/usr/bin/python

import rados, sys

try:
  cluster = rados.Rados(conffile = '/etc/ceph/ceph.conf', conf = dict (keyring = '/etc/ceph/ceph.client.admin.keyring'))
except TypeError as e:
  print 'Argument validation error: ', e
  raise e

print "librados version: " + str(cluster.version())

print "\nCreated cluster handle."


try:
  print "Will attempt to connect to: " + str(cluster.conf_get('mon initial members'))
  cluster.connect()
except Exception as e:
  print "connection error: ", e
  raise e
finally:
  print "Connected to the cluster."

print "\nCluster ID: " + cluster.get_fsid()

print "\nCluster Configuration"
print "=================="
try:
  print "Public Network: " + cluster.conf_get('public network')
  print "Cluster Network: " + cluster.conf_get('cluster network')
  print "mon host: " + cluster.conf_get('mon host')
except Exception as e:
  print "get configuration error: ", e
  raise e

print "\nCluster Statistics"
print "=================="
cluster_stats = cluster.get_cluster_stats()

for key, value in cluster_stats.iteritems():
  print key, value

print "\nShutting down the handle."
cluster.shutdown()
