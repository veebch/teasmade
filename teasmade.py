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

def main():
	pixels = Pixels()
	parser = argparse.ArgumentParser()
	parser.add_argument("--log", default='info', help='Set the log level (default: info)')
	args = parser.parse_args()
	interruptflag=False
	alarmplaying=False
	loglevel = getattr(logging, args.log.upper(), logging.WARN)
	logging.basicConfig(level=loglevel)
	try:

		lights=Pixels()
		GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
		BUTTON = 17
		GPIO.setup(BUTTON, GPIO.IN) 
		gpiopinlight = 13
		GPIO.setup(gpiopinlight, GPIO.OUT) # GPIO Assign mode
		gpiopinheat = 12
		GPIO.setup(gpiopinheat, GPIO.OUT) # GPIO Assign mode
		#Initialise to off
		poweron=False
		pixels.off()
		GPIO.output(gpiopinheat, GPIO.LOW)

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
			while poweron==False:
				#Check calendar for coffee in the next 10 minutes
				now = datetime.now()
				now_plus = now + timedelta(minutes = 8)
				result=subprocess.run(['gcalcli','--calendar',config['calendar']['name'],'search', config['calendar']['trigger'],str(now), str(now_plus)], stdout=subprocess.PIPE)
				logging.info(result.stdout.decode())
				notyet ="No Event" in result.stdout.decode()
				if notyet==False:
					logging.info("Matching appointment coming up, heating the water")
					GPIO.output(gpiopinheat, GPIO.HIGH)
					pixels.wakeup()
					time.sleep(3)
					pixels.think ()
					turnedonat=datetime.now()
					poweron=True
					break
				time.sleep(60)
			# Should I turn off yet?
			iterations=100
			heattimeseconds=int(config['relay']['closedfor'])*60
			print("Power to teasmade active for "+str(config['relay']['closedfor'])+" minutes")
			for i in tqdm(range(iterations)):
				state = GPIO.input(BUTTON)
				if not state:
					GPIO.output(gpiopinheat, GPIO.LOW)
					pixels.off()
					poweron=False
					if alarmplaying:
						brewalarm.quit()
					logging.info("Heating interrupted by button press")
					interruptflag=True
					break
				time.sleep(heattimeseconds/iterations)
			# Fanfare
			if interruptflag==True:
				logging.info("Waiting for 10 minutes before checking again")
				time.sleep(600)	
			else:
				logging.info("Alarm Music starting")
				brewalarm= vlc.MediaPlayer(config['alarm']['pathtotrack'])
				brewalarm.play()
				alarmplaying=True
			GPIO.output(gpiopinheat, GPIO.LOW)
			poweron=False
			alarmplaying=False
			pixels.off()
			time.sleep(1)
	except KeyboardInterrupt:  
		pixels.off()
		time.sleep(1)  
		logging.info("Interrupt: ctrl + c:")
		GPIO.cleanup()


if __name__ == '__main__':
	main()
