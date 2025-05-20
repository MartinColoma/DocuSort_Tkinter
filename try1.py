import RPi.GPIO as GPIO
import time

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Define pin numbers
TRIG = 20
ECHO = 21

# Set GPIO pin directions
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_single_distance(timeout=0.02):
    # Make sure the trigger pin is LOW
    GPIO.output(TRIG, False)
    time.sleep(0.0002)  # 200 microseconds

    # Send a 10 microsecond HIGH pulse on the trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG, False)

    # Wait for echo to go HIGH (pulse start)
    start_time = time.perf_counter()
    while GPIO.input(ECHO) == 0:
        if time.perf_counter() - start_time > timeout:
            return None
    pulse_start = time.perf_counter()

    # Wait for echo to go LOW (pulse end)
    while GPIO.input(ECHO) == 1:
        if time.perf_counter() - pulse_start > timeout:
            return None
    pulse_end = time.perf_counter()

    # Calculate duration
    pulse_duration = pulse_end - pulse_start

    # Calculate distance (Speed of sound = 34300 cm/s)
    distance = pulse_duration * 17150
    return round(distance, 2)

def get_average_distance(samples=5):
    readings = []
    for _ in range(samples):
        dist = get_single_distance()
        if dist is not None:
            readings.append(dist)
        time.sleep(0.05)  # short delay between samples
    if readings:
        return round(sum(readings) / len(readings), 2)
    else:
        return None

try:
    print("Measuring distance. Press Ctrl+C to stop.")
    while True:
        distance = get_average_distance()
        if distance is not None:
            print(f"Distance: {distance} cm")
        else:
            print("Out of range or no echo received.")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopping measurement.")
    GPIO.cleanup()
