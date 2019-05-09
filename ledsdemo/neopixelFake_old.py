LED_COUNT = 0

def Adafruit_NeoPixel(leds, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL):
    print('entrei no Adafruit_NeoPixel')
    global LED_COUNT
    LED_COUNT = leds
    print('Novo LED_COUNT: {}'.format(LED_COUNT))

class strip:
    def setPixelColor(pos,color_hex):
        canvas.itemconfig(r['retangulo{}'.format(pos)], fill=color_hex)
    def numPixels():
        print(LED_COUNT)
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