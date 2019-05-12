#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

print("Importando bibliotecas comuns...")
import os
import sys
import time
import random
import globals
import argparse
import threading
import platform
from decimal import *
from itertools import product
from functools import partial

erros = []

def addErros(classe,codigo,erro):
	erros.append(dict(tituloErro=classe,
    codigoProblematico=codigo,
    erroPython=erro))
print("Importando bibliotecas dos LEDs...")

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

print('Carregando funções...')

def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


def janelaLightpaint():
    tam_base = 300

    janelaParaLightpaint = Toplevel(window)
    janelaParaLightpaint.title('Lightpaint')
    janelaParaLightpaint.geometry('800x400')



    def frame_maismenos(aumentar):
        if aumentar:
            if globals.taxa_frame < 1000:
                globals.taxa_frame += 100
                lblFrame.delete(0,END)
                lblFrame.insert(0,globals.taxa_frame)
        else:
            if globals.taxa_frame > 100:
                globals.taxa_frame -= 100
                lblFrame.delete(0,END)
                lblFrame.insert(0,globals.taxa_frame)


    def coluna_maismenos(aumentar):
        if aumentar:
            if globals.taxa_coluna < 10:
                globals.taxa_coluna += 1
                lblColuna.delete(0,END)
                lblColuna.insert(0,globals.taxa_coluna)
        else:
            if globals.taxa_coluna > 1:
                globals.taxa_coluna -= 1
                lblColuna.delete(0,END)
                lblColuna.insert(0,globals.taxa_coluna)

    def trocar_velocidade():
        globals.taxa_frame = int(lblFrame.get())
        globals.taxa_coluna = int(lblColuna.get())

    def abrir_imagem():
        def miniatura(img_mini):
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

        if platform.system() == "Windows": local_arquivo = tkFileDialog.askopenfilename(initialdir = "Z:\\Projetos\\LED-py\\Images",title = "Select file",filetypes = (("Imagens","*.jpg *.png *.gif"),("Todos os arquivos","*.*")))
        else: local_arquivo = tkFileDialog.askopenfilename(initialdir = "/home/pi/Projetos/LED-py/Images",title = "Select file",filetypes = (("Imagens","*.jpg *.png *.gif"),("Todos os arquivos","*.*")))
        txtImagem.delete(0,END)
        txtImagem.insert(0,local_arquivo.split('/')[-1])
        # try:
        globals.imagem_arquivo = Image.open(local_arquivo).convert("RGB")
        imgTk = ImageTk.PhotoImage(miniatura(globals.imagem_arquivo))
        lblImagem.config(image=imgTk)
        lblImagem.image = imgTk
        lightpaintingThread = threading.Thread(target=lp)
        lightpaintingThread.start()
        globals.lpLigado = True
        # except AttributeError: print('Upload da imagem cancelado')

    def play_pausePainting():
        if globals.lpLigado:
            lp.parar_painting = True
            btnPl.config(text='Tocar')
            globals.lpLigado = False
        else:
            lightpaintingThread = threading.Thread(target=lp)
            lightpaintingThread.start()
            btnPl.config(text='Pausar')
            globals.lpLigado = True

    def reverter(alvo):
        if alvo == 'x':
            if ckb1.get() == 1:
                globals.reverter_x = True
            else:
                globals.reverter_x = False
        if alvo == 'y':
            if ckb2.get() == 1:
                globals.reverter_y = True
            else:
                globals.reverter_y = False

    


    frame_campos1 = Frame(janelaParaLightpaint,relief=RAISED,bd=5)
    frame_campos1.grid(column=0,row=0)

    txtImagem = Entry(frame_campos1,width=40)
    txtImagem.grid(column=0,row=0)
    Button(frame_campos1,text='Escolher imagem...',command=abrir_imagem).grid(column=1,row=0)
    btnPl = Button(frame_campos1,text='Pausar',command= lambda: play_pausePainting())
    btnPl.grid(column=2,row=0)

    frame_campos2 = Frame(janelaParaLightpaint,relief=RAISED,bd=5)
    frame_campos2.grid(column=0,row=1)

    Label(frame_campos2,text='Taxa Frame:').grid(column=0,row=0)
    Button(frame_campos2,text='-',command=lambda:frame_maismenos(False)).grid(column=1,row=0)
    lblFrame = Entry(frame_campos2,width=5)
    lblFrame.insert(0,globals.taxa_frame)
    lblFrame.grid(column=2,row=0)
    Button(frame_campos2,text='+',command=lambda:frame_maismenos(True)).grid(column=3,row=0)
    Button(frame_campos2,text='Trocar velocidade',command=trocar_velocidade).grid(column=4,row=0)

    frame_campos3 = Frame(janelaParaLightpaint,relief=RAISED,bd=5)
    frame_campos3.grid(column=0,row=2)

    Label(frame_campos3,text='Taxa Coluna:').grid(column=0,row=0)
    Button(frame_campos3,text='-',command=lambda:coluna_maismenos(False)).grid(column=1,row=0)
    lblColuna = Entry(frame_campos3,width=5)
    lblColuna.insert(0,globals.taxa_coluna)
    lblColuna.grid(column=2,row=0)
    Button(frame_campos3,text='+',command=lambda:coluna_maismenos(True)).grid(column=3,row=0)
    Button(frame_campos3,text='Trocar velocidade',command=trocar_velocidade).grid(column=4,row=0)

    frame_campos4 = Frame(janelaParaLightpaint,relief=RAISED,bd=5)
    frame_campos4.grid(column=0,row=3)

    ckb1 = IntVar()
    ckb2 = IntVar()
    Checkbutton(frame_campos4, text='Reverter X', variable=ckb1, command=lambda:reverter('x') ).grid(row=0,column=0)
    Checkbutton(frame_campos4, text='Reverter Y', variable=ckb2, command=lambda:reverter('y') ).grid(row=0,column=1)

    frame_imagepicker = Frame(janelaParaLightpaint,padx=10, pady=10,relief=RAISED,bd=5)
    frame_imagepicker.grid(column=1,row=0,rowspan=4)

    lblImagem = Label(frame_imagepicker, width=tam_base,height=tam_base)
    lblImagem.grid(column=1,row=0)
    abrir_imagem()



