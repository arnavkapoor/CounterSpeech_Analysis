# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs
import time
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		f = open('exporter_help_text.txt', 'r')
		print f.read()
		f.close()

		return

	try:
		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "convid=","output="))

		tweetCriteria = got.manager.TweetCriteria()
		# outputFileName = "output_got.csv"

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg

			elif opt == '--since':
				tweetCriteria.since = arg

			elif opt == '--until':
				tweetCriteria.until = arg

			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg

			elif opt == '--toptweets':
				tweetCriteria.topTweets = True

			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)

			elif opt == '--near':
				tweetCriteria.near = '"' + arg + '"'

			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--convid':
				tweetCriteria.convid = arg

			elif opt == '--output':
				outputFileName = arg

		# outputFile = codecs.open(outputFileName, "w+", "utf-8")

		# outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

		# print('Searching...\n')

		# def receiveBuffer(tweets):
		# 	for t in tweets:
		# 		outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
		# 	outputFile.flush()
		# 	print('More %d saved on file...\n' % len(tweets))

		try:
			results = got.manager.TweetManager.getTweets(tweetCriteria)
			for each_result in results:
				print("WRITING")
				with open('./output/abusive_hate.txt','a+') as final:
					final.write( str(tweetCriteria.convid) +  "," + str(each_result.id)  + '\n')

		except:
			results = []

		return results

	except arg:
		print('Arguments parser error, try -h' + arg)

	# finally:
	# 	print("WTF")
		# outputFile.close()
		# print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
	main(sys.argv[1:])
