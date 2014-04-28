#!/bin/sh

cd /mnt/us/kite/unused

eips -c
 
if wget http://server-path/weather/DisplayTeams1.png; then
	rm LogoDisplay1.png
	mv DisplayTeams1.png LogoDisplay1.png 
	eips -g LogoDisplay1.png
else
	eips -g LogoDisplay1.png
fi
