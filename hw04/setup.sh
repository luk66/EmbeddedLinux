#!/bin/bash
cd /sys/class/gpio
echo 50 > export
echo 23 > export
echo in > gpio50/direction
echo 1n > gpio23/direction
