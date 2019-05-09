from tkinter import Tk, Canvas, Frame, BOTH, Label, Button
# from neopixelFake import *
import threading
import time
# from effectsTest import *
try: from tkColorChooser import askcolor
except ImportError: from tkinter.colorchooser import askcolor


LED_COUNT = 120
root = Tk()
canvas = Canvas()
r={}


class strip:
    def setPixelColor(pos,color_hex):
        canvas.itemconfig(r['retangulo{}'.format(pos)], fill=color_hex)
    def numPixels():
        return LED_COUNT
    def show():
        pass
    def setBrightness(led,brilho):
        pass


def Color(R,G,B):
    """
    O Color original converte as cores RGB para algo em 24bit.
    Aqui é usado apenas para retornar o número em hexadecimal
    """
    novas_cores = "#%0.2X%0.2X%0.2X" % (R,G,B)
    return novas_cores

# LED strip configuration:
LED_COUNT      = 120     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).

try:
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
except: pass

def trocarCor():
    strip.setPixelColor(1,Color(255,0,255))
    strip.show()
    print(Color(255,0,255))

def off(event=0):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

parar_teatro = False
def teatroEffect(pontoA=0,pontoB=120, R=255,G=0,B=100, vel=0.1, duracao=2):
    # O tempo de duracao eh o tempo atual somada a duracao escolhida.
    # E enquanto nao chegar, continue dando o efeito

    # No primeiro for, apenas os pares ligam. Depois apenas os impares.
    tempoFim = time.time() + duracao
    while time.time() < tempoFim:
        for i in range(pontoA,pontoB):
            if i % 2 == 0: strip.setPixelColor(i, Color(G,R,B))
            if i % 2 != 0: strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(vel)
        for i in range(pontoA,pontoB):
            if i % 2 != 0: strip.setPixelColor(i, Color(G,R,B))
            if i % 2 == 0: strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(vel)
    off()

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

parar_rainbow = False
def rainbowCycle(wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        if parar_rainbow == True:
            print('parei')
            break

# rainbow_Thread = threading.Thread(target=rainbowCycle)
# teatro_Thread = threading.Thread(target=teatroEffect)
# teatro_Thread = threading.Thread(target=teatroEffect)

parar_efeito = False

def iniciar_efeito(efeito):
    print("Efeito: {}".format(efeito))
    if efeito == 0:
        global parar_efeito
        try: print(efeito_Thread.isAlive())
        except:
            print('passei')
            pass
        efeito_Thread = threading.Thread(target=rainbowCycle)
        efeito_Thread.start()
    elif efeito == 1:
        global parar_efeito
        efeito_Thread = threading.Thread(target=teatroEffect)
        efeito_Thread.start()
        


for led in range(LED_COUNT):
    base = 15*led
    ledClick_atual = "ledClick{}".format(led)
    # ledClick_atual = "ledClick"
    r["retangulo{0}".format(led)] = canvas.create_rectangle(5+base, 10, 15+base, 20,outline="#000", fill="#000",tags="ledClick1{}".format(led))
    # canvas.tag_bind("ledClick1{}".format(led),"<Button-1>",lambda e: colorLedPicker(1))
    # canvas.tag_bind("ledClick{}".format(led),"<Button-1>",lambda e: colorLedPicker(2))
    canvas.pack(fill=BOTH,expand=1)

# for s in ["button 1", "button 2", "button 3"]:
#     b=Button(root, text=s, bg="white")
#     b.pack()
#     b.bind("<Enter>", lambda e: print('enter{}'.format(s)))
#     b.bind("<Leave>", lambda e: print('Leave{}'.format(s)))

Button(root,text='Rainbow Cycle',command=lambda: iniciar_efeito(0)).pack()
Button(root,text='Teatro efeito',command=lambda: iniciar_efeito(1)).pack()

root.geometry('500x500')
root.mainloop()