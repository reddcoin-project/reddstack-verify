from bs4 import BeautifulSoup
import requests
import re

pattern = '^http(?:s)?:\/\/(?:www\.)?twitter\.com\/([a-zA-Z0-9_]+\/status)\/[0-9]+(?:\/)?'

def get_page(page):

	if re.match(pattern,page):
		print "A regex match for: " + page

		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3)'}
			pageresult = requests.get(page)
			pageresult = requests.get(page)
			content = pageresult.content
			tree = BeautifulSoup(content, features = 'lxml')

			tweet = tree.find_all('div', attrs={'class':'js-tweet-text-container'})
			para = tweet[0].select('p')

			print "Returning: " + para[0].getText()
			return para[0].getText()
		except Exception as e:
			print ("Could not retrieve %s. %s. Skipping." % (page, str(e)))
			return
	else:
		print "no regex match for: " + page
		return

def compare_result(fingerprint, page_result):
	print ("Comparing fingerprint: %s with page_reults: %s" % (fingerprint,page_result))
	if page_result.find(fingerprint) > -1:
		return True

	return False

def get_pages(users):
	print "Getting twitter pages"

	updates = []
	if users.count() > 0:
		for user in users:
			if 'proofURL' in user['twitter']:
				pageUrl = user['twitter']['proofURL']
				fingerprint = user['twitter'].get('fingerprint', 'missing')		
			result = get_page(pageUrl)
			if result != None:
				valid = compare_result(fingerprint, result)
				print ("fingerprint: %s valid %s" % (fingerprint, valid))
				user['twitter']['valid'] = valid

				print user['twitter']
				updates.append(user['twitter'])

		return updates
	else:
		print "No twitter users"

	return

