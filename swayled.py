#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

# Importanto bibliotecas comuns
import os
import sys
import time
import random
import globals
import argparse
import threading
from decimal import *
from itertools import product
from functools import partial

# Definição de erros

erros = []
def addErros(classe,codigo,erro):
	erros.append(dict(tituloErro=classe,
    codigoProblematico=codigo,
    erroPython=erro))

# Importanto biblioteca de LEDs

try: from Tkinter import *
except ImportError: from tkinter import *
except Exception: addErros((str(sys.exc_info()[0])+': Tkinter está instalado?'),'from Tkinter import *',sys.exc_info()[1])

try: import ttk
except ImportError: import tkinter.ttk as ttk
except Exception: addErros((str(sys.exc_info()[0])+': ttk está instalado?'),'from Tkinter import *',sys.exc_info()[1])

try: import tkMessageBox
except ImportError: import tkinter.messagebox as tkMessageBox

try: from tkColorChooser import askcolor
except ImportError: from tkinter.colorchooser import askcolor

try: import tkFileDialog
except ImportError: import tkinter.filedialog as tkFileDialog
except: addErros("tkinter instalado?","try: import tkFileDialog",sys.exc_info()[1])

try: from effects import *
except ImportError: addErros('ImportError: O arquivo efeitos.py está na pasta do código?','from effects import *',sys.exc_info()[1])
except NotImplementedError:	addErros('NotImplementedError: Erro na importação da biblioteca effects.py','from effects import *',sys.exc_info()[1])

try: from effectsBeta import *
except ImportError: addErros('ImportError: O arquivo efeitosBeta.py está na pasta do código?','from effectsBeta import *',sys.exc_info()[1])
except NotImplementedError:	addErros('NotImplementedError: Erro no código da biblioteca effectsBeta.py','from effectsBeta import *',sys.exc_info()[1])

try: from lightpaint import lightpainting as lp
except ImportError: addErros('ImportError: O arquivo lightpaint.py está na pasta do código?','from effectsBeta import *',sys.exc_info()[1])
except NotImplementedError: addErros('NotImplementedError: Erro no código da biblioteca lightpaint.py','import lightpaint',sys.exc_info()[1])

try: from led5050 import *
except NotImplementedError:	addErros('NotImplementedError: Erro no código da biblioteca led5050.py','try: from led5050 import *',sys.exc_info()[1])
except ModuleNotFoundError: addErros('ModuleNotFoundError: Um módulo não foi executado','from led5050 import *',sys.exc_info()[1])
except ImportError: addErros('ImportError: O arquivo led5050.py está na pasta do código?','try: from led5050 import *',sys.exc_info()[1])
except Exception: addErros(sys.exc_info()[0],'from Tkinter import *',sys.exc_info()[1])

# Lightpainting
try: from PIL import ImageTk, Image
except: print('Sem bibliotecas de imagem. Instale-as com: pip install Pillow')

