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

	def __init__(self, master=None):
		
		# Frames para serem mostrados
		self.frameCores = Frame(principal)
		self.frameEfeitos = Frame(principal)
		self.frameLightpaint = Frame(principal)
		self.frameDancypi = Frame(principal)
		self.frameServerled = Frame(principal)
		self.frameConfig = Frame(principal)
		self.frameConfigApp = Frame(principal)

		# Função para construir o menu do aplicativo
		self.construir_menu()
		# construir_configuracoes(principal, self.frameConfig)
		# construir_serverled(principal, self.frameServerled, Aplicativo)
		# construir_config_app(principal, self.frameConfigApp)
		# construir_cores(principal, self.frameCores)
		# construir_efeitos(principal, self.frameEfeitos)
		# construir_lightpaint(principal, self.frameLightpaint)
		# construir_dancyPi(principal, self.frameDancypi)

		self.mudar_tela(app_iniciando=True)

	def alterar_UDP(self):
		self.tvwMenu.item('serverLED', values=('ServerLED', 'A'))

	def mudar_tela(self, app_iniciando=False):
		def fechar_todas_as_telas():
			self.frameConfig.destroy()
			self.frameServerled.destroy()
			self.frameConfigApp.destroy()
			self.frameCores.destroy()
			self.frameEfeitos.destroy()
			self.frameLightpaint.destroy()
			self.frameDancypi.destroy()
		
			# Frames para serem mostrados
			self.frameCores = Frame(principal)
			self.frameEfeitos = Frame(principal)
			self.frameLightpaint = Frame(principal)
			self.frameDancypi = Frame(principal)
			self.frameServerled = Frame(principal)
			self.frameConfig = Frame(principal)
			self.frameConfigApp = Frame(principal)

		if app_iniciando == False:
			fechar_todas_as_telas()
			menu_selecionado = self.tvwMenu.selection()[0]
		else: menu_selecionado = config.janelaDefault

		# fechar_todas_as_telas()
		
		if menu_selecionado == 'Cores':
			construir_cores(principal, self.frameCores)
			self.frameCores.grid(row=1,column=1,sticky=N)
		
		elif menu_selecionado == 'Efeitos':
			construir_efeitos(principal, self.frameEfeitos)
			self.frameEfeitos.grid(row=1,column=1,sticky=N)
		
		elif menu_selecionado == 'Lightpaint':
			construir_lightpaint(principal, self.frameLightpaint)
			self.frameLightpaint.grid(row=1,column=1,sticky=N)
		
		elif menu_selecionado == 'DancyPi':
			construir_dancyPi(principal, self.frameDancypi)
			self.frameDancypi.grid(row=1,column=1,sticky=N)
		
		elif menu_selecionado == u'Configurações':
			construir_configuracoes(principal, self.frameConfig)
			self.frameConfig.grid(row=1,column=1,sticky=N)
		
		elif menu_selecionado == 'ServerLED':
			construir_serverled(principal, self.frameServerled)
			self.frameServerled.grid(row=1,column=1,sticky=N)
		
		elif menu_selecionado == 'Aplicativo':
			construir_config_app(principal, self.frameConfigApp)
			self.frameConfigApp.grid(row=1,column=1,sticky=N)

		# if menu_selecionado == 'Cores': self.frameCores.grid(row=1,column=1,sticky=N)
		# elif menu_selecionado == 'Efeitos': self.frameEfeitos.grid(row=1,column=1,sticky=N)
		# elif menu_selecionado == 'Lightpaint': self.frameLightpaint.grid(row=1,column=1,sticky=N)
		# elif menu_selecionado == 'DancyPi': self.frameDancypi.grid(row=1,column=1,sticky=N)
		# elif menu_selecionado == u'Configurações': self.frameConfig.grid(row=1,column=1,sticky=N)
		# elif menu_selecionado == 'ServerLED': self.frameServerled.grid(row=1,column=1,sticky=N)
		# elif menu_selecionado == 'Aplicativo': self.frameConfigApp.grid(row=1,column=1,sticky=N)

	def construir_menu(self):
		''' Definição usada para construir o menu do app.
		'''
		lblMenu = Label(principal,text='Menu:')
		lblMenu.grid(row=0, column=0, sticky=W, padx=10)

		frameMenu = Frame(principal, width=60, height=30)
		frameMenu.grid(row=1, column=0, sticky=N+W, padx=10,pady=(0,10))

		self.tvwMenu = Treeview(frameMenu, height=8, columns=('Menu', 'Status'), show="tree")
		self.tvwMenu.column('#0', width=0)
		self.tvwMenu.column('Menu', width=100)
		self.tvwMenu.column('Status', width=50)
		menus = ['Cores', 'Efeitos', 'Lightpaint', 'DancyPi', 'ServerLED', 'Configurações', 'Aplicativo']

		for menu in menus:
			if menu == 'Aplicativo':
				self.tvwMenu.insert('Configurações', 'end', menu, values=(menu))
				continue
			self.tvwMenu.insert('', 'end', menu, values=(menu), open=True)

		self.tvwMenu.bind('<<TreeviewSelect>>', lambda x: self.mudar_tela())
		self.tvwMenu.grid(row=1, column=0)

principal = Tk()
Aplicativo(principal)
principal.title('Sway LED')
principal.mainloop()