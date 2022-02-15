#!/usr/bin/bash
cd /home/pi/projects/wave-reader/src
python read_wave2.py 2950044984 3600 2>&1 >> radon.txt
