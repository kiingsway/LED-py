#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Stack CreateToolTip: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter

import os
import config # Deve ser substituído pelo configparser
import socket
import configparser
from pathlib import Path

import_neopixel = True
try:
	import neopixel
	import leds
except:
	import_neopixel = False
	class leds:
		def alterar_brilho(x): pass

try:
	# Python 3
	from tkinter import *
	from tkinter import messagebox
	import tkinter.ttk as ttk
	from tkinter.ttk import Combobox
except ImportError:
	# Python 2
	from Tkinter import *
	from ttk import Combobox as Combobox

comunicacao_udp = False

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 0     #miliseconds
        self.wraplength = 300   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class Funcionalidades:

	def iniciar_UDP(self):
		global comunicacao_udp

		if comunicacao_udp:
			comunicacao_udp = False
			self.btnIniciarUDP['text'] = 'Iniciar comunicação...'
		else:
			comunicacao_udp = True
			self.btnIniciarUDP['text'] = '-------------- Parar comunicação ---------------'


	def rgb(x, self):
		R = self.sclRvar.get()
		G = self.sclGvar.get()
		B = self.sclBvar.get()

		self.lblR['text'] = R
		self.lblG['text'] = G
		self.lblB['text'] = B

		self.lblCorAtualRGB['bg'] = '#%02x%02x%02x' % (R,G,B)

		if import_neopixel: leds.por_rgb(R,G,B)

