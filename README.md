Kindle-Hockey
=============

Kindle Hockey and Weather Station


I had an old Kindle sitting around and liked the idea of using it as a weather station, as in the great idea seen here:

http://www.mpetroff.net/archives/2012/09/14/kindle-weather-display/

Using Kite and USBnet is the easiest way to get the Kindle to do what you want:

http://www.mobileread.com/forums/showthread.php?t=168270

You also need a server to update the display files (or you could have the Kindle run it, but I already had a server so I went with that option)

It's mostly self-explanatory: The "Server" files, of course go on the server side, and "Kindle" files on the kindle. I used cron to schedule the server to update every 3 hours, and the kindle 5 minutes after. Of course that is totally arbitrary. 

The server just needs to schedule "weather-script.sh" (I use apache2 to serve the images)
The kindle just schedules "display-weather.sh"


To change team: Modify line 17 in "weather-script.py" to the 3-letter code of your favorite team.
To change season: Modify line 18 to the correct years.


To keep the Kindle from going into sleep mode, run init-weather.sh
This only needs to be done once, unless the kindle runs out of power. I keep mine plugged in.


To view all the logos, I included a process-svg.sh script which will pre-process the logos (included in the DisplayTeams templates) and add them to the server. Then just run "display-logos.sh" on the kindle side.

**Disclaimers**
I'm sure there are plenty of better ways of doing all of this. I would actually love to know them (I don't have a formal programming background).

Right now it behaves a little screwy in between playoff rounds (like when the next oponent hasn't been determined yet)

The web scraping is dependent on NHL.com's current HTML structure. This may need to be updated for later seasons.

The NHL logos were modified from Wikipedia. I do not claim ownership of them. This project is purely for entertainment purposes and I do not intend to monetize it in any way.



