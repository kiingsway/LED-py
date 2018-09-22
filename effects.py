import time
import threading
from decimal import *
from neopixel import *

BPM = 128
bpm4 = Decimal(60)/Decimal(BPM)


# LED strip configuration:
LED_COUNT      = 120      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
strip.begin()

def off(event):
    for i in range(LED_COUNT):
        strip. setPixelColor(i, Color(0,0,0))
    strip.show()
    print("desliguei")

def bassBracoInvertEffect2(pontoA,pontoB, R,G,B, vel):
    # Liga a ultima linha de LED e vai descendo ou subindo
    for i in range(6):
        if i < 4:
            for j in range(60+12*i,60+12*(1+i)):
                strip.setPixelColor(j,Color(100,100,0))
            for y in range(60-(12*i),60-(12*(1+i)),-1):
                strip.setPixelColor(y,Color(100,100,0))
        strip.show()
        time.sleep(vel)



def hihat(vel):
    for i in range(5):
        if i < 4:
            for j in range(60+12*i,60+12*(1+i)):
                strip.setPixelColor(j,Color(100,100,0))
            for y in range(60-(12*i),60-(12*(1+i)),-1):
                strip.setPixelColor(y,Color(100,100,0))
        if i >= 1:
            for j in range(60+12*(i-1),60+12*i):
                strip.setPixelColor(j,Color(0,0,0))
            for y in range(60-12*(i-1),60-12*i,-1):
                strip.setPixelColor(y,Color(0,0,0))
        strip.show()
        time.sleep(vel)

def simpleBassEffect(pontoA,pontoB, R,G,B, vel):
    # Simplesmente liga os LEDs escolhidos e vai apagando-os gradativamente
    # Para desligar gradativamente foi feito o primeiro for e diminui por porcentagem
    # Assim todos os LEDs sao desligados de forma equalitaria
    for i in range(100,-10,-10):
        for j in range(pontoA,pontoB):
            x = Decimal(G)/Decimal(100)*i
            y = Decimal(R)/Decimal(100)*i
            z = Decimal(B)/Decimal(100)*i
            strip.setPixelColor(j,Color(int(x),int(y),int(z)))
        strip.show()
        time.sleep(vel)


def corteCobraEffect(pontoA,pontoB, R,G,B, vel):
    tamanho = 10
    for i in range(60+tamanho+1):
        strip.setPixelColor(60+i,Color(G,R,B))
        strip.setPixelColor(60+i-(tamanho-2),Color(G/2,R/2,B/2))
        strip.setPixelColor(60+i-(tamanho-1),Color(G/4,R/4,B/4))
        if i > tamanho-1: strip.setPixelColor(60+i-tamanho,Color(0,0,0))
        strip.setPixelColor(60-i,Color(R,G,B))
        strip.setPixelColor(60-i+(tamanho-2),Color(G/2,R/2,B/2))
        strip.setPixelColor(60-i+(tamanho-1),Color(G/4,R/4,B/4))
        if i > tamanho-1: strip.setPixelColor(60-i+tamanho,Color(0,0,0))
        strip.show()
        time.sleep(vel)


def laserLeftEffect(pontoA,pontoB, R,G,B, vel, duracao):
    # Duracao eh o tempo atual adicionado ao desejado
    # Variavel x adicionada para fazer o laser andar.
    tempoFim = time.time() + duracao
    x = 0
    while time.time() < tempoFim:
        for i in range(-1,119,13):
            strip.setPixelColor(i+x,Color(G,R,B))
            strip.setPixelColor(i+1+x,Color(G,R,B))
            strip.setPixelColor(i-1+x,Color(0,0,0))
            print(i+x, i+1+x, i-1-x)
        strip.show()
        time.sleep(vel)
        x += 1
        if x >= 13: x = 0
    off(0)



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

def bassBracoEffect(altura, R,G,B, vel):

    def up(altura, R,G,B, vel):
        # Altura maxima: 9,23 ou 10
        # R,G,B: Cores
        # Vel: Velocidade para aparecer cada altura

        # Neste for (i), primeiro ele manda a altura desejada
        # No proximo (j) ele diz quais LEDs deverao ligar.
        for i in range(1,altura):
            for j in range(13*(i-1), 13*i):
                strip.setPixelColor(j, Color(G,R,B))
            strip.show()
            time.sleep(vel)

    def treble(altura, R,G,B, vel):
        for i in range(altura,altura+1):
            for j in range(13*(i-1), 13*i):
                strip.setPixelColor(j, Color(G,R,B))
            strip.show()
            time.sleep(vel)

        for i in range(altura+1,altura-1,-1):
            for j in range(13*(i-1), 13*i):
                strip.setPixelColor(j, Color(0,0,0))
            strip.show()
            time.sleep(.01)

    def down(altura, vel):
        for i in range(altura-1,0,-1):
            for j in range(13*(i-1), 13*i):
                strip.setPixelColor(j, Color(0,0,0))
            strip.show()
            time.sleep(vel)

    up   (altura, R,G,B, vel)
    '''
    treble(altura, R,G,B, vel)
    time.sleep(0.01)
    treble(altura, R,G,B, vel)
    time.sleep(0.01)
    treble(altura, R,G,B, vel)
    time.sleep(0.01)
    treble(altura, R,G,B, vel)
    time.sleep(0.01)
    '''
    down (altura, vel)

