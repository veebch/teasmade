#!/usr/bin/python3

import re
import os
import subprocess
import sys
import pyaudio
import RPi.GPIO as GPIO
import apa102
import time
import yaml
import argparse
import logging
from datetime import datetime, timedelta

def main():
	poweron=False
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
			print(now)
			now_plus_10 = now + timedelta(minutes = 10)
			print(now_plus_10)
			result=subprocess.run(['gcalcli','--calendar',config['calendar']['name'],'search', config['calendar']['trigger'],str(now), str(now_plus_10)], stdout=subprocess.PIPE)
			print(result.stdout.decode())
			notyet ="No Event" in result.stdout.decode()
			if notyet==False:
				print("coffeetime")
    		#if yes, 
    			#set poweron=True
    			#Turn on LED
    			#set Ontime
    			#break
			time.sleep(180)
    	# Should I turn off yet?
    	#if yes,
    		#poweron=false
    		#led off


if __name__ == '__main__':
    main()
