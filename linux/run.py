#!/usr/bin/env python
#
# EspLight firmware uploader
# https://github.com/EspLight/EspLight-firmware-uploader
#
# Copyright (C) 2015 Michiel Brink
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys
import glob
import serial
import urllib
import os


def get_serial_ports():
    """ Lists serial port names
        found at http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def numeric_input(question,max_length):
    output = raw_input(question)
    try:
        if int(output) < max_length:
            return int(output)
        else:
            print "please fill in a numeric value under " + str(max_length)
            return numeric_input(question,max_length)
    except ValueError:
        print "please fill in a numeric value"
        return numeric_input(question,max_length)

if __name__ == '__main__':
    serial_port_array = get_serial_ports()
    serial_port_array.append("quit")

    print ""
    print "This program will replace the firmware on an EspLight to the newest firmware"

    while 1:
        try:
            yesno = raw_input("Are you sure you want to continue? [Y,N]")
        except KeyboardInterrupt:
            quit()
        if yesno.lower() in ('yes','y'): break
        elif yesno.lower() in ('no','n'): quit()

    print ""
    print ".........................."
    for index, value in enumerate(serial_port_array):
        print str(index) + " : " + value
    print ".........................."
    print ""
    port_number = numeric_input("select port:",len(serial_port_array))
    print ""

    selected_port = serial_port_array[port_number]

    if port_number == len(serial_port_array)-1:
        quit()

    print "You have selected " + selected_port
    print "To set the EspLight in programming mode, follow the instructions:"
    print "1. Push the Reset and AP button together"
    print "2. Release Reset"
    print "3. Release AP"
    print ""
    raw_input("Press Enter if you are ready for flashing")
    print ""

    urllib.urlretrieve ("https://github.com/EspLight/EspLight-firmware/raw/master/bin/firmware.bin", "firmware.bin")

    # run your program and collect the string output
    os.system("python2 esptool.py -p " + selected_port + " write_flash -ff 80m -fm qio -fs 32m-c1 0x00000 firmware.bin")
