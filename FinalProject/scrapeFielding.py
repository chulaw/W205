#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import lxml.html
from lxml import html
import requests
import sqlite3
start = time.clock()

startODI = int(input('Enter starting match #: '))
# commentary starts from match 1780 onwards
startODI = 1780 if startODI == 0 else startODI

#set PYTHONIOENCODING=utf-8
conn = sqlite3.connect('cricStats.db')
c = conn.cursor()

# get odis info
c.execute('select odiId, startDate, scoreLink from odiInfo')
odisInfo = c.fetchall()
# ignore matches with no commentary data
ignoreDL = (1782, 1783, 1784, 1785, 1786, 1787, 1788, 1790, 1792, 1793, 1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803, 1804, 1806, 1807, 1808, 1810, 1812, 1813, 1814, 1815, 1816,
            1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1846, 1847, 1848, 1849,
            1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879,
            1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890)

droppedCatchWords = ("bobbles the chance", "puts it down", "has made a meal of it", "sitter", "dolly", "spills", "put down", "dropping the ball", "gets both hands to it but drops it", "drops an easy catch", "fails to take the catch", "dropped", "shelled", "grassed")
droppedCatchNonWords = ("dolly on the toes", "dropped right", "dropped with", "dropped just", "dropped it short" , "dropped short", "dropped well in front" , "drops the wrist", "dropped from" , "earlier he was dropped", "dropped his" , "dropped a touch short",
                        "dropped catches" , "dropped behind", "dropped at his feet" , "dropped in", "dropped a bit" , "dropped into", "dropped softly" , "dropped his bat", "dropped catch and" , "dropped it into", "dropped to" , "dropped him earlier",
                        "dropped far too short" , "dropped over", "tough chance", "hard chance", "hard to call it dropped", "hard to call that dropped", "like a football goalkeeper", "desperate effort", "difficult chance", "superb attempt", "good effort",
                        "screaming past", "would have been a very good", "terrific effort", "harsh to blame", "great attempt", "what an effort", "would have been a terrific catch", "would have been a wundercatch", "tough one", "fabulous attempt",
                        "tremendous effort", "difficult one", "would have been a stunner", "would have been a superb", "would have been a mind-blowing", "valiant effort", "harsh to call it", "would have been a classic catch", "would have been a cracker")
misfieldWords = ("fumble", "misfield", "poor fielding", "poor effort", "bad fielding", "makes a mess of it", "not great fielding")
greatCatchWords = ("whattay catch", "what a catch", "stunning catch", "wonderful catch", "times his jump perfectly to take this one-handed", "pulled this off one-handed", "one-handed stunner", "plucks it", "blinder", "top catch", "great catch", "amazing catch", "unbelievable catch", "stupendous catch", "tough catch", "brilliant catch", "tremendous catch", "fantastic catch", "fantastic running catch", "flying catch")
greatFieldingWords = ("fielded!", "great fielding", "good bit of fielding" or "good piece of fielding", "excellent fielding", "saved a boundary", "saved four runs", "saves four runs", "saves three runs", "saved three runs", "brilliant work", "diving stop", "saves a few runs", "saved a few runs", "saves some runs", "saved some runs", "massive dive")
directHitWords = ("direct hit", "accurate with the throw", "throw has beaten him", "hits the stumps direct")
missedStumpingWords = ("missed the stumping", "missed stumping", "stumping missed", "misses a stumping")

