#!/usr/bin/env python
import argparse
import time

from pmw3901 import BG_CS_BACK_BCM, BG_CS_FRONT_BCM, PAA5100, PMW3901

print("""frame_capture.py - Capture the raw frame data from the PMW3901

Press Ctrl+C to exit!
""")

parser = argparse.ArgumentParser()
parser.add_argument("--board", type=str, choices=["pmw3901", "paa5100"], required=True, help="Breakout type.")
parser.add_argument("--rotation", type=int, default=0, choices=[0, 90, 180, 270], help="Rotation of sensor in degrees.")
parser.add_argument("--spi-slot", type=str, default="front", choices=["front", "back"], help="Breakout Garden SPI slot.")

args = parser.parse_args()

# Pick the right class for the specified breakout
SensorClass = PMW3901 if args.board == "pmw3901" else PAA5100

flo = SensorClass(spi_port=0, spi_cs=1, spi_cs_gpio=BG_CS_FRONT_BCM if args.spi_slot == "front" else BG_CS_BACK_BCM)
flo.set_rotation(args.rotation)


def value_to_char(value):
    charmap = [" ", "░", "▒", "▓", "█"]
    value /= 255
    value *= len(charmap) - 1
    value = int(value)
    return charmap[value] * 2  # Double chars to - sort of - correct aspect ratio


try:
    while True:
        print("Capturing...")
        data = flo.frame_capture()
        for y in range(35):
            y = 35 - y - 1 if args.rotation in (180, 270) else y
            for x in range(35):
                x = 35 - x - 1 if args.rotation in (180, 90) else x
                if args.rotation in (90, 270):
                    offset = (x * 35) + y
                else:
                    offset = (y * 35) + x
                value = data[offset]
                print(value_to_char(value), end="")
            print("")
        print("5...")
        time.sleep(1.0)
        print("4...")
        time.sleep(1.0)
        print("3...")
        time.sleep(1.0)
        print("2...")
        time.sleep(1.0)
        print("Get Ready!")
        time.sleep(1.0)

except KeyboardInterrupt:
    pass
