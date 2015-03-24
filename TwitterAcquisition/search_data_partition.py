import tweepy
import json
import sys
import datetime
import signal
import urllib

consumer_key = "WbhvAAgT8qdgwgnj4Ah2HPANh";
consumer_secret = "cFZrH4bdwvgJaiTZwxxCUK8dr8JNFAXQNCIWNVyEm1lP2yP4R1";

access_token = "86446655-gqB4EWTHkbrAH0MVQsJG0eQMpW9ZRzf17scF5x3qs";
access_token_secret = "uqbF7Yc9zo1LWNrHTi4aW2V8W6uiRld0YvZGhe4wIgR3v";

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,timeout=100)

xsdDatetimeFormat = "%Y-%m-%dT%H:%M:%S"
xsdDateFormat = "%Y-%m-%d"

def datetime_partition(start,end,duration):
   current = start
   while start==current or (end-current).days > 0 or ((end-current).days==0 and (end-current).seconds>0):
      yield current
      current = current + duration
      
def date_partition(start,end):
   return datetime_partition(start,end,datetime.timedelta(days=1))

prefix = sys.argv[1]
q = sys.argv[2]
start = datetime.datetime.strptime(sys.argv[3], xsdDateFormat)
end = datetime.datetime.strptime(sys.argv[4], xsdDateFormat)

class TweetSerializer:
	out = None
	first = True
	def start(self,date):
		fname = prefix + "-" + date.strftime(xsdDateFormat)+".csv"
		self.out = open(fname,"w")
		self.first = True

	def end(self):
		if self.out is not None:
			self.out.close()
		self.out = None

	def write(self,tweet):
		if not self.first:
			self.out.write(",\n")
		self.first = False
		self.out.write(tweet.encode('utf8'))

output = TweetSerializer()

def interrupt(signum, fname):
	print "Interrupted, closing ..."
	if output is not None:
		output.end()
	exit(1)

signal.signal(signal.SIGINT, interrupt)

for current in date_partition(start,end):
	currentEnd = current + datetime.timedelta(days=1)
	query = urllib.quote_plus(q) + " since:"+current.strftime(xsdDateFormat)+" until:"+currentEnd.strftime(xsdDateFormat)
	print query

	output.start(current)
	
	for tweet in tweepy.Cursor(api.search,q=query).items():
		sys.stdout.write(".")
		output.write(tweet.text)
	sys.stdout.write("\n")
	output.end()	
