"""
Proximity Safety Servo python file
Authors: Omar Abdeen, Nathaniel Bosh
Note: A3 reads the sensor and A2 reads the potentiometer. Just works that way for some reason. so This is the working code.
Most likely reason: the PCF8591 ADC sends the result of the previous conversion first, so each read gives
the channel selected before it. The sensor is on A2 and the potentiometer on A3, and the loop reads them one
after the other, so selecting A3 returns the sensor and selecting A2 returns the potentiometer.
"""
import smbus
import time
import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BOARD)

# Constants and Pins
MAX_VALUE = 255
SERVOPIN = 13
GREENPIN = 37
REDPIN = 35
MAX_LENGTH = 80
ZERODEG = 2.5
NINETYDEG = 7.5
ONEEIGHTYDEG = 12.5
MAX_ANGLE = 180
    # we use 5 instead of 10 for a more accurate reading
MIN_LENGTH = 5
ZERO = 0

# Setup for ADC and servo motor
GPIO.setup(SERVOPIN, GPIO.OUT)
p = GPIO.PWM(SERVOPIN, 50)  # channel=12 frequency=50Hz, for servo motor
address = 0x48 #AOUT Address
A0 = 0x40 #Photoresistor
A1 = 0x41 #Thermistor
A2 = 0x42 #ExternalDevice
A3 = 0x43 #Potentiometer
p.start(ZERODEG)
bus = smbus.SMBus(1)

# Setup for LED lights and IR sensor
GPIO.setup(REDPIN, GPIO.OUT)
GPIO.setup(GREENPIN, GPIO.OUT)
p_green = GPIO.PWM(GREENPIN, 60)
p_red = GPIO.PWM(REDPIN, 60)
p_green.start(ZERO)
p_red.start(ZERO)

# Function for Updating motor angle
def Update_Angle():
    bus.write_byte(address,A2)
    Value = bus.read_byte(address)
    curr_degree = (Value / MAX_VALUE) * MAX_ANGLE
    # 0 to 180 degrees maps onto 2.5% to 12.5% duty cycle, so every 18 degrees is 1%
    curr_duty_cycle = (curr_degree / (MAX_ANGLE / (ONEEIGHTYDEG - ZERODEG))) + ZERODEG
    print("Angle read from Potentiometer: ", curr_degree, " degrees")
    return int(curr_duty_cycle)
    
# Function to get distance from sensor
def IR_distance():
    bus.write_byte(address,A3)
    value = bus.read_byte(address)
    distance = MAX_LENGTH - (value * MAX_LENGTH / MAX_VALUE) + MIN_LENGTH
    print("Distance From sensor now is: ", distance, "cm")
    return int(distance)

try:
    # Keep asking until an integer is entered
    while True:
        try:
            off_distance = int(input("Please enter an integer value from 10-80\nSuch that motor manipulation is off from INPUT to 10 cm\n"))
            break
        except ValueError:
            print("That is not an integer. Try again.")
    # Clamping for Sensor distance.
    if off_distance > MAX_LENGTH:
        off_distance = MAX_LENGTH
    elif off_distance < 10:
        off_distance = 10
    while True:
        Current_Distance = IR_distance()
        Potentiometer_Angle = Update_Angle()
        if Current_Distance > off_distance: 
            p_red.ChangeDutyCycle(ZERO)
            p_green.ChangeDutyCycle(Current_Distance + 15)
            p.ChangeDutyCycle(Potentiometer_Angle)
    
        else:
            p_green.ChangeDutyCycle(ZERO)
            p_red.ChangeDutyCycle(off_distance - Current_Distance)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    pass

finally:
    #reset and close
    p.ChangeDutyCycle(ZERODEG)
    p_red.ChangeDutyCycle(ZERO)
    p_green.ChangeDutyCycle(ZERO)
    p_red.stop()
    p_green.stop()
    p.stop()
    GPIO.cleanup()
