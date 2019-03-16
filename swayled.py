#!/usr/bin/env python3

import os
import sys
import ttk
import time
import random
import Tkinter
import argparse
import threading
import tkMessageBox

#from recipe import *
from effects import *
from effectsBeta import *
#from led5050 import *
from Tkinter import *
from decimal import *
from neopixel import *
from itertools import product
from functools import partial
from tkColorChooser import askcolor

# LED strip configuration:
LED_COUNT      = 120      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

pontoA=pontoB=redLed=greenLed=blueLed=vel = 0
atalho = 0


window = Tk()
offInNew = 0

def validateFields():
	if txtPontoA.get() == '':
		tkMessageBox.showinfo("Entrada necessaria", "Qual LED eu ligo? Ponto A necessario")
		return False
	return True

def testLED(event=0):
	if not validateFields(): return

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
	if txtBPM.get() == '': bpm = 128
	else: bpm = int(txtBPM.get())
	bpm = Decimal(60)/Decimal(bpm)

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



def pegarCor():
    color = askcolor()
    txtR.delete(0,END)
    txtR.insert(0,color[0][0])	
    txtG.delete(0,END)
    txtG.insert(0,color[0][1])	
    txtB.delete(0,END)
    txtB.insert(0,color[0][2])

def pegarCorLed5050():
	color = askcolor()
	fitaLed(color[0][0],color[0][1],color[0][2])

def off():
	for i in range(LED_COUNT):
		strip.setPixelColor(i, Color(0,0,0))
	strip.show()

def bracoLEDEffect(pontoA,pontoB,R,G,B,vel):
    for i in range(pontoA,pontoB,13):
        for j in range(i, i+13):
            strip.setPixelColor(j, Color(B,R,G))
        strip.show()
        time.sleep(vel)
        
    for i in range(pontoB,pontoA-13,-13):
        for j in range(i, i+13):
            strip.setPixelColor(j, Color(0,0,0))
        strip.show()
        time.sleep(vel)

def deleteList():
	lstEffects.delete(lstEffects.curselection())

def updateList():
	insertEffect(True)
	if lstEffects.curselection(): lstEffects.delete(lstEffects.curselection())
	else: tkMessageBox.showinfo("Entrada necessaria", "Preciso saber qual trocarei")

def corteLEDEffect(R,G,B,vel):
    for i in range(5):
        if i < 4:
            for j in range(60+12*i,60+12*(1+i)):
                strip.setPixelColor(j,Color(B,R,G))
            for y in range(60-(12*i),60-(12*(1+i)),-1):
                strip.setPixelColor(y,Color(B,R,G))
        if i >= 1:
            for j in range(60+12*(i-1),60+12*i):
                strip.setPixelColor(j,Color(0,0,0))
            for y in range(60-12*(i-1),60-12*i,-1):
                strip.setPixelColor(y,Color(0,0,0))
        strip.show()
        time.sleep(vel)	

def on_select():
	print("Itens:", len(tv.get_children("")))

def mostrarTxtFuncao(x):
	if cmbEffects.current() == 3:
		lblFuncao1.config(text = "Tamanho:")
		lblFuncao1.grid()
		txtFuncao1.grid()

	elif cmbEffects.current() == 4:
		lblFuncao1.config(text = "Duracao:")
		lblFuncao1.grid()
		txtFuncao1.grid()

	elif cmbEffects.current() == 6:
		lblFuncao1.config(text = "Duracao:")
		lblFuncao1.grid()
		txtFuncao1.grid()

	else:
		lblFuncao1.grid_remove()
		txtFuncao1.grid_remove()

def apagarTxts():
	txtR.delete(0,END)
	txtG.delete(0,END)
	txtB.delete(0,END)
	txtPontoA.delete(0,END)
	txtPontoB.delete(0,END)
	txtVel.delete(0,END)
	txtFuncao1.delete(0,END)

def atualizarCampos(pontoA,pontoB, R,G,B, vel, efeito, funcao1):
	txtR.insert(0,R)
	txtG.insert(0,G)
	txtB.insert(0,B)
	txtPontoA.insert(0,pontoA)
	txtPontoB.insert(0,pontoB)
	txtVel.insert(0,vel)
	txtFuncao1.insert(0,funcao1)
	cmbEffects.current(efeito)


