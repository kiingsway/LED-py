#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import config
try: from neopixel import *
except: pass
import configparser
from pathlib import Path
import os

pasta_atual = '\\'.join(str(Path(__file__).absolute()).split('\\')[0:-1])
# pasta_atual = os.getcwd()
arquivo = '\\config.ini'
caminho_arquivo = pasta_atual + arquivo

config = configparser.ConfigParser()
config.read(caminho_arquivo, encoding='iso-8859-1')

# LED strip configuration:
LED_COUNT      = int(config.get("LED1", "qtd"))     # Number of LED pixels.
LED_PIN        = int(config.get("LED1", "pino"))      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

def desligar(fitaled=0):

	for pos in range(LED_COUNT):
		strip.setPixelColor(pos,Color(0,0,0))
	strip.show()

def cores(h,fitaled=0):
	def hex_to_color(h):
		h = h.lstrip('#')
		return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

	r,g,b = hex_to_color(h)
	# Fazer um GOTO da última cor que colocaram para a selecionada 2.0

	for pos in range(LED_COUNT):
		strip.setPixelColor(pos,Color(g,r,b))
	strip.show()

def alterar_brilho(brilho):
	strip.setBrightness(brilho)
	strip.show()

def por_rgb(r,g,b, fitaled=0):
	for pos in range(LED_COUNT):
		strip.setPixelColor(pos, Color(g,r,b))
	strip.show()