class efeitos(object):

    def campos_validados(self):
        if self.txtPontoA.get() == '':
            tkMessageBox.showinfo("Entrada necessaria", "Qual LED eu ligo? Ponto A necessario")
            return False
        return True

    def ligar_leds(self, event=0):
        if not self.campos_validados(): return

        globals.outroEfeitoRainbow = False

        pontoA = int(txtPontoA.get())
        if txtPontoB.get() == '': pontoB = pontoA
        else: pontoB = int(txtPontoB.get())
        if txtR.get() == '': redLed = 0
        else: redLed = int(txtR.get())
        if txtG.get() == '': greenLed = 0
        else: greenLed = int(txtG.get())
        if txtB.get() == '': blueLed = 0
        else: blueLed = int(txtB.get())
        if txtVel.get() == '': vel = 0.1
        else: vel = float(txtVel.get())

        if txtFuncao1.get() == '': funcao1 = 3
        else: funcao1 = int(txtFuncao1.get())

        if cmbEffects.current() == 0:
            testThread = threading.Thread(target=acenderLEDEffect,args=(pontoA,pontoB,redLed,greenLed,blueLed,))
            testThread.start()
        if cmbEffects.current() == 1:
            testThread = threading.Thread(target=simpleBassEffect,args=(pontoA,pontoB,redLed,greenLed,blueLed,vel,))
            testThread.start()
        if cmbEffects.current() == 2:
            testThread = threading.Thread(target=bassBracoEffectBETA,args=(pontoB/10,redLed,greenLed,blueLed,vel,))
            testThread.start()
        if cmbEffects.current() == 3:
            testThread = threading.Thread(target=corteCobraEffectBETA,args=(pontoA,pontoB,redLed,greenLed,blueLed,vel,funcao1,))
            testThread.start()
        if cmbEffects.current() == 4:
            testThread = threading.Thread(target=laserLeftEffectBETA,args=(pontoA,pontoB,redLed,greenLed,blueLed,vel,funcao1,))
            testThread.start()
        if cmbEffects.current() == 5:
            testThread = threading.Thread(target=corteEffectBETA,args=(pontoA,pontoB,redLed,greenLed,blueLed,vel,))
            testThread.start()
        if cmbEffects.current() == 6:
            testThread = threading.Thread(target=teatroEffect,args=(pontoA,pontoB,redLed,greenLed,blueLed,vel,funcao1))
            testThread.start()
        if cmbEffects.current() == 7:
            testThread = threading.Thread(target=posAleatoriaFade,args=(pontoA,pontoB,redLed,greenLed,blueLed,vel))
            testThread.start()
        if cmbEffects.current() == 8:
            testThread = threading.Thread(target=bassBracoInvertEffect2,args=(pontoA,pontoB,redLed,greenLed,blueLed,vel))
            testThread.start()
        if cmbEffects.current() == 9:
            testThread = threading.Thread(target=megaman,args=(pontoA,pontoB,redLed,greenLed,blueLed,vel))
            testThread.start()

    def outros_efeitos(self):
        efeito = v.get()
        if efeito == "0":
            print("Desliguei o rainbowCycle")
            globals.outroEfeitoRainbow = False
        if efeito == "1":
            print("Tentando entrar no rainbowCycle",end=' ')
            outroEfeitoThread = threading.Thread(target=rainbowCycle)
            globals.outroEfeitoRainbow = True
            print('globals.outroEfeitoRainbow = {}'.format(globals.outroEfeitoRainbow))
            outroEfeitoThread.start()

    def desligar(self):
        try: off()
        except: pass

# Classes das janelas do programa

