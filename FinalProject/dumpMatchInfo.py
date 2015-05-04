#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
import math
start = time.clock()

# connect to db
conn = sqlite3.connect('cricStats.db')
c = conn.cursor()

# c.execute('drop table odiInfo')
c.execute('''create table odiInfo (odiId integer unique, startDate text, location text, team1 text, team2 text, season text, ground text, ballsPerOver integer, result text, margin text, series text,
          seriesStatus text, scoreLink text)''')

month2Num = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
relativeURL = '/ci/engine/records/team/match_results.html?class=2;id=1971;type=year'
defaultTeamRating = 100.0

# loop through odi matches
for x in range(0, 45):
    # load cricinfo annual match list    
    yearURL = 'http://stats.espncricinfo.com' + relativeURL
    yearPage = requests.get(yearURL)
    yearTree = html.fromstring(yearPage.text)

    data1 = yearTree.xpath('//a[@class="data-link"]/text()')
    data2 = yearTree.xpath('//td[@nowrap="nowrap"]/text()')
    links = yearTree.xpath('//a[@class="data-link"]/@href')
    
    modD2 = []
    # handle forfeits, incomplete matches
    if '1978' in relativeURL or '1987' in relativeURL or '1988' in relativeURL or '1996' in relativeURL or '2001' in relativeURL:
        for k in range(0, len(data2)):
            if 'Nov 3, 1978' in data2[k] or 'Mar 20, 1987' in data2[k] or 'Oct 14, 1988' in data2[k] or 'Mar 13, 1996' in data2[k] or 'Jun 17, 2001' in data2[k]:
                modD2.append('forfeit')
                modD2.append(data2[k])
            else:            
                modD2.append(data2[k])
        data2 = modD2
        
    relativeURL = yearTree.xpath('//a[@class="QuoteSummary"]/@href')
    relativeURL = relativeURL[len(relativeURL)-1]    
    
    groundLinks = []
    scoreLinks = []
    for j in range(0, len(links)):
        if 'match' in links[j]: scoreLinks.append(links[j])
        if 'ground' in links[j]: groundLinks.append(links[j])
    odiNum = int(len(data2) / 2)
    
    i = 0
    teams1 = []
    teams2 = []
    grounds = []
    results = []
    odiIds = []    
    while (i < len(data1)):
        team1 = data1[i]
        team2 = data1[i+1]
        teams1.append(team1)
        teams2.append(team2)                
        odiId = None
        if team1 in data1[i+2] or team2 in data1[i+2]:
            results.append(data1[i+2])
            result = data1[i+2]
            grounds.append(data1[i+3])
            odiIds.append(data1[i+4].split()[2])
            odiId = data1[i+4].split()[2]
            i = i + 5
        else:
            results.append('Tie/NR')
            result = 'Tie/NR'
            grounds.append(data1[i+2])
            odiIds.append(data1[i+3].split()[2])
            odiId = data1[i+3].split()[2]
            i = i + 4
 
    startDates = {}
    locations = {}
    for i in range(0, odiNum):
        margin = data2[2*i]
        startDate = data2[2*i+1]
        month = startDate.split()[0]
        year = startDate.split()[len(startDate.split())-1]
        day = startDate.split()[1].split('-')[0]
        day = day.split(',')[0]
        day = '0' + day if int(day) < 10 else day    
        startDate = year + month2Num[month] + day
        startDates[odiIds[i]] = startDate
        groundURL = 'http://www.espncricinfo.com' + groundLinks[i]
        groundPage = requests.get(groundURL)
        groundTree = html.fromstring(groundPage.text)
        location = groundTree.xpath('(//span[@class="SubnavSubsection"]/text())')[0]
        locations[odiIds[i]] = location
        print('Dumping details for odi #'+repr(odiIds[i])+' '+teams1[i]+' vs '+teams2[i]+', startDate: '+startDate+', result: '+results[i]+', margin: '+margin+', scoreLink: '+scoreLinks[i]+', ground: '+grounds[i]+', location: '+location)
        c.execute('insert or ignore into odiInfo (odiId, startDate, location, team1, team2, ground, result, margin, scoreLink) values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (odiIds[i], startDate, location, teams1[i], teams2[i], grounds[i], results[i], margin, scoreLinks[i]))
        conn.commit()
conn.close()
elapsed = (time.clock() - start)
print('Time elapsed: ' + repr(elapsed) + 'sec')