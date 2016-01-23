#!/usr/bin/env ruby

#libs
gem('rbvmomi','> 1.6.0')
%w(trollop rbvmomi rbvmomi/trollop json).each{|f| require f}

#declaration des variables#
USERNAME = ENV["VMWARE_USERNAME"] || "root"
PASSWORD = ENV["VMWARE_PASSWORD"] || "admin"
ADDRESS = ENV["VMWARE_ADDRESS"] || "192.168.1.200"
PORT = ENV["VMWARE_PORT"] || 443

if ARGV.length == 1
  VM_NAME = ARGV[0]

  # Signal handling ctrl+c
  trap("SIGINT") { exit 130 }

  #vcenter connection
  VIM = RbVmomi::VIM
  vim = VIM.connect(:host=>ADDRESS,:port=>PORT,:insecure=>true,:user=>USERNAME,:password=>PASSWORD)
  dc = vim.serviceInstance.content.rootFolder.traverse("Datacenter", VIM::Datacenter)

  folders = dc.vmFolder.children
  vms = []
  i = 0
  while folders.any? && i <= 200
    i += 1
    vms += folders.select{|e| e.is_a?(VIM::VirtualMachine)}
    folders.reject!{|e| e.is_a?(VIM::VirtualMachine)}
    folders.map!{|f| f.children}
    folders.flatten!
  end
  
  vms.each do |vm|
    next unless vm.name == vm_name 
    conf = vm.config
    hw = conf.hardware

    # array containing all devices ... to be sorted
    netcards = hw.device.select{|dev| dev.is_a?(VIM::VirtualEthernetCard)}
    netcards.each do |card|
    puts "#{vm.name} #{card.backing.network.name} #{card.macAddress}"
  end

else puts "\n    USAGE : #{__FILE__} [hostname] \n\n"
end
