import glob
import csv
import operator 
import matplotlib.pyplot as pl
import numpy as np

stopWords = ['and', 'in', '', 'the', 'will', 'on', 'a', 'by', 'is', 'at', 'for', '-', 'be', 'to', 'has', 'for', 'you', 'of', 'I']
for file in glob.glob("tweets*.csv"):
	reader = csv.reader(open(file,'r').read().splitlines())
	wordCount = {}
	for row in reader:
		if len(row) < 1: continue
		wordSplit = row[0].split(" ")
		print wordSplit
		for word in wordSplit:
			if word in stopWords: continue
			if word in wordCount.keys():
				wordCount[word] += 1
			else: wordCount[word] = 1	

	sortedCount = sorted(wordCount.items(), key=operator.itemgetter(1), reverse=True)
	topCounts = {}
	topStrings = {}
	histKeys = open("histogramKeys.txt", "w")
	for i in range(0, 30):
		topCounts[i] = sortedCount[i][1]
		print `(i+1)` + ": " + sortedCount[i][0]
		histKeys.write(`i` + ": " + sortedCount[i][0])
		topStrings[i] = sortedCount[i][0].decode('utf8')
	histKeys.close()
	print topCounts
	print topStrings
	X = np.arange(len(topCounts))
	pl.bar(X, topCounts.values(), align='center', width=1)
	pl.xticks(X, topCounts.keys(), size='small')	
	ymax = max(topCounts.values()) + 1
	pl.ylim(0, ymax)
	pl.show()
		
