from tkinter import Tk, Canvas, Frame, BOTH, Label, Button
import threading
import time
LED_COUNT = 120
root = Tk()
r={}


class strip:
	def setPixelColor(pos,color_hex):
		canvas.itemconfig(r['retangulo{}'.format(pos)], fill=color_hex)
	def numPixels():
		return LED_COUNT
	def show():
		pass

def Color(R,G,B):
	novas_cores = "#%0.2X%0.2X%0.2X" % (R,G,B)
	return novas_cores

def trocarCor():
	strip.setPixelColor(1,Color(255,0,255))
	print(Color(255,0,255))

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

canvas = Canvas(root)
outroEfeitoThread = threading.Thread(target=rainbowCycle,args=(strip,))

for led in range(LED_COUNT):
    base = 15*led
    r["retangulo{0}".format(led)] = canvas.create_rectangle(5+base, 10, 15+base, 20,outline="#000", fill="#000")
canvas.pack(fill=BOTH,expand=1)

Button(root,text='Trocar cor',command= lambda: outroEfeitoThread.start() ).pack()

root.mainloop()