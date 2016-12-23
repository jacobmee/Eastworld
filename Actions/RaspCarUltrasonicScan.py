import time

from Actions.Action import Action


class RaspUltrasonicScan(Action):

    # HC-SR04, the farest it can get is 4.5m
    def checkdist(self):
        # 发出触发信号
        GPIO.output(2, GPIO.HIGH)
        # 保持10us以上（我选择15us）
        time.sleep(0.000015)
        GPIO.output(2, GPIO.LOW)
        while not GPIO.input(3):
            pass
        # 发现高电平时开时计时
        t1 = time.time()
        while GPIO.input(3):
            pass
        # 高电平结束停止计时
        t2 = time.time()
        # 返回距离，单位为厘米

        distance = (t2 - t1) * 34000 / 2

        if distance > 450:
            distance = 10000

        return distance

    def execute(self):
        super(Action, self).execute()

        GPIO.setmode(GPIO.BCM)
        # 第3号针，GPIO2
        GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW)
        # 第5号针，GPIO3
        GPIO.setup(3, GPIO.IN)

        time.sleep(2)
        avg_distance = 0
        try:
            for i in range(0, 3):
                distance = self.checkdist()
                print 'Distance: %0.1f cm' %distance
                avg_distance = avg_distance + distance
                time.sleep(0.5)
        except KeyboardInterrupt:
            GPIO.cleanup()

        avg_distance = avg_distance/3
        print 'Avg Distance: %0.1f cm' %avg_distance