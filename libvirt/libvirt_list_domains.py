#!/usr/bin/env python

__author__  = 'weezhard'
__license__ = 'GPL'
__version__ = '1.0.0'

import libvirt
import sys

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

def getAllDomains(conn):
  vms = conn.listAllDomains(0)
  if len(vms) != 0:
    for vm in vms:
      print(vm.name())
  else:
    print('None')

def getAllSecrets(conn):
  secrets = conn.listAllSecrets()
  if len(secrets) != 0:
    for secret in secrets:
      print secret
  else:
    print('None')

if __name__ == '__main__':
  conn = getConnection()
  getAllSecrets(conn)
  delConnection(conn)