class Configuracoes:
	"""
	Class que armazena funções para ler e gravar configurações que serão lidas/gravadas pelo aplicativo.
	Para criar uma configuração:
		1- Apague o config.ini
		2- Altere a def criar_config para criar as configurações
		3- Dê um valor padrão em __init__
		4- Crie um Obter copiano dos outros Obter
		5- Crie um Gravar copiano dos outros Gravar
		6- Configure o READ na variável.
			6a- Se for Var() ou CBX faça .set(<valor>)
			6b- Se for Entry faça .insert(0, <valor>)
		7- Confiure o UPDATE na variável
			7a- Faça um def antes da widget set_<configuração>
			7b- Caso for SCALE, use ['command'] = lambda x: set_<configuração>(x)
			7c- Caso for ENTRY, use txt<widget>.bind('<KeyRelease>', lambda x: set_<configuração>(x))
			7d- Caso for COMBOBOX, use cbx<widget>.bind("<<ComboboxSelected>>", lambda x: set_<configuração>(x))
	"""

	def criar_config(self, arquivo):
	    """
	    Create a config file
	    """
	    config = configparser.ConfigParser()
	    config.add_section("Aplicativo")
	    config.set("Aplicativo", "Janela padrão", self._janela_padrao)
	    config.set("Aplicativo", "Linhas em cores", self._linhas_em_cores)

	    config.add_section("Rede")
	    config.set("Rede", "IP", self._udp_ip)
	    config.set("Rede", "Porta", self._udp_port)
	    
	    config.add_section("LED1")
	    config.set("LED1", "Tipo", self._led1_tipo)
	    config.set("LED1", "Pino", self._led1_pino)
	    config.set("LED1", "Qtd", self._led1_qtd)

	    with open(arquivo, "w") as config_file:
	        config.write(config_file)

	def __init__(self):
		# Valores padrão do aplicativo
		self._janela_padrao = 'Cores'
		self._linhas_em_cores = '6'
		self._udp_ip = socket.gethostbyname(socket.gethostname())
		self._udp_port = '12000'
		self._led1_tipo = 'ws2812b'
		self._led1_pino = '18'
		self._led1_qtd = '144'

		self.pasta_atual = '\\'.join(str(Path(__file__).absolute()).split('\\')[0:-1])
		self.arquivo = '\\config.ini'
		self.caminho_arquivo = self.pasta_atual + self.arquivo

		# Setando variável para as configurações
		self.config = configparser.ConfigParser()
		
		# Se o arquivo config.ini não existir, criar outro
		if not os.path.exists(self.caminho_arquivo): self.criar_config(self.caminho_arquivo)

	def gravar_configuracao(self, secao, propiedade, valor):
		self.config.read(self.caminho_arquivo)
		# Change a value in the config
		self.config.set(secao, propiedade, valor)

		# Write changes back to the config file
		with open(self.caminho_arquivo, "w") as config_file:
			self.config.write(config_file)

	def obter_janela_padrao(self):
		# Lê o arquivo config.ini
		self.config.read(self.caminho_arquivo)

		# Retorna no widget
		return self.config.get('Aplicativo', 'Janela padrão')

	def obter_linhas_em_cores(self):
		# Lê o arquivo config.ini
		self.config.read(self.caminho_arquivo)

		# Retorna no widget
		return self.config.get('Aplicativo', 'Linhas em cores')

	def obter_udp(self):
		# Lê o arquivo config.ini
		self.config.read(self.caminho_arquivo)

		# Retorna no widget
		return (self.config.get('Rede', 'IP'), self.config.get('Rede', 'Porta'))

	def obter_led1_tipo(self):
		# Lê o arquivo config.ini
		self.config.read(self.caminho_arquivo)

		# Retorna no widget
		return self.config.get('LED1', 'Tipo')

	def obter_led1_pino(self):
		# Lê o arquivo config.ini
		self.config.read(self.caminho_arquivo)

		# Retorna no widget
		return self.config.get('LED1', 'Pino')

	def obter_led1_qtd(self):
		# Lê o arquivo config.ini
		self.config.read(self.caminho_arquivo)

		# Retorna no widget
		return self.config.get('LED1', 'Qtd')

	def gravar_janela_padrao(self, valor):
		secao = 'Aplicativo'
		propiedade = 'Janela padrão'
		self.gravar_configuracao(secao, propiedade, valor)

	def gravar_linhas_em_cores(self, valor):
		secao = 'Aplicativo'
		propiedade = 'Linhas em cores'
		self.gravar_configuracao(secao, propiedade, valor)

	def gravar_udp_ip(self, valor):
		secao = 'Rede'
		propiedade = 'IP'
		self.gravar_configuracao(secao, propiedade, valor)

	def gravar_udp_port(self, valor):
		secao = 'Rede'
		propiedade = 'Porta'
		self.gravar_configuracao(secao, propiedade, valor)

	def gravar_led1_tipo(self, valor):
		secao = 'LED1'
		propiedade = 'Tipo'
		self.gravar_configuracao(secao, propiedade, valor)

	def gravar_led1_pino(self, valor):
		secao = 'LED1'
		propiedade = 'Pino'
		self.gravar_configuracao(secao, propiedade, valor)

	def gravar_led1_qtd(self, valor):
		secao = 'LED1'
		propiedade = 'Qtd'
		self.gravar_configuracao(secao, propiedade, valor)

	
	linhas_cores = property(obter_linhas_em_cores, gravar_linhas_em_cores)
	janela_padrao = property(obter_janela_padrao, gravar_janela_padrao)
	udp_ip = property(obter_udp, gravar_udp_ip)
	udp_port = property(obter_udp, gravar_udp_port)
	led1_tipo = property(obter_led1_tipo, gravar_led1_tipo)
	led1_pino = property(obter_led1_pino, gravar_led1_pino)
	led1_qtd = property(obter_led1_qtd, gravar_led1_qtd)

