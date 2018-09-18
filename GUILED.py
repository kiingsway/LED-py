#!/usr/bin/env python3
from Tkinter import *
from functools import partial
from itertools import product
#from tkinter.font import Font
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

import threading

from decimal import *

# LED strip configuration:
LED_COUNT      = 120      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

win = Tk()

ledBtn = [0] * LED_COUNT

BPM = 128
bpm4 = Decimal(60)/Decimal(BPM)

#myFont = Font(family = 'Helvetica', size = 36, weight = 'bold')

# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
strip.begin()



def key(event):        
    print (repr(event.char))
    evento = repr(event.char)
    if (evento == "'1'"):
        ef1 = threading.Thread(target=laser)
        ef1.start()
    if (evento == "'2'"):
        ef2 = threading.Thread(target=hihat)
        ef2.start()
    if (evento == "'3'"):
        ef3 = threading.Thread(target=bpmtest)
        ef3.start()
    if (evento == "'4'"):
        ef4 = threading.Thread(target=bassLBaixoTouca)
        ef4.start()
    if (evento == "'5'"):
        ef5 = threading.Thread(target=bassLAltoTouca)
        ef5.start()
    if (evento == "'6'"):
        ef6 = threading.Thread(target=bassAltoTouca)
        ef6.start()
    if (evento == "'7'"):
        ef7 = threading.Thread(target=tresPontos)
        ef7.start()
    if (evento == "'8'"):
        ef8 = threading.Thread(target=tresPontosInvert)
        ef8.start()
    if (evento == "'9'"):
        ef9 = threading.Thread(target=bracoUp)
        ef9.start()
    if (evento == "'0'"):
        ef10 = threading.Thread(target=bracoDown)
        ef10.start()

def off(event):
    for i in range(LED_COUNT):
        strip. setPixelColor(i, Color(0,0,0))
    strip.show()
    print("desliguei")

def luz(R, G, B, pontoA, pontoB):
    for i in range(pontoA, pontoB):
        strip.setPixelColor(i, Color(R, G, B))
    
def cobra(R, G, B, pontoA, pontoB, velocidade, sobeDesce):
    for i in range(pontoA, pontoB):
        strip.setPixelColor(i, Color(R, G, B))
        strip.show()
        time.sleep(velocidade)
    if (sobeDesce == 1):
        for i in range(pontoB, pontoA-1, -1):
            strip.setPixelColor(i, Color(0,0,0))
            strip.setPixelColor(i-1, Color(R,G,B))
            strip.show()
            time.sleep(velocidade)

def bpmtest():
    for i in range(2):
        bracoUp()
        time.sleep(bpm4/8)
        hihat()
        time.sleep(bpm4/8)
        bracoDown()
        time.sleep(bpm4/8)
        hihat()
        time.sleep(bpm4/8)

def TAN():
    luz(100,100,0,60,120)
    strip.show();

def TUN():
    luz(100,100,0,0,60)
    strip.show();
    
        
def BASS():
    cobra(0,100,100,0,40,.0001,1)
        

def bassLBaixoTouca():
    kill=0
    luz(100,100,100,0,40)
    strip.show()
    for rgb in range(100,-1,-5):
        if kill==1: return
        luz(rgb,rgb,rgb,0,40)
        strip.show()
        time.sleep(.05)

def bassLAltoTouca():
    luz(100,100,100,40,80)
    strip.show()
    for rgb in range(100,-1,-5):
        luz(rgb,rgb,rgb,40,80)
        strip.show()
        time.sleep(.05)

def bassAltoTouca():
    luz(100,100,100,80,120)
    strip.show()
    for rgb in range(100,-1,-5):
        luz(rgb,rgb,rgb,80,120)
        strip.show()
        time.sleep(.05)

def tresPontos():
    for i in range(0,29+6):
        if (i <= 30):
            strip.setPixelColor(i, Color(100,0,100))
            strip.setPixelColor(60-i, Color(100,0,100))
            strip.setPixelColor(i+60, Color(100,0,100))
            strip.setPixelColor(120-i, Color(100,0,100))
	if (i >= 3):
            strip.setPixelColor(i-4, Color(0,0,0))
            strip.setPixelColor(64-i, Color(0,0,0))
            strip.setPixelColor(i+56, Color(0,0,0))
            strip.setPixelColor(124-i, Color(0,0,0))
	strip.show()
	time.sleep(.05)
    
def tresPontosInvert():
    for i in range(0,29+6):
        if (i <= 30):
            strip.setPixelColor(30-i, Color(0,100,0))
            strip.setPixelColor(30+i, Color(0,100,0))
            strip.setPixelColor(90-i, Color(0,100,0))
            strip.setPixelColor(90+i, Color(0,100,0))
	if (i >= 4):
            strip.setPixelColor(34-i, Color(0,0,0))
            strip.setPixelColor(26+i, Color(0,0,0))
            strip.setPixelColor(94-i, Color(0,0,0))
            strip.setPixelColor(86+i, Color(0,0,0))
	strip.show()
	time.sleep(.05)

def bracoUp():
    delay = .025
    for i in range(1,5):
        for j in range(13*(i-1), 13*i):
            strip.setPixelColor(j, Color(100,100,100))
        strip.show()
        time.sleep(delay)
        
    for i in range(4,0,-1):
        for j in range(13*(i-1), 13*i):
            strip.setPixelColor(j, Color(0,0,0))
        strip.show()
        time.sleep(delay)

def bracoDown():
    delay = .025
    for i in range(1,5):
        for j in range(120-(13*(i-1)), 120-(13*i),-1):
            strip.setPixelColor(j, Color(100,100,100))
        strip.show()
        time.sleep(delay)
        
    for i in range(4,0,-1):
        for j in range(120-(13*(i-1)), 120-(13*i),-1):
            strip.setPixelColor(j, Color(0,0,0))
        strip.show()
        time.sleep(delay)

def laser():
	for i in range(14+2):
            for j in range(0,133,13):
                j = j+i
                if (i < 14):
                    strip.setPixelColor(j,Color(0,0,100))
                    strip.setPixelColor(j-1,Color(0,0,100))
                strip.setPixelColor(j-2,Color(0,0,0))
                strip.setPixelColor(j-3,Color(0,0,0))
            strip.show()
            time.sleep(.05)

def hihat():
    for i in range(5):
        if i < 4:
            for j in range(60+12*i,60+12*(1+i)):
                strip.setPixelColor(j,Color(100,100,0))
            for y in range(60-(12*i),60-(12*(1+i)),-1):
                strip.setPixelColor(y,Color(100,100,0))
        if i >= 1:
            for j in range(60+12*(i-1),60+12*i):
                strip.setPixelColor(j,Color(0,0,0))
            for y in range(60-12*(i-1),60-12*i,-1):
                strip.setPixelColor(y,Color(0,0,0))
        strip.show()
        time.sleep(.05)

win.title("Projeto LED em GUI")
win.geometry('300x300')
win.bind("<KeyPress>", key)
#win.bind("<KeyRelease>", off)


strip.begin()
mainloop()


    

