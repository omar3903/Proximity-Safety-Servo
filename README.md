# Proximity Safety Servo

A Raspberry Pi project in Python: a servo motor you steer with a knob, which stops when something comes too close. An infrared distance sensor watches the space in front of it. While the space is clear, the servo follows the potentiometer and a green LED glows brighter the farther away the nearest object is. When something comes closer than a cutoff distance you choose, the servo stops and a red LED glows brighter the closer it gets.

Built with Nathaniel Bosh in November 2023, during my Computer Science degree at Wilfrid Laurier University.

## Hardware

| Part | Connection |
|---|---|
| PCF8591 ADC module | I2C bus 1, address `0x48` |
| Infrared distance sensor (10 to 80 cm) | ADC input A2 |
| Potentiometer | ADC input A3 |
| Servo motor | pin 13, 50 Hz PWM |
| Green LED | pin 37, PWM |
| Red LED | pin 35, PWM |

Pins use the Pi's physical (BOARD) numbering.

## Run

Turn on I2C with `sudo raspi-config`, then:

```bash
sudo apt install python3-smbus python3-rpi.gpio
python3 proximity_servo.py
```

Enter the cutoff distance in cm (10 to 80). Ctrl+C stops the program and resets the servo and LEDs.

## Notes

- The PCF8591 sends the result of its previous conversion first, so each read returns the channel selected before it. That's why the code selects A3 to read the sensor and A2 to read the potentiometer.
- Fixed in 2026: the servo's angle formula divided by 20 instead of 18, so it stopped short of 180°, and typing something other than a number for the cutoff crashed the program. These two fixes haven't been run on the hardware yet.
