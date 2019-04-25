#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import argparse
import threading

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


velocidade = 0.01

def restart_program(event=0):
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

def desligar():
	off()

def janelaErros():
	janelaParaErros = Toplevel(principal)
	janelaParaErros.title("Erros Sway LED")

principal = Tk()

principal.title("Sway LED")
principal.bind_all("<F9>",restart_program)
'''
principal.bind_all("<F2>",atalhosVolta)
principal.bind_all("<F3>",atalhos)
principal.bind_all("<Return>",testLED)
principal.bind_all("q",atalhoQ)
principal.bind_all("w",atalhoW)
principal.bind_all("e",atalhoE)
principal.bind_all("a",atalhoA)
principal.bind_all("s",atalhoS)
principal.bind_all("d",atalhoD)
'''



menu = Menu(principal)
new_item = Menu(menu,tearoff=False)
new_item.add_command(label='Desligar LEDs',command=desligar)
new_item.add_separator()
new_item.add_command(label='Resetar App',command=restart_program,accelerator="F9")
new_item.add_command(label='Sobre')
menu.add_cascade(label='Arquivo', menu=new_item)

if len(erros) > 0: menu.add_cascade(label='Erros', command=janelaErros)

principal.config(menu=menu)

principal.mainloop()