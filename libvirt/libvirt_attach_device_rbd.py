#!/usr/bin/env python

__author__  = 'weezhard'
__license__ = 'GPL'
__version__ = '1.0.0'

import sys
import argparse
import libvirt
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-d','--domain', help='Domain libvirt',required=True)
parser.add_argument('-p','--pool',help='Pool ceph', required=True)
parser.add_argument('-i','--image',help='Volume ceph', required=True)
parser.add_argument('-t','--target',help='Device target', default='vdz')
args = parser.parse_args()

def getConnection():
  try:
    conn=libvirt.open("qemu:///system")
    return conn
  except libvirt.libvirtError, e:
    print e.get_error_message()
    sys.exit(1)

def delConnection(conn):
  try:
    conn.close()
  except:
    print get_error_message()
    sys.exit(1)

def getSecretUUID(conn, client):
  for secret in conn.listAllSecrets():
    username, stype = secret.usageID().split()
    if username == client: 
      uuid = secret.UUIDString()
  try:
    return uuid
  except NameError, e:
    print "Not UUID For this client name : %s." % name 
    print e
    sys.exit(1)

def attach_device(dom, uuid, pool, volume, dev):
  device = """\
    <disk type='network' device='disk'>
      <driver name='qemu' type='raw'/>
      <auth username='libvirt'>
        <secret type='ceph' uuid="{uuid}"/>
      </auth>
      <source protocol='rbd' name="{pool}/{volume}">
        <host name='192.168.102.100' port='6789'/>
        <host name='192.168.102.101' port='6789'/>
        <host name='192.168.102.102' port='6789'/>
      </source>
      <target dev="{dev}" bus='virtio'/>
    </disk>
  """
  device = device.format(uuid=uuid, pool=pool, volume=volume, dev=dev)
  dom.attachDevice(device)

if __name__ == '__main__':
  conn = getConnection()
  dom = conn.lookupByName(args.domain)
  attach_device( dom, getSecretUUID(conn, args.name), args.pool, args.image, args.target)
  delConnection(conn)