def atalhoQ(event=0):
	rdbTheSermon.select()
	global atalho
	if atalho == 0:
		apagarTxts()
		# Atualizar Campos: Ponto A, Ponto B, R, G, B, Velocidade, Efeito, Funcao 1
		atualizarCampos("80","95","50","0","5",".02",1,"0")
		testLED()
		rdbTunnel1.select()
	elif atalho == 1:
		apagarTxts()
		atualizarCampos("80","95","50","50","0",".01",1,"0")
		testLED()
		rdbTunnel2.select()
	elif atalho == 2:
		apagarTxts()
		atualizarCampos("20","100","50","0","50",".01",4,"2")
		testLED()
		rdbTunnel3.select()
	elif atalho == 3:
		apagarTxts()
		atualizarCampos("20","80","24","0","100",".06",6,"2")
		testLED()
		rdbTunnel4.select()
	else:
		apagarTxts()
		# Atualizar Campos: Ponto A, Ponto B, R, G, B, Velocidade, Efeito, Funcao 1
		atualizarCampos("79", "119", "100", "100", "100", ".028", 1, "2")
		testLED()
		rdbTunnel5.select()


def atalhoW(event=0):
	rdbTheSermon.select()
	global atalho
	if atalho == 0:
		apagarTxts()
		atualizarCampos("50", "65", "50", "0", "5", ".02", 1, "0")		
		testLED()
	elif atalho == 1:
		apagarTxts()
		txtR.insert(0,"50")
		txtG.insert(0,"50")
		txtPontoA.insert(0,"50")
		txtPontoB.insert(0,"65")
		txtVel.insert(0,".01")
		testLED()
	elif atalho == 4:
		apagarTxts()
		cmbEffects.current(1)
		txtR.insert(0,"100")
		txtG.insert(0,"100")
		txtB.insert(0,"100")
		txtPontoA.insert(0,"39")
		txtPontoB.insert(0,"79")
		txtVel.insert(0,".026")
		txtFuncao1.insert(0,"2")
		testLED()

def atalhoE(event=0):
	rdbTheSermon.select()
	global atalho
	if atalho == 0:
		cmbEffects.current(1)
		apagarTxts()
		txtR.insert(0,"50")
		txtB.insert(0,"5")
		txtPontoA.insert(0,"10")
		txtPontoB.insert(0,"25")
		txtVel.insert(0,".02")
		testLED()
	elif atalho == 1:
		apagarTxts()
		txtR.insert(0,"50")
		txtG.insert(0,"50")
		txtPontoA.insert(0,"10")
		txtPontoB.insert(0,"25")
		txtVel.insert(0,".01")
		testLED()
	elif atalho == 4:
		apagarTxts()
		cmbEffects.current(1)
		txtR.insert(0,"100")
		txtG.insert(0,"100")
		txtB.insert(0,"100")
		txtPontoA.insert(0,"0")
		txtPontoB.insert(0,"39")
		txtVel.insert(0,".019")
		txtFuncao1.insert(0,"2")
		testLED()

def atalhoA(event=0):
	apagarTxts()
	rndR = random.randint(40,100)
	rndG = random.randint(0,100)
	rndB = random.randint(0,100)
	atualizarCampos("50", "65", rndR,rndG,rndB, ".005", 3, "10")		
	testLED()
	rdbTunnel.select()
def atalhoS(event=0):
	global atalho
	apagarTxts()
	atualizarCampos(0,60, 80,80,80, .06, 2, 0)
	testLED()
	rdbTunnel.select()
def atalhoD(event=0):
	pass

def atalhosVolta(event=0):
	global atalho
	if atalho == 0:
		atalho = 4
		rdbTheSermon5.select()
		rdbTunnel5.select()
	elif atalho == 1:
		atalho -= 1
		rdbTheSermon1.select()
		rdbTunnel1.select()
	elif atalho == 2:
		atalho -= 1
		rdbTheSermon2.select()
		rdbTunnel2.select()
	elif atalho == 3:
		atalho -= 1
		rdbTheSermon3.select()
		rdbTunnel3.select()
	else:
		atalho -= 1
		rdbTheSermon4.select()
		rdbTunnel4.select()

def atalhos(event=0):
	global atalho
	if atalho == 0:
		atalho += 1
		rdbTheSermon2.select()
		rdbTunnel2.select()
	elif atalho == 1:
		atalho += 1
		rdbTheSermon3.select()
		rdbTunnel3.select()
	elif atalho == 2:
		atalho += 1
		rdbTheSermon4.select()
		rdbTunnel4.select()
	elif atalho == 3:
		atalho += 1
		rdbTheSermon5.select()
		rdbTunnel5.select()
	else:
		atalho = 0
		rdbTheSermon1.select()
		rdbTunnel1.select()




def restart_program(event=0):
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

menu = Menu(window)
new_item = Menu(menu)
new_item.add_command(label='Abrir',command=on_select)
new_item.add_command(label='Salvar')
new_item.add_command(label='Salvar como...')
new_item.add_separator()
new_item.add_command(label='Desligar LEDs',command=off)
new_item.add_separator()
new_item.add_command(label='Resetar App',command=restart_program,accelerator="F9")
new_item.add_command(label='Sobre')
menu.add_cascade(label='Arquivo', menu=new_item)

