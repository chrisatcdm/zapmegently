import time
import RPi.GPIO as GPIO
import threading

GPIO.setwarnings(False)

class PWMController:
    def __init__(self, led_pin, frequency, duty_cycle):
        self.led_pin = led_pin
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.led_pin, self.frequency)
        self.thread = None
        self.stop_event = threading.Event()

    def start(self):
        if self.thread is not None and self.thread.is_alive():
            print("PWM is already running.")
            return
        self.thread = threading.Thread(target=self.pwm.start, args=(self.duty_cycle,))
        self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.pwm.stop()
            self.thread.join()
            self.thread = None

    def change_frequency(self, new_frequency):
        self.stop()
        self.frequency = new_frequency
        self.pwm = GPIO.PWM(self.led_pin, self.frequency)
        self.start()

    # Inside PWMController class
    def run_calibration(self, frequency, increment_duty_cycle_by, speed):
        self.start()
        while not self.stop_event.is_set():
            # Increase the duty cycle by the specified increment
            for duty_cycle in range(0, 100, increment_duty_cycle_by):
                self.pwm.ChangeDutyCycle(duty_cycle)
                # Sleep for the specified speed, but wake up every 0.1 second to check the stop_event
                for _ in range(int(speed * 10)):  # Convert seconds to tenths of a second
                    if self.stop_event.is_set():
                        break
                    time.sleep(0.1)
        self.stop()

    def stop_calibration(self):
        self.stop_event.set()

    def run_interrupter(self, duty_cycle1, duty_cycle2, time1, time2):
        self.start()
        while not self.stop_event.is_set():
            self.pwm.ChangeDutyCycle(duty_cycle1)
            # Sleep for the specified speed, but wake up every 0.1 second to check the stop_event
            for _ in range(int(time1 * 10)):  # Convert seconds to tenths of a second
                if self.stop_event.is_set():
                    break
                time.sleep(0.1)
            self.pwm.ChangeDutyCycle(duty_cycle2)
            for _ in range(int(time2 * 10)):  # Convert seconds to tenths of a second
                if self.stop_event.is_set():
                    break
                time.sleep(0.1)
        self.stop()


    def stop_interrupter(self):
        self.stop_event.set()

