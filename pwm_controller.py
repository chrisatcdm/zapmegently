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
        # Set up LED pins
        self.red_pin = 2
        self.green_pin = 3
        self.blue_pin = 4

        # Set up LED pins as outputs
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)


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
                GPIO.output(self.red_pin, GPIO.HIGH)
                GPIO.output(self.green_pin, GPIO.LOW)
                GPIO.output(self.blue_pin, GPIO.HIGH)
                time.sleep(0.01)
                GPIO.output(self.red_pin, GPIO.HIGH)
                GPIO.output(self.green_pin, GPIO.HIGH)
                GPIO.output(self.blue_pin, GPIO.HIGH)
                # Sleep for the specified speed, but wake up every 0.1 second to check the stop_event
                for _ in range(int(speed * 10)):  # Convert seconds to tenths of a second
                    if self.stop_event.is_set():
                        break
                    time.sleep(0.1)
        GPIO.cleanup()  
        self.stop()

    def stop_calibration(self):
        self.stop_event.set()

    def run_interrupter(self, duty_cycle1, duty_cycle2, time1, time2):
        self.start()
        while not self.stop_event.is_set():
            self.pwm.ChangeDutyCycle(duty_cycle1)
            # Turn on the LED
            GPIO.output(self.red_pin, GPIO.LOW)
            GPIO.output(self.green_pin, GPIO.HIGH)
            GPIO.output(self.blue_pin, GPIO.HIGH)
            # Sleep for the specified speed, but wake up every 0.1 second to check the stop_event
            for _ in range(int(time1 * 10)):  # Convert seconds to tenths of a second
                if self.stop_event.is_set():
                    break
                time.sleep(0.1)
            self.pwm.ChangeDutyCycle(duty_cycle2)
            # Turn on the LED
            GPIO.output(self.red_pin, GPIO.HIGH)
            GPIO.output(self.green_pin, GPIO.LOW)
            GPIO.output(self.blue_pin, GPIO.HIGH)
            for _ in range(int(time2 * 10)):  # Convert seconds to tenths of a second
                if self.stop_event.is_set():
                    break
                time.sleep(0.1)
        # Clean up GPIO
        GPIO.cleanup()  
        self.stop()


    def stop_interrupter(self):
        self.stop_event.set()

    def start_traction_simulation(self):
        self.start()
        while not self.stop_event.is_set():
            GPIO.output(self.red_pin, GPIO.HIGH)
            GPIO.output(self.green_pin, GPIO.HIGH)
            GPIO.output(self.blue_pin, GPIO.LOW)
            with open('dc1_data.csv', 'r') as file:
                dc1_data = [int(line.strip()) for line in file.readlines()]
                # print the first 10 values
                # print(dc1_data[:10])
            for data in dc1_data:
                # print(data)
                self.pwm.ChangeDutyCycle(data)
                # Sleep for the specified speed, but wake up every 0.1 second to check the stop_event
                for _ in range(int(.2 * 10)):  # Convert seconds to tenths of a second
                    if self.stop_event.is_set():
                        break
                    time.sleep(0.1)
        GPIO.cleanup()  
        self.stop()

    def stop_traction_simulation(self):
        self.stop_event.set()