def construir_lightpaint(self, frame):

	frameTitulo = LabelFrame(frame)
	frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblTitulo = Label(frameTitulo, text='Para ver esse efeito é necessário uma camera com\najuste de velocidade de disparo e um local escuro')
	lblTitulo.pack(fill=BOTH,expand=1)

	framePlayPauseLp = LabelFrame(frame)
	framePlayPauseLp.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	btnPlayPauseLp = Button(framePlayPauseLp, text='Selecione a imagem.../Rodar/Pausar')
	btnPlayPauseLp.pack(fill=BOTH,expand=1)

	frameImagem = LabelFrame(frame, text='Imagem')
	frameImagem.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblImagem = Label(frameImagem)
	lblImagem.pack(fill=BOTH, expand=1)

	txtNomeImagem = Entry(frameImagem)
	txtNomeImagem.pack(fill=BOTH,expand=1)

	btnAlterarImagem = Button(frameImagem, text='Selecionar imagem...')
	btnAlterarImagem.pack(fill=BOTH,expand=1)

	frameConfiguracoesLightpaint = LabelFrame(frame, text='Configurações')
	frameConfiguracoesLightpaint.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblVelFrame = Label(frameConfiguracoesLightpaint, text='Velocidade do frame:')
	lblVelFrame.grid(row=0,column=0, sticky=S)

	sclVelFrame = Scale(frameConfiguracoesLightpaint, from_=0, to=100, sliderlength=15, orient=HORIZONTAL)
	sclVelFrame.grid(row=0,column=1, sticky=W+E)

	lblVelFrame = Label(frameConfiguracoesLightpaint, text='Velocidade da coluna:')
	lblVelFrame.grid(row=1,column=0, sticky=S)

	sclVelFrame = Scale(frameConfiguracoesLightpaint, from_=0, to=100, sliderlength=15, orient=HORIZONTAL)
	sclVelFrame.grid(row=1,column=1, sticky=W+E)

	Checkbutton(frameConfiguracoesLightpaint, text='Inverter X').grid(row=2,column=0)
	Checkbutton(frameConfiguracoesLightpaint, text='Inverter Y').grid(row=2,column=1)

def construir_dancyPi(self, frame):

	frameTitulo = LabelFrame(frame)
	frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblTitulo = Label(frameTitulo, text='LEDs dançando ao som da música\n(ouvindo pelo microfone)')
	lblTitulo.pack(fill=BOTH,expand=1)

	frameIniciar = LabelFrame(frame)
	frameIniciar.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	btnIniciar = Button(frameIniciar, text='Iniciar/Parar')
	btnIniciar.pack(fill=BOTH,expand=1)

	lblFPS = Label(frameIniciar, text='FPS 50 / 50')
	lblFPS.pack(fill=BOTH,expand=1)

