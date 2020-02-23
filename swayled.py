#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Feito por Marcos Oranmiyan.
Aqui controlamos LEDs ws2812x e 5050.
'''

# Importa a declaração print como uma função no Python 2.
from __future__ import print_function

import os
import sys
import config # Deve ser substituído pelo configparser
import configparser

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

		# Função para construir o menu do aplicativo e rodar a função para abrir a primeira tela
		self.construir_menu()
		self.mudar_tela(app_iniciando=True)

	def alterar_UDP(self):
		self.tvwMenu.item('serverLED', values=('ServerLED', 'A'))

	def mudar_tela(self, app_iniciando=False):
		def fechar_todas_as_telas():

			# Remove todas as janelas
			self.frameConfig.grid_remove()
			self.frameServerled.grid_remove()
			self.frameConfigApp.grid_remove()
			self.frameCores.grid_remove()
			self.frameEfeitos.grid_remove()
			self.frameLightpaint.grid_remove()
			self.frameDancypi.grid_remove()

		def construir_as_coisas():
			# Janelas sendo construídas no fundo.
			construir_cores(principal, self.frameCores)
			construir_efeitos(principal, self.frameEfeitos)
			construir_lightpaint(principal, self.frameLightpaint)
			construir_dancyPi(principal, self.frameDancypi)
			construir_configuracoes(principal, self.frameConfig)
			construir_serverled(principal, self.frameServerled)
			construir_config_app(principal, self.frameConfigApp)

		if app_iniciando:
			# Se o app estiver iniciando, setar que a tela salva nas configs abrirá
			# E construa todas as janelas no fundo
			menu_selecionado = Configuracoes().janela_padrao
			construir_as_coisas() 

		else:
			# Se o app já estiver iniciado, feche todas as janelas e
			# Abra a janela que o usuário selecionou no menu
			fechar_todas_as_telas()
			menu_selecionado = self.tvwMenu.selection()[0]
		
		if menu_selecionado == 'Cores': self.frameCores.grid(row=1,column=1,sticky=N)		
		elif menu_selecionado == 'Efeitos': self.frameEfeitos.grid(row=1,column=1,sticky=N)		
		elif menu_selecionado == 'Lightpaint': self.frameLightpaint.grid(row=1,column=1,sticky=N)		
		elif menu_selecionado == 'DancyPi': self.frameDancypi.grid(row=1,column=1,sticky=N)		
		elif menu_selecionado == u'Configurações': self.frameConfig.grid(row=1,column=1,sticky=N)		
		elif menu_selecionado == 'ServerLED': self.frameServerled.grid(row=1,column=1,sticky=N)		
		elif menu_selecionado == 'Aplicativo': self.frameConfigApp.grid(row=1,column=1,sticky=N)

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