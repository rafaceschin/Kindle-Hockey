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

TEAM='pit'

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


#This will give screwy results at the end of the season, but at that point
# You will be too depressed/happy to mind

def get_team_name(href):
    m = re.search('(?<=team/_/name/).*', href)
    return m.group(0)[:3]

def get_team_record(text):
    record = text.split('(')
    team_record = record[1].split(')')[0]
    return team_record


def get_info(Team, header):
    status = 0 ## status is the state that the site is currently displaying
               ## the next game. 1 == ongoing, 2 == preview
    if header == 'previous':
        tag = 'mod-container mod-game prev'
    else:
        tag = 'mod-container mod-no-footer mod-game current'
    try:
        search_url = str('http://espn.go.com/nhl/team/_/name/'+Team)
        html = urlopen(search_url)
        soup = BeautifulSoup(html, "lxml")
        results = soup.find_all('div', {'class': tag})
        if len(results) >= 1:
            result = results
            status = 1
        else:
            result = soup.find_all('div',
                 {'class': 'mod-container mod-no-footer mod-game current pre'})
            status = 2

        return result, status

    except IndexError:
        return 0

def get_previous(Team):
    table = get_info(Team, 'previous')[0]
    try:
        info = table[0]
        other_team = get_team_name(info.find('a')['href'])
        home_away = info.find_all('div',{'class':'home-away'})
        if home_away[0].get_text() == u'@':
            away = Team
            home = other_team
        else:
            home = Team
            away = other_team

        results = info.find_all('div',{'class':'results'})
        result_text = results[0].get_text().encode('ascii','ignore')
        date = info.get_text()[:9]
        return home, away, date, result_text
    except IndexError:
        return 'pit_alt', 'pit', ':('

def get_next(Team):
    table, status = get_info(Team, 'current')
    try:
        info = table[0]
        home = info.find_all('div',{'class':'team-home'})
        home_team = get_team_name(home[0].find('a')['href'])
        home_record_text = home[0].find('div', {'class':'record'}).get_text()
        home_record = get_team_record(home_record_text)

        away = info.find_all('div',{'class':'team-away'})
        away_team = get_team_name(away[0].find('a')['href'])
        away_record = away[0].find('div', {'class':'record'}).get_text()
        away_record_text = away[0].find('div', {'class':'record'}).get_text()
        away_record = get_team_record(away_record_text)


        date = info.get_text()[0:10]
        if status == 1:
            time = info.find_all('div', {'class':'time'})[0].get_text()

        elif status == 2:
            time = info.get_text()[11:22]

        return home_team, home_record, away_team, away_record, date, time

    except IndexError:
        return 'pit_alt', '0 - 0 - 0', 'pit', '0 - 0 - 0', ':(', ':('


PAST_HOME, PAST_AWAY, PAST_DATE, PAST_SCORE = get_previous(TEAM)
NEXT_HOME, HOME_REC, NEXT_AWAY, AWAY_REC, NEXT_DATE, NEXT_TIME = get_next(TEAM)


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





