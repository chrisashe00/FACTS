# Code to start communication between jetson nano and esp32 only works on jetson nano 
# Chris Ashe, 21/03/2023

import serial
import time

# esp32 = serial.Serial('/dev/ttyACM0' , 115200, timeout=5)

esp32 = serial.Serial(
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
        esp32.write("1".encode())
        esp32.write("2".encode())
        data = esp32.readline()

        if data:
            print(data)
    except Exception as e:
        print(e)
        esp32.close()