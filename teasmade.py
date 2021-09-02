#!/usr/bin/python3
from tqdm import tqdm
import vlc
import struct
import re
import os
import subprocess
import sys
import pyaudio
import gpiozero
import apa102
from pixels import Pixels
import time
import yaml
import argparse
import logging
import threading
import argparse
from datetime import datetime, timedelta
# Initialise things, lights loglevel, flags etc
pixels = Pixels()
parser = argparse.ArgumentParser()
parser.add_argument("--log", default='info', help='Set the log level (default: info)')
args = parser.parse_args()
loglevel = getattr(logging, args.log.upper(), logging.WARN)
logging.basicConfig(level=loglevel)	
gpiosparerelay = 13 # Only one relay is currently used, this is the spare
gpiopinheat = 12
heatrelay = gpiozero.OutputDevice(gpiopinheat, active_high=True, initial_value=False)

def resetkettle():
	pixels.off()
	heatrelay.off()
	return

def boil(config):
	# Turn the relay on
	heatrelay.on()
	# Visual Indicator of Heating
	pixels.wakeup()
	time.sleep(3)
	pixels.think()
	# Pause for the time in the config file
	iterations=100
	heattimeseconds=int(config['relay']['closedfor'])*60
	notify = "Power to teasmade active for "+str(config['relay']['closedfor'])+" minutes"
	logging.info(notify)
            
	for i in tqdm(range(iterations)):
		time.sleep(heattimeseconds/iterations)

	return

def alarm(config):
	logging.info("Alarm Music starting")
	brewalarm= vlc.MediaPlayer(config['alarm']['pathtotrack'])
	brewalarm.play()
	return

def togglerelay():
	if heatrelay.value==1:
		print("On... Turning off")
		pixels.off()
		heatrelay.off()
	elif heatrelay.value==0:
		print("Off...Turning on")
		heatrelay.on()
		# Visual Indicator of Heating
		pixels.wakeup()
		time.sleep(1)
		pixels.think()
	return

def main():

	# Set up the button
	button = gpiozero.Button(17)
	button.when_pressed = togglerelay # Note missing brackets, it's a label

	configfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.yaml')
	parser = argparse.ArgumentParser()
	parser.add_argument("--log", default='info', help='Set the log level (default: info)')
	args = parser.parse_args()
	loglevel = getattr(logging, args.log.upper(), logging.WARN)
	logging.basicConfig(level=loglevel)

	with open(configfile) as f:
		config = yaml.load(f, Loader=yaml.FullLoader)
	logging.info(config)

	try:
		#Initialise to off
		poweron=resetkettle()
		
		while True:
			# Check calendar for coffee in the next 10 minutes
			now = datetime.now()
			lookahead = config['calendar']['lookahead']
			now_plus_start = now + timedelta(minutes = lookahead)
			now_plus_end= now + timedelta(minutes = lookahead+1)
			result=subprocess.run(['gcalcli','--calendar',config['calendar']['name'],'search', config['calendar']['trigger'],str(now_plus_start), str(now_plus_end)], stdout=subprocess.PIPE)
			logging.info(result.stdout.decode())
			waitforit =not(config['calendar']['trigger'] in result.stdout.decode())
			if waitforit==False:
				logging.info("Matching appointment coming up, heating the water")
				boil(config)
				# if boil completed without interrupt, play the alarm
				if heatrelay.value==1:
					alarm(config)
					# Turn the kettle off. Teasmade should have already done this. Safety first etc
					resetkettle()
			else:
				time.sleep(60)
			# Back to beginning of loop to check the calendar

	except KeyboardInterrupt:  
		resetkettle()
		time.sleep(1)  
		logging.info("Interrupt: ctrl + c:")
		heatrelay.close()


if __name__ == '__main__':
	main()
