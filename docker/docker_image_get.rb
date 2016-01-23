#!/usr/bin/env ruby

require 'docker'

# Environment variables
USERNAME = ENV["DOCKER_USERNAME"] || "root"
PASSWORD = ENV["DOCKER_PASSWORD"] || "admin"
URL = ENV["DOCKER_URL"] || "unix:///var/run/docker.sock"

puts Docker.version
puts Docker.info
puts Docker.url
puts Docker::Image.all({}, Docker::Connection.new(URL, {}))
#puts Docker::Containers.all({}, Docker::Connection.new(URL, {}))
