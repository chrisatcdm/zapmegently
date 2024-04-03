import time

import RPi.GPIO as GPIO

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up LED pins
red_pin = 2
green_pin = 3
blue_pin = 4

# Set up LED colors
red = GPIO.PWM(red_pin, 100)
green = GPIO.PWM(green_pin, 100)
blue = GPIO.PWM(blue_pin, 100)

# Start PWM
red.start(0)
green.start(0)
blue.start(0)

# Set LED color to purple
red.ChangeDutyCycle(100)
blue.ChangeDutyCycle(100)

# Wait for 5 seconds
time.sleep(5)

# Clean up GPIO
red.stop()
green.stop()
blue.stop()
GPIO.cleanup()