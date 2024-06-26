# CP Simulator

Welcome to the CP Simulator, a powerful tool designed for quality assurance, demonstration, and training. This simulator includes a range of features to help you test and calibrate remote monitoring systems/data loggers, and simulate test point scenarios for training CP technicains.

## Features

- 0V to 3V Calibration Mode: This feature allows the simulator to ramp up from 0 volts to 3.3V in increments over a period of time. Users can customize the frequency of the PWM in Hz (default is 38Hz), the magnitude of the steps in voltage as a percentage of the PWM (default is 5% which is approx. 0.177mV), and the speed, which is the duration of time each step takes (default is 5 seconds).
- Simulated On/Off Survey of a Protected System: This function simulates a system interrupting at a 12s on / 3s off cycle. The output values are approximately 1.3V on, and 1V off.
- Simulated On/Off Survey of an Unprotected System: Similar to the previous function, this feature simulates a system interrupting at a 12s on / 3s off cycle. The output values are approximately 1.3V on, and 0.6V off.
- Traction output: a 0-3V DC traction simulation.

## How to Use

1. SSH into the console via windows command prompt: `ssh chris@rpiz2w.local`
2. Change directory: `cd zapmegently`
3. Run the script: `./simulator.py`

Enjoy using your CP Simulator!


### Upcoming Features

- Non interruption mode
- Interference switching (9/3 and a 12/3 defaults) but also make them customisable
- Custom mode where you can program in all of the parameters
- Be able to program/upload potential curves
- Add SD card slot
- Add programmable interface to add local wifi credentials
- File viewer for web interface
- Shunt simulation
- Non-coarse on/off curve
- Depolarisation curve