def construir_cores(self, frame):
	""" Função para construir a tela de cores únicas para enviar aos LEDs
	"""
	
	coluna = 3
	linha = int(Configuracoes().linhas_cores)

	frameTitulo = LabelFrame(frame)
	frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblTitulo = Label(frameTitulo, text='Clique nas cores para mudar a fita LED')
	lblTitulo.pack(fill=BOTH,expand=1)

	frameDesligarCores = LabelFrame(frame)
	frameDesligarCores.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	btnDesligarCores = Button(frameDesligarCores, text='Desligar')
	if import_neopixel: btnDesligarCores['command'] = leds.desligar
	btnDesligarCores.pack(fill=BOTH,expand=1)

	lblBrilho = Label(frameDesligarCores, text='Brilho:')
	lblBrilho.pack(fill=BOTH,expand=1)

	try: sclBrilho = Scale(frameDesligarCores, from_=0, to=255, sliderlength=15, orient=HORIZONTAL, command=lambda x: leds.alterar_brilho(sclBrilho.get()))
	except NameError: sclBrilho = Scale(frameDesligarCores, from_=0, to=255, sliderlength=15, orient=HORIZONTAL)

	sclBrilho.set(40)
	if import_neopixel: leds.alterar_brilho(sclBrilho.get())
	sclBrilho.pack(fill=BOTH,expand=1)

	frameCoresBtn = LabelFrame(frame)
	frameCoresBtn.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	c = 0
	l = 0

	rgb = ['#FF0000', '#00FF00', '#0000FF', '#FFFFFF']
	add = 255/(linha-1)

	def hex_to_color(h):
		h = h.lstrip('#')
		return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
	def color_to_hex(r,g,b):
		return '#%02x%02x%02x' % (r, g, b)

	# Variável armazenará todos os botões para as cores
	btnCor = {}

	"""
	Para as cores, serão 4 colunas: LED vermelho, Azul, Verde e o Branco.
	A última linha deve ser: Amarelo, Verde-água e Rosa. #FFFF00, #00FFFF e #FF00FF respectivamente.

	Dependendo de quantas linhas forem configuradas,
	a cor dessas linhas será dividida proporcionalmente ao número de botões em uma coluna.
	"""
 
	for i in range((linha*coluna)+1):

		# Obtendo a cor primária da coluna (primeira linha) e transformando em tuple
		r, g, b = hex_to_color(rgb[c])

		# Alterando a variável da cor que será construída com base na coluna
		if c == 0: g += add*l
		elif c == 1: b += add*l
		elif c == 2: r += add*l

		# Transformando em hexadecimal a nova cor
		bg = color_to_hex(int(r), int(g), int(b))

		# Definindo a ação de cada botão sobre que cor enviar para os LEDs.
		try: acao = lambda x = bg: leds.cores(x)
		except: pass

		# Construindo o botão
		btnCor[bg] = Button(frameCoresBtn, bg=bg, width=3, height=1, command=acao)
		btnCor[bg].grid(row=l, column=c, padx=10,pady=10)

		# Acrescenta que uma linha foi preenchida
		l += 1

		# Caso não for a primeira linha e der a quantidade de linhas que devem ser preenchidas
		# Reinicie a var de linha e acrescente um a var de coluna
		if i != 0 and (i+1) % linha == 0:
			c += 1
			l = 0

	frameCoresScale = LabelFrame(frame)
	frameCoresScale.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	self.sclRvar = IntVar()
	self.sclGvar = IntVar()
	self.sclBvar = IntVar()

	self.sclR = Scale(frameCoresScale, from_=0, length=200, to=255, showvalue=False, sliderlength=15, orient=HORIZONTAL,variable=self.sclRvar,command=lambda x: Funcionalidades().rgb(self))
	self.sclG = Scale(frameCoresScale, from_=0, length=200, to=255, showvalue=False, sliderlength=15, orient=HORIZONTAL,variable=self.sclGvar,command=lambda x: Funcionalidades().rgb(self))
	self.sclB = Scale(frameCoresScale, from_=0, length=200, to=255, showvalue=False, sliderlength=15, orient=HORIZONTAL,variable=self.sclBvar,command=lambda x: Funcionalidades().rgb(self))

	self.lblR = Label(frameCoresScale, text=self.sclRvar.get(), width=3)
	self.lblG = Label(frameCoresScale, text=self.sclGvar.get(), width=3)
	self.lblB = Label(frameCoresScale, text=self.sclBvar.get(), width=3)

	Label(frameCoresScale, text='R:').grid(row=0,column=0)
	self.lblR.grid(row=0,column=1)
	self.sclR.grid(row=0,column=2)

	Label(frameCoresScale, text='G:').grid(row=1,column=0)
	self.lblG.grid(row=1,column=1)
	self.sclG.grid(row=1,column=2)

	Label(frameCoresScale, text='B:').grid(row=2,column=0)
	self.lblB.grid(row=2,column=1)
	self.sclB.grid(row=2,column=2)

	frameCorAtualRGB = LabelFrame(frameCoresScale)
	frameCorAtualRGB.grid(row=3,column=0,columnspan=5)

	self.lblCorAtualRGB = Label(frameCorAtualRGB, text='',  width=33)
	self.lblCorAtualRGB['bg'] = '#000000'
	self.lblCorAtualRGB.pack(fill=BOTH, expand=1)

