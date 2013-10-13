#!/usr/bin/env python
 
import os
import xively
import subprocess
import time
import datetime
import requests
from decimal import *
 
# extract feed_id and api_key from environment variables
FEED_ID = "<xively feed id>"
API_KEY = "<xively api key>"
 
# initialize api client
api = xively.XivelyAPIClient(API_KEY)
 
# function to read 1 minute load average from system uptime command
def read_loadavg():
  return subprocess.check_output(["awk '{print $1}' /proc/loadavg"], shell=True)
 
# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream(feed):
  try:
    datastream = feed.datastreams.get("load")
    return datastream
  except:
    datastream = feed.datastreams.create("load",)
    return datastream
 
# main program entry point - runs continuously updating our datastream with the
# current 1 minute load average
def run():
  print "run"
  feed = api.feeds.get(FEED_ID)
  datastream = get_datastream(feed)
  datastream.max_value = None
  datastream.min_value = None
 
  load_avg = read_loadavg()
 
  datastream.current_value = str(Decimal(load_avg) * 100)
  datastream.at = datetime.datetime.utcnow()
  try:
    print "updating datastream"
    datastream.update()
  except requests.HTTPError as e:
    print "HTTPError({0}): {1}".format(e.errno, e.strerror)
 
 
run()