#!/usr/bin/python

import virtualbox
import sys

vbox = virtualbox.VirtualBox()
for vm in vbox.machines:
  print(vm.name)