def construir_efeitos(self, frame):
	""" Função para construir a tela de efeitos
	"""

	frameTitulo = LabelFrame(frame)
	frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblTitulo = Label(frameTitulo, text='Selecione um efeito para ver a mágica acontecer')
	lblTitulo.pack(fill=BOTH,expand=1)

	frameEfeitos = LabelFrame(frame)
	frameEfeitos.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	# print('\n')
	efeitosVar = StringVar()
	efeitos = [("Desligado","Desligado"),("ArcoIris",1)]

	for efeito, val in efeitos:
		# print('Efeito:', efeito, '- Val:', val)
		Radiobutton(frameEfeitos, text=efeito, indicatoron = 0, variable=efeitosVar, value=val, relief=FLAT).pack(fill=BOTH,expand=1,pady=5,padx=5)

	# print('\n')
	# efeitosVar.set('Desligado')
	# print(efeitosVar.get())

	frameConfigEfeitos = LabelFrame(frame)
	frameConfigEfeitos.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	Label(frameConfigEfeitos, text='Velocidade do efeito').pack()
	Label(frameConfigEfeitos, text='Mais lento').pack(side=LEFT)
	Label(frameConfigEfeitos, text='Mais rápido').pack(side=RIGHT)

	sclVelEfeito = Scale(frameConfigEfeitos, from_=-50, to=50, sliderlength=15,orient=HORIZONTAL,showvalue=False)
	sclVelEfeito.bind('<Double-Button-1>', lambda x: sclVelEfeito.set(0))
	sclVelEfeito.pack(fill=BOTH,expand=1)

def construir_serverled(self, frame):
	""" Função para construir a tela do serverLED. A comunicação via UDP
	"""

	frameTitulo = LabelFrame(frame)
	frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblTitulo = Label(frameTitulo, text='Comunicação via UDP para outro dispositivo')
	lblTitulo.pack(fill=BOTH,expand=1)

	frameClienteServidor = LabelFrame(frame)
	frameClienteServidor.pack(fill=BOTH,expand=1,padx=(0,10))

	opcoesClienteServidor = ['Vou usar esse app para enviar os LEDs pela rede', 'Vou receber e ligar os LEDs nesse dispositivo']

	lblAtencao = Label(frameClienteServidor, text='LEDs não estão disponíveis nesse dispositivo, portanto...', fg='red')
	if import_neopixel == False:
		lblAtencao.pack(anchor='w')
		opcoesClienteServidor = opcoesClienteServidor[0].split(maxsplit=0)
	
	cbxCliServ = Combobox(frameClienteServidor)
	cbxCliServ['values'] = opcoesClienteServidor
	cbxCliServ.set(opcoesClienteServidor[0])
	cbxCliServ.pack(fill=BOTH,expand=1)

	frameUDP = LabelFrame(frame, text='Rede')
	frameUDP.pack(fill=BOTH,expand=1,padx=(0,10))

	def set_udpIP(x): Configuracoes().udp_ip = x.widget.get()
	def set_udpPORT(x): Configuracoes().udp_port = x.widget.get()

	lblIP = Label(frameUDP, text='IP:')
	lblIP.grid(row=0,column=0)

	txtIP = Entry(frameUDP)
	txtIP.insert(0, Configuracoes().udp_ip[0])
	txtIP.grid(row=0,column=1)

	lblPorta = Label(frameUDP, text='Porta:')
	lblPorta.grid(row=0,column=2)

	txtPorta = Entry(frameUDP)
	txtPorta.insert(0, Configuracoes().udp_port[1])
	txtPorta.grid(row=0,column=3)

	self.btnIniciarUDP = Button(frameUDP, text='Iniciar comunicação...')
	self.btnIniciarUDP['command'] = lambda: Funcionalidades().iniciar_UDP(self)
	self.btnIniciarUDP.grid(row=1,column=0, columnspan=5, sticky=W+E)

	txtIP.bind('<KeyRelease>', lambda x: set_udpIP(x))
	txtPorta.bind('<KeyRelease>', lambda x: set_udpPORT(x))

