from bs4 import BeautifulSoup
import requests
import re
from ..config import log

pattern = '^http(?:s)?:\/\/(?:www\.)?youtube\.com\/channel\/UC[A-Za-z0-9-]+\/about'

def get_page(page):

	if re.match(pattern,page):
		log.info("A regex match for: " + page)

		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3)'}
			pageresult = requests.get(page, headers=headers)
			
			tree = BeautifulSoup(pageresult.content, features = 'lxml')

			attrs = {'class': 'about-description'}

			about = tree.find_all('div', attrs=attrs)

			aboutContent = about[0].find('pre').text
		
			log.info("Returning: " + aboutContent)
			return aboutContent

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
	log.info("Getting youtube pages")
	updates = []
	if users.count() > 0:
		for user in users:
			pageUrl = user['youtube']['proofURL']
			fingerprint = user['youtube'].get('fingerprint', 'missing')
			result = get_page(pageUrl)
			if result is not None:
				valid = compare_result(fingerprint, result)
				log.info("fingerprint: %s valid %s" % (fingerprint, valid))
				user['youtube']['valid'] = valid

				log.info(user['youtube'])
				updates.append(user['youtube'])

		return updates
	else:
		log.info("No youtube users")

	return
