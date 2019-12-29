#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Stack Tooltip: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter

import config

import_neopixel = True
try:
	import neopixel
except: 
	import_neopixel = False

try:
	# Python 3
	from tkinter import *
	import tkinter.ttk as ttk
	from tkinter.ttk import Combobox
except ImportError:
	# Python 2
	from Tkinter import *
	from ttk import Combobox as Combobox

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

class funcionalidades:
	def iniciar_UDP(self):
		print('Iniciando conexão UDP...')

def construir_cores(self, frame):
	""" Função para construir a tela de cores únicas para enviar aos LEDs
	"""

	coluna = 3
	linha = config.linhasCores

	frameTitulo = LabelFrame(frame)
	frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblTitulo = Label(frameTitulo, text='Clique nas cores para mudar a fita LED')
	lblTitulo.pack(fill=BOTH,expand=1)

	frameDesligarCores = LabelFrame(frame)
	frameDesligarCores.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	btnDesligarCores = Button(frameDesligarCores, text='Desligar')
	btnDesligarCores.pack(fill=BOTH,expand=1)

	frameCoresBtn = LabelFrame(frame)
	frameCoresBtn.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	c = 0
	l = 0

	rgb = ['#FF0000', '#00FF00', '#0000FF']
	add = 255/(linha-1)

	def hex_to_color(h):
		h = h.lstrip('#')
		return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
	def color_to_hex(r,g,b):
		return '#%02x%02x%02x' % (r, g, b)

	for i in range(linha*coluna):

		r,g,b = hex_to_color(rgb[c])

		if c == 0:
			g += add*l
		elif c == 1:
			b += add*l
		elif c == 2:
			r += add*l

		bg = color_to_hex(int(r), int(g), int(b))


		btnCor = Button(frameCoresBtn, bg=bg, width=3, height=1)
		btnCor.grid(row=l, column=c, padx=10,pady=10)
		l += 1
		if i != 0 and (i+1) % linha == 0:
			c += 1
			l = 0
		if i == len(range(linha*coluna))-1:
			btnCor = Button(frameCoresBtn, bg='#fff', width=3, height=1)
			btnCor.grid(row=l, column=c, padx=10,pady=10)

	frameCoresScale = LabelFrame(frame)
	frameCoresScale.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	slrR = Scale(frameCoresScale, from_=0, to=255, sliderlength=15)
	slrG = Scale(frameCoresScale, from_=0, to=255, sliderlength=15)
	slrB = Scale(frameCoresScale, from_=0, to=255, sliderlength=15)
	slrW = Scale(frameCoresScale, from_=0, to=100, sliderlength=15)

	slrR.grid(row=0,column=0)
	slrG.grid(row=0,column=1)
	slrB.grid(row=0,column=2)
	slrW.grid(row=0,column=3)

def construir_efeitos(self, frame):
	""" Função para construir a tela de efeitos
	"""

	frameTitulo = LabelFrame(frame)
	frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblTitulo = Label(frameTitulo, text='Selecione um efeito para ver a mágica acontecer')
	lblTitulo.pack(fill=BOTH,expand=1)

	frameEfeitos = LabelFrame(frame)
	frameEfeitos.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	efeitos = [('Desligado','0'),('Arco íris','1')]

	for efeito, val in efeitos:
		Radiobutton(frameEfeitos, text=efeito, indicatoron = 0, value=val, relief=FLAT).pack(fill=BOTH,expand=1,pady=5,padx=5)


