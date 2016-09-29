"""
standalone module for turning off and on the monitor using an ultrasonic sensor.
adapted from https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
"""

import RPi.GPIO as GPIO
import time

# Initialise Pins
GPIO.setmode(GPIO.BOARD)
TRIG_PIN = 12
ECHO_PIN = 16

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

print('GPIO Initialised')
print ('Waiting For Sensor To Settle')
GPIO.output(TRIG_PIN, False)
time.sleep(2)

try:
	while True:
		GPIO.output(TRIG_PIN, False)
		time.sleep(1)

		# send burst
		GPIO.output(TRIG_PIN, True)
		time.sleep(0.00001)
		GPIO.output(TRIG_PIN, False)

		# measure incoming burst
		while GPIO.input(ECHO_PIN)==0:
			pulse_start = time.time()

		while GPIO.input(ECHO_PIN)==1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = round(pulse_duration * 17150, 2)

		print ("distance={0}cm".format(distance))

		# delay half a second
		#time.sleep(500)

except KeyboardInterrupt:
	GPIO.cleanup()
	print(" Quit ")