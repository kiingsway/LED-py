import RPi.GPIO as GPIO
from time import sleep
#GPIO.setWarnings(False)
GPIO.cleanup()

ledRPin = 23
ledGPin = 24
ledBPin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRPin, GPIO.OUT)		# set GPIO 25 as output for the PWM signal
GPIO.setup(ledGPin, GPIO.OUT)    	# set GPIO 25 as output for the PWM signal
GPIO.setup(ledBPin, GPIO.OUT)    	# set GPIO 25 as output for the PWM signal
ledRD2A = GPIO.PWM(ledRPin, 1000)    # create object D2A for PWM on port 25 at 1KHz
ledGD2A = GPIO.PWM(ledGPin, 1000)    # create object D2A for PWM on port 25 at 1KHz
ledBD2A = GPIO.PWM(ledBPin, 1000)    # create object D2A for PWM on port 25 at 1KHz
ledRD2A.start(0)                	# start the PWM with a 0 percent duty cycle (off)
ledGD2A.start(0)               	 	# start the PWM with a 0 percent duty cycle (off)
ledBD2A.start(0)              		  # start the PWM with a 0 percent duty cycle (off)

def fitaLed(r,g,b):
	ledRD2A.ChangeDutyCycle(r)
	ledGD2A.ChangeDutyCycle(g)
	ledBD2A.ChangeDutyCycle(b)