def construir_config_app(self, frame):
	""" Função para construir a tela das configurações.
	"""

	frameTitulo = LabelFrame(frame)
	frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblTitulo = Label(frameTitulo, text='Configurações do aplicativo')
	lblTitulo.pack(fill=BOTH,expand=1)

	appConfigFrame = LabelFrame(frame)
	appConfigFrame.pack(fill=BOTH,expand=1,padx=(0,10))

	lblJanelaDefault = Label(appConfigFrame, text='Iniciar na janela:')
	lblJanelaDefault.grid(row=0,column=0)

	janelas = ['Cores', 'Efeitos', 'Lightpaint', 'DancyPi', 'ServerLED', 'Configurações', 'Aplicativo']

	def set_janelaPadrao(x): Configuracoes().janela_padrao = x.widget.get()

	cbxJanelaDefault = Combobox(appConfigFrame)
	cbxJanelaDefault['values'] = janelas
	cbxJanelaDefault.set(Configuracoes().janela_padrao)
	cbxJanelaDefault.bind("<<ComboboxSelected>>", lambda x: set_janelaPadrao(x))
	cbxJanelaDefault.grid(row=0,column=1)

	appConfigCoresFrame = LabelFrame(frame, text='Cores')
	appConfigCoresFrame.pack(fill=BOTH,expand=1,padx=(0,10))

	lblQtdLinhasCores = Label(appConfigCoresFrame, text='Quantas linhas na tabela de Cores:')
	lblQtdLinhasCores.grid(row=0,column=0,sticky=S)

	def set_colunaCores(x):	Configuracoes().linhas_cores = QtdLinhasCoresVar.get()

	QtdLinhasCoresVar = StringVar()
	QtdLinhasCoresVar.set(Configuracoes().linhas_cores)
	sclQtdLinhasCores = Scale(appConfigCoresFrame, variable=QtdLinhasCoresVar, from_=3, to=10, sliderlength=15, orient=HORIZONTAL)
	sclQtdLinhasCores['command'] = lambda x: set_colunaCores(x)
	sclQtdLinhasCores.grid(row=0,column=1)

