#!/bin/sh

cd /server/path/kindle_weather/

python2 weather-script.py

svgfile=weather-script-output

rsvg-convert --background-color=white -o "$svgfile".png "$svgfile".svg
pngcrush -c 0 -ow "$svgfile".png  "$svgfile"_c.png
rm "$svgfile".png
convert "$svgfile"_c.png -colorspace Gray "$svgfile".png
rm "$svgfile"_c.png
cp -f "$svgfile".png /var/www/weather/"$svgfile".png

