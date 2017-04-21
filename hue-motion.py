#!/usr/bin/python

import sys

# Default lamp
light_id = 'xxx'

if len(sys.argv) == 1:
  print "Missing required %action %light"
  quit()
elif len(sys.argv) >= 2:
  action = str(sys.argv[1])
  if len(sys.argv) == 3:
    light_id = str(sys.argv[2])

import os
import json
import requests
from requests.auth import HTTPBasicAuth
import urllib2
import base64
import datetime as dt

def domoticzrequest (url):
  
  global auth_username
  global auth_password
  
  request = urllib2.Request(url)
  base64string = base64.b64encode('%s:%s' % (auth_username, auth_password))
  request.add_header("Authorization", "Basic %s" % base64string)
  response = urllib2.urlopen(request)
  return response.read()

domoticz_ip = 'xxx'
auth_username = 'xxx'
auth_password = 'xxx'

hue_ip = 'xxx'
hue_username = 'xxx'

command_option = ''

if action == 'flash':

  args = {"alert": "select"}

  # Check for all lamps
  if light_id == 'all':
    light_id = [0,1,2,3,4,5,6]
    for i in range(len(light_id)):
      url = 'http://' + hue_ip + '/api/' + hue_username + '/lights/' + str(light_id[i]) + '/state'
      response = requests.put(url, data=json.dumps(args))
  else:
    url = 'http://' + hue_ip + '/api/' + hue_username + '/lights/' + light_id + '/state'
    response = requests.put(url, data=json.dumps(args))

  # Notify Domoticz logging
  url = 'http://' + domoticz_ip + '/json.htm?type=command&param=addlogmessage&message=Hue-flash-logging-from-Raspberry-Pi'
  r = requests.get(url, auth=HTTPBasicAuth(auth_username, auth_password))

elif action == 'motion':

  # Check for sensors

  # If light_id is set just check for motion
  if light_id <> 'xxx':

    # Presence - Bedroom
    sensor_id = 'xxx'
    url = 'http://' + hue_ip + '/api/' + hue_username + '/sensors/' + sensor_id
    json_object = json.loads(domoticzrequest(url))
    presence = json_object["state"]["presence"]
    print 'Presence (Bedroom): ' + str(presence)

    idx = 'xxx'
    if str(presence) == 'True':
      presence = '1'
    else:
      presence = '0'

    # Get existing value
    domoticzurl = "http://" + domoticz_ip + "/json.htm?type=devices&rid=" + idx
    device="pid"
    json_object = json.loads(domoticzrequest(domoticzurl))
    # print json_object
    if json_object["status"] == "OK":
      if json_object["result"][0]["idx"] == idx:
        existing_presence = json_object["result"][0]["Data"]
        existing_currentime = json_object['ServerTime'];
        existing_lastupdate = json_object["result"][0]["LastUpdate"]
        if str(existing_presence) == 'On':
          existing_presence = '1'
        else:
          existing_presence = '0'

    # print existing_presence + ' vs ' + presence
    if existing_presence == presence:
      print 'Presence unchanged'
    else:
      d1 = dt.datetime( int(existing_lastupdate[0:4]), int(existing_lastupdate[5:7]), int(existing_lastupdate[8:10]), int(existing_lastupdate[11:13]), int(existing_lastupdate[14:16]), int(existing_lastupdate[17:19]) )
      d2 = dt.datetime( int(existing_currentime[0:4]), int(existing_currentime[5:7]), int(existing_currentime[8:10]), int(existing_currentime[11:13]), int(existing_currentime[14:16]), int(existing_currentime[17:19]) )
      # Check if 600 seconds has passed if existing value was on
      if existing_presence == '1' and int( (d2-d1).total_seconds() ) < 600:
        print 'Presence unchanged; timeout still in effect'
        url = 'http://' + domoticz_ip + '/json.htm?type=command&param=addlogmessage&message=Presence-unchanged-timeout-still-in-effect'
        r = requests.get(url, auth=HTTPBasicAuth(auth_username, auth_password))
      else:
        url = 'http://' + domoticz_ip + '/json.htm?type=command&param=udevice&idx=' + idx + '&nvalue=' + presence + '&svalue='
        r = requests.get(url, auth=HTTPBasicAuth(auth_username, auth_password))
        print 'Presence updated'
        url = 'http://' + domoticz_ip + '/json.htm?type=command&param=addlogmessage&message=Presence-updated'
        r = requests.get(url, auth=HTTPBasicAuth(auth_username, auth_password))

    # Notify Domoticz logging
    url = 'http://' + domoticz_ip + '/json.htm?type=command&param=addlogmessage&message=Hue-motion-quick-logging-from-Raspberry-Pi'
    r = requests.get(url, auth=HTTPBasicAuth(auth_username, auth_password))

  else:

    # Temperature - Bedroom
    sensor_id = 'xxx'
    url = 'http://' + hue_ip + '/api/' + hue_username + '/sensors/' + sensor_id
    json_object = json.loads(domoticzrequest(url))
    temperature = json_object["state"]["temperature"]

    idx = 'xxx'
    temperature_before = str(temperature)[:2]
    temperature_after = str(temperature)[-2:]
    temperature = temperature_before + '.' + temperature_after
    print 'Temperature (Bedroom): ' + str(temperature)
    url = 'http://' + domoticz_ip + '/json.htm?type=command&param=udevice&idx=' + idx + '&nvalue=0&svalue=' + temperature
    r = requests.get(url, auth=HTTPBasicAuth(auth_username, auth_password))

    # Ambient light - Bedroom
    sensor_id = 'xxx'
    url = 'http://' + hue_ip + '/api/' + hue_username + '/sensors/' + sensor_id
    json_object = json.loads(domoticzrequest(url))
    dark = json_object["state"]["dark"]
    daylight = json_object["state"]["daylight"]
    light_level = json_object["state"]["lightlevel"]
    print 'Dark (Bedroom): ' + str(dark)
    print 'Daylight (Bedroom): ' + str(daylight)
    print 'Light level (Bedroom): ' + str(light_level)

    idx = 'xxx'
    url = 'http://' + domoticz_ip + '/json.htm?type=command&param=udevice&idx=' + idx + '&svalue=' + str(light_level)
    r = requests.get(url, auth=HTTPBasicAuth(auth_username, auth_password))

    idx = 'xxx'
    if str(daylight) == 'True':
      daylight = '1'
    else:
      daylight = '0'
    url = 'http://' + domoticz_ip + '/json.htm?type=command&param=udevice&idx=' + idx + '&nvalue=' + daylight + '&svalue='
    r = requests.get(url, auth=HTTPBasicAuth(auth_username, auth_password))

    # Dark is natively supported by Domoticz via the Dusk sensor
    # idx = 'xxx'
    # if str(dark) == 'True':
    #   dark = '1'
    # else:
    #   dark = '0'
    # url = 'http://' + domoticz_ip + '/json.htm?type=command&param=udevice&idx=' + idx + '&nvalue=' + dark + '&svalue='
    # r = requests.get(url, auth=HTTPBasicAuth(auth_username, auth_password))

    # Notify Domoticz logging
    url = 'http://' + domoticz_ip + '/json.htm?type=command&param=addlogmessage&message=Hue-motion-logging-from-Raspberry-Pi'
    r = requests.get(url, auth=HTTPBasicAuth(auth_username, auth_password))

print('Hue command sent')