def validateFields():
    if txtPontoA.get() == '':
        tkMessageBox.showinfo("Entrada necessaria", "Qual LED eu ligo? Ponto A necessario")
        return False
    return True

def testLED(event=0):
    if not validateFields(): return

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

def outros_efeitos():
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

def desligar():
    try: off()
    except: pass

def colorPicker_w2812b():
    color = askcolor()
    rPicker = int(color[0][0])
    gPicker = int(color[0][1])
    bPicker = int(color[0][2])

    txtR.delete(0,END)
    txtR.insert(0,rPicker)	
    txtG.delete(0,END)
    txtG.insert(0,gPicker)
    txtB.delete(0,END)
    txtB.insert(0,bPicker)

    labelTroca_de_Cores(rPicker,gPicker,bPicker)

def label_trocarCores(sv):
    if txtR.get() == '': corVermelha = 0
    else: corVermelha = int(txtR.get())
    if txtG.get() == '': corVerde = 0
    else: corVerde = int(txtG.get())
    if txtB.get() == '': corAzul = 0
    else: corAzul = int(txtB.get())
    labelTroca_de_Cores(corVermelha, corVerde, corAzul)

def labelTroca_de_Cores(R,G,B):
    novas_cores = "#%0.2X%0.2X%0.2X" % (R,G,B)
    # lblCores.config(bg=novas_cores)
    try: lblCores.config(bg=novas_cores)
    except TclError: print ("Cor inválida: R:{} G:{} B:{} {}".format(R,G,B,novas_cores))

