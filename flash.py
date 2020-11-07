#!/usr/bin/env python3

import pyboard
import sys

SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUD = 115200

if len(sys.argv) < 2:
    print("Usage: flash.py INPUT_FILE:DEST_PATH...")
    sys.exit(1)

def send_file(pyb, src, dest):
    template = "with open('{}', 'w') as f:\n    f.write('''{}''')\n\n"
    with open(src, 'r') as f:
        code = f.read()
    code = code.replace("\\", "\\\\")
    pyb.exec(template.format(dest, code))

print("Make sure your badge is connected and awake.")

#print("Opening direct serial connection...")
#with serial.Serial(SERIAL_PORT, SERIAL_BAUD) as f:
#    pass

print("Opening pyboard connection...")
pyb = pyboard.Pyboard(SERIAL_PORT)

print("Starting python shell...")
pyb.serial.write(b'\r\n')
pyb.read_until(1, b"\r\n>>> ")

print("Entering raw mode...")
pyb.enter_raw_repl()

for pair in sys.argv[1:]:
    src, _, dest = pair.partition(':')
    print("Sending file {} to {}...".format(src, dest))
    send_file(pyb, src, dest)

print("Exiting raw mode...")
pyb.exit_raw_repl()

print("Leaving python shell...")
pyb.serial.write(b'\x04')

pyb.close()

print("Done!")
