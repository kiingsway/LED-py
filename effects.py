import time
import threading
from decimal import *
from neopixel import *

BPM = 128
bpm4 = Decimal(60)/Decimal(BPM)


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

def off(event=0):
    for i in range(LED_COUNT):
        strip. setPixelColor(i, Color(0,0,0))
    strip.show()


# Efeitos PRONTOS
def acenderLEDEffect(pontoA,pontoB,R,G,B):
    # De um ponto escolhido, liga os LEDs solicitados
    off()
    for i in range(pontoA,pontoB+1):
        strip.setPixelColor(i,Color(G,R,B))
    strip.show()

def simpleBassEffect(pontoA,pontoB,R,G,B,vel):
    # Primeiro acende os LEDs desejados
    # Depois diminui seu brilho (no fim o brilho volta)

    # Nao usual: Diminui o brilho de toda fita. Trabalhando em um BETA
    for i in range(pontoA,pontoB):
        strip.setPixelColor(i,Color(G,R,B))
    strip.show()
    for brightness in range(255,-1,-15):
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(vel)
    off()
    strip.setBrightness(LED_BRIGHTNESS)

def teatroEffect(pontoA,pontoB, R,G,B, vel, duracao):
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