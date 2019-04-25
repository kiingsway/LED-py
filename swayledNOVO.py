#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import argparse
import threading
from decimal import *
from itertools import product
from functools import partial

erros = []

def addErros(classe,codigo,erro):
	erros.append(dict(tituloErro=classe,
    codigoProblematico=codigo,
    erroPython=erro))

try: from Tkinter import *
except ImportError: from tkinter import *
except Exception: addErros((str(sys.exc_info()[0])+': Tkinter está instalado?'),'from Tkinter import *',sys.exc_info()[1])

try: import ttk
except ImportError: import tkinter.ttk as ttk
except Exception: addErros((str(sys.exc_info()[0])+': ttk está instalado?'),'from Tkinter import *',sys.exc_info()[1])

try: import tkMessageBox
except ImportError: import tkinter.messagebox

try: from tkColorChooser import askcolor
except ImportError: from tkinter.colorchooser import askcolor

try: from effects import *
except ImportError: addErros('ImportError: O arquivo efeitos.py está na pasta do código?','from effects import *',sys.exc_info()[1])
except NotImplementedError:	addErros('NotImplementedError: Erro na importação da biblioteca effects.py','from effects import *',sys.exc_info()[1])

try: from effectsBeta import *
except ImportError: addErros('ImportError: O arquivo efeitosBeta.py está na pasta do código?','from effectsBeta import *',sys.exc_info()[1])
except NotImplementedError:	addErros('NotImplementedError: Erro no código da biblioteca effectsBeta.py','from effectsBeta import *',sys.exc_info()[1])

try: from led5050 import *
except NotImplementedError:	addErros('NotImplementedError: Erro no código da biblioteca led5050.py','try: from led5050 import *',sys.exc_info()[1])
except ModuleNotFoundError: addErros('ModuleNotFoundError: Um módulo não foi executado','from led5050 import *',sys.exc_info()[1])
except ImportError: addErros('ImportError: O arquivo led5050.py está na pasta do código?','try: from led5050 import *',sys.exc_info()[1])
except Exception: addErros(sys.exc_info()[0],'from Tkinter import *',sys.exc_info()[1])

def janelaErros():

    janelaParaErros = Toplevel(window)
    janelaParaErros.title("Erros Sway LED")
    
    #   Barras horizontais
    vsb = ttk.Scrollbar(orient="vertical")
    hsb = ttk.Scrollbar(orient="horizontal")

    #   Objeto Treeview
    tree = ttk.Treeview(janelaParaErros, columns=("codigoProblematico","erroPython"), yscrollcommand=lambda f, l: autoscroll(vsb, f, l),
    xscrollcommand=lambda f, l:autoscroll(hsb, f, l))

    #   Barras de scroll às vistas x e y do objeto Treeview
    vsb['command'] = tree.yview
    hsb['command'] = tree.xview

    #   Cabeçalhos das diferentes colunas
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
    janelaParaErros.grid_columnconfigure(0, weight=1)
    janelaParaErros.grid_rowconfigure(0, weight=1)

def desligar():
	off()

def colorPicker_w2812b():
    color = askcolor()
    txtR.delete(0,END)
    txtR.insert(0,int(color[0][0]))	
    txtG.delete(0,END)
    txtG.insert(0,int(color[0][1]))
    txtB.delete(0,END)
    txtB.insert(0,int(color[0][2]))

def colorPicker_5050():
	color = askcolor()
	fitaLed(color[0][0],color[0][1],color[0][2])

def reiniciar_app(event=0):
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

window = Tk()

menu = Menu(window)
sel_menu = Menu(menu,tearoff=False)
sel_menu.add_command(label='Desligar LEDs',command=desligar)
sel_menu.add_separator()
sel_menu.add_command(label='Resetar App',command=reiniciar_app,accelerator="F9")
sel_menu.add_command(label='Sobre')
menu.add_cascade(label='Arquivo', menu=sel_menu)

sel_menu = Menu(menu,tearoff=False)
sel_menu.add_command(label='Pegar RGB',command=colorPicker_w2812b)
sel_menu.add_command(label='Pegar RGB 5050',command=colorPicker_5050)
menu.add_cascade(label='Selecionar', menu=sel_menu)

if len(erros) > 0: menu.add_cascade(label='Erros', command=janelaErros)

frameWindow = Frame(window, relief=RAISED)
frameWindow.pack(fill=BOTH, expand=True)

frameCor = Frame(frameWindow, relief=RAISED, padx=10, pady=10, borderwidth=2)
#frameCor.pack(fill=BOTH, expand=True, side=LEFT)
frameCor.grid(column=0,row=0,sticky=W+E+N+S)

Label(frameCor, text="R:").grid(column=0, row=0)
txtR = Entry(frameCor,width=5)
txtR.grid(column=1, row=0)

Label(frameCor, text="G:").grid(column=0, row=1)
txtG = Entry(frameCor,width=5)
txtG.grid(column=1, row=1)

Label(frameCor, text="B:").grid(column=0, row=2)
txtB = Entry(frameCor,width=5)
txtB.grid(column=1, row=2)

Label(frameCor, text='Amostra de cores', bg="red").grid(column=2, row=0, rowspan=3, sticky=W+E+N+S)
Button(frameCor, text='Color Picker',command=colorPicker_w2812b).grid(column=0, row=3,columnspan=3, sticky=W+E) # JUSTIFICAR NA DIREITA

framePonto = Frame(frameWindow, relief=RAISED, padx=10, pady=10, borderwidth=2)
#framePonto.pack(fill=BOTH, expand=True, side=LEFT)
framePonto.grid(column=1,row=0,sticky=W+E+N+S)

Label(framePonto, text="Ponto A:").grid(column=0, row=0)
txtPontoA = Entry(framePonto,width=5)
txtPontoA.grid(column=1, row=0,sticky=W)

Label(framePonto, text="Ponto B:").grid(column=2, row=0)
txtPontoB = Entry(framePonto,width=5)
txtPontoB.grid(column=3, row=0)

Label(framePonto, text="Vel:").grid(column=0, row=1,sticky=E)
txtVel = Entry(framePonto,width=5)
txtVel.grid(column=1, row=1,sticky=W)

lblEffects = Label(framePonto, text="Efeitos:")
lblEffects.grid(column=0,row=2,pady=10)

cmbEffects = ttk.Combobox(framePonto,width=20,state="readonly")
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
cmbEffects.current(0) #set the selected item
cmbEffects.grid(column=1, row=2,columnspan=3)
#cmbEffects.bind("<<ComboboxSelected>>", mostrarTxtFuncao)

frameBotaoTocar = Frame(frameWindow, relief=RAISED, padx=10, pady=10, borderwidth=1)
#frameBotaoTocar.pack(fill=BOTH, expand=True, side=BOTTOM)
frameBotaoTocar.grid(column=0,row=1,columnspan=2,sticky=W+E)

Button(frameBotaoTocar,text='LIGHTS ON!',width=50).grid(column=0,row=0)

window.config(menu=menu)
window.title("Sway LED")
window.mainloop()