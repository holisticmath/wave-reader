#!/usr/bin/bash
cd /home/pi/projects/wave-reader/src
nohup python read_wave2.py --SERIAL_NUMBER=2950044984  --LOGGING=INFO --SAMPLE_PERIOD=600 &
