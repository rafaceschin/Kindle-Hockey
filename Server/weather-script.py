#!/usr/bin/python2

# Kindle Weather Display
# Matthew Petroff (http://www.mpetroff.net/)
# September 2012

import urllib2
from xml.dom import minidom
import datetime
import codecs
from bs4 import BeautifulSoup
from urllib import urlopen
import re

#CHANGE TEAM AND SEASON INFO HERE:

Team='PIT'
Season='20142015'

#
# Download and parse weather data
#

# Fetch data (change lat and lon to desired location)
weather_xml = urllib2.urlopen('http://graphical.weather.gov/xml/SOAP_server/ndfdSOAPclientByDay.php?whichClient=NDFDgenByDay&lat=40.500634230786204&lon=-80.06653856750012&format=24+hourly&numDays=4&Unit=e').read()
dom = minidom.parseString(weather_xml)

# Parse temperatures
xml_temperatures = dom.getElementsByTagName('temperature')
highs = [None]*4
lows = [None]*4
for item in xml_temperatures:
    if item.getAttribute('type') == 'maximum':
        values = item.getElementsByTagName('value')
        for i in range(len(values)):
            highs[i] = int(values[i].firstChild.nodeValue)
    if item.getAttribute('type') == 'minimum':
        values = item.getElementsByTagName('value')
        for i in range(len(values)):
            lows[i] = int(values[i].firstChild.nodeValue)

# Parse icons
xml_icons = dom.getElementsByTagName('icon-link')
icons = [None]*4
for i in range(len(xml_icons)):
    icons[i] = xml_icons[i].firstChild.nodeValue.split('/')[-1].split('.')[0].rstrip('0123456789')

# Parse dates
xml_day_one = dom.getElementsByTagName('start-valid-time')[0].firstChild.nodeValue[0:10]
day_one = datetime.datetime.strptime(xml_day_one, '%Y-%m-%d')

# Get Hockey info

def get_sched(Team, Game_Type, Season):
    try:
        game_type = str(Game_Type)
        search_url =str('http://www.nhl.com/ice/schedulebyseason.htm?season='
                     +Season+'&gameType='+game_type+'&team='+Team)

        html = urlopen(search_url)
        soup = BeautifulSoup(html, "lxml")
        return soup.findAll('table', {'class':'data schedTbl'})
    except IndexError:
        return 0


def get_next_info(table):
    try:
        sched_rows = table.find_all('td')[0:4]
        next_date = sched_rows[0].get_text().encode('ascii').split(' ')[0:3]
        next_date_str = next_date[0] + ' ' + next_date[1] + ' ' + next_date[2][:-1] 
        next_away_str = sched_rows[1].get_text().encode('ascii','ignore')
        next_home_str = sched_rows[2].get_text().encode('ascii','ignore')
        print next_home_str
        next_time = sched_rows[3].get_text().encode('ascii').split(' ')[0:2]
        next_time_str= next_time[0] + ' ' + next_time[1]
        return next_date_str,next_away_str, next_home_str, next_time_str
    except IndexError:
        return 0,0,0,0


def get_past_info(table):
    try:
        past_rows = table.find_all('td')[-6:-1]
        past_date = past_rows[0].get_text().encode('ascii').split(' ')[0:3]
        past_date_str= past_date[0] + ' ' + past_date[1] + ' ' + past_date[2][:-1]
        past_away_str = past_rows[1].get_text().encode('ascii','ignore')
        past_home_str = past_rows[2].get_text().encode('ascii','ignore')
        past_score = past_rows[4].get_text().encode('ascii').split('\n')
        past_score_str= str(past_score[2] + past_score[3] +
                            past_score[4] + ' ' + past_score[5])
        return past_date_str, past_away_str, past_home_str,past_score_str
    except IndexError:
        return 0,0,0,0

pre_season = get_sched(Team, 1, Season)
reg_season = get_sched(Team, 2, Season)
post_season = get_sched(Team, 3, Season)

#This will give screwy results at the end of the season, but at that point
# You will be too depressed/happy to mind
if pre_season == 0:
    PAST_DATE = ':('
    PAST_AWAY = 'Pittsburgh'
    PAST_HOME = 'Pittsburgh_alt'
    PAST_SCORE = 'Waiting on Schedule'
    NEXT_DATE = ':('
    NEXT_AWAY = 'Pittsburgh_alt'
    NEXT_HOME = 'Pittsburgh'
    NEXT_TIME = 'SUMMER' 