def construir_configuracoes(self, frame):
	""" Função para construir a tela das configurações.
	"""

	frameConfigTitulo = LabelFrame(frame)
	frameConfigTitulo.pack(fill=BOTH,expand=1,padx=(0,10))

	lblConfigTitulo = Label(frameConfigTitulo, text='Configurações dos LEDs e informações de energia')
	lblConfigTitulo.pack(fill=BOTH,expand=1)

	ledsConfigFrame = LabelFrame(frame, text='LEDs')
	ledsConfigFrame.pack(fill=BOTH,expand=1,padx=(0,10))

	ledsEnergiaFrame = LabelFrame(frame, text='Energia (informações adicionais)')
	ledsEnergiaFrame.pack(fill=BOTH,expand=1,padx=(0,10))

	tipos_de_leds = ['ws2812b', '5050']
	pinos_dos_leds = ['18']

	lblTipoLED = Label(ledsConfigFrame, text='Tipo:')
	lblPinoLED = Label(ledsConfigFrame, text='Pino:')
	lblQtdPixelsLED = Label(ledsConfigFrame, text='LEDs:')

	lblTipoLED.grid(row=0,column=1, sticky=W)	
	lblPinoLED.grid(row=0,column=2, sticky=W)
	lblQtdPixelsLED.grid(row=0,column=3, sticky=W)

	def construir_configs_leds(linha):

		# Por estar em testes, desabilitarei apenas para terminar de construir a interface
		# Apenas a primeira linha está programada. Para adicionar mais, precisa mudar as variáveis aqui e nas Configuracoes
		# Caso for usar mais, precisa adicionar opções para selecionar os LEDs em cada tela
		if linha > 0: estado_widgets = DISABLED
		else: estado_widgets = NORMAL

		lblLED = Label(ledsConfigFrame, text='LED {}:'.format(linha+1))
		lblLED['state'] = estado_widgets
		lblLED.grid(row=linha+1,column=0)

		def set_led1_tipo(x): Configuracoes().led1_tipo = cbxTiposLED.get()
		cbxTiposLED = Combobox(ledsConfigFrame,width=8)
		cbxTiposLED['values'] = tipos_de_leds
		cbxTiposLED['state'] = estado_widgets
		cbxTiposLED.set(Configuracoes().led1_tipo)
		cbxTiposLED.grid(row=linha+1,column=1, padx=(0,10))
		cbxTiposLED.bind("<<ComboboxSelected>>", lambda x: set_led1_tipo(x))

		def set_led1_pino(x): Configuracoes().led1_pino = cbxPinosLED.get()
		cbxPinosLED = Combobox(ledsConfigFrame,width=4)
		cbxPinosLED['values'] = pinos_dos_leds
		cbxPinosLED['state'] = estado_widgets
		cbxPinosLED.set(Configuracoes().led1_pino)
		cbxPinosLED.grid(row=linha+1,column=2, padx=(0,10))
		cbxPinosLED.bind("<<ComboboxSelected>>", lambda x: set_led1_pino(x))

		def set_led1Qtd(x):	Configuracoes().led1_qtd = txtQtdPixelsLED.get()
		txtQtdPixelsLED = Entry(ledsConfigFrame, width=5)
		txtQtdPixelsLED['state'] = estado_widgets
		txtQtdPixelsLED.insert(0, Configuracoes().led1_qtd)
		txtQtdPixelsLED.grid(row=linha+1,column=3, padx=(0,10))
		txtQtdPixelsLED.bind('<KeyRelease>', lambda x: set_led1Qtd(x))

		varInverterLED = BooleanVar()
		varInverterLED.set(config.led[linha]['inverter'])
		cbxInverterLED = Checkbutton(ledsConfigFrame, text="Inverter", var=varInverterLED)
		cbxInverterLED['state'] = DISABLED # EM TESTES...
		cbxInverterLED.grid(row=linha+1, column=7)

	def construir_energia_leds(linha):
		# Por estar em testes, desabilitarei apenas para terminar de construir a interface
		if linha > 0: estado_widgets = DISABLED
		else: estado_widgets = NORMAL

		lblLED = Label(ledsEnergiaFrame, text='LED {}:'.format(linha+1))
		lblLED['state'] = estado_widgets
		lblLED.grid(row=linha,column=0, padx=(0,10))

		lblVolts = Label(ledsEnergiaFrame)
		lblVolts['state'] = estado_widgets
		lblVolts['text'] = config.led[linha]['volts']		
		lblVolts.grid(row=linha,column=1, padx=(0,10))

		qtd = int(Configuracoes().led1_qtd)
		
		conta_amperes_leds = '{} leds = {}A ~ {}A'.format(
			qtd,
			qtd * config.led[linha]['ampere_pixel_min'] / 1000,
			qtd * config.led[linha]['ampere_pixel_max'] / 1000
			)
		
		conta_amperes_ledsFULL = '{0} leds * {1}mA /1000 = {2}A (mínimo)\n{0} leds * {3}mA /1000 = {4}A (máximo)'.format(
			qtd,
			config.led[linha]['ampere_pixel_min'],
			qtd * config.led[linha]['ampere_pixel_min'] / 1000,
			config.led[linha]['ampere_pixel_max'],			
			qtd * config.led[linha]['ampere_pixel_max'] / 1000
			)

		lblAmpere = Label(ledsEnergiaFrame)
		lblAmpere['state'] = estado_widgets
		lblAmpere['text'] = conta_amperes_leds
		lblAmpere.grid(row=linha,column=2, padx=(0,10))
		lblAmpereTooltip = CreateToolTip(lblAmpere, conta_amperes_ledsFULL)

	for i in range(4):
		construir_configs_leds(i)
		construir_energia_leds(i)