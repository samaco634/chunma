#! /bin/bash
echo Exporting pin 92
echo 92 >/sys/class/gpio/export
echo Exporting pin 52
echo 52 >/sys/class/gpio/export
echo in >/sys/class/gpio/gpio92/direction
echo in >/sys/class/gpio/gpio52/direction

# $ echo 92 >/sys/class/gpio/export (physical 22)
# $ echo 52 >/sys/class/gpio/export (physical 24)
# $ ls /sys/class/gpio
# $ ls /sys/class/gpio/gpio92/
# $ ls /sys/class/gpio/gpio52/
# $ echo in >/sys/class/gpio/gpio92/direction
# $ echo in >/sys/class/gpio/gpio52/direction
