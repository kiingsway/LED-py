#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Stack Tooltip: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter

import config

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

def construir_serverled(self, frame):
	""" Função para construir a tela do serverLED. A comunicação via UDP
	"""

	frameConfigTitulo = LabelFrame(frame)
	frameConfigTitulo.pack(fill=BOTH,expand=1)

	lblConfigTitulo = Label(frameConfigTitulo, text='Comunicação via UDP para outro dispositivo')
	lblConfigTitulo.pack(fill=BOTH,expand=1)


def construir_configuracoes(self, frame):
	""" Função para construir a tela das configurações.
	"""

	frameConfigTitulo = LabelFrame(frame)
	frameConfigTitulo.pack(fill=BOTH,expand=1)

	lblConfigTitulo = Label(frameConfigTitulo, text='Configurações dos LEDs e informações de energia')
	lblConfigTitulo.pack(fill=BOTH,expand=1)

	ledsConfigFrame = LabelFrame(frame, text='LEDs')
	ledsConfigFrame.pack(fill=BOTH,expand=1)

	ledsEnergiaFrame = LabelFrame(frame, text='Energia (informações adicionais)')
	ledsEnergiaFrame.pack(fill=BOTH,expand=1)

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

		lblQtdPixelsLED = Label(ledsConfigFrame, text='Quantidade')
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