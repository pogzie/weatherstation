# Title: Python Wrapper for Sensor Data
# Author: Allan Paul "Pogz" Sy Ortile
# Date: 2017-03-21
# Version: 0.01 (2017-03-21)
# Notes:
#       - This assumes that you are allowing trusted devices to communicate to your endpoint.
#       - Proper backend SQL handling to prevent SQL injection. Duh.
#       - This python file SHOULD be at the same directory where the sensor apps are.

# Import stuff here
import time
from subprocess import Popen, PIPE

# Configuration Section
#       This is wher all the important values are set. The goal is to throw a curl that would do a PUT to your endpoint
#       given a key and all the needed parameters.

#       This is the FQDN or the IP address of your endpoint
ENDPOINT_HOST = "127.0.0.1"
#       This is the API location with a leading / and a trailing ? expecting variable name and values as its assembled
ENDPOINT_API_URL = "/weatherstation/index.php/api/put?"
#       For security sake, A KEY PLEASE!
ENDPOINT_KEY = "12345qwert"

#       This is the list of parameters the endpoint API is expecting
#       ie. http://localhost/weatherstation/index.php/api/put?key=1&temp=10
#       this is a list of the "key" and the "temp" (name) which is caught on the endpoint side
ENDPOINT_UNIX_TIME_NAME = "utm"
ENDPOINT_ID_DEVICE_NAME = "id"
ENDPOINT_TEMPERATURE_NAME = "tmp"
ENDPOINT_HUMIDITY_NAME = "hum"
ENDPOINT_BAROMETRIC_PRESURE_NAME = "bmp"
ENDPOINT_ALTITUDE_NAME = "alt"
ENDPOINT_WIND_SPEED_NAME = "wds"
ENDPOINT_WIND_DIRECTION_NAME = "wdn"
ENDPOINT_RAINFALL_NAME = "rnf"
ENDPOINT_SOLAR_RADIATION_NAME = "srd"
ENDPOINT_UV_INDEX_NAME = "uvi"
ENDPOINT_WATER_LEVEL_NAME = "wtr"
ENDPOINT_AIR_QUALITY_NAME = "air"


### DO NOT EDIT BEYOND THIS POINT (EXCEPT IF YOU ARE ADDING COMMANDS)###

#       This is the actual values of the sensor readings. By default value is null except id_device and temperature
ENDPOINT_UNIX_TIME = 0
ENDPOINT_ID_DEVICE = 0
ENDPOINT_TEMPERATURE = 0
ENDPOINT_HUMIDITY = 0
ENDPOINT_BAROMETRIC_PRESURE = 0
ENDPOINT_ALTITUDE = 0
ENDPOINT_WIND_SPEED = 0
ENDPOINT_WIND_DIRECTION = 0
ENDPOINT_RAINFALL = 0
ENDPOINT_SOLAR_RADIATION = 0
ENDPOINT_UV_INDEX = 0
ENDPOINT_WATER_LEVEL = 0
ENDPOINT_AIR_QUALITY = 0

# Function Section
#       As a caveat, this is the section that will call your C compiled apps that talks to the sensor and parses and
#       assigns it to a variable. You may have to add stuff here depending if you have other sensors that you may
#       need to read. Again, as an advice, dump everything as a single line, separated by commas with errors thrown as ERROR.
#       CAVEAT:
#               Python 3.5 or higher can use subprocess.run
#       ADDITIONAL NOTES:
#                http://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call

# Declare a function that eats the commands that you want to run
#       If output is error, repeat the command, else, return the value
#       NOTES:
#               This is a damn awful hastily written crap function. It does the job but is not the most optimized solution
#               and needs to be rewritten.
def run_command(COMMAND):
        command_output = ""
        # This is basically just an infinite loop with the return function as the easy way out
        while not command_output:
                p = Popen([COMMAND], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                SENSOR = p.communicate("")[0]
                if "ERROR" not in SENSOR:
                        # First off SENSOR contains a flat string
                        # Remove all new lines
                        SENSOR = SENSOR.strip('\n')
                        # Remove all spaces
                        SENSOR = SENSOR.replace(" ","")
                        # Split it into an array and return
                        return SENSOR.split(",")
                # Sleep for a while, dont hammer the sensor
                time.sleep(1)

### PUT YOUR COMMANDS HERE ###
# NOTE:
#       You need to know about ARRAYS. Seriously. The string is split into arrays for easy parsing.

### DHT11 COMMAND ###
# SENSOR_DHT will run the command, and get an array of values based from its output
SENSOR_DHT = run_command("./dht")
ENDPOINT_HUMIDITY = SENSOR_DHT[0]

### MPL13115A2 COMMAND ###
SENSOR_MPL = run_command("./mpl3115a2")
ENDPOINT_PRESSURE = SENSOR_MPL[0]
ENDPOINT_ALTITUDE = SENSOR_MPL[1]
ENDPOINT_TEMPERATURE = SENSOR_MPL[2]

### DEBUGGING ###
# Ouput the values of the items to be passed to the endpoint
print ENDPOINT_HUMIDITY
print ENDPOINT_PRESSURE
print ENDPOINT_ALTITUDE
print ENDPOINT_TEMPERATURE

# Strip everything before the = sign since we know what that is anyway

# Assemble the URL for cURLing
