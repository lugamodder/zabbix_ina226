#!/bin/bash

echo 66 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio66/direction
cat /sys/class/gpio/gpio66/value
echo 66 > /sys/class/gpio/unexport
