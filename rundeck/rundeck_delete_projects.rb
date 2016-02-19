#!/usr/bin/env ruby

#@author::   'weezhard'
#@usage::    'Delete projects rundeck'
#@licence::  'GPL'
#@version:   1.0.0

require 'uri'
require 'time'
require 'rubygems'
require 'json'
require 'net/http'
require 'optparse'

# default options
options = {}
options[:url]   = "localhost"
options[:port]  = 4440
options[:token] = "kfC91qhEZBMNikzY5NFNEywqhOnBKtSC"
options[:all]   = false

# parse options
optparse = OptionParser.new do |opts|
  opts.banner = "Usage: #{$0} [options]"
  opts.on('-u', '--url URL', "URL for Rundeck server", String) { |val| options[:url] = val }
  opts.on('-p', '--port PORT', "PORT for Rundeck server", Integer) { |val| options[:port] = val }
  opts.on('-t', '--token TOKEN', "TOKEN for Rundeck server", String) { |val| options[:token] = val }
  opts.on('-p', '--project PROJECT', "PROJECT Rundeck delete", String) { |val| options[:project] = val }
  opts.on('-a', '--all', "DELETE All projects") { options[:all] = true }
  opts.on('-h', '--help') do 
    puts opts
    exit
  end
end

optparse.parse!

# if we have not found a projet
raise OptionParser::MissingArgument if options[:project].nil? and options[:all] == false

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

def deleteProject(project)
  uri = URI.parse("http://localhost:4440/api/11/project/#{project}")
  http = Net::HTTP.new(uri.host, uri.port)
  resp = http.delete(uri.path, @headers)
  puts resp.body
end

if __FILE__ == $0
  if options[:all] == true
    projects = getProjects(options[:url], options[:port])
    for project in projects
      deleteProject(project["name"])
    end
  else
    deleteProject(options[:project])
  end
end
