"""
standalone module for turning off and on the monitor using an ultrasonic sensor.
adapted from https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
"""

import RPi.GPIO as GPIO
import time
import subprocess

# set variables
max_standing_distance = 200
min_standing_distance = 15
max_timeout = 20
timeout = 0
monitor_state = 1

# Initialise Pins
GPIO.setmode(GPIO.BOARD)
TRIG_PIN = 12
ECHO_PIN = 16

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def monitor_power(status, monitor_state):
	"""change state of monitor if it already hasnt changed"""
	if status == 0:
		print('turning monitor off')
		if monitor_state == 1:
			subprocess.call(['tvservice','-o'])
			print('off')
		return 0
	elif status == 1:
		print('turning monitor on')
		if monitor_state == 0:
			subprocess.call(['tvservice','-p'])
			print('on')
		return  1


print('GPIO Initialised')
print('Waiting For Sensor To Settle')
time.sleep(2)
print('')

try:
	while True:
		GPIO.output(TRIG_PIN, False)
		time.sleep(2)

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

		#print ("distance={0}cm".format(distance))

		# >10 & <3500 because my sensor seems to bug out because its stupid
		if distance > 10 and distance < 3500:
			if distance > min_standing_distance and distance < max_standing_distance:
				timeout = 0
				monitor_state = monitor_power(1, monitor_state)
		else:
			timeout = 0
			monitor_state = monitor_power(1, monitor_state)

		# Timeout 
		timeout += 1
		if timeout >= max_timeout:
			timeout = 0
			monitor_state = monitor_power(0, monitor_state)
			

except KeyboardInterrupt:
	GPIO.cleanup()

	# turn on monitor
	if monitor_state == 0:
		subprocess.call(['tvservice','-p'])

	print(" Quit ")