#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Quantas linhas terá a tabela de cores
linhasCores = 6

# Janela padrão em que o aplicativo é aberto
janelaDefault = 'Cores'

# Configuração UDP
udp = {'ip': '192.168.0.31', 'porta': 12000}

# Configuração dos LEDs
led = [{
		'tipo': 'ws2812b',
		'pino': '18',
		'qtd': 144+120,
		'inverter': False,
		'volts': '5v',
		'ampere_pixel_min': 20,
		'ampere_pixel_max': 60
	},
	{
		'tipo': '5050',
		'pino': '18',
		'qtd': 0,
		'inverter': True,
		'volts': '0v',
		'ampere_pixel_min': 0,
		'ampere_pixel_max': 0
	},
	{
		'tipo': '5050',
		'pino': '18',
		'qtd': 0,
		'inverter': True,
		'volts': '0v',
		'ampere_pixel_min': 0,
		'ampere_pixel_max': 0
	},
	{
		'tipo': '5050',
		'pino': '18',
		'qtd': 0,
		'inverter': True,
		'volts': '0v',
		'ampere_pixel_min': 0,
		'ampere_pixel_max': 0
	}
]