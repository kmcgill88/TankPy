#!/bin/bash

#enable the driver
sudo usermod -a -G video pi
sudo modprobe uvcvideo

sudo fswebcam --device /dev/video0 --title "Tank Cam" --timestamp "%m/%d/%Y %r (%Z)" --resolution 640x480 --save /var/www/html/tank.jpg


#for i in {1..12}
#do
# sudo fswebcam --device /dev/video0 --resolution 640x480 --save /var/www/html/tank.jpg
# echo "Snapshot $i"
# sleep 5
#done

