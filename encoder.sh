#! /bin/bash
echo Exporting pin 92
echo 92 > /sys/class/gpio/export
echo Setting direction to out.
echo 0 > /sys/class/gpio/gpio$1/direction