class JanelaLightpaint(Toplevel):
    """ Classe que define a janela de lightpaint
    Lightpaint é fotografia em longa exposição com
    alguma luz em movimento. """

    def __init__(self):
        # Constrói toda a janela lightpaint
        Toplevel.__init__(self)
        self.title("Lightpaint")
        self.construir_janela()
        self.abrir_imagem()

    def construir_janela(self):
        # Define o primeiro quadro:
        frame_campos1 = Frame(self, relief=RAISED, bd=5)
        self.txtImagem = Entry(frame_campos1, width=40)
        btnEscolherImagem = Button(frame_campos1, text='Escolher imagem...', command=self.abrir_imagem)
        self.btnPlayPause = Button(frame_campos1, text='Pausar', command=self.play_pausePainting)

        # Define o segundo quadro:
        frame_campos2 = Frame(self, relief=RAISED, bd=5)
        lblTaxaFrame = Label(frame_campos2, text='Taxa Frame:')
        btnDiminuirFrame = Button(frame_campos2, text='-', command=lambda:self.alterar_frame(False))
        self.txtFrame = Entry(frame_campos2, width=5)
        btnAumentarFrame = Button(frame_campos2, text='+', command=lambda:self.alterar_frame(True))
        btnTrocarVelocidadeFrame = Button(frame_campos2, text='Trocar velocidade', command=lambda:self.trocar_velocidade("frame"))

        # Define o terceiro quadro:
        frame_campos3 = Frame(self, relief=RAISED, bd=5)
        self.lblTaxaColuna = Label(frame_campos3, text='Taxa Coluna:')
        btnDiminuirColuna = Button(frame_campos3, text='-', command=lambda:self.alterar_coluna(False))
        self.txtColuna = Entry(frame_campos3, width=5)
        btnAumentarColuna = Button(frame_campos3, text='+', command=lambda:self.alterar_coluna(True))
        btnTrocarVelocidadeColuna = Button(frame_campos3, text='Trocar velocidade', command=lambda:self.trocar_velocidade("coluna"))
        
        # Define o quarto quadro:
        frame_campos4 = Frame(self, relief=RAISED, bd=5)
        self.ckbx = IntVar()
        self.ckby = IntVar()
        ckbReverterX = Checkbutton(frame_campos4, text='Reverter X', variable=self.ckbx, command=lambda:self.reverter('x') )
        ckbReverterY = Checkbutton(frame_campos4, text='Reverter Y', variable=self.ckby, command=lambda:self.reverter('y') )

        # Define o quinto quadro, visualização da imagem:
        frame_imagepicker = Frame(self, padx=10, pady=10, relief=RAISED, bd=5)
        self.lblImagem = Label(frame_imagepicker)

        # Constrói o primeiro quadro:
        frame_campos1.grid(column=0, row=0)
        self.txtImagem.grid(column=0, row=0)
        btnEscolherImagem.grid(column=1, row=0)
        self.btnPlayPause.grid(column=2, row=0)

        # Constrói o segundo quadro:
        frame_campos2.grid(column=0, row=1)
        lblTaxaFrame.grid(column=0, row=0)
        btnDiminuirFrame.grid(column=1, row=0)
        self.txtFrame.insert(0, globals.taxa_frame)
        self.txtFrame.grid(column=2, row=0)
        btnAumentarFrame.grid(column=3, row=0)
        btnTrocarVelocidadeFrame.grid(column=4, row=0)

        # Constrói o terceiro quadro:
        frame_campos3.grid(column=0, row=2)
        self.lblTaxaColuna.grid(column=0, row=0)
        btnDiminuirColuna.grid(column=1, row=0)
        self.txtColuna.insert(0, globals.taxa_coluna)
        self.txtColuna.grid(column=2, row=0)
        btnAumentarColuna.grid(column=3, row=0)
        btnTrocarVelocidadeColuna.grid(column=4, row=0)

        # Constrói o quarto quadro:
        frame_campos4.grid(column=0, row=3)
        ckbReverterX.grid(row=0, column=0)
        ckbReverterY.grid(row=0, column=1)

        # Constrói o quinto quadro:
        frame_imagepicker.grid(column=1, row=0, rowspan=4)
        self.lblImagem.grid(column=1, row=0)

        
    def abrir_imagem(self):
        # Insere a imagem que for selecionada em uma variável
        local_arquivo = tkFileDialog.askopenfilename(initialdir = os.getcwd(),
            title = "Selecione a imagem...",
            filetypes = (("Imagens","*.jpg *.png *.gif"),("Todos os arquivos","*.*")))

        # Apaga o texto do txtImagem e insere o nome do arquivo com extensão
        self.txtImagem.delete(0,END)
        self.txtImagem.insert(0,local_arquivo.split('/')[-1])

        # Converte a imagem em RGB (valor triplo de 8 bits)
        # Faz uma miniatura da imagem na lblImagem e 
        # Inicia o processo de lightpainting
        globals.imagem_arquivo = Image.open(local_arquivo).convert("RGB")
        imgTk = ImageTk.PhotoImage(self.miniatura(globals.imagem_arquivo))
        self.lblImagem.config(image=imgTk)
        self.lblImagem.image = imgTk
        globals.lpLigado = False
        self.play_pausePainting()

    def miniatura(self, img_mini):
        """ Faz uma miniatura da imagem original """
        tam_base = 300
        alt = img_mini.size[0]
        lar = img_mini.size[1]
        if alt >= tam_base or lar >= tam_base:
            if alt > lar:
                proporcao = alt / tam_base
            elif lar >= alt:
                proporcao = lar / tam_base
            nova_alt = alt / proporcao
            nova_lar = lar / proporcao
            img_mini = img_mini.resize((int(nova_alt),int(nova_lar)), Image.ANTIALIAS)
        return img_mini

    def trocar_velocidade(self, botao_pressionado):
        """ Ao pressionar o botão de trocar velocidade,
        altera a taxa de frame ou da coluna para a velocidade
        inserida. """
        if botao_pressionado == "frame": 
            globals.taxa_frame = int(self.txtFrame.get())
        else:
            globals.taxa_coluna = int(self.txtColuna.get())

    def alterar_frame(self, aumentar):
        if aumentar:
            if globals.taxa_frame < 1000:
                globals.taxa_frame += 100
                self.txtFrame.delete(0,END)
                self.txtFrame.insert(0,globals.taxa_frame)
        else:
            if globals.taxa_frame > 100:
                globals.taxa_frame -= 100
                self.txtFrame.delete(0,END)
                self.txtFrame.insert(0,globals.taxa_frame)

    def alterar_coluna(self, aumentar):
        if aumentar:
            if globals.taxa_coluna < 10:
                globals.taxa_coluna += 1
                self.txtColuna.delete(0,END)
                self.txtColuna.insert(0,globals.taxa_coluna)
        else:
            if globals.taxa_coluna > 1:
                globals.taxa_coluna -= 1
                self.txtColuna.delete(0,END)
                self.txtColuna.insert(0,globals.taxa_coluna)

    def reverter(self, alvo):
        if alvo == 'x':
            if self.ckbx.get() == 1:
                globals.reverter_x = True
            else:
                globals.reverter_x = False
        if alvo == 'y':
            if self.ckby.get() == 1:
                globals.reverter_y = True
            else:
                globals.reverter_y = False

    def play_pausePainting(self):
        if globals.lpLigado:
            lp.parar_painting = True
            self.btnPlayPause.config(text='Ligar')
            globals.lpLigado = False
        else:
            lightpaintingThread = threading.Thread(target=lp)
            lightpaintingThread.start()
            self.btnPlayPause.config(text='Pausar')
            globals.lpLigado = True

