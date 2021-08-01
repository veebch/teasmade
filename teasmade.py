#!/usr/bin/python3

import pvrhino

handle = pvrhino.create(context_path='/home/pi/teasmade/context/Teasmade_en_raspberry-pi_2021-08-31-utc_v1_6_0.rhn')

import struct
import pyaudio
import pvporcupine
import RPi.GPIO as GPIO
import time
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
    porcupine = pvporcupine.create(keywords=["bumblebee"])

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