def construir_serverled(self, frame, app):
	""" Função para construir a tela do serverLED. A comunicação via UDP
	"""

	frameTitulo = LabelFrame(frame)
	frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(0,10))

	lblTitulo = Label(frameTitulo, text='Comunicação via UDP para outro dispositivo')
	lblTitulo.pack(fill=BOTH,expand=1)

	frameClienteServidor = LabelFrame(frame)
	frameClienteServidor.pack(fill=BOTH,expand=1,padx=(0,10))

	opcoesClienteServidor = ['Vou usar esse app para enviar os LEDs', 'Vou receber e ligar os LEDs nesse app']

	lblAtencao = Label(frameClienteServidor, text='LEDs não foram configurados, portanto')
	if import_neopixel == False:
		lblAtencao.pack(anchor=W)
		opcoesClienteServidor = ['Vou usar esse app para enviar os LEDs']
	
	cbxCliServ = Combobox(frameClienteServidor)
	cbxCliServ['values'] = opcoesClienteServidor
	cbxCliServ.set('Vou usar esse app para disparar os LEDs')
	cbxCliServ.pack(fill=BOTH,expand=1)

	frameUDP = LabelFrame(frame, text='Rede')
	frameUDP.pack(fill=BOTH,expand=1,padx=(0,10))

	lblIP = Label(frameUDP, text='IP:')
	lblIP.grid(row=0,column=0)

	txtIP = Entry(frameUDP)
	txtIP.insert(0, config.udp['ip'])
	txtIP.grid(row=0,column=1)

	lblPorta = Label(frameUDP, text='Porta:')
	lblPorta.grid(row=0,column=2)

	txtPorta = Entry(frameUDP)
	txtPorta.insert(0, config.udp['porta'])
	txtPorta.grid(row=0,column=3)

	btnIniciarUDP = Button(frameUDP, text='Iniciar comunicação...')
	btnIniciarUDP['command'] = lambda: funcionalidades.iniciar_UDP(app)
	btnIniciarUDP.grid(row=1,column=0, columnspan=5, sticky=W+E)

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

	janelas = ['Cores', 'Efeitos', 'Lightpaint', 'DancyPi', 'Server LED', 'Configurações', '-- Aplicativo']

	cbxJanelaDefault = Combobox(appConfigFrame)
	cbxJanelaDefault['values'] = janelas
	cbxJanelaDefault.set(config.janelaDefault)
	cbxJanelaDefault.grid(row=0,column=1)

	appConfigCoresFrame = LabelFrame(frame, text='Cores')
	appConfigCoresFrame.pack(fill=BOTH,expand=1,padx=(0,10))

	lblQtdLinhasCores = Label(appConfigCoresFrame, text='Quantas linhas na tabela de Cores:')
	lblQtdLinhasCores.grid(row=0,column=0,sticky=S)

	sclQtdLinhasCores = Scale(appConfigCoresFrame, from_=3, to=10, sliderlength=15, orient=HORIZONTAL)
	sclQtdLinhasCores.set(config.linhasCores)
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

	def construir_configs_leds(linha):

		# Por estar em testes, desabilitarei apenas para terminar de construir a interface
		if linha > 0: estado_widgets = DISABLED
		else: estado_widgets = NORMAL

		lblLED = Label(ledsConfigFrame, text='LED {}:'.format(linha+1))
		lblLED['state'] = estado_widgets
		lblLED.grid(row=linha,column=0)

		lblTipoLED = Label(ledsConfigFrame, text='Tipo')
		lblTipoLED['state'] = estado_widgets
		lblTipoLED.grid(row=linha,column=1)

		cbxTiposLED = Combobox(ledsConfigFrame,width=8)
		cbxTiposLED['values'] = tipos_de_leds
		cbxTiposLED['state'] = estado_widgets
		cbxTiposLED.set(config.led[linha]['tipo'])
		cbxTiposLED.grid(row=linha,column=2, padx=(0,10))

		lblPinoLED = Label(ledsConfigFrame, text='Pino')
		lblPinoLED['state'] = estado_widgets
		lblPinoLED.grid(row=linha,column=3)

		cbxPinosLED = Combobox(ledsConfigFrame,width=4)
		cbxPinosLED['values'] = pinos_dos_leds
		cbxPinosLED['state'] = estado_widgets
		cbxPinosLED.set(config.led[linha]['pino'])
		cbxPinosLED.grid(row=linha,column=4, padx=(0,10))

		lblQtdPixelsLED = Label(ledsConfigFrame, text='Pixels')
		lblQtdPixelsLED['state'] = estado_widgets		
		lblQtdPixelsLED.grid(row=linha,column=5)

		txtQtdPixelsLED = Entry(ledsConfigFrame, width=5)
		txtQtdPixelsLED['state'] = estado_widgets
		txtQtdPixelsLED.insert(0, config.led[linha]['qtd'])
		txtQtdPixelsLED.grid(row=linha,column=6, padx=(0,10))

		varInverterLED = BooleanVar()
		varInverterLED.set(config.led[linha]['inverter'])
		cbxInverterLED = Checkbutton(ledsConfigFrame, text="Inverter", var=varInverterLED)
		cbxInverterLED['state'] = DISABLED # EM TESTES...
		cbxInverterLED.grid(row=linha, column=7)

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
		
		conta_amperes_leds = '{} leds = {}A ~ {}A'.format(
			config.led[linha]['qtd'],
			config.led[linha]['qtd'] * config.led[linha]['ampere_pixel_min'] / 1000,
			config.led[linha]['qtd'] * config.led[linha]['ampere_pixel_max'] / 1000
			)
		
		conta_amperes_ledsFULL = '{0} leds * {1}mA /1000 = {2}A (mínimo)\n{0} leds * {3}mA /1000 = {4}A (máximo)'.format(
			config.led[linha]['qtd'],
			config.led[linha]['ampere_pixel_min'],
			config.led[linha]['qtd'] * config.led[linha]['ampere_pixel_min'] / 1000,
			config.led[linha]['ampere_pixel_max'],			
			config.led[linha]['qtd'] * config.led[linha]['ampere_pixel_max'] / 1000
			)

		lblAmpere = Label(ledsEnergiaFrame)
		lblAmpere['state'] = estado_widgets
		lblAmpere['text'] = conta_amperes_leds
		lblAmpere.grid(row=linha,column=2, padx=(0,10))
		lblAmpereTooltip = CreateToolTip(lblAmpere, conta_amperes_ledsFULL)

	for i in range(4):
		construir_configs_leds(i)
		construir_energia_leds(i)