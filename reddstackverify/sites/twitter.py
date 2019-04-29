from bs4 import BeautifulSoup
import requests
import re
from ..config import log

pattern = '^http(?:s)?:\/\/(?:www\.)?twitter\.com\/([a-zA-Z0-9_]+\/status)\/[0-9]+(?:\/)?'

def get_page(page):

	if re.match(pattern,page):
		log.info("A regex match for: " + page)

		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3)'}
			pageresult = requests.get(page)
			pageresult = requests.get(page)
			content = pageresult.content
			tree = BeautifulSoup(content, features = 'lxml')

			tweet = tree.find_all('div', attrs={'class':'js-tweet-text-container'})
			para = tweet[0].select('p')

			log.info("Returning: " + para[0].getText())
			return para[0].getText()
		except Exception as e:
			log.info("Could not retrieve %s. %s. Skipping." % (page, str(e)))
			return
	else:
		log.info("no regex match for: " + page)
		return

def compare_result(fingerprint, page_result):
	log.info("Comparing fingerprint: %s with page_reults: %s" % (fingerprint,page_result))
	if page_result.find(fingerprint) > -1:
		return True

	return False

def get_pages(users):
	log.info("Getting twitter pages")

	updates = []
	if users.count() > 0:
		for user in users:
			if 'proofURL' in user:
				pageUrl = user['proofURL']
				fingerprint = user.get('fingerprint', 'missing')
			result = get_page(pageUrl)
			if result != None:
				valid = compare_result(fingerprint, result)
				log.info("fingerprint: %s valid %s" % (fingerprint, valid))
				user['valid'] = valid

				log.info(user)
				updates.append(user)

		return updates
	else:
		log.info("No twitter users")

	return

