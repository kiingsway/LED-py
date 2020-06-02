# -*- coding: UTF-8 -*-
import json, os

class Config:

	def __init__(self):
		# Definindo valores padrão do JSON caso ele não exista ou esteja vazio
		self.fitas_conectadas = 2

		pasta_atual = os.path.dirname(os.path.abspath(__file__))

		self.caminho_arquivo_config = pasta_atual + '/config.json'

		with open(self.caminho_arquivo_config, 'r+') as config_json:

			config_vazia = config_json.read() == ''
			if config_vazia: self.recriar_config()

		with open(self.caminho_arquivo_config, 'r') as config_json:
			data = json.load(config_json)

			self._led_type = data['led config'][0]['LED_TYPE']
			self._led_pin = data['led config'][0]['LED_PIN']
			self._led_count = data['led config'][0]['LED_COUNT']
			self._led_invert = data['led config'][0]['LED_INVERT']

			self._janela_padrao = data['ui config']['iniciar na janela']
			self._linhas_cores = data['ui config']['linhas em cores']

			self._udp = (data['net config']['UPD_IP'], data['net config']['UPD_PORT'])

	def recriar_config(self):

		print('recriando config...')

		led_config = [{'LED_TYPE':'ws2812b', 'LED_COUNT': 120, 'LED_PIN': 18, 'LED_INVERT': False}] * self.fitas_conectadas
		ui_config = {'iniciar na janela': 'Cores', 'linhas em cores': 6}
		net_config = {'UPD_IP': '192.168.1.1', 'UPD_PORT': 12000}

		config_data = {'led config': led_config, 'ui config': ui_config, 'net config': net_config}

		with open(self.caminho_arquivo_config, 'w') as config_json:

			json.dump(config_data, config_json, indent=4)

	@property
	def led_type(self):
		return self._led_type

	@led_type.setter
	def led_type(self, led_type):

		self._led_type = led_type

		with open(self.caminho_arquivo_config, 'r') as config_json:
			
			data = json.load(config_json)			

		with open(self.caminho_arquivo_config, 'w') as config_json:

			data['led config'][0]['LED_TYPE'] = led_type

			json.dump(data, config_json, indent=4)

	@property
	def led_pin(self):
		return self._led_pin

	@led_pin.setter
	def led_pin(self, led_pin):

		self._led_pin = led_pin

		with open(self.caminho_arquivo_config, 'r') as config_json:
			
			data = json.load(config_json)			

		with open(self.caminho_arquivo_config, 'w') as config_json:

			data['led config'][0]['LED_PIN'] = int(led_pin)

			json.dump(data, config_json, indent=4)

	@property
	def led_count(self):

		with open(self.caminho_arquivo_config, 'r') as config_json: data = json.load(config_json)

		return data['led config'][0]['LED_COUNT']

	@led_count.setter
	def led_count(self, led_count):

		self._led_count = led_count

		with open(self.caminho_arquivo_config, 'r') as config_json:
			
			data = json.load(config_json)			

		with open(self.caminho_arquivo_config, 'w') as config_json:

			data['led config'][0]['LED_COUNT'] = int(led_count)

			json.dump(data, config_json, indent=4)

	@property
	def led_invert(self):

		with open(self.caminho_arquivo_config, 'r') as config_json: data = json.load(config_json)

		return data['led config'][0]['LED_INVERT']

	@led_invert.setter
	def led_invert(self, led_invert):

		self._led_invert = led_invert

		with open(self.caminho_arquivo_config, 'r') as config_json:
			
			data = json.load(config_json)			

		with open(self.caminho_arquivo_config, 'w') as config_json:

			data['led config'][0]['LED_INVERT'] = led_invert

			json.dump(data, config_json, indent=4)

	@property
	def janela_padrao(self):

		with open(self.caminho_arquivo_config, 'r') as config_json: data = json.load(config_json)

		return data['ui config'][0]['iniciar na janela']

	@janela_padrao.setter
	def janela_padrao(self, janela):

		self._janela_padrao = janela

		with open(self.caminho_arquivo_config, 'r') as config_json:
			
			data = json.load(config_json)			

		with open(self.caminho_arquivo_config, 'w') as config_json:

			data['ui config'][0]['iniciar na janela'] = janela

			json.dump(data, config_json, indent=4)
	


	@property
	def udp(self):

		with open(self.caminho_arquivo_config, 'r') as config_json: data = json.load(config_json)

		return (data['net config']['UPD_IP'], data['net config']['UPD_PORT'])

	@udp.setter
	def udp(self, udp):

		ip = udp[0]
		port = udp[1]

		if port:
			try: int(port)
			except ValueError: port = self._udp[1]
		else: port = 12000

		self._udp = udp

		with open(self.caminho_arquivo_config, 'r') as config_json:
			
			data = json.load(config_json)			

		with open(self.caminho_arquivo_config, 'w') as config_json:

			data['net config']['UPD_IP'] = ip
			data['net config']['UPD_PORT'] = int(port)

			json.dump(data, config_json, indent=4)


	@property
	def janela_padrao(self):
		return self._janela_padrao

	@janela_padrao.setter
	def janela_padrao(self, janela_padrao):

		self._janela_padrao = janela_padrao

		with open(self.caminho_arquivo_config, 'r') as config_json:
			
			data = json.load(config_json)			

		with open(self.caminho_arquivo_config, 'w') as config_json:

			data['ui config']['iniciar na janela'] = janela_padrao

			json.dump(data, config_json, indent=4)


	@property
	def linhas_cores(self):

		with open(self.caminho_arquivo_config, 'r') as config_json: data = json.load(config_json)

		return data['ui config']['linhas em cores']

	@linhas_cores.setter
	def linhas_cores(self, linhas_cores):

		self._linhas_cores = linhas_cores

		with open(self.caminho_arquivo_config, 'r') as config_json:
			
			data = json.load(config_json)			

		with open(self.caminho_arquivo_config, 'w') as config_json:

			data['ui config']['linhas em cores'] = linhas_cores

			json.dump(data, config_json, indent=4)
	
if __name__ == '__main__':

	c = Config()

	# c.recriar_config()

	# print(c.led_type)
	# c.led_type = 'w2812b'
	# print(c.led_type)

	# print(c.janela_padrao)
	# c.janela_padrao = "ServerLED"
	# c.janela_padrao = "Cores"
	# ip = '192.168.1.2'
	# port = '23'
	# c.udp = (ip,port)
	# print(c.janela_padrao)

	print(c.linhas_cores)
	c.linhas_cores = 7
	print(c.linhas_cores)