def colorPicker_5050():
    color = askcolor()
    try: fitaLed(color[0][0],color[0][1],color[0][2])
    except: print ("LEDs 5050 (não endereçáveis) não foi adicionado")

def mostrarTxtFuncao(x):
    if cmbEffects.current() == 3:
        lblFuncao1.config(text = "Tamanho:")
        lblFuncao1.grid()
        txtFuncao1.grid()

    elif cmbEffects.current() == 4:
        lblFuncao1.config(text = "Duração:")
        lblFuncao1.grid()
        txtFuncao1.grid()

    elif cmbEffects.current() == 6:
        lblFuncao1.config(text = "Duração:")
        lblFuncao1.grid()
        txtFuncao1.grid()

    else:
        lblFuncao1.grid_remove()
        txtFuncao1.grid_remove()





def character_limit(entry_text, limit_char):
    if len(entry_text.get()) > limit_char:
        entry_text.delete(limit_char,END)

print('Carregando programa...')

    

class JanelaErros(Toplevel):
    """ Class que define a janela de erros """

    def __init__(self, original):
        """ Constrói toda a janela de erros """
        self.janela_original = original
        Toplevel.__init__(self)
        self.title("Erros SwayLED")
        self.construir_janela()

    def construir_janela(self):
        #   Barras horizontais
        vsb = ttk.Scrollbar(orient="vertical")
        hsb = ttk.Scrollbar(orient="horizontal")

        #   Objeto Treeview
        tree = ttk.Treeview(self, columns=("codigoProblematico","erroPython"), yscrollcommand=lambda f, l: autoscroll(vsb, f, l),
        xscrollcommand=lambda f, l:autoscroll(hsb, f, l))

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

