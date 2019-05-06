from tkinter import Canvas

LED_COUNT = 120

def Color(R,G,B):
    novas_cores = "#%0.2X%0.2X%0.2X" % (R,G,B)
    return novas_cores

class strip:
    def setPixelColor(pos,color_hex):
        print('a',end='a')
        globals.canvas.itemconfig(globals.r['retangulo{}'.format(pos)], fill=color_hex)
    def numPixels():
        return LED_COUNT
    def show():
        pass
    def begin():
        pass

def Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL):
    LED_COUNT = 120
    return strip