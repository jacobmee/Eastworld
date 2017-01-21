import time
import RPi.GPIO as GPIO

PIN_LED_RED = 33
PIN_LED_GREEN = 31
PIN_LED_BLUE = 29
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_LED_RED, GPIO.OUT)
GPIO.setup(PIN_LED_GREEN, GPIO.OUT)
GPIO.setup(PIN_LED_BLUE, GPIO.OUT)

r = GPIO.PWM(PIN_LED_RED, 50)
r.start(0)
g = GPIO.PWM(PIN_LED_GREEN, 50)
g.start(0)
b = GPIO.PWM(PIN_LED_BLUE, 50)
b.start(0)


def set_color(color):
    r.ChangeDutyCycle(color[0]/2.55)
    g.ChangeDutyCycle(color[1]/2.55)
    b.ChangeDutyCycle(color[2]/2.55)

try:
    color = [0, 0, 205]  # Dodger Blue
    set_color(color)
    time.sleep(1)

    color = [0, 100, 0]  # Sea Green
    set_color(color)
    time.sleep(1)

    color = [80, 0, 80]  # Purple
    set_color(color)
    time.sleep(1)

    color = [50, 205, 50]
    set_color(color)
    time.sleep(1)

    color = [218,165,32]
    set_color(color)
    time.sleep(1)

except KeyboardInterrupt:
    pass
r.stop()
g.stop()
b.stop()

GPIO.cleanup()