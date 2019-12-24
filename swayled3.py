#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Feito por Marcos Oranmiyan.
Aqui controlamos LEDs ws2812x e 5050.
'''

# Importa a declaração print como uma função no Python 2.
from __future__ import print_function

import os
import sys
import config

# Importando pythons para construir as janelas
from sl_config import * # Configurações dos leds

try:
	# Python 3
	from tkinter import *
	from tkinter.ttk import Treeview
	# from tkinter.ttk import Combobox
except ImportError:
	# Python 2
	from Tkinter import *
	from ttk import Combobox, Treeview


class Aplicativo:

	def mudar_tela(self, app_iniciando=False):
		def fechar_todas_as_telas():
			self.frameConfig.grid_remove()
			self.frameServerled.grid_remove()
			self.frameConfigApp.grid_remove()

		if app_iniciando == False: menu_selecionado = self.tvwMenu.selection()[0]
		else: menu_selecionado = config.janelaDefault


		if menu_selecionado == 'Configurações':
			fechar_todas_as_telas()
			self.frameConfig.grid(row=1,column=1,sticky=N)

		elif menu_selecionado == 'ServerLED':
			fechar_todas_as_telas()
			self.frameServerled.grid(row=1,column=1,sticky=N)

		elif menu_selecionado == 'app':
			fechar_todas_as_telas()
			self.frameConfigApp.grid(row=1,column=1,sticky=N)

		else:
			fechar_todas_as_telas()


	def construir_menu(self):
		''' Definição usada para construir o menu do app.
		'''
		lblMenu = Label(principal,text='Menu:')
		lblMenu.grid(row=0, column=0, sticky=W, padx=10)

		frameMenu = Frame(principal, width=60, height=30)
		frameMenu.grid(row=1, column=0, sticky=N+W, padx=10)

		self.tvwMenu = Treeview(frameMenu, height=8)
		self.tvwMenu.column('#0', width=125)
		self.tvwMenu.insert('', 'end', 'cores', text='Cores')
		self.tvwMenu.insert('', 'end', 'efeitos', text='Efeitos')
		self.tvwMenu.insert('', 'end', 'lightpaint', text='Lightpaint')
		self.tvwMenu.insert('', 'end', 'dancypi', text='DancyPi')
		self.tvwMenu.insert('', 'end', 'neon', text='Neon')
		self.tvwMenu.insert('', 'end', 'ServerLED', text='Server LED')
		self.tvwMenu.insert('', 'end', 'Configurações', text='Configurações')
		self.tvwMenu.insert('Configurações', 'end', 'app', text='Aplicativo')
		self.tvwMenu.bind('<<TreeviewSelect>>', lambda x: self.mudar_tela())
		self.tvwMenu.grid(row=1, column=0)


	def __init__(self, master=None):
		
		# Frames para serem mostrados
		self.frameConfig = Frame(principal)
		self.frameServerled = Frame(principal)
		self.frameConfigApp = Frame(principal)

		# Função para construir o menu do aplicativo e as configurações
		self.construir_menu()
		construir_configuracoes(principal, self.frameConfig)
		construir_serverled(principal, self.frameServerled)
		construir_config_app(principal, self.frameConfigApp)

		self.mudar_tela(app_iniciando=True)

principal = Tk()
Aplicativo(principal)
# principal.geometry("722x399")
# principal.minsize(722, 399)
principal.title('Sway LED')
principal.mainloop()