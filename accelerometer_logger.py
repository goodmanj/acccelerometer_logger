# accelerometer_logger.py
#
# Interfaces a MSA311 3-axis accelerometer with an Adafruit Adalogger RP2040 using CircuitPython.  Writes 3-axis
# acceleration data to the SD card in a file named "acceldata.csv".  The MSA311 should be connected via I2C: the
# Adalogger's QWIIC connector is convenient for this purpose.
#
# IMPORTANT: This code will *overwrite* the acceldata.csv file every time the Adalogger is powered on or reset.
# Be sure to copy this file to your local computer if you want to save it!
#
# The following Python libraries must be installed on the Adalogger in order to use this code:
#
# adafruit_register/
# adafruit_msa3xx.mpy
#
# For more information about the hardware and software used for this project, see:
# https://learn.adafruit.com/adafruit-feather-rp2040-adalogger/install-circuitpython
# https://learn.adafruit.com/msa301-triple-axis-accelerometer/
# https://docs.circuitpython.org/projects/msa301/en/latest/
# https://docs.circuitpython.org/projects/bundle/en/latest/drivers.html
# https://docs.python.org/3/tutorial/inputoutput.html
#

# User-changeable parameters
sample_rate = 10  # Acceleration samples stored per second

# Import modules
import time
import board
import adafruit_msa3xx
import digitalio

# set up blinky led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Blink the LED slowly to indicate a problem.
def slowblink(blinkrate=1):
    while True:
        led.value = True
        time.sleep(1./blinkrate)
        led.value = False
        time.sleep(1./blinkrate)

# Set up MSA311 accelerometer
try:
    i2c = board.I2C()
    accelerometer = adafruit_msa3xx.MSA311(i2c)
except:
    print('Error: could not initialize accelerometer, check connections.')
    slowblink(2)

# Open file
try:
    f = open("/sd/acceldata.csv","w")
except:
    print('Error: could not communicate with SD card.  Is it inserted?')
    slowblink()

while True:  # Repeat forever
  led.value = True  # Turn on LED
  (ax,ay,az) = accelerometer.acceleration
  print(f'{ax}, {ay}, {az}')       # Print acceleration components to serial connection
  try:
    f.write(f'{ax}, {ay}, {az}\n')   # Write acceleration components to SD card
    f.flush()  # Forces the data to be written immediately
  except:
    print('Error: could not write to SD card.  Is it inserted?')
    slowblink()

  led.value = False # Turn off LED
  time.sleep(1./sample_rate)
