from bs4 import BeautifulSoup
import requests
import re

pattern = '^http(?:s)?:\/\/(?:www\.)?reddit\.com\/r\/verifyreddid\/comments\/[a-z0-9]{6,}\/[a-z0-9]{2,}(?:\/)?'

def get_page(page):

	if re.match(pattern,page):
		print "A regex match for: " + page

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
		
			print "Returning: " + title
			return title

		except Exception as e:
			print ("Could not retrieve %s. %s. Skipping." % (page, str(e)))
			return

	else:
		print "no regex match for: " + page
		return

def compare_result(fingerprint, page_result):
	print ("Comparing fingerprint: %s with page_reults: %s" % (fingerprint,page_result))
	if fingerprint == page_result:
		return True

	return False

def get_pages(users):
	print "Getting reddit pages"
	updates = []
	if users.count() > 0:
		for user in users:
			pageUrl = user['reddit']['proofURL']
			fingerprint = user['reddit'].get('fingerprint', 'missing')
			result = get_page(pageUrl)
			if result != None:
				valid = compare_result(fingerprint, result)
				print ("fingerprint: %s valid %s" % (fingerprint, valid))
				user['reddit']['valid'] = valid

				print user['reddit']
				updates.append(user['reddit'])

		return updates
	else:
		print "No reddit users"

	return
