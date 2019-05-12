#!/bin/sh
#Enable capture device
amixer -c 0 cset numid=18,iface=MIXER,name='Mic1 Capture Switch' on,on > /dev/null && \
echo "Capture device enabled"

#Start program
cd /app
python3 main.py $@

