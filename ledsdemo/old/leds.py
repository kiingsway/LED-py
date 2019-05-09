from tkinter import Tk, Canvas, Frame, BOTH, Label, Button
# from neopixelFake import *
import threading
import time
try: from tkColorChooser import askcolor
except ImportError: from tkinter.colorchooser import askcolor

LED_COUNT = 120

root = Tk()

b = {}

def ledClick(v):
	print(v)
	print('Entrei no LED')

for btn in range(LED_COUNT):
	b['btn{}'.format(btn)] = Button(root,bd=1,width=1,height=0,text=btn,command=lambda: ledClick(b['btn{}'.format(btn)]))
	b['btn{}'.format(btn)].grid(row=0,column=btn)

# Button(root,bd=0,text='a',bg="#FF00FF").pack()
# Button(root,bd=0,text='b',bg="#FFFF00").pack()
# Button(root,bd=0,text='c',bg="#00FFFF").pack()
# Button(root,bd=0,text='d',bg="#FFFFFF").pack()

root.mainloop()