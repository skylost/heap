#!/usr/bin/python

import libvirt
import sys

conn=libvirt.open("qemu:///system")
if conn == None:
    print('Failed to open connection to qemu:///system', sys.stderr)
    exit(1)

#vms = conn.listDefinedDomains()
#print '\n'.join(vms)
vms = conn.listAllDomains(0)
if len(vms) != 0:
    for vm in vms:
        print(vm.name())
else:
    print('None')

conn.close()
exit(0)
