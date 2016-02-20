#!/usr/bin/env ruby

#@author::   'weezhard'
#@usage::    'Delete projects rundeck'
#@licence::  'GPL'
#@version:   1.0.0

require 'uri'
require 'rubygems'
require 'json'
require 'net/http'
require 'optparse'

# default options
options = {}
options[:url]   = "localhost"
options[:port]  = 4440
options[:token] = "kfC91qhEZBMNikzY5NFNEywqhOnBKtSC"
options[:json]   = false

# parse options
optparse = OptionParser.new do |opts|
  opts.banner = "Usage: #{$0} [options]"
  opts.on('-u', '--url URL', "URL for Rundeck server", String) { |val| options[:url] = val }
  opts.on('-p', '--port PORT', "PORT for Rundeck server", Integer) { |val| options[:port] = val }
  opts.on('-t', '--token TOKEN', "TOKEN for Rundeck server", String) { |val| options[:token] = val }
  opts.on('-j', '--json', "List of projects JSON") { options[:json] = true }
  opts.on('-h', '--help') do 
    puts opts
    exit
  end
end

optparse.parse!

# Get Projects
@headers = {"X-Rundeck-Auth-Token" => options[:token],
           "Accept" => "application/json"}

def getProjects(url, port)
  uri = URI.parse("http://#{url}:#{port}/api/1/projects")
  http = Net::HTTP.new(uri.host, uri.port)
  resp = http.get(uri.path, @headers)
  projects = resp.body
  return JSON.parse(projects)
end

if __FILE__ == $0
  if options[:json] == true
    for project in getProjects(options[:url], options[:port])
      puts project
    end
  else
    for project in getProjects(options[:url], options[:port])
      puts project["name"]
    end
  end
end
