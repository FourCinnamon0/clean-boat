from machine import Pin, PWM

class Thrusters():
    def __init__(self):
        self.left_motor = PWM(Pin(12, Pin.OUT))
        self.right_motor = PWM(Pin(13, Pin.OUT))

        self.left_motor.freq(500)
        self.right_motor.freq(500)

        self.left_motor.duty_u16(0)
        self.right_motor.duty_u16(0)

    def apply_power(self, left_power, right_power):
        self.left_motor.duty_u16(left_power)
        self.right_motor.duty_u16(right_power)

#65535 = 100%
#32767 = 50%
