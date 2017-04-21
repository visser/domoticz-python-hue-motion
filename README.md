# Hue Motion support for Domoticz
This Python script is able to communicate with the Philips Hue Bridge and fetch the status of Hue Motion sensor devices including PIR, Presence, temperature, ambient light and dusk detection. It can also flash supported lights.

### Domoticz integration ###

1. Put the script in your Domoticz scripts/python/... folder
2. Change the default variables to match your environment:
2.1. light_id
2.1. domoticz_ip
2.2. auth_username
2.3. auth_password
2.4. hue_ip
2.5. hue_username
3. Add virtual/dummy switches in Domoticz (see https://www.domoticz.com/wiki/Wemo#Creating_Dummy_Switches) for the following sensors:
3.1. Name: xxx (Hue/PIR), Sensor Type: Switch
4. Open the Switches screen and edit the xxx (Hue/PIR) device
4.1. Change the Switch Type to: Motion Sensor
4.2. Set the Off Delay to 600 seconds
5. Add a crontab entry to run hue-motion.py every 5 minutes

### Standalone usage ###

The script can also be executed in standalone mode: 

    $ python hue-motion.py flash
    $ python hue-motion.py motion
    $ python hue-motion.py motion refresh