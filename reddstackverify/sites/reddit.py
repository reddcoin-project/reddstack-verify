from bs4 import BeautifulSoup
import requests
import re
from ..config import log

pattern = '^http(?:s)?:\/\/(?:www\.)?reddit\.com\/r\/verifyreddid\/comments\/[a-z0-9]{6,}\/[a-z0-9]{2,}(?:\/)?'

def get_page(page):

	if re.match(pattern,page):
		log.info("A regex match for: " + page)

		# we need to use the old reddit to make life easy
		# sub www -> old

		page = page.replace('www','old')

		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3)'}
			pageresult = requests.get(page, headers=headers)
			
			tree = BeautifulSoup(pageresult.content, features = 'lxml')

			attrs = {'class': 'thing', 'data-domain': 'self.verifyreddid'}

			posts = tree.find_all('div', attrs=attrs)

			title = posts[0].find('a', class_="title").text
		
			log.info("Returning: " + title)
			return title

		except Exception as e:
			log.info("Could not retrieve %s. %s. Skipping." % (page, str(e)))
			return

	else:
		log.info("no regex match for: " + page)
		return

def compare_result(fingerprint, page_result):
	log.info("Comparing fingerprint: %s with page_reults: %s" % (fingerprint,page_result))
	if fingerprint == page_result:
		return True

	return False

def get_pages(users):
	log.info("Getting reddit pages")
	updates = []
	if users.count() > 0:
		for user in users:
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
		log.info("No reddit users")

	return
