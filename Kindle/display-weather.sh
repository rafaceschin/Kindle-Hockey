#!/bin/sh

cd /mnt/us/kite/unused

eips -c
eips -c

if wget http://path/to/server/weather/weather-script-output.png; then
	rm display-weather.png
	mv weather-script-output.png display-weather.png
	eips -g display-weather.png
else
	eips -g display-weather.png
fi