def bassBracoInvertEffect(altura, R,G,B, vel):
    def up(altura, R,G,B, vel):
        for i in range(1,altura):
            for j in range(120-(13*(i-1)), 120-(13*i),-1):
                strip.setPixelColor(j, Color(G,R,B))
            strip.show()
            time.sleep(vel)

    def treble(altura, R,G,B, vel):
        for i in range(altura,altura+1):
            for j in range(120-(13*(i-1)), 120-(13*i),-1):
                strip.setPixelColor(j, Color(G,R,B))
            strip.show()
            time.sleep(vel)

        for i in range(altura+1,altura-1,-1):
            for j in range(120-(13*(i-1)), 120-(13*i),-1):
                strip.setPixelColor(j, Color(0,0,0))
            strip.show()
            time.sleep(.01)
    
    def down(altura, vel):
        for i in range(altura-1,0,-1):
            for j in range(120-(13*(i-1)), 120-(13*i),-1):
                strip.setPixelColor(j, Color(0,0,0))
            strip.show()
            time.sleep(vel)

    up   (altura, R,G,B, vel)
    '''
    treble(altura, R,G,B, vel)
    time.sleep(0.01)
    treble(altura, R,G,B, vel)
    time.sleep(0.01)
    treble(altura, R,G,B, vel)
    time.sleep(0.01)
    treble(altura, R,G,B, vel)
    time.sleep(0.01)
    '''
    down (altura, vel)


def cobraEffect(R, G, B, pontoA, pontoB, vel, sobeDesce):
    for i in range(pontoA, pontoB):
        strip.setPixelColor(i, Color(R, G, B))
        strip.show()
        time.sleep(vel)
    if sobeDesce:
        for i in range(pontoB, pontoA-1, -1):
            strip.setPixelColor(i, Color(0,0,0))
            strip.setPixelColor(i-1, Color(R,G,B))
            strip.show()
            time.sleep(vel)


def guitarGFY(cor):
    if cor == 1:
        for i in range(100,-5,-5):
            strip.setPixelColor(92, Color(i,0,i))
            strip.setPixelColor(93, Color(i,0,i))
            strip.setPixelColor(94, Color(i,0,i))
            strip.show()
            time.sleep(.005)
    if cor == 2:
        for i in range(100,-5,-5):
            strip.setPixelColor(106, Color(i,0,i))
            strip.setPixelColor(107, Color(i,0,i))
            strip.setPixelColor(108, Color(i,0,i))
            strip.show()
            time.sleep(.005)
    if cor == 3:
        for i in range(100,-5,-5):
            strip.setPixelColor(118, Color(i,0,i))
            strip.setPixelColor(117, Color(i,0,i))
            strip.setPixelColor(116, Color(i,0,i))
            strip.show()
            time.sleep(.005)





def luz(R, G, B, pontoA, pontoB):
    for i in range(pontoA, pontoB):
        strip.setPixelColor(i, Color(R, G, B))

def bpmtest():
    for i in range(5):
    	bpmT1 = threading.Thread(target=bracoUp,args=(0.025,))
    	bpmT1.start()
        time.sleep(bpm4/2)
        bpmT2 = threading.Thread(target=hihat,args=(0.025,))
    	bpmT2.start()
        time.sleep(bpm4/2)
        bpmT3 = threading.Thread(target=bracoDown,args=(0.025,))
    	bpmT3.start()
        time.sleep(bpm4/2)
        bpmT4 = threading.Thread(target=hihat,args=(0.025,))
    	bpmT4.start()
        time.sleep(bpm4/2)

def TAN():
    luz(100,100,0,60,120)
    strip.show();

def TUN():
    luz(100,100,0,0,60)
    strip.show();
    
        
def BASS():
    cobra(0,100,100,0,40,.0001,1)
        

def bassLBaixoTouca():
    kill=0
    luz(100,100,100,0,40)
    strip.show()
    for rgb in range(100,-1,-5):
        if kill==1: return
        luz(rgb,rgb,rgb,0,40)
        strip.show()
        time.sleep(.05)

def bassLAltoTouca():
    luz(100,100,100,40,80)
    strip.show()
    for rgb in range(100,-1,-5):
        luz(rgb,rgb,rgb,40,80)
        strip.show()
        time.sleep(.05)

def bassAltoTouca():
    luz(100,100,100,80,120)
    strip.show()
    for rgb in range(100,-1,-5):
        luz(rgb,rgb,rgb,80,120)
        strip.show()
        time.sleep(.05)

def tresPontos():
    for i in range(0,29+6):
        if (i <= 30):
            strip.setPixelColor(i, Color(100,0,100))
            strip.setPixelColor(60-i, Color(100,0,100))
            strip.setPixelColor(i+60, Color(100,0,100))
            strip.setPixelColor(120-i, Color(100,0,100))
	if (i >= 3):
            strip.setPixelColor(i-4, Color(0,0,0))
            strip.setPixelColor(64-i, Color(0,0,0))
            strip.setPixelColor(i+56, Color(0,0,0))
            strip.setPixelColor(124-i, Color(0,0,0))
	strip.show()
	time.sleep(.05)
    
def tresPontosInvert():
    for i in range(0,29+6):
        if (i <= 30):
            strip.setPixelColor(30-i, Color(0,100,0))
            strip.setPixelColor(30+i, Color(0,100,0))
            strip.setPixelColor(90-i, Color(0,100,0))
            strip.setPixelColor(90+i, Color(0,100,0))
	if (i >= 4):
            strip.setPixelColor(34-i, Color(0,0,0))
            strip.setPixelColor(26+i, Color(0,0,0))
            strip.setPixelColor(94-i, Color(0,0,0))
            strip.setPixelColor(86+i, Color(0,0,0))
	strip.show()
	time.sleep(.05)

strip.begin()


    

