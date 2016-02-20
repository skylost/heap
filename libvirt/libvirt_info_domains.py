#!/usr/bin/env python

__author__  = 'weezhard'
__license__ = 'GPL'
__version__ = '1.0.0'

import libvirt
import sys
from xml.etree import ElementTree

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

def getXmlDesc(dom):
  return ElementTree.fromstring(dom.XMLDesc(0))

def getDomainName(xmltree):
  return xmltree.find('name').text

def getDomainVcpu(xmltree):
  return xmltree.find('vcpu').text

def getDomainMemory(xmltree):
  return int(xmltree.find('memory').text) / 1024 / 1024

if __name__=="__main__":
  conn = getConnection()   

  domlist = []
  header = (' Name ',' vCPU ',' RAM ')
  struct = dict(zip((0,1,2),(len(str(x)) for x in header)))
  
  # For all available domains.
  for id in conn.listDomainsID():
    dom=conn.lookupByID(id)
    name=getDomainName(getXmlDesc(dom))
    cpu=getDomainVcpu(getXmlDesc(dom))
    ram=getDomainMemory(getXmlDesc(dom))
    domlist.append((name, cpu, ram))

  for x,y,z in domlist:
    struct[0] = max(struct[0],len(str(x)))
    struct[1] = max(struct[1],len(str(y)))
    struct[2] = max(struct[2],len(str(z)))

  hyphen = ' | '.join('%%-%ss' % struct[i] for i in xrange(0,3))
  print '\n'.join(('-|-'.join( struct[i]*'-' for i in xrange(3)),
                   hyphen % header,
                   '-|-'.join( struct[i]*'-' for i in xrange(3)),
                   '\n'.join( hyphen % (x,y,z) for x,y,z in domlist ),
                   '-|-'.join( struct[i]*'-' for i in xrange(3) )))

  delConnection(conn)
