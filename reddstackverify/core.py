from .sites import twitter, reddit, facebook, youtube
import time
import config
from pymongo import MongoClient

clientDB = MongoClient('localhost', 27017)
db = clientDB['socialNetworks']
network_colls = db.networks

log = config.log

def run():
	while True:
		log.info("Running Loop")
		log.info("Processing Youtube Users")
		youtubeUsers = get_network('youtube')
		updates = youtube.get_pages(youtubeUsers)
		update_networks('youtube', updates)

		log.info("Processing Twitter Users")
		twitterUsers = get_network('twitter')
		updates = twitter.get_pages(twitterUsers)
		update_networks('twitter', updates)

		log.info("Processing Reddit Users")
		redditUsers = get_network('reddit')
		updates = reddit.get_pages(redditUsers)
		update_networks('reddit', updates)

		log.info("Processing Facebook Users")
		fbUsers = get_network('facebook')
		updates = facebook.get_pages(fbUsers)
		update_networks('facebook', updates)

		log.info("sleeping 10 mins")
		time.sleep(600)

def get_network(network):
	results = network_colls.find({"network": network})

	return results

def update_networks(network, users):
	log.info("Updating Users")
	log.info("Update count " + str(len(users)))

	for user in users:
		log.info(user["username"] +" & " + str(user["valid"]))
		name = user['username']

		result = network_colls.update({"network": network, "username": name},{'$set': {"valid": user['valid']}})

		log.info('Inserted {0} : {1}'.format(name,user['valid']))
