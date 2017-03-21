# PogzNet Weather Station

## Introduction
This is just a simple Raspberry Pi based weather station. All sensor data are gathered via C programs which is then wrapped around Python to be able to do parsing, formatting and finally submission to the reporting server. 

A simple architecture for this setup would be

```
              +---------------+   +-----------------------+
  +-------+   |Raspberry Pi   |   |Report Server          |
  |Sensors+---> Sensor reader +---> API to accept readings|
  +-------+   | Python wrapper|   | MySQL Server          |
              +---------------+   | Graphing              |
                                  +-----------------------+
```

## Bill of Materials
- 40$ Raspberry Pi - https://www.adafruit.com/products/3055
  - Obviously you need this. Older versions of the RPi will do as long as it can accommodate all your sensors
- 10$ MPL3115A2 I2C Barometric Pressure/Altitude/Temperature Sensor - https://www.adafruit.com/products/1893
  - Accurate enough sensor for pressure, altitude and temp
- 6$ Gravity DHT11 Temperature Humidity Sensor For Arduino https://www.dfrobot.com/product-174.html
  - The MPL3115A2 reads better temperature than this, this is mainly for humidity
- 50c Headers (for DHT11) - https://www.adafruit.com/products/3002
  - For the MLP, you could wire it directly and skip this
- 2$ Female-Male/Male-Male/Male-Female Jumpers - https://www.adafruit.com/products/1957
  - Depending on the need, but for prototyping, get this and a breadboard
- 3$ Breadboard - https://www.dfrobot.com/product-575.html
  - For prototyping purposes. Get a bigger one if you have a bunch of sensors
  
## Collection Node Setup
The collection node will be your Raspberry Pi with the sensors hooked up. Its recommended to just remotely configure it via ssh. 

You will need to enable I2C via `raspi-config` (I2C on Pi - https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial) to be able to read data from the I2C pins. Dont forget to install i2c tools via `apt-get install i2c-tools` and reboot your Pi after setting this up.

You will also need to install a neat little tool called WiringPi http://wiringpi.com/download-and-install/. This will help you debug and the modules included are sometimes used in the code we will be using.

### Source Code Used for Sensors
I have sourced out a couple of source codes already written for the sensors mentioned above

- DHT11 (and 22) - http://www.uugear.com/portfolio/read-dht1122-temperature-humidity-sensor-from-raspberry-pi/
- MPL3115A2 - https://github.com/ControlEverythingCommunity/MPL3115A2

One important note to consider is that I simplified the outputs to look like this: 

```
root@PogzPi1:/home/pi# ./mpl3115a2 
Pressure = 100.66, Altitude = 55.56, Temp = 31.00
root@PogzPi1:/home/pi# ./dht
Humidity = 42.0, Temp = 30.0
```

For any errors, it will output an `ERROR`. The logic behind this is that parsing the output via Python would be easier. All are in one line separated by a comma. Catching the error would also be easier since it generally outputs a universal `ERROR` if something goes wrong. 
