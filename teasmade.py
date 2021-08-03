#!/usr/bin/python3


from tqdm import tqdm
import struct
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
import threading
from datetime import datetime, timedelta
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

class Pixels:
    PIXELS_N = 3

    def __init__(self):
        self.basis = [0] * 3 * self.PIXELS_N
        self.basis[0] = 2
        self.basis[3] = 1
        self.basis[4] = 1
        self.basis[7] = 2

        self.colors = [0] * 3 * self.PIXELS_N
        self.dev = apa102.APA102(num_led=self.PIXELS_N)

        self.next = threading.Event()
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def wakeup(self, direction=0):
        def f():
            self._wakeup(direction)

        self.next.set()
        self.queue.put(f)

    def listen(self):
        self.next.set()
        self.queue.put(self._listen)

    def think(self):
        self.next.set()
        self.queue.put(self._think)

    def speak(self):
        self.next.set()
        self.queue.put(self._speak)

    def off(self):
        self.next.set()
        self.queue.put(self._off)

    def _run(self):
        while True:
            func = self.queue.get()
            func()

    def _wakeup(self, direction=0):
        for i in range(1, 25):
            colors = [i * v for v in self.basis]
            self.write(colors)
            time.sleep(0.01)

        self.colors = colors

    def _listen(self):
        for i in range(1, 25):
            colors = [i * v for v in self.basis]
            self.write(colors)
            time.sleep(0.01)

        self.colors = colors

    def _think(self):
        colors = self.colors

        self.next.clear()
        while not self.next.is_set():
            colors = colors[3:] + colors[:3]
            self.write(colors)
            time.sleep(0.2)

        t = 0.1
        for i in range(0, 5):
            colors = colors[3:] + colors[:3]
            self.write([(v * (4 - i) / 4) for v in colors])
            time.sleep(t)
            t /= 2

        # time.sleep(0.5)

        self.colors = colors

    def _speak(self):
        colors = self.colors
        gradient = -1
        position = 24

        self.next.clear()
        while not self.next.is_set():
            position += gradient
            self.write([(v * position / 24) for v in colors])

            if position == 24 or position == 4:
                gradient = -gradient
                time.sleep(0.2)
            else:
                time.sleep(0.01)

        while position > 0:
            position -= 1
            self.write([(v * position / 24) for v in colors])
            time.sleep(0.01)

        # self._off()

    def _off(self):
        self.write([0] * 3 * self.PIXELS_N)

    def write(self, colors):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(colors[3*i]), int(colors[3*i + 1]), int(colors[3*i + 2]))

        self.dev.show()


pixels = Pixels()

def main():
	lights=Pixels()
	GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
	gpiopinlight = 13
	GPIO.setup(gpiopinlight, GPIO.OUT) # GPIO Assign mode
	gpiopinheat = 12
	GPIO.setup(gpiopinheat, GPIO.OUT) # GPIO Assign mode
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
				GPIO.output(gpiopinheat, GPIO.HIGH)
				pixels.wakeup()
				turnedonat=datetime.now()
				poweron=True
				break
			time.sleep(60)
    	# Should I turn off yet?
		print("Power to teasmade active for 20 mins")
		for i in tqdm(range(100)):
			time.sleep(12)
		GPIO.output(gpiopinheat, GPIO.LOW)
		poweron=False
		pixels.off()


if __name__ == '__main__':
    main()
