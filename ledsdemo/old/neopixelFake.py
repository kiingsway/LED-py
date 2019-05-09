from tkinter import Canvas, Tk

ledDemo = Tk()
canvas = Canvas(ledDemo)
r = {}

def Color(R,G,B):
	"""
	O Color original converte as cores RGB para algo em 24bit.
	Aqui é usado apenas para retornar o número em hexadecimal
	"""
	novas_cores = "#%0.2X%0.2X%0.2X" % (R,G,B)
	return novas_cores

# class strip:
# 	def setPixelColor(pos,color_hex):
# 		canvas.itemconfig(r['retangulo{}'.format(pos)], fill=color_hex)
# 	def numPixels():
# 		return LED_COUNT
# 	def show():
# 		pass


class Adafruit_NeoPixel(object):
	def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False,
		brightness=255, channel=0, strip_type='ws.WS2811_STRIP_RGB'):
		"""Init apenas para os parâmetros serem ignorados
		"""
		try: del self._led_data
		except: pass
		self._led_data = []
		print("Num: {}".format(num),end='\n\n')
		print("Leds: ",end='')
		for led in range(num):
			print(led,end=', ')
			if led % 10 == 0: print('')
			base = 15*led
			r["retangulo{0}".format(led)] = canvas.create_rectangle(5+base, 10, 15+base, 20,outline="#000", fill="#000")
			self._led_data.append('#000000')
		print('\n')

	def begin(self):
		"""Originalmente inicializava a biblioteca.
		Mais uma coisa que vamos ignorar
		"""
		pass

	def show(self):
		"""Update the display with the data from the LED buffer."""
		print ('\nTamanho do _led_data: {}\n\n'.format(len(self._led_data)))
		print('_led_data: {}'.format(self._led_data))
		for pos in range(len(self._led_data)-1):
			canvas.itemconfig(r['retangulo{}'.format(pos)], fill=self._led_data[pos])

	def setPixelColor(self, n, color):
		"""Set LED at position n to the provided 24-bit color value (in RGB order).
		"""
		# self._led_data[n] = color
		# print('Posição: {} Cor: {}'.format(n,color))
		self._led_data.insert(n,color)

	def setPixelColorRGB(self, n, red, green, blue, white = 0):
		"""Set LED at position n to the provided red, green, and blue color.
		Each color component should be a value from 0 to 255 (where 0 is the
		lowest intensity and 255 is the highest intensity).
		"""
		self.setPixelColor(n, Color(red, green, blue, white))

	def setBrightness(self, brightness):
		"""Scale each LED in the buffer by the provided brightness.  A brightness
		of 0 is the darkest and 255 is the brightest.
		"""
		ws.ws2811_channel_t_brightness_set(self._channel, brightness)

	def getBrightness(self):
		"""Get the brightness value for each LED in the buffer. A brightness
		of 0 is the darkest and 255 is the brightest.
		"""
		return ws.ws2811_channel_t_brightness_get(self._channel)

	def getPixels(self):
		"""Return an object which allows access to the LED display data as if
		it were a sequence of 24-bit RGB values.
		"""
		return self._led_data

	def numPixels(self):
		"""Return the number of pixels in the display."""
		# return ws.ws2811_channel_t_count_get(self._channel)
		return LED_COUNT

	def getPixelColor(self, n):
		"""Get the 24-bit RGB color value for the LED at position n."""
		return self._led_data[n]