import socket, config

class Conexao:

	def __init__(self):

		self.led_conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.config = config.Config()

	def enviar_teste(self):
		ip, port = self.config.udp

		led_envio = [255] * 100
		led_envio = str(led_envio)

		self.led_conexao.sendto(led_envio.encode(), (ip, port))

	def enviar_array(self, array):
		ip, port = self.config.udp

		led_envio = str(array)

		self.led_conexao.sendto(led_envio.encode(), (ip, port))

	def enviar_rgb(self, r,g,b):
		ip, port = self.config.udp

		led_envio = str(array)

		self.led_conexao.sendto(led_envio.encode(), (ip, port))

	def desligar_leds(self):
		ip, port = self.config.udp

		led_envio = [0] * self.config.led_count
		led_envio = str(led_envio)

		self.led_conexao.sendto(led_envio.encode(), (ip, port))

	def enviar_comando(self, comando):
		ip, port = self.config.udp

		self.led_conexao.sendto(comando.encode(), (ip, port))


if __name__ == '__main__':

	Conexao().desligar_leds()