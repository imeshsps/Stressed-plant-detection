#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -r 1024x768 --no-banner /home/pi/Deep_data/infa_1/$DATE.jpg
fswebcam -r 1024x768 --no-banner /home/pi/Deep_data/infa_2/$DATE.jpg