class JanelaErros(Toplevel):
    """ Classe que define a janela de erros """

    def __init__(self):
        """ Constrói toda a janela de erros """
        Toplevel.__init__(self)
        self.title("Erros SwayLED")
        self.construir_janela()

    def construir_janela(self):
        #   Barras horizontais
        vsb = ttk.Scrollbar(orient="vertical")
        hsb = ttk.Scrollbar(orient="horizontal")

        #   Objeto Treeview
        tree = ttk.Treeview(self, columns=("codigoProblematico","erroPython"), yscrollcommand=lambda f, l: self.autoscroll(vsb, f, l),
        xscrollcommand=lambda f, l:self.autoscroll(hsb, f, l))

        #   Barras de scroll às vistas x e y do objeto Treeview
        vsb['command'] = tree.yview
        hsb['command'] = tree.xview

        #   Cabeçalhos das colunas
        tree.heading("#0", text="Erro", anchor='w')
        tree.heading("codigoProblematico", text="Parte do código", anchor='w')
        tree.heading("erroPython", text="Erro Python", anchor='w')
        tree.column("#0", stretch=0, width=500)
        tree.column("codigoProblematico", stretch=0, width=200)
        tree.column("erroPython", stretch=0, width=200)

        #   Inserção na treeview
        for i in range(len(erros)):
            tree.insert('', 'end', text=erros[i]["tituloErro"], values=[erros[i]["codigoProblematico"], erros[i]["erroPython"]])

        # Arrange the tree and its scrollbars in the toplevel
        tree.grid(column=0, row=0, sticky='nswe')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def autoscroll(self, sbar, first, last):
        """Hide and show scrollbar as needed."""
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)

