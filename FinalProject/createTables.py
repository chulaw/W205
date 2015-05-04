#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
conn = sqlite3.connect('cricStats.db')

c = conn.cursor()
c.execute('drop table detailsODIInnings')
c.execute('drop table fowODIInnings')
c.execute('drop table playerInfo')
c.execute('drop table battingODIInnings')
c.execute('drop table bowlingODIInnings')
c.execute('drop table commentaryEventODI')
c.execute('drop table fieldingEventODI')
c.execute('drop table fieldingODIMatch')

c.execute('create table playerInfo (playerId integer unique, player text, fullName text, country text, cid integer)')
c.execute('''create table detailsODIInnings (inningsId integer unique, odiId integer, innings integer, batTeam text, bowlTeam text, extras integer, runs integer, balls integer, minutes integer, wickets integer,
          inningsEndDetail text)''')
c.execute('create table fowODIInnings (fowId integer unique, odiId integer, innings integer, runs integer, wicket integer, player text, balls integer)')
c.execute('''create table battingODIInnings (inningsId integer unique, playerId integer, player text, odiId integer, innings integer, position integer, dismissalInfo text, notOut integer, runs integer,
         minutes integer, balls integer, fours integer, sixes integer, totalPct real, bowlingRating real, entryRuns integer, entryWkts integer, wicketsAtCrease integer, homeAway integer, status integer,
         result integer, rating real)''')
c.execute('''create table bowlingODIInnings (inningsId integer unique, playerId integer, player text, odiId integer, innings integer, position integer, wkts integer, battingRating real, wktsRating real,
          balls integer, maidens integer, runs integer, homeAway integer, status integer, result integer, rating real)''')
c.execute('''create table commentaryEventODI (eventId integer unique, odiId integer, bowler text, batsman text, bowlerId integer, batsmanId integer, commentary text)''')
c.execute('''create table fieldingEventODI (eventId integer unique, odiId integer, bowler text, batsman text, bowlerId integer, batsmanId integer, fielder text, fielderId integer,
             droppedCatch integer, misfield integer, missedStumping integer, greatCatch integer, directHit integer, greatFielding integer, runsSaved integer, commentary text)''')
c.execute('''create table fieldingODIMatch (matchId integer unique, playerId integer, player text, odiId integer, keeper integer, catches integer, droppedCatches integer, misfields integer, stumpings integer, missedStumpings integer,
             greatCatches integer, directHits integer, greatSaves integer, runsSaved integer, rating real)''')
conn.commit()
conn.close()