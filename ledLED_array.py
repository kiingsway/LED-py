# -*- coding: utf-8 -*-
# ESSE CÓDIGO DEVE SER RODADO NO RASPBERRY
from __future__ import print_function
import socket, threading, time, random
from neopixel import *

habilitar_segundo_led = False

# Conexão com o PC usando IPv4 e UDP
rpi_conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if habilitar_segundo_led: rpi_conexao_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Lendo a própria máquina na porta 12000 e 12001
rpi_conexao.bind(('',12000))
if habilitar_segundo_led: rpi_conexao_2.bind(('',12001))

# LED strip configuration (LED 1):
LED_COUNT      = 144     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).

# LED strip configuration (LED 2):
LED_COUNT_2      = 120     # Number of LED pixels.
LED_PIN_2        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ_2    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA_2        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS_2 = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT_2     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL_2    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

if habilitar_segundo_led:
	strip_2 = Adafruit_NeoPixel(LED_COUNT_2, LED_PIN_2, LED_FREQ_HZ_2, LED_DMA_2, LED_INVERT_2, LED_BRIGHTNESS_2, LED_CHANNEL_2)
	strip_2.begin()

def off():
	for i in range(LED_COUNT): strip.setPixelColor(i, Color(0,0,0))
	strip.show()
	if habilitar_segundo_led:
		for i in range(LED_COUNT_2): strip_2.setPixelColor(i, Color(0,0,0))
		strip_2.show()

if habilitar_segundo_led:
	off()
	print('Testes no LED 1 (red)...')
	for i in range(LED_COUNT):
		strip.setPixelColor(i, Color(0,255,0))
		strip.show()
		time.sleep(0.05)

	print('Testes no LED 2 (blue)...')
	for i in range(LED_COUNT_2):
		strip_2.setPixelColor(i, Color(0,0,255))
		strip_2.show()
		time.sleep(0.05)
	off()


if habilitar_segundo_led: print('Recebendo {} pixels no LED 1 e {} pixels no LED 2...'.format(LED_COUNT,LED_COUNT_2))
else: print('Recebendo {} pixels no LED 1...'.format(LED_COUNT))


def Color(red, green, blue, white = 0): return (white << 24) | (red << 16)| (green << 8) | blue

def comando(cmd):
	"""
	Essa função definirá quais comandos utilizar:

	- Efeitos
	!Exvy (ex: !E1v10)
	x - Seleção do efeito
	y - Velocidade do efeito
	
	- Brilho
	!Bx (ex: !B20)
	x = valor do brilho (0-100)

	"""

	funcao = cmd[1]

	if funcao == 'E':
		# Fazer efeito (p.ex: Rainbow)
		for i in range(LED_COUNT):
			strip.setPixelColor(i, Color(0,245,0))

	if funcao == 'B':
		# Alterar brilho
		brilho = int(cmd.split('B')[-1])
		strip.setBrightness(brilho)
		strip.show()



def led_1():
	while True:
		mensagem_bytes, ip_pc = rpi_conexao.recvfrom(2048)

		if mensagem_bytes == 'off':
			print('Solicitado comando para fechar.')
			for i in range(1,0,-1):
				print("Fechando em {}...".format(i))
				time.sleep(1)
			break

		if mensagem_bytes.startswith('!'): comando(mensagem_bytes)

		else:

			# Receberá uma array
			led_array = mensagem_bytes.strip('[]')

			try:
				# Recebendo por array
				index = 0
				for led in led_array.split():
					strip.setPixelColor(index, int(led))
					index += 1
				strip.show()
			except ValueError:
				# Recebendo por list
				index = 0
				for led in led_array.split(', '):
					strip.setPixelColor(index, int(led))
					index += 1
				strip.show()

			except: print(mensagem_bytes)

def led_2():
	while True:
		mensagem_bytes, ip_pc = rpi_conexao_2.recvfrom(2048)

		# Receberá uma array
		led_array = mensagem_bytes.strip('[]')

		try:
			# Recebendo por array
			index = 0
			for led in led_array.split():
				strip_2.setPixelColor(index, int(led))
				index += 1
			strip_2.show()
		except ValueError:
			# Recebendo por list
			index = 0
			for led in led_array.split(', '):
				strip_2.setPixelColor(index, int(led))
				index += 1
			strip_2.show()

led_1_thread = threading.Thread(target=led_1)
led_1_thread.start()

if habilitar_segundo_led:
	led_2_thread = threading.Thread(target=led_2)
	led_2_thread.start()