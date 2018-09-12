from bs4 import BeautifulSoup
import requests
import re

pattern = '^http(?:s)?:\/\/(?:www\.)?facebook\.com\/[a-z0-9._-]+\/posts\/[0-9]+(?:\/)?'

def get_page(page):

	if re.match(pattern,page):
		# trim excess url (after the "?")
		if page.find("?") > -1:
			page = page[0: int(page.find("?"))]

		print "A regex match for: " + page

		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3)'}
			pageresult = requests.get(page)
			content = pageresult.content
			tree = BeautifulSoup(content, features = 'lxml')

			comment = tree.select('code#u_0_q')
			comment_data = comment[0].string.encode("utf-8")

			soup = BeautifulSoup(comment_data, 'lxml')
			divs = soup.select('div._5pbx.userContent')

			para = divs[0].select('p')

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
	if fingerprint == page_result:
		return True

	return False

def get_pages(users):
	print "Getting facebook pages"
	if users.count() > 0:
		for user in users:
			pageUrl = user['facebook']['proofURL']
			fingerprint = user['facebook'].get('fingerprint', 'missing')
			result = get_page(pageUrl)
			if result != None:
				valid = compare_result(fingerprint, result)
				print ("fingerprint: %s valid %s" % (fingerprint, valid))
				user['facebook']['valid'] = valid

				print user['facebook']

		return users
	else:
		print "No Facebook users"

	return
