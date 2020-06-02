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

import config, led, conexao

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

class ConstruirAplicacao:

	def __init__(self, app, var_status_leds):

		self._app = app

		self.config = config.Config()

		self.led = led.Led(var_status_leds)

		self.conexao = conexao.Conexao()

		self.var_status_leds = var_status_leds

		self.verificar_se_temos_led()

	def construir_cores(self, frame):
		""" Função para construir a tela de cores únicas para enviar aos LEDs
		"""
		coluna = 3
		linha = self.config.linhas_cores

		frameTitulo = LabelFrame(frame)
		frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(10,10))

		lblTitulo = Label(frameTitulo, text='Clique nas cores para mudar a fita LED')
		lblTitulo.pack(fill=BOTH,expand=1)

		frameDesligarCores = LabelFrame(frame)
		frameDesligarCores.pack(fill=BOTH,expand=1,pady=(0,10),padx=(10,10))

		btnDesligarCores = Button(frameDesligarCores, text='Desligar')
		btnDesligarCores['command'] = self.led.desligar
		btnDesligarCores.pack(fill=BOTH,expand=1)

		lblBrilho = Label(frameDesligarCores, text='Brilho:')
		lblBrilho.pack(fill=BOTH,expand=1)
		
		sclBrilho = Scale(frameDesligarCores, from_=0, to=255, sliderlength=15, orient=HORIZONTAL, command=lambda b: self.led.alterar_brilho(sclBrilho.get()))
		sclBrilho.set(40)
		sclBrilho.pack(fill=BOTH,expand=1)

		frameCoresBtn = LabelFrame(frame)
		frameCoresBtn.pack(fill=BOTH,expand=1,pady=(0,10),padx=(10,10))

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
			r, g, b = self.led.hex_to_color(rgb[c])

			# Alterando a variável da cor que será construída com base na coluna
			if c == 0: g += add*l
			elif c == 1: b += add*l
			elif c == 2: r += add*l

			# Transformando em hexadecimal a nova cor
			bg = self.led.color_to_hex(int(r), int(g), int(b))

			# Definindo a ação de cada botão sobre que cor enviar para os LEDs.
			# try: acao = lambda x = bg: leds.cores(x)
			try: acao = lambda hex = bg: self.led.enviar_rgb(hex=hex)
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
		frameCoresScale.pack(fill=BOTH,expand=1,pady=(0,10),padx=(10,10))

		self.sclRvar = IntVar()
		self.sclGvar = IntVar()
		self.sclBvar = IntVar()

		self.sclR = Scale(frameCoresScale, from_=0, length=200, to=255, showvalue=False, sliderlength=15, orient=HORIZONTAL,variable=self.sclRvar,command=lambda x: self.led.enviar_rgb(self.sclRvar.get(),self.sclGvar.get(),self.sclBvar.get()))
		self.sclG = Scale(frameCoresScale, from_=0, length=200, to=255, showvalue=False, sliderlength=15, orient=HORIZONTAL,variable=self.sclGvar,command=lambda x: self.led.enviar_rgb(self.sclRvar.get(),self.sclGvar.get(),self.sclBvar.get()))
		self.sclB = Scale(frameCoresScale, from_=0, length=200, to=255, showvalue=False, sliderlength=15, orient=HORIZONTAL,variable=self.sclBvar,command=lambda x: self.led.enviar_rgb(self.sclRvar.get(),self.sclGvar.get(),self.sclBvar.get()))

		self.lblR = Label(frameCoresScale, textvariable=self.sclRvar, width=3)
		self.lblG = Label(frameCoresScale, textvariable=self.sclGvar, width=3)
		self.lblB = Label(frameCoresScale, textvariable=self.sclBvar, width=3)

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

	def construir_serverled(self, frame):
		""" Função para construir a tela do serverLED. A comunicação via UDP
		"""

		frameTitulo = LabelFrame(frame)
		frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(10,10))

		lblTitulo = Label(frameTitulo, text='Comunicação via UDP para outro dispositivo')
		lblTitulo.pack(fill=BOTH,expand=1)

		frameClienteServidor = LabelFrame(frame)
		frameClienteServidor.pack(fill=BOTH,expand=1,padx=(10,10))

		opcoesClienteServidor = ['Vou usar esse app para enviar os LEDs pela rede', 'Vou receber e ligar os LEDs nesse dispositivo']

		lblAtencao = Label(frameClienteServidor, text='LEDs não estão disponíveis nesse dispositivo, portanto...', fg='red')
		if self.led.neopixel_importado == False:
			lblAtencao.pack(anchor='w')
			opcoesClienteServidor = opcoesClienteServidor[0].split(maxsplit=0)
		
		cbxCliServ = Combobox(frameClienteServidor)
		cbxCliServ['values'] = opcoesClienteServidor
		cbxCliServ.set(opcoesClienteServidor[0])
		cbxCliServ.pack(fill=BOTH,expand=1)

		frameUDP = LabelFrame(frame, text='Rede')
		frameUDP.pack(fill=BOTH,expand=1,padx=(10,10))

		def set_udp(w):
			port = self.config.udp[1]

			# Validando se é um número. Se não for, utiliza o último inserido.
			if portVar.get().isdigit(): port = portVar.get()

			self.config.udp = (ipVar.get(), port)

			self.var_status_leds.set("Sem LED importado.\n Enviando para {}, {}".format(ipVar.get(), port))

		lblIP = Label(frameUDP, text='IP:')
		lblIP.grid(row=0,column=0)

		ipVar = StringVar()
		portVar = StringVar()

		txtIP = Entry(frameUDP, textvariable=ipVar)
		txtIP.insert(0, self.config.udp[0])
		txtIP.grid(row=0,column=1)

		lblPorta = Label(frameUDP, text='Porta:')
		lblPorta.grid(row=0,column=2)

		txtPorta = Entry(frameUDP, textvariable=portVar)
		txtPorta.insert(0, self.config.udp[1])
		txtPorta.grid(row=0,column=3)

		# self.btnIniciarUDP = Button(frameUDP, text='Iniciar comunicação...')
		# self.btnIniciarUDP['command'] = lambda: self.iniciar_conexao(self.var_status_leds)
		# self.btnIniciarUDP.grid(row=1,column=0, columnspan=5, sticky=W+E)

		self.btnIniciarUDP = Button(frameUDP, text='Fechar ServerLED')
		self.btnIniciarUDP['command'] = lambda: self.fechar_serverLED()
		self.btnIniciarUDP.grid(row=1,column=0, columnspan=5, sticky=W+E)

		txtIP.bind('<KeyRelease>', lambda x: set_udp(x))
		txtPorta.bind('<KeyRelease>', lambda x: set_udp(x))

	def construir_configuracoes(self, frame):
		""" Função para construir a tela das configurações.	"""
		frameConfigTitulo = LabelFrame(frame)
		frameConfigTitulo.pack(fill=BOTH,expand=1,padx=(10,10))

		lblConfigTitulo = Label(frameConfigTitulo, text='Configurações dos LEDs e informações de energia')
		lblConfigTitulo.pack(fill=BOTH,expand=1)

		ledsConfigFrame = LabelFrame(frame, text='LEDs')
		ledsConfigFrame.pack(fill=BOTH,expand=1,padx=(10,10))

		ledsEnergiaFrame = LabelFrame(frame, text='Energia (informações adicionais)')
		ledsEnergiaFrame.pack(fill=BOTH,expand=1,padx=(10,10))

		tipos_de_leds = ['ws2812b', '5050']
		pinos_dos_leds = ['13', '18']

		lblTipoLED = Label(ledsConfigFrame, text='Tipo:')
		lblPinoLED = Label(ledsConfigFrame, text='Pino:')
		lblQtdPixelsLED = Label(ledsConfigFrame, text='LEDs:')
		lblInverterLED = Label(ledsConfigFrame, text='Inverter:')

		lblTipoLED.grid(row=0,column=1, sticky=W)	
		lblPinoLED.grid(row=0,column=2, sticky=W)
		lblQtdPixelsLED.grid(row=0,column=3, sticky=W)
		lblInverterLED.grid(row=0,column=4, sticky=W)

		def construir_configs_leds(linha):

			# Por estar em testes, desabilitarei apenas para terminar de construir a interface
			if linha > 0: estado_widgets = DISABLED
			else: estado_widgets = NORMAL

			lblLED = Label(ledsConfigFrame, text='LED {}:'.format(linha+1))
			lblLED['state'] = estado_widgets
			lblLED.grid(row=linha+1,column=0)

			cbxTiposLED = Combobox(ledsConfigFrame,width=8)
			cbxTiposLED['values'] = tipos_de_leds
			# cbxTiposLED['state'] = estado_widgets
			cbxTiposLED['state'] = DISABLED
			cbxTiposLED.set(self.config.led_type)
			cbxTiposLED.grid(row=linha+1,column=1, padx=(0,10))

			cbxPinosLED = Combobox(ledsConfigFrame,width=4)
			cbxPinosLED['values'] = pinos_dos_leds
			cbxPinosLED['state'] = estado_widgets
			cbxPinosLED.set(self.config.led_pin)
			cbxPinosLED.grid(row=linha+1,column=2, padx=(0,10))

			QtdLEDVar = StringVar()
			QtdLEDVar.set(self.config.led_count)
			txtQtdPixelsLED = Entry(ledsConfigFrame, textvariable=QtdLEDVar, width=5)
			txtQtdPixelsLED['state'] = estado_widgets
			# txtQtdPixelsLED.insert(0, self.config.led_count)
			txtQtdPixelsLED.grid(row=linha+1,column=3, padx=(0,10))

			cbxInverterLED = Combobox(ledsConfigFrame,width=4)
			cbxInverterLED['values'] = ['Sim', 'Não']
			cbxInverterLED['state'] = estado_widgets
			cbxInverterLED.set('Sim' if self.config.led_invert else 'Não')
			cbxInverterLED.grid(row=linha+1, column=4, padx=(0,10))

			def salvar_configs(c):
				qtd_pixels = self.config.led_count

				# Validando se é um número. Se não for, utiliza o último inserido.
				if QtdLEDVar.get().isdigit(): qtd_pixels = QtdLEDVar.get()

				self.config.led_type = cbxTiposLED.get()
				self.config.led_pin = cbxPinosLED.get()
				self.config.led_count = qtd_pixels
				self.config.led_invert = False if cbxInverterLED.get() == 'Não' else True

			cbxTiposLED.bind("<<ComboboxSelected>>", salvar_configs)
			cbxPinosLED.bind("<<ComboboxSelected>>", salvar_configs)
			txtQtdPixelsLED.bind('<KeyRelease>', salvar_configs)
			cbxInverterLED.bind("<<ComboboxSelected>>", salvar_configs)

		def construir_energia_leds(linha):
			# Por estar em testes, desabilitarei apenas para terminar de construir a interface
			if linha > 0: estado_widgets = DISABLED
			else: estado_widgets = NORMAL

			lblLED = Label(ledsEnergiaFrame, text='LED {}:'.format(linha+1))
			lblLED['state'] = estado_widgets
			lblLED.grid(row=linha,column=0, padx=(0,10))

			lblVolts = Label(ledsEnergiaFrame)
			lblVolts['state'] = estado_widgets
			lblVolts['text'] = '5v'
			lblVolts.grid(row=linha,column=1, padx=(0,10))

			led_count = int(self.config.led_count)
			
			conta_amperes_leds = '{} leds = {}A ~ {}A'.format(
				led_count,
				led_count * 20 / 1000,
				led_count * 60 / 1000
				)
			
			conta_amperes_ledsFULL = '{0} leds * {1}mA /1000 = {2}A (mínimo)\n{0} leds * {3}mA /1000 = {4}A (máximo)'.format(
				led_count, 20, led_count * 20 / 1000, 60, led_count * 60 / 1000)

			lblAmpere = Label(ledsEnergiaFrame)
			lblAmpere['state'] = estado_widgets
			lblAmpere['text'] = conta_amperes_leds
			lblAmpere.grid(row=linha,column=2, padx=(0,10))
			lblAmpereTooltip = CreateToolTip(lblAmpere, conta_amperes_ledsFULL)

		for i in range(2):
			construir_configs_leds(i)
			construir_energia_leds(i)

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

		def set_janelaPadrao(x): self.config.janela_padrao = x.widget.get()

		cbxJanelaDefault = Combobox(appConfigFrame)
		cbxJanelaDefault['values'] = janelas
		cbxJanelaDefault.set(self.config.janela_padrao)
		cbxJanelaDefault.bind("<<ComboboxSelected>>", lambda x: set_janelaPadrao(x))
		cbxJanelaDefault.grid(row=0,column=1)

		appConfigCoresFrame = LabelFrame(frame, text='Cores')
		appConfigCoresFrame.pack(fill=BOTH,expand=1,padx=(0,10))

		lblQtdLinhasCores = Label(appConfigCoresFrame, text='Quantas linhas na tabela de Cores:')
		lblQtdLinhasCores.grid(row=0,column=0,sticky=S)

		def set_linhasCores(x):
			# print(x)
			self.config.linhas_cores = int(x)

		sclQtdLinhasCores = Scale(appConfigCoresFrame, from_=3, to=10, sliderlength=15, orient=HORIZONTAL, command= lambda x: set_linhasCores(x))
		sclQtdLinhasCores.set(self.config.linhas_cores)
		sclQtdLinhasCores.grid(row=0,column=1)

	def construir_efeitos(self, frame):
		""" Função para construir a tela de efeitos
		"""

		frameTitulo = LabelFrame(frame)
		frameTitulo.pack(fill=BOTH,expand=1,pady=(0,10),padx=(10,10))

		lblTitulo = Label(frameTitulo, text='Selecione um efeito para ver a mágica acontecer')
		lblTitulo.pack(fill=BOTH,expand=1)

		frameEfeitos = LabelFrame(frame)
		frameEfeitos.pack(fill=BOTH,expand=1,pady=(0,10),padx=(10,10))

		efeitos = [('Desligado','0'),('Arco íris','1')]

		def alterar_efeito(efeito):

			if efeito == 'Desligado': self.led.enviar_comando('!E0v{}'.format(sclVelEfeito.get()))
			elif efeito == 'Arco íris': self.led.enviar_comando('!E1v{}'.format(sclVelEfeito.get()))

		for efeito, val in efeitos:
			Radiobutton(frameEfeitos, text=efeito, indicatoron = 0, value=val, command=lambda e = efeito: alterar_efeito(e), relief=FLAT).pack(fill=BOTH,expand=1,pady=5,padx=5)

		frameConfigEfeitos = LabelFrame(frame)
		frameConfigEfeitos.pack(fill=BOTH,expand=1,pady=(0,10),padx=(10,10))

		Label(frameConfigEfeitos, text='Velocidade do efeito').pack()
		Label(frameConfigEfeitos, text='Mais lento').pack(side=LEFT)
		Label(frameConfigEfeitos, text='Mais rápido').pack(side=RIGHT)

		sclVelEfeito = Scale(frameConfigEfeitos, from_=-50, to=50, sliderlength=15,orient=HORIZONTAL,showvalue=False)
		sclVelEfeito.bind('<Double-Button-1>', lambda x: sclVelEfeito.set(0))
		sclVelEfeito.pack(fill=BOTH,expand=1)

	def iniciar_conexao(self,status):

		cx = conexao.Conexao()

		cx.enviar_teste()
		status.set('aaaa')

	def fechar_serverLED(self):
		self.led.enviar_comando('off')

	def verificar_se_temos_led(self):
		ip, udp = self.config.udp
		if not led.neopixel_importado: self.var_status_leds.set("Sem LED importado.\n Enviando para\nIP: {}, Port: {}".format(ip, udp))

if __name__ == '__main__':
	app = Tk()

	statusVar = StringVar()

	statusTeste = Label(app, bd=1, textvariable=statusVar, relief=SUNKEN)
	statusTeste.pack()

	testFrame = Frame(app)
	testFrame.pack()

	a = ConstruirAplicacao(app, statusVar)

	a.construir_cores(testFrame)
	# a.construir_serverled(testFrame)

	app.mainloop()