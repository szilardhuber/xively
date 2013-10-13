#!/usr/bin/env python

import subprocess
import xively
import datetime
import time
import requests

FEED_ID = "<xively feed id>"
API_KEY = "<xively API key>"

api = xively.XivelyAPIClient(API_KEY)

""" A series of MAC address - Channel name pairs """
devices = { '00:00:00:00:00:00': 'My device' }

""" Used for running queries in a loop. Will be replaced later for a more elegant solution """
online = {  '00:00:00:00:00:00': False }

""" Number of tries in a minute to check if a device is online.
	For mobile devices it seems to need more tries to catch them online as they seem to
	work such a way that they come online for a short time and 
	go offline again almost immediately. """
number_of_tries = 10

def get_datastream(feed, stream_name):
	""" function to return a datastream object. This either creates a new datastream,
	or returns an existing one """
  try:
    datastream = feed.datastreams.get(stream_name)
    return datastream
  except:
    datastream = feed.datastreams.create(stream_name,)
    return datastream

def get_online_devices():
	ret = ''
	proc1 = subprocess.Popen("sudo nmap -sP 192.168.0.1/24", stdout=subprocess.PIPE, shell=True)
	out, err = proc1.communicate()
	return [ line[13:30] for line in out.split('\n') if 'MAC Address' in line], out

def run():
	feed = api.feeds.get(FEED_ID)

	for i in range(0, number_of_tries):
		online_devices, raw_output = get_online_devices()
		for mac_address in devices:
			if online[mac_address]:
				continue
			print 'testing device: ' + devices[mac_address]
			if mac_address in online_devices:
				print devices[mac_address] + ' is online'
				online[mac_address] = True
		time.sleep(0.75 / number_of_tries)

	for mac_address in devices:
		datastream = get_datastream(feed, devices[mac_address])
		if online[mac_address]:
			datastream.current_value = 1
		else:
			datastream.current_value = 0
		datastream.at = datetime.datetime.utcnow()
		try:
			datastream.update()
		except requests.HTTPError as e:
			print "HTTPError({0}): {1}".format(e.errno, e.strerror)
	for found_device in online_devices:
		if found_device not in devices:
			print found_device
			print raw_output

run()
