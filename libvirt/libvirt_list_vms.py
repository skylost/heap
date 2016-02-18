#!/usr/bin/python

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

if __name__ == '__main__':
  conn = getConnection()
  getAllDomains(conn)
  delConnection(conn)
