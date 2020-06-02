neopixel_importado = True
try: from neopixel import *
except: neopixel_importado = False
import conexao, config

class Led:

	def __init__(self, str_status_led):

		self.neopixel_importado = neopixel_importado
		self.str_status_led = str_status_led
		self.config = config.Config()
		
		if self.neopixel_importado:
			# LED strip configuration:
			self.LED_COUNT      = self.config.led_count     # Number of LED pixels.
			self.LED_PIN        = self.config.led_pin      # GPIO pin connected to the pixels (18 uses PWM!).
			self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
			self.LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
			self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
			self.LED_INVERT     = self.config.led_invert   # True to invert the signal (when using NPN transistor level shift)
			self.LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
			#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).

			# Create NeoPixel object with appropriate configuration.
			self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
			# Intialize the library (must be called once before other functions).
			self.strip.begin()

		else:
			self.conexao_rpi = conexao.Conexao()

	def enviar_teste(self):

		if self.neopixel_importado: pass
		else: self.conexao_rpi.enviar_teste()

	def desligar(self):

		if neopixel_importado:
			for i in range(self.LED_COUNT): self.strip.setPixelColor(i, Color(0,0,0))
			self.strip.show()

		else: self.conexao_rpi.desligar_leds()

	def enviar_array(self, array):
		self.conexao_rpi.enviar_array(array)

	def enviar_rgb(self, r=0,g=0,b=0, hex=0):

		if hex: r,g,b = Led.hex_to_color(hex)

		if neopixel_importado:

			for i in range(self.LED_COUNT): self.strip.setPixelColor(i, Color(g,r,b))

			self.strip.show()

		else:

			array = [Led.Color(g,r,b)] * self.config.led_count

			self.conexao_rpi.enviar_array(array)

	def enviar_comando(self, comando):

		self.conexao_rpi.enviar_comando(comando)

	def alterar_brilho(self, brilho):

		# Se não tiver neopixel importado
		if self.neopixel_importado:
			self.strip.setBrightness(int(brilho))
			self.strip.show()
		else: self.enviar_comando('!B{}'.format(brilho))

	@staticmethod
	def Color(red, green, blue, white = 0): return (white << 24) | (red << 16)| (green << 8) | blue

	@staticmethod
	def hex_to_color(h):
		h = h.lstrip('#')
		return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

	@staticmethod
	def color_to_hex(r,g,b):
		return '#%02x%02x%02x' % (r, g, b)

if __name__ == '__main__':
	Led('x').alterar_brilho(10)