try:
	# Python 3
	from tkinter import *
	from tkinter.ttk import Treeview
	# from tkinter.ttk import Combobox
except ImportError:
	# Python 2
	from Tkinter import *
	from ttk import Combobox, Treeview

import config, conexao, gui
# import led

class Aplicativo:

	def __init__(self):

		# Definindo variáveis do Tkinter
		self.app = Tk()
		self.app.title('Sway LED')

		# StringVar para as classes definir os status do programa
		self.str_status_leds = StringVar()
		# self.str_status_leds.trace("w", self.alterar_status)

		# Frames usados na janela do aplicativo
		self.frameCores = Frame(self.app)
		self.frameEfeitos = Frame(self.app)
		self.frameLightpaint = Frame(self.app)
		self.frameDancypi = Frame(self.app)
		self.frameServerled = Frame(self.app)
		self.frameConfig = Frame(self.app)
		self.frameConfigApp = Frame(self.app)

		# Chamando a classe Led (levando a stringvar de status), de Configurações, conexão e construir aplicação
		# self.led = led.Led(self.str_status_leds)
		self.config = config.Config()
		self.conexao = conexao.Conexao()
		self.build = gui.ConstruirAplicacao(self.app, self.str_status_leds)

		# Função para inserir todos os widgets necessários e alterar a tela
		self.construir_menu()
		self.mudar_tela(app_iniciando=True)

		# Abrir o aplicativo
		self.app.mainloop()

	def construir_menu(self):
		''' Definição usada para construir o menu do app.
		'''
		lblMenu = Label(self.app, text='Menu:')
		lblMenu.grid(row=0, column=0, sticky=W, padx=10)

		frameMenu = Frame(self.app, width=60, height=30)
		frameMenu.grid(row=1, column=0, sticky=N+W, padx=(10,0),pady=(0,0))

		self.tvwMenu = Treeview(frameMenu, height=8, columns=('Menu', 'Status'), show="tree")
		self.tvwMenu.column('#0', width=0)
		self.tvwMenu.column('Menu', width=100)
		self.tvwMenu.column('Status', width=50)
		menus = ['Cores', 'Efeitos', 'Lightpaint', 'DancyPi', 'ServerLED', 'Configurações', 'Aplicativo']

		# Definindo que o menu Aplicativo será filho de Configurações
		for menu in menus:
			if menu == 'Aplicativo':
				self.tvwMenu.insert('Configurações', 'end', menu, values=(menu))
				continue
			self.tvwMenu.insert('', 'end', menu, values=(menu), open=True)

		self.tvwMenu.bind('<<TreeviewSelect>>', lambda x: self.mudar_tela())
		self.tvwMenu.grid(row=1, column=0)

		self.lblStatusLed = Label(frameMenu, textvariable=self.str_status_leds, bd=1, relief=SUNKEN)
		self.lblStatusLed.grid(row=2, column=0, pady=(10,10))

	def mudar_tela(self, app_iniciando=False):

		def fechar_todas_as_telas():
			""" Destrói todas as janelas para serem recriadas novamente. """
			self.frameConfig.destroy()
			self.frameServerled.destroy()
			self.frameConfigApp.destroy()
			self.frameCores.destroy()
			self.frameEfeitos.destroy()
			self.frameLightpaint.destroy()
			self.frameDancypi.destroy()
		
			# Frames para serem mostrados
			self.frameCores = Frame(self.app)
			self.frameEfeitos = Frame(self.app)
			self.frameLightpaint = Frame(self.app)
			self.frameDancypi = Frame(self.app)
			self.frameServerled = Frame(self.app)
			self.frameConfig = Frame(self.app)
			self.frameConfigApp = Frame(self.app)

		if app_iniciando == False:
			fechar_todas_as_telas()
			menu_selecionado = self.tvwMenu.selection()[0]

		else: menu_selecionado = self.config.janela_padrao

		if menu_selecionado == 'Cores':
			self.build.construir_cores(self.frameCores)
			self.frameCores.grid(row=1,column=1,sticky=N)
		
		elif menu_selecionado == 'Efeitos':
			self.build.construir_efeitos(self.frameEfeitos)
			self.frameEfeitos.grid(row=1,column=1,sticky=N)
		
		# elif menu_selecionado == 'Lightpaint':
		# 	construir_lightpaint(self.app, self.frameLightpaint)
		# 	self.frameLightpaint.grid(row=1,column=1,sticky=N)
		
		# elif menu_selecionado == 'DancyPi':
		# 	construir_dancyPi(self.app, self.frameDancypi)
		# 	self.frameDancypi.grid(row=1,column=1,sticky=N)
		
		elif menu_selecionado == u'Configurações':
			self.build.construir_configuracoes(self.frameConfig)
			self.frameConfig.grid(row=1,column=1,sticky=N)
		
		elif menu_selecionado == 'ServerLED':
			self.build.construir_serverled(self.frameServerled)
			self.frameServerled.grid(row=1,column=1,sticky=N)
		
		elif menu_selecionado == 'Aplicativo':
			self.build.construir_config_app(self.frameConfigApp)
			self.frameConfigApp.grid(row=1,column=1,sticky=N)

if __name__ == '__main__':
	Aplicativo()