class SwayLEDapp(object):
    """Classe que define a janela principal do programa"""

    def __init__(self, parent):
        """ Constrói toda a janela principal """
        self.window = parent
        self.window.title("Sway LED")
        self.window.bind_all("<F9>",self.reiniciar_app)
        self.window.bind_all("<Return>",testLED)
        self.frameWindow = Frame(window, relief=GROOVE)
        self.frameWindow.grid(column=0,row=0)
        self.construir_menu()
        self.construir_frame_cores()
        self.construir_frame_pontos()
        frameBotaoTocar = Frame(self.frameWindow, relief=GROOVE, padx=10, pady=10, borderwidth=0)
        frameBotaoTocar.grid(column=0,row=1,columnspan=2,sticky=W+E)
        Button(frameBotaoTocar,text='LIGHTS ON!',width=50,command=testLED).grid(column=0,row=0)

    def construir_menu(self):
        """ Constrói o menu da janela principal """
        self.menu = Menu(self.window)
        sel_menu = Menu(self.menu,tearoff=False)
        sel_menu.add_command(label='Pegar RGB 5050',command=colorPicker_5050)
        sel_menu.add_separator()
        sel_menu.add_command(label='Desligar LEDs',command=desligar)
        sel_menu.add_separator()
        if len(erros) > 0: sel_menu.add_command(label='Erros', command=self.abrir_janela_erros)
        sel_menu.add_command(label='Resetar App',command=self.reiniciar_app,accelerator="F9")
        sel_menu.add_command(label='Sobre')
        self.menu.add_cascade(label='Arquivo', menu=sel_menu)

        sel_menu = Menu(self.menu,tearoff=False)
        sel_menu.add_command(label='LightPaint',command=janelaLightpaint)
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
        txtR = Entry(frameCor,width=5,textvariable=svR)
        lblG = Label(frameCor, text="G:")
        txtG = Entry(frameCor,width=5,textvariable=svG)
        lblB = Label(frameCor, text="B:")
        txtB = Entry(frameCor,width=5,textvariable=svB)
        lblCores = Label(frameCor, text='Amostra de cores', bg="red")
        btnColorPicker = Button(frameCor, text='Color Picker',command=colorPicker_w2812b)


        svR.trace("w", lambda name, index, mode, sv=svR: label_trocarCores(svR))
        svG.trace("w", lambda name, index, mode, sv=svG: label_trocarCores(svG))
        svB.trace("w", lambda name, index, mode, sv=svB: label_trocarCores(svB))
        svR.trace("w", lambda *args: character_limit(txtR,3))
        svG.trace("w", lambda *args: character_limit(txtG,3))
        svB.trace("w", lambda *args: character_limit(txtB,3))

        
        lblR.grid(column=0, row=0)
        txtR.grid(column=1, row=0)
        lblG.grid(column=0, row=1)
        txtG.grid(column=1, row=1)
        lblB.grid(column=0, row=2)
        txtB.grid(column=1, row=2)
        lblCores.grid(column=2, row=0, rowspan=3, sticky=W+E+N+S)
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
        svPA.trace("w", lambda *args: character_limit(txtPontoA,3))
        svPB.trace("w", lambda *args: character_limit(txtPontoB,3))


        # Define Labels e Entrys
        lblPontoA = Label(framePonto, text="Ponto A:")
        txtPontoA = Entry(framePonto,width=5,textvariable=svPA)
        lblPontoB = Label(framePonto, text="Ponto B:")
        txtPontoB = Entry(framePonto,width=5,textvariable=svPB)
        lblVel = Label(framePonto, text="Vel:")        
        txtVel = Entry(framePonto,width=5)
        lblFuncao1 = Label(framePonto, text="Função 1:")
        txtFuncao1 = Entry(framePonto,width=5)
        lblEffects = Label(framePonto, text="Efeitos:")
        cmbEffects = ttk.Combobox(framePonto,width=20,state="readonly")

        # Define localização dos labels e entrys
        lblPontoA.grid(column=0, row=0)     
        txtPontoA.grid(column=1, row=0,sticky=W)        
        lblPontoB.grid(column=2, row=0,sticky=E)        
        txtPontoB.grid(column=3, row=0,sticky=E)
        lblVel.grid(column=0, row=1,sticky=E)        
        txtVel.grid(column=1, row=1,sticky=W)
        lblFuncao1.grid(column=2, row=1,sticky=E)        
        txtFuncao1.grid(column=3, row=1,sticky=E)
        lblEffects.grid(column=0,row=2,pady=10)
        cmbEffects.grid(column=1, row=2,columnspan=3)

        # Remove a funcao1 pois ela será mostrada dependendo do efeito seleiconado
        lblFuncao1.grid_remove()
        txtFuncao1.grid_remove()
        cmbEffects['values']= ("0 - Ligar",
            "1 - Grave",
            "2 - Braco",
            "3 - Corte Cobra",
            "4 - Laser Esq",
            "5 - Corte",
            "6 - Teatro",
            "7 - Aleatorio Fade",
            "8 - Bass Braco Invert",
            "9 - Teste")
        cmbEffects.current(0)
        cmbEffects.bind("<<ComboboxSelected>>", mostrarTxtFuncao)

        # Define Radiobutton de outros efeitos
        outrosEfeitos = [("Desligado","0"),("ArcoIris","1")]
        for outroEfeito, val in outrosEfeitos:
            Radiobutton(framePonto,text=outroEfeito,indicatoron = 0,variable=rdbtn,value=val,relief=FLAT,command=outros_efeitos).grid(column=val,row=3)

    def abrir_janela_erros(self):
        outra_janela = JanelaErros(self)

    def reiniciar_app(self, event=0):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.system('cls' if os.name == 'nt' else 'clear')
        print("App reiniciado")
        os.execl(python, python, * sys.argv)


if __name__ == "__main__":
    window = Tk()
    try:
        window.iconbitmap("swayled.ico")
    except:
        addErros('_tkinter.TclError','window.iconbitmap("swayled.ico")',sys.exc_info()[1])
    aplicativo = SwayLEDapp(window)
    window.mainloop()