sel_menu = Menu(menu)
sel_menu.add_command(label='Pegar RGB',command=pegarCor)
sel_menu.add_command(label='Pegar RGB 5050',command=pegarCorLed5050)
menu.add_cascade(label='Selecionar', menu=sel_menu)


lblPontoA = Label(window, text="Ponto A:")
lblPontoA.grid(column=0, row=0)
lblPontoB = Label(window, text="Ponto B:")
lblPontoB.grid(column=0, row=1)
lblBPM = Label(window, text="BPM:")
lblBPM.grid(column=0, row=2)
lblVel = Label(window, text="Vel:")
lblVel.grid(column=0, row=3)

txtPontoA = Entry(window,width=10,text="0")
txtPontoA.grid(column=1,row=0)
txtPontoB = Entry(window,width=10,text="85")
txtPontoB.grid(column=1,row=1)
txtBPM = Entry(window,width=10)
txtBPM.grid(column=1,row=2)
txtVel = Entry(window,width=10)
txtVel.grid(column=1, row=3)

lblR = Label(window, text="R:")
lblR.grid(column=2, row=0)
lblG = Label(window, text="G:")
lblG.grid(column=2, row=1)
lblB = Label(window, text="B:")
lblB.grid(column=2, row=2)
lblFuncao1 = Label(window, text="...:")
lblFuncao1.grid(column=2, row=3)
lblFuncao1.grid_remove()
 
txtR = Entry(window,width=10)
txtR.grid(column=3, row=0)
txtG = Entry(window,width=10)
txtG.grid(column=3, row=1)
txtB = Entry(window,width=10)
txtB.grid(column=3, row=2)
txtFuncao1 = Entry(window,width=10)
txtFuncao1.grid(column=3, row=3)
txtFuncao1.grid_remove()

lblEffects = Label(window, text="Efeitos:")
lblEffects.grid(column=0,row=4,pady=10)

cmbEffects = ttk.Combobox(window,width=20,state="readonly")
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
cmbEffects.grid(column=1, row=4,columnspan=3)
cmbEffects.bind("<<ComboboxSelected>>", mostrarTxtFuncao)

btnTest = Button(window, text="Testar", command=testLED)
btnTest.grid(column=0, row=5)


offInNew = IntVar()
Checkbutton(window, text="Desligar em novo efeito",variable=offInNew).grid(column=3,row=5)

musicaFrame = LabelFrame(window,text='Musicas')
musicaFrame.grid(column=0,row=6,columnspan=6)

rdbTheSermon = Radiobutton(musicaFrame, text="The Sermon", value=1,variable='musica')
rdbTheSermon.grid(column=0, row=6)
rdbTheSermon.select()
rdbTheSermon1 = Radiobutton(musicaFrame, text="1- Mini Bass (Q,W,E)", value=1,variable='sermonEfeito')
rdbTheSermon1.grid(column=1,row=6,sticky=W)
rdbTheSermon1.select()
rdbTheSermon2 = Radiobutton(musicaFrame, text="2- Hats (Q,W,E)", value=2,variable='sermonEfeito')
rdbTheSermon2.grid(column=2,row=6,sticky=W)
rdbTheSermon3 = Radiobutton(musicaFrame, text="3- Laser (Q)", value=3,variable='sermonEfeito')
rdbTheSermon3.grid(column=1,row=7,sticky=W)
rdbTheSermon4 = Radiobutton(musicaFrame, text="4- Teatro (Q)", value=4,variable='sermonEfeito')
rdbTheSermon4.grid(column=2,row=7,sticky=W)
rdbTheSermon5 = Radiobutton(musicaFrame, text="5- Bass (Q,W,E)", value=5,variable='sermonEfeito')
rdbTheSermon5.grid(column=1,row=8,sticky=W)

rdbTunnel = Radiobutton(musicaFrame, text="Tunnel Vision", value=2,variable='musica')
rdbTunnel.grid(column=0, row=9)
rdbTunnel1 = Radiobutton(musicaFrame, text="Tunnel + Bass (A, S)", value=1,variable='tunnelEfeito')
rdbTunnel1.grid(column=1,row=9,sticky=W)
rdbTunnel1.select()

window.title("Sway LED")
window.geometry('420x400')
window.bind_all("<F9>",restart_program)
window.bind_all("<F2>",atalhosVolta)
window.bind_all("<F3>",atalhos)
window.bind_all("<Return>",testLED)
window.bind_all("q",atalhoQ)
window.bind_all("w",atalhoW)
window.bind_all("e",atalhoE)
window.bind_all("a",atalhoA)
window.bind_all("s",atalhoS)
window.bind_all("d",atalhoD)

strip.begin()
window.config(menu=menu)
window.mainloop()
