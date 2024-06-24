import serial
import time

# Establish the connection to the Arduino
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1) # Replace 'COM3' with the port your Arduino is connected to

def send_data(data):
    arduino.write(bytes(data, 'utf-8'))
    time.sleep(0.05) # Give some time for the Arduino to process the data

while True:
    data_to_send = input("Enter data to send to Arduino: ")
    send_data(data_to_send) # Send data with newline character