# Code to start communication between jetson nano and esp32 only works on jetson nano 
# Chris Ashe, 21/03/2023

import serial
import time

# arduino = serial.Serial('/dev/ttyACM0' , 115200, timeout=5)

arduino = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 115200,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 5,
    xonxoff = False,
    rtscts = False,
    dsrdtr = False,
    writeTimeout = 2
)
# This is just an example, you can put whatever you want here, the strings '1' '2' move the stepper CW and CCW
# when passed to serial monitor

while True: 
    try:
        arduino.write("1".encode())
        arduino.write("2".encode())
        data = arduino.readline()

        if data:
            print(data)
    except Exception as e:
        print(e)
        arduino.close()