class SwayLEDapp(object):
    """Classe que define a janela principal do programa"""

    def __init__(self, parent):
        """ Constrói toda a janela principal """
        self.window = parent
        self.window.title("Sway LED")
        self.window.bind_all("<F9>",self.reiniciar_app)
        self.window.bind_all("<Return>",lambda: efeitos.ligar_leds(self))
        self.frameWindow = Frame(self.window, relief=GROOVE)
        self.frameWindow.grid(column=0,row=0)
        self.construir_menu()
        self.construir_frame_cores()
        self.construir_frame_pontos()
        frameBotaoTocar = Frame(self.frameWindow, relief=GROOVE, padx=10, pady=10, borderwidth=0)
        frameBotaoTocar.grid(column=0,row=1,columnspan=2,sticky=W+E)
        Button(frameBotaoTocar,text='LIGHTS ON!',width=50,command=efeitos.ligar_leds).grid(column=0,row=0)

    def construir_menu(self):
        """ Constrói o menu da janela principal """
        self.menu = Menu(self.window)
        sel_menu = Menu(self.menu,tearoff=False)
        sel_menu.add_command(label='Pegar RGB 5050',command=self.colorPicker_5050)
        sel_menu.add_separator()
        sel_menu.add_command(label='Desligar LEDs',command=efeitos.desligar)
        sel_menu.add_separator()
        if len(erros) > 0: sel_menu.add_command(label='Erros', command=self.abrir_janela_erros)
        sel_menu.add_command(label='Resetar App',command=self.reiniciar_app,accelerator="F9")
        sel_menu.add_command(label='Sobre')
        self.menu.add_cascade(label='Arquivo', menu=sel_menu)

        sel_menu = Menu(self.menu,tearoff=False)
        sel_menu.add_command(label='LightPaint',command=JanelaLightpaint)
        self.menu.add_cascade(label='Efeitos', menu=sel_menu)
        self.window.config(menu=self.menu)

    def construir_frame_cores(self):
        """ Constrói o quadro que define as cores dos LEDs """
        frameCor = Frame(self.frameWindow, relief=GROOVE, padx=10, pady=10, borderwidth=2)
        frameCor.grid(column=0,row=0,sticky=W+E+N+S)

        svR = StringVar()
        svG = StringVar()
        svB = StringVar()

        lblR = Label(frameCor, text="R:")
        self.txtR = Entry(frameCor,width=5,textvariable=svR)
        lblG = Label(frameCor, text="G:")
        self.txtG = Entry(frameCor,width=5,textvariable=svG)
        lblB = Label(frameCor, text="B:")
        self.txtB = Entry(frameCor,width=5,textvariable=svB)
        self.lblCores = Label(frameCor, text='Amostra de cores', bg="red")
        btnColorPicker = Button(frameCor, text='Color Picker',command=self.colorPicker_w2812b)

        svR.trace("w", lambda name, index, mode, sv=svR: self.label_trocarCores(svR))
        svG.trace("w", lambda name, index, mode, sv=svG: self.label_trocarCores(svG))
        svB.trace("w", lambda name, index, mode, sv=svB: self.label_trocarCores(svB))
        svR.trace("w", lambda *args: self.limite_caracteres(self.txtR,3))
        svG.trace("w", lambda *args: self.limite_caracteres(self.txtG,3))
        svB.trace("w", lambda *args: self.limite_caracteres(self.txtB,3))
        
        lblR.grid(column=0, row=0)
        self.txtR.grid(column=1, row=0)
        lblG.grid(column=0, row=1)
        self.txtG.grid(column=1, row=1)
        lblB.grid(column=0, row=2)
        self.txtB.grid(column=1, row=2)
        self.lblCores.grid(column=2, row=0, rowspan=3, sticky=W+E+N+S)
        btnColorPicker.grid(column=0, row=3,columnspan=3, sticky=W+E)

    def construir_frame_pontos(self):
        """ Constrói o quadro que define a região dos LEDs e efeitos """
        framePonto = Frame(self.frameWindow, relief=GROOVE, padx=10, pady=10, borderwidth=2)
        framePonto.grid(column=1,row=0,sticky=W+E+N+S)

        # Define variáveis e eventos
        # Ponto A e Ponto B possuem limite de 3 caracteres.
        svPA = StringVar()
        svPB = StringVar()
        rdbtn = StringVar()
        svPA.trace("w", lambda *args: self.limite_caracteres(self.txtPontoA,3))
        svPB.trace("w", lambda *args: self.limite_caracteres(self.txtPontoB,3))


        # Define Labels e Entrys
        lblPontoA = Label(framePonto, text="Ponto A:")
        self.txtPontoA = Entry(framePonto,width=5,textvariable=svPA)
        lblPontoB = Label(framePonto, text="Ponto B:")
        self.txtPontoB = Entry(framePonto,width=5,textvariable=svPB)
        lblVel = Label(framePonto, text="Vel:")        
        self.txtVel = Entry(framePonto,width=5)
        self.lblFuncao1 = Label(framePonto, text="Função 1:")
        self.txtFuncao1 = Entry(framePonto,width=5)
        lblEffects = Label(framePonto, text="Efeitos:")
        self.cmbEffects = ttk.Combobox(framePonto,width=20,state="readonly")

        # Define localização dos labels e entrys
        lblPontoA.grid(column=0, row=0)     
        self.txtPontoA.grid(column=1, row=0,sticky=W)        
        lblPontoB.grid(column=2, row=0,sticky=E)        
        self.txtPontoB.grid(column=3, row=0,sticky=E)
        lblVel.grid(column=0, row=1,sticky=E)        
        self.txtVel.grid(column=1, row=1,sticky=W)
        self.lblFuncao1.grid(column=2, row=1,sticky=E)        
        self.txtFuncao1.grid(column=3, row=1,sticky=E)
        lblEffects.grid(column=0,row=2,pady=10)
        self.cmbEffects.grid(column=1, row=2,columnspan=3)

        # Remove a funcao1 pois ela será mostrada dependendo do efeito seleiconado
        self.lblFuncao1.grid_remove()
        self.txtFuncao1.grid_remove()
        self.cmbEffects['values']= ("0 - Ligar",
            "1 - Grave",
            "2 - Braco",
            "3 - Corte Cobra",
            "4 - Laser Esq",
            "5 - Corte",
            "6 - Teatro",
            "7 - Aleatorio Fade",
            "8 - Bass Braco Invert",
            "9 - Teste")
        self.cmbEffects.current(0)
        self.cmbEffects.bind("<<ComboboxSelected>>", self.mostrar_funcao)

        # Define Radiobutton de outros efeitos
        outrosEfeitos = [("Desligado","0"),("ArcoIris","1")]
        for outroEfeito, val in outrosEfeitos:
            Radiobutton(framePonto,text=outroEfeito,indicatoron = 0,variable=rdbtn,value=val,relief=FLAT,command=efeitos.outros_efeitos).grid(column=val,row=3)

    def abrir_janela_erros(self):
        outra_janela = JanelaErros()

    def reiniciar_app(self, event=0):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.system('cls' if os.name == 'nt' else 'clear')
        print("App reiniciado")
        os.execl(python, python, * sys.argv)

    def limite_caracteres(self, texto, limite):
        """ Deleta o último caracter quando passar do limite """
        if len(texto.get()) > limite:
            texto.delete(limite,END)

    def mostrar_funcao(self, event=0):
        """ Dependendo do efeito escolhido, mostra-se um campo para
        definir o tamanho dos pixels do efeito ou a duração do efeito """
        if self.cmbEffects.current() == 3:
            self.lblFuncao1.config(text = "Tamanho:")
            self.lblFuncao1.grid()
            self.txtFuncao1.grid()

        elif self.cmbEffects.current() == 4:
            self.lblFuncao1.config(text = "Duração:")
            self.lblFuncao1.grid()
            self.txtFuncao1.grid()

        elif self.cmbEffects.current() == 6:
            self.lblFuncao1.config(text = "Duração:")
            self.lblFuncao1.grid()
            self.txtFuncao1.grid()

        else:
            self.lblFuncao1.grid_remove()
            self.txtFuncao1.grid_remove()

    def label_trocarCores(self, event=0):
        if self.txtR.get() == '': corVermelha = 0
        else: corVermelha = int(self.txtR.get())
        if self.txtG.get() == '': corVerde = 0
        else: corVerde = int(self.txtG.get())
        if self.txtB.get() == '': corAzul = 0
        else: corAzul = int(self.txtB.get())
        self.labelTroca_de_Cores(corVermelha, corVerde, corAzul)

    def colorPicker_w2812b(self, event=0):
        color = askcolor()
        rPicker = int(color[0][0])
        gPicker = int(color[0][1])
        bPicker = int(color[0][2])

        self.txtR.delete(0,END)
        self.txtR.insert(0,rPicker)  
        self.txtG.delete(0,END)
        self.txtG.insert(0,gPicker)
        self.txtB.delete(0,END)
        self.txtB.insert(0,bPicker)

        self.labelTroca_de_Cores(rPicker,gPicker,bPicker)

    def colorPicker_5050(self):
        color = askcolor()
        try: fitaLed(color[0][0],color[0][1],color[0][2])
        except: print ("LEDs 5050 (não endereçáveis) não foi adicionado")

    def labelTroca_de_Cores(self, R,G,B):
        novas_cores = "#%0.2X%0.2X%0.2X" % (R,G,B)
        # self.lblCores.config(bg=novas_cores)
        try: self.lblCores.config(bg=novas_cores)
        except TclError: print ("Cor inválida: R:{} G:{} B:{} {}".format(R,G,B,novas_cores))

    # def campos_validados(self):
    #     if self.txtPontoA.get() == '':
    #         tkMessageBox.showinfo("Entrada necessaria", "Qual LED eu ligo? Ponto A necessario")
    #         return False
    #     return True

    # def ligar_leds(self, event=0):
    #     if not self.campos_validados(): return

    #     globals.outroEfeitoRainbow = False

    #     pontoA = int(self.txtPontoA.get())
    #     if self.txtPontoB.get() == '': pontoB = pontoA
    #     else: pontoB = int(self.txtPontoB.get())
    #     if self.txtR.get() == '': redLed = 0
    #     else: redLed = int(self.txtR.get())
    #     if self.txtG.get() == '': greenLed = 0
    #     else: greenLed = int(self.txtG.get())
    #     if self.txtB.get() == '': blueLed = 0
    #     else: blueLed = int(self.txtB.get())
    #     if self.txtVel.get() == '': vel = 0.1
    #     else: vel = float(self.txtVel.get())
    #     if self.txtFuncao1.get() == '': funcao1 = 3
    #     else: funcao1 = int(self.txtFuncao1.get())

if __name__ == "__main__":
    window = Tk()
    try:
        window.iconbitmap("swayled.ico")
    except:
        addErros('_tkinter.TclError','window.iconbitmap("swayled.ico")',sys.exc_info()[1])
    aplicativo = SwayLEDapp(window)
    window.mainloop()