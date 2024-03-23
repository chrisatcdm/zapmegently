#!/usr/bin/env python3

import os
import time
import threading


from pwm_controller import PWMController


def get_integer_input(prompt, default_value):
    while True:
        try:
            value = input(prompt)
            if value == '':
                return int(default_value)
            else:
                return int(value)
        except ValueError:
            print("That's not a valid integer. Please try again.")

def get_yn_input(prompt, default_value):
    while True:
        value = input(prompt)
        if value == '':
            return default_value
        elif value.lower() == 'y':
            return True
        elif value.lower() == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome_message():
    print("Zap Me Gently - CP Simulator - v0.1")
    print(30 * "-")

print_welcome_message()
print("\n")  # Add some margin


def get_menu_choice():
    def print_menu():       # Your menu design here
        print(30 * "-", "Zap Me Gently - CP Simulator - v0.1", 30 * "-")
        print()
        print("1. 0-3V calibration ")
        print("2. 12/3 Interrupt cycle (protected) ")
        print("3. 12/3 Interrupt cycle (unprotected) ")
        print("4. Exit ")
        print()
        print(97 * "-")

    loop = True
    int_choice = -1

    while loop:  # While loop which will keep going until loop = False
        clear_screen()
        print_menu()  # Displays menu
        choice = input("Enter your choice [1-4]: ")
        if choice == '1':
            clear_screen()
            print("Enter custom values for calibration, or press enter to use default values.\n")

            frequency = get_integer_input("Frequency in Hz (default=38): ", 38)
            duty_cycle = 0
            increment_duty_cycle_by = get_integer_input("Increment duty cycle (default=5): ", 5)
            speed = get_integer_input("Enter speed in seconds (default=5): ", 5)

            pwm_controller = PWMController(led_pin=12, frequency=frequency, duty_cycle=duty_cycle)

            # Start calibration in a separate thread
            calibration_thread = threading.Thread(target=pwm_controller.run_calibration, args=(frequency, increment_duty_cycle_by, speed))
            calibration_thread.start()

            # Inform the user and wait for input asynchronously
            print("\nCalibration running. Press Enter at any time to stop...")
            input_thread = threading.Thread(target=lambda: input(""))
            input_thread.start()

            # Wait for the input thread to finish, which means the user pressed Enter
            input_thread.join()

            # Signal the calibration thread to stop
            pwm_controller.stop_calibration()
            calibration_thread.join()

            del pwm_controller
            loop = True
        elif choice == '2':
            clear_screen()
            print("Starting 12/3 interrupt cycle (protected).\n")

            # Initialize the PWMController
            pwm_controller = PWMController(led_pin=12, frequency=38, duty_cycle=0)
            interrupt_thread = threading.Thread(target=pwm_controller.run_interrupter, args=(40, 30, 12, 3))
            interrupt_thread.start()

            # Inform the user and wait for input synchronously
            input("Interrupter running. Press Enter at any time to stop...")

            # Signal the interrupter to stop
            pwm_controller.stop_interrupter()

            # Wait for the interrupter thread to complete
            interrupt_thread.join()

            del pwm_controller
            loop = True
        elif choice == '3':
            clear_screen()
            print("Starting 12/3 interrupt cycle (unprotected).\n")

            # Initialize the PWMController
            pwm_controller = PWMController(led_pin=12, frequency=38, duty_cycle=0)
            interrupt_thread = threading.Thread(target=pwm_controller.run_interrupter, args=(40, 18, 12, 3))
            interrupt_thread.start()

            # Inform the user and wait for input synchronously
            input("Interrupter running. Press Enter at any time to stop...")

            # Signal the interrupter to stop
            pwm_controller.stop_interrupter()

            # Wait for the interrupter thread to complete
            interrupt_thread.join()

            del pwm_controller
            loop = True
        elif choice == '4':
            int_choice = -1
            print("Exiting...")
            loop = False  # This will make the while loop to end
            # break
        else:
            # Any inputs other than values 1-4 we print an error message
            input("Wrong menu selection. Enter any key to try again..")
    return [int_choice, choice]

# Main loop
while True:
    choice, _ = get_menu_choice()
    if choice == -1:  # User chose to exit
        break
