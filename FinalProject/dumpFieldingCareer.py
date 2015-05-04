#!/usr/bin/env python
from datetime import date
import sqlite3
import math

# connect to db
conn = sqlite3.connect('cricStats.db')
c = conn.cursor()

#c.execute('drop table fieldingODICareer')
c.execute('''create table fieldingODICareer (startDate date, endDate date, playerId integer unique, player text, odis integer, keeper integer, catches integer, droppedCatches integer, misfields integer,
            stumpings integer, missedStumpings integer, greatCatches integer, directHits integer, greatFieldings integer, runsSaved integer, matPerCatch real, matPerDrop real, dropRate real, matPerRunSaved real,
            matPerMisfield real, stumpRate real, matPerGreatCatch real, matPerDirectHit real, matPerGreatFielding real, rating real)''')

# loop through each player and his fielding events and aggregate
c.execute('select playerId, player, country from playerInfo')
for player in c.fetchall():
    country = player[2]
    if country == "United Arab Emirates": country = "U.A.E."
    if country == "United States of America": country = "U.S.A."
    if country == "Papua New Guinea": country = "P.N.G."
    if player[1] == "Dale Steyn": country = "South Africa"
    if player[1] == "Morne Morkel": country = "South Africa"
    #print player[1]
    startDate = ""
    endDate = ""

    c.execute('select odiId, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatSaves, runsSaved, rating from fieldingODIMatch where playerId=?',(player[0], ))
    numMat = 0
    keeping = 0
    firstODI = 99999
    lastODI = 0
    catches = 0
    droppedCatches = 0
    misfields = 0
    stumpings = 0
    missedStumpings = 0
    greatCatches = 0
    directHits = 0
    greatFieldings = 0
    runsSaved = 0
    rating = 0
    for fieldingMatch in c.fetchall():
        if fieldingMatch[0] < firstODI: firstODI = fieldingMatch[0]
        if fieldingMatch[0] > lastODI: lastODI = fieldingMatch[0]
        numMat += 1
        keeping += fieldingMatch[1]
        catches += fieldingMatch[2]
        droppedCatches += fieldingMatch[3]
        misfields += fieldingMatch[4]
        stumpings += fieldingMatch[5]
        missedStumpings += fieldingMatch[6]
        greatCatches += fieldingMatch[7]
        directHits += fieldingMatch[8]
        greatFieldings += fieldingMatch[9]
        runsSaved += fieldingMatch[10]
        rating += fieldingMatch[11]
    dropRate = float(droppedCatches) / float(droppedCatches + catches) if (droppedCatches + catches) > 0 else None
    stumpRate = float(stumpings) / float(stumpings + missedStumpings) if (stumpings + missedStumpings) > 0 else None
    keepRate = float(keeping) / float(numMat) if numMat > 0 else None
    matPerCatch = float(numMat) / float(catches) if catches > 0 else None
    matPerRunSaved = float(numMat) / float(runsSaved) if runsSaved > 0 else None
    matPerDrop = float(numMat) / float(droppedCatches) if droppedCatches > 0 else None
    matPerMisfield = float(numMat) / float(misfields) if misfields > 0 else None
    matPerGreatCatch = float(numMat) / float(greatCatches) if greatCatches > 0 else None
    matPerDirectHit = float(numMat) / float(directHits) if directHits > 0 else None
    matPerGreatFielding = float(numMat) / float(greatFieldings) if greatFieldings > 0 else None
    rating = rating * 25 / numMat if numMat > 0 else None
    # discount rating for those that have played <100 odis
    if numMat < 100 and numMat >= 50 and rating != None: rating = rating * math.exp(-float(100-numMat)/100)
    if numMat < 50 and numMat >= 25 and rating != None: rating = rating * math.exp(-float(100-numMat)/50)
    if numMat < 25 and rating != None: rating = rating * math.exp(-float(100-numMat)/25)
    if numMat < 10 and rating != None: rating = rating * math.exp(-float(100-numMat)/12.5)

    c.execute('select startDate from odiInfo where odiId=?',(firstODI, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from odiInfo where odiId=?',(lastODI, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]

    # rudimentary ratings formula to rate fielder careers
    if rating != None and rating > 0: rating = rating + rating * float(numMat) / 50
    keeper = 1 if keepRate > 0.5 else 0
    # drop rate bonus:
    rating = rating + (1 - dropRate) * 200 if not dropRate == None else rating

    c.execute('''insert or ignore into fieldingODICareer (startDate, endDate, playerId, player, odis, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatFieldings,
                runsSaved, matPerCatch, matPerDrop, dropRate, matPerRunSaved, matPerMisfield, stumpRate, matPerGreatCatch, matPerDirectHit, matPerGreatFielding, rating)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], numMat, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatFieldings, runsSaved, matPerCatch, matPerDrop,
               dropRate, matPerRunSaved, matPerMisfield, stumpRate, matPerGreatCatch, matPerDirectHit, matPerGreatFielding, rating))

conn.commit()
conn.close()