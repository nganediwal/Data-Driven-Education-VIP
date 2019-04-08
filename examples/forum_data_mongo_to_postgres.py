from statistics import *
import pymongo
import pprint #pretty print
from bson import json_util #handles json
import json, re
from credentials import returns_psql_credentials,returns_mongo_credentials #other script that returns username and password for PSQL and MongoDB access

import psycopg2
PSQL_HOST = "gatechmoocs.cjlu8nfb8vh0.us-east-1.rds.amazonaws.com"
PSQL_PORT = 5432
PSQL_DB = "gatechmoocs"

def psql_connect():
	PSQL_USER, PSQL_PASS = returns_psql_credentials()
	print("Connecting to the PostgreSQL database...")
	conn=None
	try:
		print(PSQL_HOST,PSQL_USER,PSQL_PASS,PSQL_DB)
		conn = psycopg2.connect(host=PSQL_HOST,database=PSQL_DB, user=PSQL_USER, password=PSQL_PASS,port=PSQL_PORT)
		print(conn.get_dsn_parameters(),"\n")
		# create a cursor
		cur = conn.cursor()
		print('PostgreSQL database version:')
		cur.execute('SELECT version()')
		# display the PostgreSQL database server version
		db_version = cur.fetchone()
		print(db_version)
		# close the communication with the PostgreSQL
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
			print('Database connection closed.')
#nltk

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def nltk_sentiment(sentence):
    # tokenized_text=sent_tokenize(sentence)
    nltk_sentiment = SentimentIntensityAnalyzer()
    score = nltk_sentiment.polarity_scores(sentence)
    return score

MONGO_HOST = "34.193.51.227"
MONGO_PORT = 27017
MONGO_DB = "edx"
write=True
def mongo_connect():
	MONGO_USER,MONGO_PASS = returns_mongo_credentials(write)
	print("Connecting to the Mongo database...")
	con = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
	db = con[MONGO_DB]
	db.authenticate(MONGO_USER, MONGO_PASS)

	# print(db)
	# print(db.collection_names(include_system_collections=False))

	#iterate across users/authors/students
	for forum in db.agg_forum.find().limit(5):
		#print the id of author
		pprint.pprint('author_id - '+forum['_id'])
		# pprint.pprint(forum)
		# pprint.pprint(forum['entry'][0])
		# bson_data = str(forum['entry'][0])
		# jsondata = re.sub(r'ObjectId\s*\(\s*\"(\S+)\"\s*\)',r'{"$oid": "\1"}',bson_data)
		# jsondata = re.sub(r'Date\s*\(\s*(\S+)\s*\)',r'{"$date": \1}',jsondata)

		# now we can parse this as JSON, and use MongoDB's object_hook
		# function to get rich Python data structures inside a dictionary
		# data = json.loads(jsondata, object_hook=json_util.object_hook)
		data = json_util.loads(json_util.dumps(forum['entry']))
		num_of_posts = len(data)
		post_length = []
		post_sentiment = []
		net_positive_votes = 0
		net_negative_votes = 0
		all_posts_concat = ''
		for i in range(0,len(data)):
			body = data[i]['body']
			all_posts_concat += body
			post_length.append(len(body))
			post_sentiment.append(nltk_sentiment(body)['compound'])
			net_positive_votes += data[i]['votes']['up_count']
			net_negative_votes += data[i]['votes']['down_count']
		# data = json_util.loads(str(forum['entry']).replace("'", '"'))
		all_posts_tokenize = word_tokenize(all_posts_concat)
		# stopwords = nltk.corpus.stopwords.words('english')
		# word_freq = nltk.FreqDist(all_posts_tokenize)
		# dict_filter = lambda word_freq, stopwords: dict( (word,word_freq[word]) for word in word_freq if word not in stopwords )
		# filtered_word_freq = dict_filter(word_freq, stopwords)

		list_unique_words_no_stop_word = list(set(w.title() for w in all_posts_tokenize if w.lower() not in stopwords.words()))

		unique_words = len(list_unique_words_no_stop_word)
		avg_post_length = mean(post_length)
		avg_post_sentiment = mean(post_sentiment)
		net_votes = net_positive_votes - net_negative_votes
		pprint.pprint('net_votes - '+str(net_votes))
		pprint.pprint('unique_words - '+str(unique_words))
		pprint.pprint('avg_post_sentiment - '+str(avg_post_sentiment))
		pprint.pprint('avg_post_length - '+str(avg_post_length))
		pprint.pprint('num_of_posts - '+str(num_of_posts))
		pprint.pprint('----')
		# pprint.pprint()
		# pprint.pprint(data[0]['body'])
		# print(forum['entry'])

# import re

# REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
# REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

# def sentiment_analysis():
# 	reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
#     reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]    
#     return reviews
if __name__ == '__main__':
    psql_connect()
    # mongo_connect()