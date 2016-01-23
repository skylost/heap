#!/usr/bin/env ruby

#libs
gem('rbvmomi','> 1.6.0')
%w(trollop rbvmomi rbvmomi/trollop json).each{|f| require f}

# Environment variables
USERNAME = ENV["VMWARE_USERNAME"] || "root"
PASSWORD = ENV["VMWARE_PASSWORD"] || "admin"
HOST = ENV["VMWARE_HOST"] || "localhost"
PORT = ENV["VMWARE_PORT"] || 443

if ARGV.length == 2
  VM_NAME = ARGV[0]
  CM_NAME = ARGV[1]

  # Signal handling ctrl+c
  trap("SIGINT") { exit 130 }

  #vcenter connection
  VIM = RbVmomi::VIM
  vim = VIM.connect(:host=>HOST,:port=>PORT,:insecure=>true,:user=>USERNAME,:password=>PASSWORD)
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
    next unless vm.name == VM_NAME
    conf = vm.config
    hw = conf.hardware
    case CM_NAME
      when 'on'
	    vm.PowerOnVM_Task.wait_for_completion
      when 'off'
	    vm.PowerOffVM_Task.wait_for_completion
      when 'reset'
	    vm.ResetVM_Task.wait_for_completion
      when 'suspend'
	    vm.SuspendVM_Task.wait_for_completion
      when 'destroy'
	    vm.Destroy_Task.wait_for_completion
    else
	    abort "invalid command"
    end
  end

else puts "\n    USAGE : #{__FILE__} [hostname] [cmdname] \n\n"
end
