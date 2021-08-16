#!/usr/bin/python3
from tqdm import tqdm
import vlc
import struct
import re
import os
import subprocess
import sys
import pyaudio
import RPi.GPIO as GPIO
import apa102
from pixels import Pixels
import time
import yaml
import argparse
import logging
import threading
import argparse
from datetime import datetime, timedelta
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
# Initialise things, lights loglevel, flags etc
pixels = Pixels()
parser = argparse.ArgumentParser()
parser.add_argument("--log", default='info', help='Set the log level (default: info)')
args = parser.parse_args()
loglevel = getattr(logging, args.log.upper(), logging.WARN)
logging.basicConfig(level=loglevel)	
gpiopinlight = 13
GPIO.setup(gpiopinlight, GPIO.OUT) # GPIO Assign mode
gpiopinheat = 12
GPIO.setup(gpiopinheat, GPIO.OUT) # GPIO Assign mode

def resetkettle():
	poweron=False
	pixels.off()
	GPIO.output(gpiopinheat, GPIO.LOW)
	return poweron

def boil():
	# Turn the relay on
	GPIO.output(gpiopinheat, GPIO.HIGH)
	# Visual Indicator of Heating
	pixels.wakeup()
	time.sleep(3)
	pixels.think()
	# Note the time it was turned on at
	turnedonat=datetime.now()
	poweron=True
	# The Kettle is on now, so we can move on
	return poweron

def main():
	
	try:
		#Initialise to off
		poweron=resetkettle()

		configfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.yaml')
		parser = argparse.ArgumentParser()
		parser.add_argument("--log", default='info', help='Set the log level (default: info)')
		args = parser.parse_args()
		loglevel = getattr(logging, args.log.upper(), logging.WARN)
		logging.basicConfig(level=loglevel)

		with open(configfile) as f:
			config = yaml.load(f, Loader=yaml.FullLoader)
		logging.info(config)
		
		while True:
			# If the kettle isn't on, check if it should be
			while poweron==False:
				# Check calendar for coffee in the next 10 minutes
				now = datetime.now()
				now_plus = now + timedelta(minutes = 10)
				result=subprocess.run(['gcalcli','--calendar',config['calendar']['name'],'search', config['calendar']['trigger'],str(now), str(now_plus)], stdout=subprocess.PIPE)
				logging.info(result.stdout.decode())
				waitforit ="No Event" in result.stdout.decode()
				if waitforit==False:
					logging.info("Matching appointment coming up, heating the water")
					poweron=boil()
				else:
					time.sleep(60)

			# The Kettle must have turned on, so we wait, then play an alarm?
			iterations=100
			heattimeseconds=int(config['relay']['closedfor'])*60

			notify = "Power to teasmade active for "+str(config['relay']['closedfor'])+" minutes"
			logging.info(notify)

			for i in tqdm(range(iterations)):
				time.sleep(heattimeseconds/iterations)

			# Been boiling for a while, time for a glorious fanfare
			logging.info("Alarm Music starting")
			brewalarm= vlc.MediaPlayer(config['alarm']['pathtotrack'])
			brewalarm.play()

			# Turn the kettle off. Teasmade should have already done this. Safety first etc
			poweron=resetkettle()
			
	except KeyboardInterrupt:  
		resetkettle()
		time.sleep(1)  
		logging.info("Interrupt: ctrl + c:")
		GPIO.cleanup()


if __name__ == '__main__':
	main()
