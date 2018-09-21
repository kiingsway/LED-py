#!/usr/bin/env python3
from Tkinter import *
from functools import partial
from itertools import product
import os
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

BPM = 110
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
    '''
    if (evento == "'1'"):
        ef1 = threading.Thread(target=laser)
        ef1.start()
    if (evento == "'2'"):
        ef2 = threading.Thread(target=hihat,args=(0.05,))
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
        ef9 = threading.Thread(target=bracoUp,args=(0.025,))
        ef9.start()
    if (evento == "'0'"):
        ef10 = threading.Thread(target=bracoDown)
        ef10.start()
        '''
    if (evento == "'0'"):
        ef1 = threading.Thread(target=off,args=(0,))
        ef1.start()

    if (evento == "'1'"):
        ef1 = threading.Thread(target=bassGFY,args=(1,))
        ef1.start()
    if (evento == "'4'"):
        ef1 = threading.Thread(target=bassGFY,args=(2,))
        ef1.start()
    if (evento == "'7'"):
        ef1 = threading.Thread(target=bassGFY,args=(3,))
        ef1.start()

    if (evento == "'2'"):
        ef1 = threading.Thread(target=guitarGFY,args=(1,))
        ef1.start()
    if (evento == "'5'"):
        ef1 = threading.Thread(target=guitarGFY,args=(2,))
        ef1.start()
    if (evento == "'8'"):
        ef1 = threading.Thread(target=guitarGFY,args=(3,))
        ef1.start()

def off(event):
    for i in range(LED_COUNT):
        strip. setPixelColor(i, Color(0,0,0))
    strip.show()
    print("desliguei")


def guitarGFY(cor):
    if cor == 1:
        for i in range(100,-5,-5):
            strip.setPixelColor(92, Color(i,0,i))
            strip.setPixelColor(93, Color(i,0,i))
            strip.setPixelColor(94, Color(i,0,i))
            strip.show()
            time.sleep(.005)
    if cor == 2:
        for i in range(100,-5,-5):
            strip.setPixelColor(106, Color(i,0,i))
            strip.setPixelColor(107, Color(i,0,i))
            strip.setPixelColor(108, Color(i,0,i))
            strip.show()
            time.sleep(.005)
    if cor == 3:
        for i in range(100,-5,-5):
            strip.setPixelColor(118, Color(i,0,i))
            strip.setPixelColor(117, Color(i,0,i))
            strip.setPixelColor(116, Color(i,0,i))
            strip.show()
            time.sleep(.005)



def bassGFY(cor):
    for i in range(4):
        #strip.setBrightness(100)

        def up():
            for i in range(1,7):
                for j in range(13*(i-1), 13*i):
                    if cor == 1: strip.setPixelColor(j, Color(0,100,0))
                    if cor == 2: strip.setPixelColor(j, Color(0,100,0))
                    if cor == 3: strip.setPixelColor(j, Color(100,100,0))
                    if cor == 4: strip.setPixelColor(j, Color(100,0,0))
                strip.show()
                time.sleep(.01)

        def treble():
            for i in range(7,8):
                for j in range(13*(i-1), 13*i):
                    if cor == 1: strip.setPixelColor(j, Color(0,100,0))
                    if cor == 2: strip.setPixelColor(j, Color(0,100,0))
                    if cor == 3: strip.setPixelColor(j, Color(100,100,0))
                    if cor == 4: strip.setPixelColor(j, Color(100,0,0))
                strip.show()
                time.sleep(.01)

            brT = threading.Thread(target=brilho)
            brT.start()

            for i in range(8,6,-1):
                for j in range(13*(i-1), 13*i):
                    strip.setPixelColor(j, Color(0,0,0))
                strip.show()
                time.sleep(.01)

        def down():
            for i in range(6,0,-1):
                for j in range(13*(i-1), 13*i):
                    strip.setPixelColor(j, Color(0,0,0))
                strip.show()
            time.sleep(.01)

        def brilho():
            for i in range(1):
                for j in range(105,255,31):
                    strip.setBrightness(j)
                    strip.show()
                    time.sleep(.01)
                for j in range(255,105,-31):
                    strip.setBrightness(j)
                    strip.show()
                    time.sleep(.01)
            for j in range(105,255,31):
                    strip.setBrightness(j)
                    strip.show()
                    time.sleep(.01)



        up()
        time.sleep(.05)
        treble()
        time.sleep(.05)
        treble()
        time.sleep(.05)
        treble()
        time.sleep(.05)
        treble()
        time.sleep(.05)
        treble()
        time.sleep(.05)
        treble()
        time.sleep(.05)
        treble()
        time.sleep(.05)
        down()

        cor = cor+1
        time.sleep(.7)





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
    for i in range(5):
    	bpmT1 = threading.Thread(target=bracoUp,args=(0.025,))
    	bpmT1.start()
        time.sleep(bpm4/2)
        bpmT2 = threading.Thread(target=hihat,args=(0.025,))
    	bpmT2.start()
        time.sleep(bpm4/2)
        bpmT3 = threading.Thread(target=bracoDown,args=(0.025,))
    	bpmT3.start()
        time.sleep(bpm4/2)
        bpmT4 = threading.Thread(target=hihat,args=(0.025,))
    	bpmT4.start()
        time.sleep(bpm4/2)

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

def bracoUp(vel):
    for i in range(1,5):
        for j in range(13*(i-1), 13*i):
            strip.setPixelColor(j, Color(100,100,100))
        strip.show()
        time.sleep(vel)
        
    for i in range(4,0,-1):
        for j in range(13*(i-1), 13*i):
            strip.setPixelColor(j, Color(0,0,0))
        strip.show()
        time.sleep(vel)

def bracoDown(vel):
    for i in range(1,5):
        for j in range(120-(13*(i-1)), 120-(13*i),-1):
            strip.setPixelColor(j, Color(100,100,100))
        strip.show()
        time.sleep(vel)
        
    for i in range(4,0,-1):
        for j in range(120-(13*(i-1)), 120-(13*i),-1):
            strip.setPixelColor(j, Color(0,0,0))
        strip.show()
        time.sleep(vel)

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

def hihat(vel):
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
        time.sleep(vel)

def restart_program(event):
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


win.title("Projeto LED em GUI")
win.geometry('300x300')
win.bind("<KeyPress>", key)
#win.bind("<KeyRelease>", off)
win.bind_all("<F9>",restart_program)



strip.begin()
mainloop()


    

