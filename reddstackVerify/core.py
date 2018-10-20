from .sites import twitter, reddit, facebook, youtube
import time
from pymongo import MongoClient

clientDB = MongoClient('localhost', 27017)
db = clientDB['socialAccounts']
networkColls = db.networks

def run():
	while True:
		print "Running Loop"
		print "Processing Youtube Users"
		youtubeUsers = get_network('youtube')
		updates = youtube.get_pages(youtubeUsers)
		update_networks('youtube', updates)

		print "Processing Twitter Users"
		twitterUsers = get_network('twitter')
		updates = twitter.get_pages(twitterUsers)
		update_networks('twitter', updates)

		print "Processing Reddit Users"
		redditUsers = get_network('reddit')
		updates = reddit.get_pages(redditUsers)
		update_networks('reddit', updates)

		print "Processing Facebook Users"
		fbUsers = get_network('facebook')
		updates = facebook.get_pages(fbUsers)
		update_networks('facebook', updates)

		print "sleeping 10 mins"
		time.sleep(600)

def get_network(network):
	results = networkColls.find({network:{'$exists':1}})

	return results

def update_networks(network, users):
	print ("Updating Users")
	print "Update count " + str(len(users))

	for user in users:
		print user["username"] +" & " + str(user["valid"])
		name = user['username']

		networkColls.update({network + '.username': user['username']},{'$set': {network + '.valid': user['valid']}})
