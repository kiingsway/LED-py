import time
import threading
from decimal import *


from random import randint


def off(event=0):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()


# Efeitos PRONTOS
def acenderLEDEffect(pontoA,pontoB,R,G,B):
    # De um ponto escolhido, liga os LEDs solicitados
    #swayled.offInNew
    #if swayled.offInNew == 1:
    off()
    for i in range(pontoA,pontoB):
        strip.setPixelColor(i,Color(G,R,B))
    strip.show()

def simpleBassEffect(pontoA=0,pontoB=120,R=255,G=0,B=255,vel=0.01):
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


def posAleatoriaFade(pontoA,pontoB, R,G,B, vel):
    # Criado para dar efeito a musica "Swagga", Point.Blank
    # Liga posicoes aleatorias com a cor selecionada
    for pos in range(pontoA,pontoB):
        if (randint(0,1)) == 1: strip.setPixelColor(pos,Color(G,R,B))

    for brilho in range(0,100,5):
        strip.setBrightness(brilho)
        strip.show()
        time.sleep(vel)

    for brilho in range(100,0,-5):
        strip.setBrightness(brilho)
        strip.show()
        time.sleep(vel)
    off()
    strip.setBrightness(LED_BRIGHTNESS)

def bracoLivre(pontoA,pontoB, R,G,B, vel):
    # Antigo pistol para a musica "Swagga", Point.Blank
    # Pinta as cada cor e aparece quando for divisivel por 10
    # Pinta de 1 a 10. Depois mostra. Apaga os 20 ultimos
    for pos in range(pontoB,pontoA,-1):
        strip.setPixelColor(pos-20,Color(G,R,B))
        strip.setPixelColor(pos,Color(0,0,0))
        if (pos % 10 == 0):
            strip.show()
            time.sleep(vel)

    for pos in range(pontoB):
        strip.setPixelColor(pos,Color(G,R,B))
        strip.setPixelColor(pos-20,Color(0,0,0))
        if (pos % 10 == 0):
            strip.show()
            time.sleep(vel)


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

    
def rainbowCycle(wait_ms=20, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    print('entrei no rainbow')
    print(strip.numPixels())
    print
    for j in range(256*iterations):
        if not globals.outroEfeitoRainbow:
            off()
            break
        for i in range(strip.numPixels()):
            print('entrei naquele for')
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        
