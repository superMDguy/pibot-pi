#!/bin/sh

export FLASK_APP=/home/pi/robot/control_server.py
flask run --host=0.0.0.0 --port=5000 &

raspivid -t 0 -h 720 -w 1280 -fps 30 -hf -vf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=0.0.0.0 port=9000 &

cd /home/pi/robot/public
sudo python2 -m SimpleHTTPServer 80 &

trap "sudo killall flask; killall raspivid; sudo killall python2" INT HUP ERROR EXIT
sleep infinity

