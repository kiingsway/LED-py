#!/usr/bin/env python3
# NeoPixel library light-painting example
# Author: Gary Servin (garyservin@gmail.com)
#
# Lightpainting example for displaying images one column at a time and capturing
# it by taking a long exposure photograph.
# Based on https://github.com/scottjgibson/PixelPi

import time
import globals
try: from neopixel import *
except:
    def Color(r,g,b): pass
    # def Color(r,g,b): print("R: %x    G: %x    B: %x", (r,g,b),end='\r')
import argparse

# Lightpainting
from PIL import Image

# LED strip configuration:
LED_COUNT      = 55     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

try:
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
except:
    print('Estamos sem LEDs :(')

def lightpainting():

    img = globals.imagem_arquivo

    print("Tamanho: {}x{}".format(img.size[0],img.size[1]))

    # Check that the height of the image is greater than or equal the number of LEDs on the strip
    if(img.size[1] < LED_COUNT):
        raise Exception("Image height is smaller than led strip size. Required height = {}".format(LED_COUNT))
    elif(img.size[1] > LED_COUNT):
        print ("Redimensionando a imagem...")
        new_width  = LED_COUNT * img.size[0] / img.size[1]
        img = img.resize((int(new_width), LED_COUNT), Image.ANTIALIAS)

    input_image = img.load()
    image_width = img.size[0]

    column = [0 for x in range(image_width)]
    for x in range(image_width):
        column[x] = [None] * (LED_COUNT)

    for x in range(image_width):
        for y in range(LED_COUNT):
            value = input_image[x, y]
            column[x][y] = Color(value[1], value[0], value[2])

    while True:
        frame_rate = globals.velocidade
        print("Lightpainting rodando em velocidade {}...".format(frame_rate))
        # Wait for button to be pressed before displaying image
        #if not loop:
            #print("Waiting for button to be pressed")
            #GPIO.wait_for_edge(BUTTON_CHANNEL, GPIO.FALLING)
            #time.sleep(0.5)

        x_range = range(image_width)
        # if reverse_x:
            # x_range.reverse()

        y_range = range(LED_COUNT)
        # if reverse_y:
            # y_range.reverse()

        for x in x_range:
            led_pos = 0
            for y in y_range:
                try: strip.setPixelColor(led_pos, column[x][y])
                except: pass
                led_pos += 1
            try: strip.show()
            except: pass
            #time.sleep(column_rate / 1000.0)
            time.sleep(0.01)
            
            if not globals.lpLigado:
                print("Parando lightpainting...")
                break
        # Wait for `frame_rate` ms before drawing a new frame
        time.sleep(frame_rate / 1000.0)

        