from tkinter import Tk, Canvas, Frame, BOTH, Label, Button
from neopixelFake import *
import threading
import time


LED_COUNT = 120
root = Tk()
r={}

# LED strip configuration:
LED_COUNT      = 120     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

def trocarCor():
    strip.setPixelColor(1,Color(255,0,255))
    strip.show()
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


outroEfeitoThread = threading.Thread(target=rainbowCycle,args=(strip,))

for led in range(LED_COUNT):
    base = 15*led
    r["retangulo{0}".format(led)] = canvas.create_rectangle(5+base, 10, 15+base, 20,outline="#000", fill="#000")
canvas.pack(fill=BOTH,expand=1)

# Button(root,text='Trocar cor',command= lambda: outroEfeitoThread.start() ).pack()
Button(root,text='Trocar cor',command=trocarCor).pack()

root.geometry('500x500')
root.mainloop()