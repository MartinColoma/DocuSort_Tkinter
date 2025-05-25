import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import messagebox
import threading

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Ultrasonic Sensor Pins
TRIG = 23
ECHO = 24

# Setup pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_single_distance(timeout=0.02):
    GPIO.output(TRIG, False)
    time.sleep(0.0002)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.perf_counter()
    while GPIO.input(ECHO) == 0:
        if time.perf_counter() - start_time > timeout:
            return None
    pulse_start = time.perf_counter()

    while GPIO.input(ECHO) == 1:
        if time.perf_counter() - pulse_start > timeout:
            return None
    pulse_end = time.perf_counter()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

def is_bin_full(check_duration=5, distance_threshold=18):
    """Check if distance is = 18 cm for the entire duration."""
    start_time = time.time()
    while time.time() - start_time < check_duration:
        dist = get_single_distance()
        if dist is None or dist > distance_threshold:
            return False
        time.sleep(0.5)  # Check every 0.5s
    return True

def check_bin_status():
    if is_bin_full():
        messagebox.showerror("Bin Status", "?? The bin is full!")
    else:
        messagebox.showinfo("Bin Status", "? The bin is NOT full.")

# GUI
def run_gui():
    root = tk.Tk()
    root.title("Ultrasonic Bin Checker")
    root.geometry("300x200")
    
    label = tk.Label(root, text="Click to check bin status", font=("Courier New", 12))
    label.pack(pady=20)

    def on_check():
        threading.Thread(target=check_bin_status).start()

    check_button = tk.Button(root, text="Check Bin", font=("Courier New", 14), command=on_check)
    check_button.pack(pady=20)

    def on_close():
        GPIO.cleanup()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    try:
        run_gui()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Exiting program.")