elif len(pre_season) == 2: #mid pre season
    NEXT_DATE, NEXT_AWAY, NEXT_HOME, NEXT_TIME = get_next_info(pre_season[0])
    PAST_DATE, PAST_AWAY, PAST_HOME, PAST_SCORE = get_past_info(pre_season[1])

elif len(reg_season) == 2: #mid season
    NEXT_DATE, NEXT_AWAY, NEXT_HOME, NEXT_TIME = get_next_info(reg_season[0])
    PAST_DATE, PAST_AWAY, PAST_HOME, PAST_SCORE = get_past_info(reg_season[1])

elif len(post_season) == 2: #mid post season
    NEXT_DATE, NEXT_AWAY, NEXT_HOME, NEXT_TIME = get_next_info(post_season[0])
    PAST_DATE, PAST_AWAY, PAST_HOME, PAST_SCORE = get_past_info(post_season[1])

elif len(pre_season) == 1 and len(post_season)==0 : #pre-season to reg season
    NEXT_DATE, NEXT_AWAY, NEXT_HOME, NEXT_TIME = get_next_info(reg_season[0])
    PAST_DATE, PAST_AWAY, PAST_HOME, PAST_SCORE = get_past_info(pre_season[0])

elif len(reg_season) == 1 and len(post_season)==1 : #reg season to post season (or in-between rounds)
    NEXT_DATE, NEXT_AWAY, NEXT_HOME, NEXT_TIME = get_next_info(post_season[0])
    PAST_DATE, PAST_AWAY, PAST_HOME, PAST_SCORE = get_past_info(reg_season[0])

else:
    PAST_DATE = ':('
    PAST_AWAY = 'Pittsburgh'
    PAST_HOME = 'Pittsburgh_alt'
    PAST_SCORE = 'Waiting on Schedule'
    NEXT_DATE = ':('
    NEXT_AWAY = 'Pittsburgh_alt'
    NEXT_HOME = 'Pittsburgh'
    NEXT_TIME = 'SUMMER'



record_search=str('http://www.nhl.com/ice/standings.htm?season='
        +Season+'&type=LEA')
html = urlopen(record_search)
soup = BeautifulSoup(html, "lxml")
table = soup.findAll('table', {'class':'data standings League'})

def get_record(team, table):
    try:
        rec_name = table[0].find('a', text=re.compile(team))
        win = rec_name.find_next().find_next().find_next()
        loss = win.find_next()
        ot = loss.find_next()
        return str(win.text.encode('ascii') + '-' +
                      loss.text.encode('ascii') + '-' +
                      ot.text.encode('ascii'))
    except AttributeError:
        return "0 - 0 - 0"

HOME_REC= get_record(NEXT_HOME, table)
AWAY_REC= get_record(NEXT_AWAY, table)


#
# Preprocess SVG
#

# Open SVG to process
output = codecs.open('weather-hockey-prefile.svg', 'r', encoding='utf-8').read()

# Insert icons and temperatures
output = output.replace('ICON_ONE',icons[0])
output = output.replace('ICON_TWO',icons[1])
output = output.replace('HIGH_ONE',str(highs[0]))
output = output.replace('HIGH_TWO',str(highs[1]))
output = output.replace('LOW_ONE',str(lows[0]))
output = output.replace('LOW_TWO',str(lows[1]))

# Insert days of week
one_day = datetime.timedelta(days=1)
days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

output = output.replace('DAY_ONE',days_of_week[(day_one).weekday()])
output = output.replace('DAY_TWO',days_of_week[(day_one + one_day).weekday()])



# Insert Hockey INFO
output = output.replace('N_DATE', str(NEXT_DATE))
output = output.replace('N_TIME', str(NEXT_TIME))
output = output.replace('P_DATE', str(PAST_DATE))
output = output.replace('P_SCORE', str(PAST_SCORE))
output = output.replace('AWAY_REC', str(AWAY_REC))
output = output.replace('HOME_REC', str(HOME_REC))
output = output.replace('N_AWAY', str(NEXT_AWAY))
output = output.replace('N_HOME', str(NEXT_HOME))
output = output.replace('P_AWAY', str(PAST_AWAY))
output = output.replace('P_HOME', str(PAST_HOME))

# Write output
codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)





