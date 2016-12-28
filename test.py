
import time
import RPi.GPIO as GPIO

PIN_TRIGGER = 3
PIN_ECHO = 5


def checkdist():
    # Set trigger
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    # Wait for 15us
    time.sleep(0.00005)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    while not GPIO.input(PIN_ECHO):
        pass

    # Start counting
    t1 = time.time()
    while GPIO.input(PIN_ECHO):
        pass

    # Stop counting
    t2 = time.time()

    # Return cm
    distance = (t2 - t1) * 34000 / 2

    # Anything more than 450, means too far.
    if distance > 450:
        distance = 10000

    return distance


GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT)
GPIO.output(36, GPIO.HIGH)
# PIN3 for trigger
GPIO.setup(PIN_TRIGGER, GPIO.OUT, initial=GPIO.LOW)
# PIN5 for Echo
GPIO.setup(PIN_ECHO, GPIO.IN)


p = GPIO.PWM(36, 50)  # 50HZ
p.start(0)


for k in range (0, 3):
    for i in range(0, 181, 10):
        cycle = 2.5 + 10 * i / 180
        p.ChangeDutyCycle(cycle)
        time.sleep(0.02)
        distance = checkdist()
        print "c:[%.1f], a:[%d], d:[%d]" % (cycle, i, distance)
        p.ChangeDutyCycle(0)
        time.sleep(0.2)

    for i in range(180, -1, -10):
        cycle = 2.5 + 10 * i / 180
        p.ChangeDutyCycle(cycle)
        time.sleep(0.2)
        #distance = checkdist()
        #print "c:[%.1f], a:[%d], d:[%d]" % (cycle, i, distance)
        #p.ChangeDutyCycle(0)
        #time.sleep(0.02)
    time.sleep(5)

'''
for i in range(0, 180, 10):
    cycle = 7 + 6 * i / 30
    print "i:%d  c:%d" %(i, cycle)
    p.ChangeDutyCycle(cycle)
    time.sleep(0.02)
    distance = checkdist()
    print "distance: %d" % distance
    #time.sleep(0.1)
    #p.ChangeDutyCycle(0)
    #time.sleep(0.2)

for i in range(50, -50, -10):
    cycle = 7 + 5 * i / 50
    print "i:%d  c:%d" % (i, cycle)
    p.ChangeDutyCycle(cycle)
    time.sleep(0.2)
    distance = checkdist()
    print "distance: %d" % distance
    #time.sleep(0.1)'''


GPIO.cleanup()