# loop through odi matches
for x in range(startODI, len(odisInfo)):
    odiId = odisInfo[x][0]
    startDate = odisInfo[x][1]
    if odiId in ignoreDL:
        continue
    print `odiId` + "\n"

    # store batters and bowlers involved for each team to match with fielder last names in commentary
    c.execute('select player, playerId from bowlingODIInnings where odiId=? and innings=1',(odiId,))
    bowlers1 = c.fetchall()
    bowler1Names = []
    bowler2Id1 = {}

    for i in range(len(bowlers1)):
        bowler1Names.append(bowlers1[i][0])
        bowler2Id1[bowlers1[i][0]] = bowlers1[i][1]

    c.execute('select player, playerId from battingODIInnings where odiId=? and innings=1',(odiId,))
    batsmen1 = c.fetchall()
    batsmen1Names = []
    batsman2Id1 = {}

    for i in range(len(batsmen1)):
        batsmen1Names.append(batsmen1[i][0])
        batsman2Id1[batsmen1[i][0]] = batsmen1[i][1]

    c.execute('select player, playerId from bowlingODIInnings where odiId=? and innings=2',(odiId,))
    bowlers2 = c.fetchall()
    bowler2Names = []
    bowler2Id2 = {}

    for i in range(len(bowlers2)):
        bowler2Names.append(bowlers2[i][0])
        bowler2Id2[bowlers2[i][0]] = bowlers2[i][1]

    c.execute('select player, playerId from battingODIInnings where odiId=? and innings=2',(odiId,))
    batsmen2 = c.fetchall()
    batsmen2Names = []
    batsman2Id2 = {}

    for i in range(len(batsmen2)):
        batsmen2Names.append(batsmen2[i][0])
        batsman2Id2[batsmen2[i][0]] = batsmen2[i][1]

    fielderName = {}
    catches = {}
    droppedCatches = {}
    misfields = {}
    stumpings = {}
    missedStumpings = {}
    greatCatches = {}
    directHits = {}
    greatSaves = {}
    runsSaveds = {}
    fieldingNumCareerMatches = {}
    keeper = {}
    detailedCommentaryCount = 0
    # loop through each of the two innings
    for inn in range(1, 3):
        fieldingURL = 'http://www.espncricinfo.com' + odisInfo[x][2] + '?innings=' + `inn` + ';view=commentary'
        print fieldingURL
        fieldingPage = requests.get(fieldingURL)
        fieldingTree = html.fromstring(fieldingPage.text)

        commentaryEvent = fieldingTree.xpath('(//div[@class="commentary-section"]/div[@class="commentary-event"])')
        overBalls = fieldingTree.xpath('(//div[@class="commentary-section"]/div[@class="commentary-event"]/div[@class="commentary-overs"]/text())')
        commentary = fieldingTree.xpath('(//div[@class="commentary-section"]/div[@class="commentary-event"]/div[@class="commentary-text"])')

        for i in range(len(commentaryEvent)):
            # parse commentary text to usable form
            eventText =  commentaryEvent[i].text_content()
            eventText = eventText.replace("\t\n", "")
            eventText = eventText.replace("\n\t", "")
            eventText = eventText.replace("\t", "")
            eventSplit = eventText.split("\n")
            commentary = ""
            eventBowler = ""
            eventBatsman = ""
            isKeeper = 0
            if len(eventSplit) == 4:
                detailedCommentaryCount =+ 1
                overBalls = eventSplit[0].split(".")
                if overBalls[0] == "": continue
                over = overBalls[0]
                over = `over` if over > 9 else '0' + `over`
                ball = overBalls[1]
                bowlerBatsman = eventSplit[1].replace(",","").split(" to ")
                bowler = bowlerBatsman[0].strip()
                # handle mistypes and name changes for rare specific cases manually
                bowler = "Shamsudeen" if bowler == "Shamshudeen" else bowler
                bowler = "Ahsan Malik" if bowler == "Jamil" else bowler
                bowler = "M'shangwe" if bowler == "Mushangwe" else bowler
                bowlerFI = ""
                if " " in bowler:
                    bowlerFI = bowler.split(" ")[0]
                    bowlerFI = bowlerFI if bowlerFI.isupper() else ""
                    bowler = bowler.split(" ")[1]
                batsman = bowlerBatsman[1].strip()
                batsman = "Mohammad Yousuf" if batsman == "Yousuf Youhana" else batsman
                batsman = "Shamsudeen" if batsman == "Shamshudeen" else batsman
                batsman = "Ahsan Malik" if batsman == "Jamil" else batsman
                batsman = "M'shangwe" if batsman == "Mushangwe" else batsman
                batsman = "Ankur Vasishta" if batsman == "Ankur Sharma" else batsman
                batsman = "Amini" if batsman == "Raho" and odiId == 3541 else batsman
                batsmanFI = ""
                if " " in batsman:
                    batsmanFI = batsman.split(" ")[0]
                    batsmanFI = batsmanFI if batsmanFI.isupper() else ""
                    batsman = batsman.split(" ")[1]
                commentary = eventSplit[3]

                eventId = `odiId` + `inn` + over + `ball`
                if inn == 1:
                    for bowlerName in bowler1Names:
                        if bowler in bowlerName and (bowlerFI == "" or bowlerName[0] in bowlerFI):
                            eventBowler = bowlerName

                    for batsmanName in batsmen1Names:
                        if batsman in batsmanName and (batsmanFI == "" or batsmanName[0] in batsmanFI):
                            eventBatsman = batsmanName

                    if batsmanFI == "JO" and batsman == "Ngoche":
                        eventBatsman = "James Ngoche"
                        batsman2Id1[eventBatsman] = 617385

                    c.execute('insert or ignore into commentaryEventODI (eventId, odiId, bowler, batsman, bowlerId, batsmanId, commentary) values (?, ?, ?, ?, ?, ?, ?)',
                          (eventId, odiId, eventBowler, eventBatsman, bowler2Id1[eventBowler], batsman2Id1[eventBatsman], commentary))
                else:
                    for bowlerName in bowler2Names:
                        if bowler in bowlerName and (bowlerFI == "" or bowlerName[0] in bowlerFI):
                            eventBowler = bowlerName

                    for batsmanName in batsmen2Names:
                        if batsman in batsmanName and (batsmanFI == "" or batsmanName[0] in batsmanFI):
                            eventBatsman = batsmanName

                    if bowlerFI == "JO" and bowler == "Ngoche":
                        eventBowler = "James Ngoche"
                        bowler2Id1[eventBowler] = 617385

                    c.execute('insert or ignore into commentaryEventODI (eventId, odiId, bowler, batsman, bowlerId, batsmanId, commentary) values (?, ?, ?, ?, ?, ?, ?)',
                          (eventId, odiId, eventBowler, eventBatsman, bowler2Id2[eventBowler], batsman2Id2[eventBatsman], commentary))

            else:
                # parse catcher in caught out event
                if ("c " in eventText or "st" in eventText) and "SR:" in eventText:
                    beg = eventText.find("c ") if "c " in eventText else eventText.find("st ")
                    end = eventText.find(" b ")
                    catcherI = ""
                    catcher = ""
                    catcherId = 0
                    catcherEventName = eventText[beg+2:end] if "c " in eventText else eventText[beg+3:end]
                    if u"†" in catcherEventName: isKeeper = 1
                    catcherEventName = catcherEventName.replace(u"†", "")
                    catcherLastName = catcherEventName
                    batsmanEventName = eventText[0:beg].strip()
                    batsmanEventName = batsmanEventName.replace(u"†", "")
                    batsmanLastName = batsmanEventName
                    if " " in catcherLastName:
                        catcherI = catcherLastName.split(" ")[0]
                        catcherI = catcherI if catcherI.isupper() else ""
                        catcherLastNameSplit = catcherLastName.split(" ")
                        catcherLastName = catcherLastNameSplit[1] if len(catcherLastNameSplit) == 2 else catcherLastNameSplit[2]
                    if " " in batsmanLastName:
                        batsmanI = batsmanLastName.split(" ")[0]
                        batsmanI = batsmanI if batsmanI.isupper() else ""
                        batsmanLastNameSplit = batsmanLastName.split(" ")
                        batsmanLastName = batsmanLastNameSplit[1] if len(batsmanLastNameSplit) == 2 else batsmanLastNameSplit[2]
                    if inn == 1:
                        for bowler in bowler1Names:
                            if catcherEventName == bowler:
                                catcher = bowler
                                catcherId = bowler2Id1[bowler]
                        for batsman in batsmen2Names:
                            if catcherEventName == batsman:
                                catcher = batsman
                                catcherId = batsman2Id2[batsman]
                        for batsman in batsmen1Names:
                            if batsmanEventName == batsman:
                                eventBatsman = batsman
                        if catcher == "":
                            for bowler in bowler1Names:
                                bowlerSplit = bowler.split(" ")
                                bowlerSplit = bowler.split("-") if len(bowlerSplit) == 1 else bowlerSplit
                                if len(bowlerSplit) == 1: bowlerSplit.append("")
                                if len(bowlerSplit) == 2: bowlerSplit.append("")
                                if catcherLastName == bowlerSplit[0].strip() or catcherLastName == bowlerSplit[1].strip() or catcherLastName == bowlerSplit[2].strip() and (catcherI == "" or catcherI == bowler[0]):
                                    catcher = bowler
                                    catcherId = bowler2Id1[bowler]
                            for batsman in batsmen2Names:
                                batsmanSplit = batsman.split(" ")
                                batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                                if len(batsmanSplit) == 1: batsmanSplit.append("")
                                if len(batsmanSplit) == 2: batsmanSplit.append("")
                                if catcherLastName == batsmanSplit[0].strip() or catcherLastName == batsmanSplit[1].strip() or catcherLastName == batsmanSplit[2].strip() and (catcherI == "" or catcherI == batsman[0]):
                                    catcher = batsman
                                    catcherId = batsman2Id2[batsman]
                        if eventBatsman == "":
                            for batsman in batsmen1Names:
                                batsmanSplit = batsman.split(" ")
                                batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                                if len(batsmanSplit) == 1: batsmanSplit.append("")
                                if len(batsmanSplit) == 2: batsmanSplit.append("")
                                if batsmanLastName == batsmanSplit[0].strip() or batsmanLastName == batsmanSplit[1].strip() or batsmanLastName == batsmanSplit[2].strip() and (batsmanI == "" or batsmanI == batsman[0]):
                                    eventBatsman = batsman
                    else:
                        for bowler in bowler2Names:
                            if catcherEventName == bowler:
                                catcher = bowler
                                catcherId = bowler2Id2[bowler]
                        for batsman in batsmen1Names:
                            if catcherEventName == batsman:
                                catcher = batsman
                                catcherId = batsman2Id1[batsman]
                        for batsman in batsmen2Names:
                            if batsmanEventName == batsman:
                                eventBatsman = batsman
                        if catcher == "":
                            for bowler in bowler2Names:
                                bowlerSplit = bowler.split(" ")
                                bowlerSplit = bowler.split("-") if len(bowlerSplit) == 1 else bowlerSplit
                                if len(bowlerSplit) == 1: bowlerSplit.append("")
                                if len(bowlerSplit) == 2: bowlerSplit.append("")
                                if catcherLastName == bowlerSplit[0].strip() or catcherLastName == bowlerSplit[1].strip() or catcherLastName == bowlerSplit[2].strip() and (catcherI == "" or catcherI == bowler[0]):
                                    catcher = bowler
                                    catcherId = bowler2Id2[bowler]
                            for batsman in batsmen1Names:
                                batsmanSplit = batsman.split(" ")
                                batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                                if len(batsmanSplit) == 1: batsmanSplit.append("")
                                if len(batsmanSplit) == 2: batsmanSplit.append("")
                                if catcherLastName == batsmanSplit[0].strip() or catcherLastName == batsmanSplit[1].strip() or catcherLastName == batsmanSplit[2].strip() and (catcherI == "" or catcherI == batsman[0]):
                                    catcher = batsman
                                    catcherId = batsman2Id1[batsman]
                        if eventBatsman == "":
                            for batsman in batsmen2Names:
                                batsmanSplit = batsman.split(" ")
                                batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                                if len(batsmanSplit) == 1: batsmanSplit.append("")
                                if len(batsmanSplit) == 2: batsmanSplit.append("")
                                if batsmanLastName == batsmanSplit[0].strip() or batsmanLastName == batsmanSplit[1].strip() or batsmanLastName == batsmanSplit[2].strip() and (batsmanI == "" or batsmanI == batsman[0]):
                                    eventBatsman = batsman

                    if isKeeper == 1: keeper[catcherId] = 1
                    if "c " in eventText:
                        fielderName[catcherId] = catcher
                        catches[catcherId] = catches[catcherId] + 1 if catcherId in catches else 1
                    else:
                        fielderName[catcherId] = catcher
                        stumpings[catcherId] = stumpings[catcherId] + 1 if catcherId in stumpings else 1

            commentary = commentary.replace("'s ", " ")
            commentary = commentary.replace(",", "")
            commentary = commentary.replace(".", "")
            commentary = commentary.replace("!","") if "fielded!" not in commentary else commentary
            commentaryNoCaps = commentary.lower()
            commentarySplit = commentary.split(" ")
            fielder = ""
            fielderId = 0
            droppedCatch = 0
            misfield = 0
            greatCatch = 0
            greatSave = 0
            eventFound = 0
            runsSaved = 0
            directHit = 0
            missedStumping = 0
            # loop through each word in the commentary and look for last names and match with batter and bowler lists
            for word in commentarySplit:
                if len(word) < 2: continue
                if not word[0].isupper(): continue
                if inn == 1:
                    for bowler in bowler1Names:
                        bowlerSplit = bowler.split(" ")
                        bowlerSplit = bowler.split("-") if len(bowlerSplit) == 1 else bowlerSplit
                        if len(bowlerSplit) == 1: bowlerSplit.append("")
                        if len(bowlerSplit) == 2: bowlerSplit.append("")
                        if word == bowlerSplit[0].strip() or word == bowlerSplit[1].strip() or word == bowlerSplit[2].strip():
                            if (fielder == "" or fielder == eventBowler or fielder == eventBatsman) and (bowlerFI == "" or bowlerFI == bowler[0]):
                                fielder = bowler
                                fielderId = bowler2Id1[bowler]
                            wordPos = commentary.find(word)
                            comChunk = commentary[wordPos:]
                            nextSpacePos = comChunk[comChunk.find(" ")+1:].find(" ")
                            nextWord = comChunk[comChunk.find(" ")+1:comChunk.find(" ")+1+nextSpacePos]
                            if nextWord == "": continue
                            if nextWord[0].isupper() and (word + " " + nextWord) == bowler and bowler != eventBatsman and bowler != eventBowler:
                                fielder = bowler
                                fielderId = bowler2Id1[bowler]
                    for batsman in batsmen2Names:
                        batsmanSplit = batsman.split(" ")
                        batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                        if len(batsmanSplit) == 1: batsmanSplit.append("")
                        if len(batsmanSplit) == 2: batsmanSplit.append("")
                        if word == batsmanSplit[0].strip() or word == batsmanSplit[1].strip() or word == batsmanSplit[2].strip():
                            if (fielder == "" or fielder == eventBatsman or fielder == eventBowler) and (batsmanFI == "" or batsmanFI == batsman[0]):
                                fielder = batsman
                                fielderId = batsman2Id2[batsman]
                            wordPos = commentary.find(word)
                            comChunk = commentary[wordPos:]
                            nextSpacePos = comChunk[comChunk.find(" ")+1:].find(" ")
                            nextWord = comChunk[comChunk.find(" ")+1:comChunk.find(" ")+1+nextSpacePos]
                            if nextWord == "": continue
                            if nextWord[0].isupper() and (word + " " + nextWord) == batsman and batsman != eventBatsman and batsman != eventBowler:
                                fielder = batsman
                                fielderId = batsman2Id2[batsman]
                else:
                    for bowler in bowler2Names:
                        bowlerSplit = bowler.split(" ")
                        bowlerSplit = bowler.split("-") if len(bowlerSplit) == 1 else bowlerSplit
                        if len(bowlerSplit) == 1: bowlerSplit.append("")
                        if len(bowlerSplit) == 2: bowlerSplit.append("")
                        if word == bowlerSplit[0].strip() or word == bowlerSplit[1].strip() or word == bowlerSplit[2].strip():
                            if (fielder == "" or fielder == eventBowler or fielder == eventBatsman) and (bowlerFI == "" or bowlerFI == bowler[0]):
                                fielder = bowler
                                fielderId = bowler2Id2[bowler]
                            wordPos = commentary.find(word)
                            comChunk = commentary[wordPos:]
                            nextSpacePos = comChunk[comChunk.find(" ")+1:].find(" ")
                            nextWord = comChunk[comChunk.find(" ")+1:comChunk.find(" ")+1+nextSpacePos]
                            if nextWord == "": continue
                            if nextWord[0].isupper() and (word + " " + nextWord) == bowler and bowler != eventBatsman and bowler != eventBowler:
                                fielder = bowler
                                fielderId = bowler2Id2[bowler]
                    for batsman in batsmen1Names:
                        batsmanSplit = batsman.split(" ")
                        batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                        if len(batsmanSplit) == 1: batsmanSplit.append("")
                        if len(batsmanSplit) == 2: batsmanSplit.append("")
                        if word == batsmanSplit[0].strip() or word == batsmanSplit[1].strip() or word == batsmanSplit[2].strip():
                            if (fielder == "" or fielder == eventBatsman or fielder == eventBowler) and (batsmanFI == "" or batsmanFI == batsman[0]):
                                fielder = batsman
                                fielderId = batsman2Id1[batsman]
                            wordPos = commentary.find(word)
                            comChunk = commentary[wordPos:]
                            nextSpacePos = comChunk[comChunk.find(" ")+1:].find(" ")
                            nextWord = comChunk[comChunk.find(" ")+1:comChunk.find(" ")+1+nextSpacePos]
                            if nextWord == "": continue
                            if nextWord[0].isupper() and (word + " " + nextWord) == batsman and batsman != eventBatsman and batsman != eventBowler:
                                fielder = batsman
                                fielderId = batsman2Id1[batsman]
                if (any(expr in commentaryNoCaps for expr in missedStumpingWords) and "OUT" not in eventSplit[2] and fielder == eventBowler): fielder = "";

            # look for fielding events in commentary and store by fielder
            catches[fielderId] = catches[fielderId] if fielderId in catches else 0
            stumpings[fielderId] = stumpings[fielderId] if fielderId in stumpings else 0
            fielderName[fielderId] = fielder
            droppedCatches[fielderId] = droppedCatches[fielderId] if fielderId in droppedCatches else 0
            misfields[fielderId] = misfields[fielderId] if fielderId in misfields else 0
            missedStumpings[fielderId] = missedStumpings[fielderId] if fielderId in missedStumpings else 0
            greatCatches[fielderId] = greatCatches[fielderId] if fielderId in greatCatches else 0
            directHits[fielderId] = directHits[fielderId] if fielderId in directHits else 0
            greatSaves[fielderId] = greatSaves[fielderId] if fielderId in greatSaves else 0
            runsSaveds[fielderId] = runsSaveds[fielderId] if fielderId in runsSaveds else 0
            if any(expr in commentaryNoCaps for expr in droppedCatchWords) and not any(expr in commentaryNoCaps for expr in droppedCatchNonWords) and ("OUT" not in eventSplit[2]):
                droppedCatch = 1
            if any(expr in commentaryNoCaps for expr in misfieldWords) and ("OUT" not in eventSplit[2]):
                misfield = 1
                if ("1" in eventSplit[2]): runsSaved = -1
                if ("2" in eventSplit[2]): runsSaved = -1
                if ("3" in eventSplit[2]): runsSaved = -1
                if ("FOUR" in eventSplit[2] or "4" in eventSplit[2]): runsSaved = -2
            if any(expr in commentaryNoCaps for expr in greatCatchWords) and ("OUT" in eventSplit[2]):
                greatCatch = 1
            if any(expr in commentaryNoCaps for expr in greatFieldingWords) and not ("not great fielding"  in commentaryNoCaps):
                greatSave = 1
            if any(expr in commentaryNoCaps for expr in directHitWords) and ("OUT" in eventSplit[2]):
                directHit = 1
            if any(expr in commentaryNoCaps for expr in missedStumpingWords) and ("OUT" not in eventSplit[2]):
                missedStumping = 1
            if ("saved a boundary" in commentaryNoCaps) or ("saves three runs" in commentaryNoCaps) or ("saved three runs" in commentaryNoCaps):
                runsSaved = 3
            elif ("saved four runs" in commentaryNoCaps) or ("saves four runs" in commentaryNoCaps):
                runsSaved = 4
            elif ("saved two runs" in commentaryNoCaps) or ("saves two runs" in commentaryNoCaps) or ("saves a couple" in commentaryNoCaps) or ("saves a couple" in commentaryNoCaps) or ("saved at least two" in commentaryNoCaps):
                runsSaved = 2
            elif ("saved a single" in commentaryNoCaps) or ("saves a single" in commentaryNoCaps) or ("saves a run" in commentaryNoCaps) or ("saved a run" in commentaryNoCaps):
                runsSaved = 1
            if greatSave == 1 and runsSaved == 0: runsSaved = 2
            if droppedCatch == 1 and fielder == "" and "bowler" in commentaryNoCaps: fielder = eventBowler
            if "substitute" in commentaryNoCaps: fielder = ""
            # store each fielder event in match with detail
            if eventFound == 0 and fielder != "" and fielder != eventBatsman and (droppedCatch == 1 or misfield == 1 or missedStumpings == 1 or greatCatch == 1 or directHit == 1 or greatSave == 1):
                eventFound = 1
                print eventSplit
                droppedCatches[fielderId] += droppedCatch
                misfields[fielderId] += misfield
                missedStumpings[fielderId] += missedStumping
                greatCatches[fielderId] += greatCatch
                directHits[fielderId] += directHit
                greatSaves[fielderId] += greatSave
                runsSaveds[fielderId] += runsSaved
                if inn == 1:
                    c.execute('insert or ignore into fieldingEventODI (eventId, odiId, bowler, batsman, bowlerId, batsmanId, fielder, fielderId, droppedCatch, misfield, missedStumping,'
                              'greatCatch, directHit, greatFielding, runsSaved, commentary) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (eventId, odiId, eventBowler, eventBatsman, bowler2Id1[eventBowler], batsman2Id1[eventBatsman], fielder, fielderId, droppedCatch, misfield, missedStumping,
                             greatCatch, directHit, greatSave, runsSaved, commentary))
                else:
                    c.execute('insert or ignore into fieldingEventODI (eventId, odiId, bowler, batsman, bowlerId, batsmanId, fielder, fielderId, droppedCatch, misfield, missedStumping,'
                              'greatCatch, directHit, greatFielding, runsSaved, commentary) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (eventId, odiId, eventBowler, eventBatsman, bowler2Id2[eventBowler], batsman2Id2[eventBatsman], fielder, fielderId, droppedCatch, misfield, missedStumping,
                             greatCatch, directHit, greatSave, runsSaved, commentary))

    if detailedCommentaryCount == 0: continue
    if 0 in catches: del catches[0]
    # store aggregated events by fielder for the match
    for fielderId in catches.keys():
        stumpings[fielderId] = 0 if fielderId not in stumpings else stumpings[fielderId]
        missedStumpings[fielderId] = 0 if fielderId not in missedStumpings else missedStumpings[fielderId]
        greatCatches[fielderId] = 0 if fielderId not in greatCatches else greatCatches[fielderId]
        directHits[fielderId] = 0 if fielderId not in directHits else directHits[fielderId]
        runsSaveds[fielderId] = 0 if fielderId not in runsSaveds else runsSaveds[fielderId]
        droppedCatches[fielderId] = 0 if fielderId not in droppedCatches else droppedCatches[fielderId]
        misfields[fielderId] = 0 if fielderId not in misfields else misfields[fielderId]
        greatSaves[fielderId] = 0 if fielderId not in greatSaves else greatSaves[fielderId]
        if greatCatches[fielderId] > 0 and catches[fielderId] < greatCatches[fielderId]: catches[fielderId] = greatCatches[fielderId]
        rating = catches[fielderId] + stumpings[fielderId]  - missedStumpings[fielderId] * 20 + greatCatches[fielderId] * 20 + directHits[fielderId] * 20 + runsSaveds[fielderId] - droppedCatches[fielderId] * 20
        if rating == 0: continue
        print fielderName[fielderId] + " " + `rating`
        matchId = repr(int(odiId)) + repr(fielderId)
        c.execute('insert or ignore into fieldingODIMatch (matchId, playerId, player, odiId, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatSaves, runsSaved, '
                  'rating) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (matchId, fielderId, fielderName[fielderId], odiId, (1 if fielderId in keeper else 0), catches[fielderId], droppedCatches[fielderId], misfields[fielderId], stumpings[fielderId], missedStumpings[fielderId],
                  greatCatches[fielderId], directHits[fielderId], greatSaves[fielderId], runsSaveds[fielderId], rating))
    conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'