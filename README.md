# Hue Motion support for Domoticz
This Python script is able to communicate with the Philips Hue Bridge and fetch the status of Hue Motion sensor devices including PIR, Presence, temperature, ambient light and dusk detection. It can also flash supported lights.

### Understanding the variables ###

- light_id is a default Hue lamp, it can be set to 0 if none are available
- domoticz_ip is the local IP address of your Domoticz instance, if you use a port other than 80 then set the port number aswell (e.g. 192.168.0.2:8080)
- auth_username is your Domoticz login username, if not set it can be left empty
- auth_password is your Domoticz login password, if not set it can be left empty
- hue_ip is the local IP address of your Hue Bridge
- hue_username is the Hue Bridge authentication token
- sensor_id is the ID assigned by the Hue Bridge to your Hue Motion sensor
- idx is the ID of your Domoticz device

### Domoticz integration ###

1. Put the script in your Domoticz scripts/python/... folder
2. Change the default variables to match your environment:
- light_id
- domoticz_ip
- auth_username
- auth_password
- hue_ip
- hue_username
3. Add virtual/dummy switches in Domoticz (see https://www.domoticz.com/wiki/Wemo#Creating_Dummy_Switches) for the following sensors:
- Name: xxx (Hue/PIR), Sensor Type: Switch
4. Open the Switches screen and edit the xxx (Hue/PIR) device
- Change the Switch Type to: Motion Sensor
- Set the Off Delay to 600 seconds
5. Add a crontab entry to run hue-motion.py every 5 minutes

### Standalone usage ###

The script can also be executed in standalone mode: 

    $ python hue-motion.py flash
    $ python hue-motion.py motion
    $ python hue-motion.py motion refresh
