#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")
DATE2=$(date +"%Y-%m-%d")

fswebcam -r 1024x768 --no-banner /home/pi/Deep_data/infa_1/$DATE2/$DATE.jpg
fswebcam -r 1024x768 --no-banner /home/pi/Deep_data/infa_2/$DATE2/$DATE.jpg
