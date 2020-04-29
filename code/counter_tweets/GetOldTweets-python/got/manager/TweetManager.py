import urllib,urllib2,json,re,datetime,sys,cookielib
from .. import models
from pyquery import PyQuery
import time,random
import socket
import socks

class TweetManager:

	def __init__(self):
		pass

	@staticmethod
	def getTweets(tweetCriteria, receiveBuffer=None, bufferLength=100, proxy=None):
		refreshCursor = ''

		results = []
		resultsAux = []
		cookieJar = cookielib.CookieJar()

		if hasattr(tweetCriteria, 'username') and (tweetCriteria.username.startswith("\'") or tweetCriteria.username.startswith("\"")) and (tweetCriteria.username.endswith("\'") or tweetCriteria.username.endswith("\"")):
			tweetCriteria.username = tweetCriteria.username[1:-1]

		active = True
		print(time.time())
		# tm = 3*random.random() + 1
		# time.sleep(tm)
		while active:
			json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy)
			if len(json['items_html'].strip()) == 0:
				break

			refreshCursor = json['min_position']
			scrapedTweets = PyQuery(json['items_html'])
			#Remove incomplete tweets withheld by Twitter Guidelines
			scrapedTweets.remove('div.withheld-tweet')
			tweets = scrapedTweets('div.js-stream-tweet')

			if len(tweets) == 0:
				break

			for tweetHTML in tweets:
				tweetPQ = PyQuery(tweetHTML)
				tweet = models.Tweet()

				# print(tweetPQ)
				# print("----------------- NEXT -----------")
				# continue
				usernameTweet = tweetPQ("span:first.username.u-dir b").text()
				txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))
				retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
				favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
				dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))

				id = tweetPQ.attr("data-tweet-id")
				try:
					convid = tweetPQ.attr("data-conversation-id")
					if tweetCriteria.convid != convid:
						# print(convid)
						continue

				except:
					continue

				permalink = tweetPQ.attr("data-permalink-path")

				geo = ''
				geoSpan = tweetPQ('span.Tweet-geo')
				if len(geoSpan) > 0:
					geo = geoSpan.attr('title')

				tweet.id = id
				tweet.permalink = 'https://twitter.com' + permalink
				tweet.username = usernameTweet
				tweet.text = txt
				tweet.date = datetime.datetime.fromtimestamp(dateSec)
				tweet.retweets = retweets
				tweet.favorites = favorites
				tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
				tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
				tweet.geo = geo



				# if(tweet.username != "ShailenyWoodley"):
				# print(tweetPQ)
				#print("---NEXT---")

				results.append(tweet)
				resultsAux.append(tweet)

				if receiveBuffer and len(resultsAux) >= bufferLength:
					receiveBuffer(resultsAux)
					resultsAux = []

				if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:
					active = False
					break


		if receiveBuffer and len(resultsAux) > 0:
			receiveBuffer(resultsAux)

		return results

	@staticmethod
	def getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy="127.0.0.1:8118"):
		url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

		urlGetData = ''

		if hasattr(tweetCriteria, 'username'):
			urlGetData += ' to:' + tweetCriteria.username

		if hasattr(tweetCriteria, 'querySearch'):
			urlGetData += ' ' + tweetCriteria.querySearch

		if hasattr(tweetCriteria, 'near'):
			urlGetData += "&near:" + tweetCriteria.near + " within:" + tweetCriteria.within

		if hasattr(tweetCriteria, 'since'):
			urlGetData += ' since:' + tweetCriteria.since

		if hasattr(tweetCriteria, 'until'):
			urlGetData += ' until:' + tweetCriteria.until


		if hasattr(tweetCriteria, 'topTweets'):
			if tweetCriteria.topTweets:
				url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"


		url = url % (urllib.quote(urlGetData), urllib.quote(refreshCursor))

		headers = [
			('Host', "twitter.com"),
			('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"),
			('Accept', "application/json, text/javascript, */*; q=0.01"),
			('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
			('X-Requested-With', "XMLHttpRequest"),
			('Referer', url),
			('Connection', "keep-alive")
		]


		# if proxy:
		# 	# proxy_support = urllib2.ProxyHandler({"http" : ""})
		# 	opener = urllib2.build_opener(urllib2.ProxyHandler({'https': proxy}), urllib2.HTTPCookieProcessor(cookieJar))
		# else:
		# 	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		# opener.addheaders = headers

		try:
			# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 8080)
			# socket.socket = socks.socksocket
			opener = urllib2.build_opener()
			opener.addheaders = headers
			response = opener.open(url)
			jsonResponse = response.read()

		except:
			temp = socket.socket
			# ipcheck_url = 'http://checkip.amazonaws.com/'

			# Actual IP.
			# print(urllib2.urlopen(ipcheck_url).read())

			# Tor IP.
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
			socket.socket = socks.socksocket
			print("TOR")
			# print(urllib2.urlopen(ipcheck_url).read())

			try:
				opener = urllib2.build_opener()
				opener.addheaders = headers
				response = opener.open(url)
				jsonResponse = response.read()
				# socket.socket=temp

			except:
				# time.sleep(300)
				print "Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" % urllib.quote(urlGetData)
				with open('./output/missed.txt','a+') as final:
						final.write( str(tweetCriteria.convid) + '\n')

				print(tweetCriteria.convid)
				time.sleep(random.random() * 15)
				# sys.exit()
				socket.socket=temp

				return

		dataJson = json.loads(jsonResponse)

		return dataJson
