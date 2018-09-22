import os
from Tkinter import *

bpm = 128

def alterarBPM(x):
	global bpm
	if x: bpm += 1
	else: bpm -= 1
	lblBPM.config(text=bpm)


def restart_program(event):
    python = sys.executable
    os.execl(python, python, * sys.argv)


window = Tk()
 
window.title("Sway LED 2")
window.geometry('720x480')

frameBPM = Frame(window)
frameBPM.place(relx=.5,anchor=N)

btnMenosBPM = Button(frameBPM, text="-",command=lambda: alterarBPM(False))
btnMenosBPM.grid(column=0, row=0)

lblBPM = Label(frameBPM, text=bpm)
lblBPM.grid(column=1, row=0)
 
btnMaisBPM = Button(frameBPM, text="+",command=lambda: alterarBPM(True))
btnMaisBPM.grid(column=2, row=0)


window.bind_all("<F9>",restart_program)
window.mainloop()