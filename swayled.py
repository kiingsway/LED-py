#!/usr/bin/env python3

import ttk
import time
import argparse
import threading
import tkMessageBox

from Tkinter import *
from decimal import *
from neopixel import *
from itertools import product
from functools import partial

# LED strip configuration:
LED_COUNT      = 120      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


#BPM = 110
#bpm4 = Decimal(60)/Decimal(BPM)

# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
strip.begin()

pontoA=pontoB=redLed=greenLed=blueLed=vel = 0


window = Tk()
window.title("Sway LED")
window.geometry('325x270')

def validateFields():
	if txtPontoA.get() == '':
		tkMessageBox.showinfo("Entrada necessaria", "Qual LED eu ligo? Ponto A necessario")
		return False
	return True

def testLED():
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

	print("Teste:",pontoA,pontoB,redLed,greenLed,blueLed)
	if cmbEffects.current() == 0: acenderLEDEffect(pontoA,pontoB,redLed,greenLed,blueLed)
	if cmbEffects.current() == 1: graveLEDEffect(pontoA,pontoB,redLed,greenLed,blueLed)


def insertEffect():
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
	effect = cmbEffects.current()
	if txtVel.get() == '': vel = 1
	else: vel = float(txtVel.get())
	if txtBPM.get() == '': bpm = 128
	else: bpm = int(txtBPM.get())
	bpm = 60/bpm

	txtToList = redLed,greenLed,blueLed,pontoA,pontoB,effect,vel,bpm
	lstEffects.insert(END, txtToList)

def playLED():
	for i in range(lstEffects.size()):
		R = lstEffects.get(i)[0]
		G = lstEffects.get(i)[1]
		B = lstEffects.get(i)[2]
		pA = lstEffects.get(i)[3]
		pB = lstEffects.get(i)[4]
		ef = lstEffects.get(i)[5]
		vel = lstEffects.get(i)[6]
		bpm = lstEffects.get(i)[7]

		if ef == 0:	acenderLEDEffect(pA,pB,R,G,B)
		if ef == 1:	graveLEDEffect(pA,pB,R,G,B,vel)
		print("Wait BPM:",bpm)
		time.sleep(bpm)

def off():
	for i in range(LED_COUNT):
		strip.setPixelColor(i, Color(0,0,0))
	strip.show()

def acenderLEDEffect(pontoA,pontoB,R,G,B):
	for i in range(pontoA,pontoB+1):
		strip.setPixelColor(i,Color(B,R,G))
	strip.show()

def graveLEDEffect(pontoA,pontoB,R,G,B,vel):
	acenderLEDEffect(pontoA,pontoB,R,G,B)
	for brightness in range(255,-1,-15):
		strip.setBrightness(brightness)
		strip.show()
		time.sleep(vel)
	off()
	strip.setBrightness(LED_BRIGHTNESS)



menu = Menu(window)
new_item = Menu(menu)
new_item.add_command(label='Abrir')
new_item.add_command(label='Salvar')
new_item.add_command(label='Salvar como...')
new_item.add_separator()
new_item.add_command(label='Desligar LEDs',command=off)
new_item.add_separator()
new_item.add_command(label='Sobre')
menu.add_cascade(label='Arquivo', menu=new_item)


lblPontoA = Label(window, text="Ponto A:")
lblPontoA.grid(column=0, row=0)
lblPontoB = Label(window, text="Ponto B:")
lblPontoB.grid(column=0, row=1)
lblBPM = Label(window, text="BPM:")
lblBPM.grid(column=0, row=2)
lblVel = Label(window, text="Vel:")
lblVel.grid(column=0, row=3)

txtPontoA = Entry(window,width=10)
txtPontoA.grid(column=1,row=0)
txtPontoB = Entry(window,width=10)
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
 
txtR = Entry(window,width=10)
txtR.grid(column=3, row=0)
txtB = Entry(window,width=10)
txtB.grid(column=3, row=1)
txtG = Entry(window,width=10)
txtG.grid(column=3, row=2)

lblEffects = Label(window, text="Efeitos:")
lblEffects.grid(column=0,row=4)

cmbEffects = ttk.Combobox(window,width=20,state="readonly")
cmbEffects['values']= ("Ligar","Grave", 2, 3, 4, 5, "Text")
cmbEffects.current(0) #set the selected item
cmbEffects.grid(column=1, row=4,columnspan=3)

btnTest = Button(window, text="Testar", command=testLED)
btnTest.grid(column=0, row=5)
btnInsert = Button(window, text="Inserir", command=insertEffect)
btnInsert.grid(column=1, row=5)
btnPlay = Button(window, text="Tocar",command=playLED)
btnPlay.grid(column=2,row=5)

lstEffects = Listbox(window,width=40)
lstEffects.grid(column=0,row=6,columnspan=4)
 
strip.begin()
window.config(menu=menu)
window.mainloop()