import pigpio
import time

servo_pin = 17
pi = pigpio.pi()
if not pi.connected:
    exit()

def set_angle(angle):
    pulsewidth = 500 + (angle / 180.0) * 2000  # Maps 0-180 to 500-2500 us
    pi.set_servo_pulsewidth(servo_pin, pulsewidth)

try:
    while True:
        angle = float(input("Enter angle (0�180): "))
        if 0 <= angle <= 180:
            set_angle(angle)
        else:
            print("Out of range!")
except KeyboardInterrupt:
    pass
finally:
    pi.set_servo_pulsewidth(servo_pin, 0)
    pi.stop()
