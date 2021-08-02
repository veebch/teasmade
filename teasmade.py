#!/usr/bin/python3

import pvrhino

handle = pvrhino.create(context_path='/home/pi/teasmade/context/Teasmade_en_raspberry-pi_2021-08-31-utc_v1_6_0.rhn')

import struct
import pyaudio
import pvporcupine
import RPi.GPIO as GPIO
import apa102
import time
import threading
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
print(pvporcupine.KEYWORDS) 
porcupine = None
pa = None
audio_stream = None
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
gpiopinlight = 13
GPIO.setup(gpiopinlight, GPIO.OUT) # GPIO Assign mode
gpiopinheat = 12
GPIO.setup(gpiopinheat, GPIO.OUT) # GPIO Assign mode

try:
    porcupine = pvporcupine.create(keywords=["computer"])

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            state = GPIO.input(gpiopinlight)
            pixels.wakeup()
            print("Awake and Awaiting instructions!", state)
            commandwait=True
            while commandwait==True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                is_finalized = handle.process(pcm)
                if is_finalized:
                    inference = handle.get_inference()
                    if not inference.is_understood:
                        # add code to handle unsupported commands
                        print("I beg your pardon?")
                        pixels.speak()
                        time.sleep(2)
                    else:
                        # Figure out the intent
                        intent = inference.intent
                        slots = inference.slots
                        print(intent)
                        print(slots)
                        if intent=='light':              
                            if slots['state']=="on":
                                GPIO.output(gpiopinlight, GPIO.HIGH)
                            if slots['state']=="off":
                                GPIO.output(gpiopinlight, GPIO.LOW)
                        if intent=='water':
                            GPIO.output(gpiopinheat, GPIO.HIGH)
                        if intent=='power':
                            GPIO.output(gpiopinheat, GPIO.LOW)

                    pixels.off()
                    commandwait=False
            print("outerloop")
            time.sleep(1)
finally:
    if porcupine is not None:
        porcupine.delete()

    if audio_stream is not None:
        audio_stream.close()

    if pa is not None:
            pa.terminate()
    handle.delete
    GPIO.cleanup()