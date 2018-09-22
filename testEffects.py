import os
import time
import argparse
import threading
from effects import *
from decimal import *
from Tkinter import *
from neopixel import *
from functools import partial
from itertools import product




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

# DURATION OF THE NOTES 
BPM     = 120           #  you can change this value changing all the others
Q       = 60000/BPM     # quarter 1/4
H       = 2*Q           # half 2/4
E       = Q/2           # eighth 1/8
S       = Q/4           # sixteenth 1/16
W       = 4*Q           # whole 4/4

def key(event):        
    print (repr(event.char))
    evento = repr(event.char)
    if (evento == "'0'"):
        ef1 = threading.Thread(target=off,args=(0,))
        ef1.start()

    if (evento == "'1'"):
        ef1 = threading.Thread(target=bassBracoInvertEffect2,args=(0,50, 100,100,100, .1,))
        ef1.start()
    if (evento == "'2'"):
        ef1 = threading.Thread(target=hihat,args=(0.5,))
        ef1.start()
    if (evento == "'9'"):
        ef1 = threading.Thread(target=laranja)
        ef1.start()

def restart_program(event):
    python = sys.executable
    os.execl(python, python, * sys.argv)

def laranja():
    for i in range(20):
        for j in range(LED_COUNT):
            strip.setPixelColor(j,Color(175,255,0))
        strip.setBrightness(i)
        strip.show()
        time.sleep(0.1)

    for i in range(20,0,-1):
        for j in range(LED_COUNT):
            strip.setPixelColor(j,Color(175,255,0))
        strip.setBrightness(i)
        strip.show()
        time.sleep(0.1)


win.title("Projeto LED em GUI")
win.geometry('300x300')
win.bind("<KeyPress>", key)
#win.bind("<KeyRelease>", off)
win.bind_all("<F9>",restart_program)



strip.begin()
mainloop()


    

