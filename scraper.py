import requests
from bs4 import BeautifulSoup
from reddstackverify.config import log

IDENTIFIER = "reddid="

'''
# @params
# url = a string representing a profile URL
# reddid = a string representing the user's ReddID
'''


def scrape(url, reddid):

    page = requests.get(url)

    # Confirm page is valid
    if page.status_code == 404:
        log.info("Error: user profile not found.")
        return 1

    soup = BeautifulSoup(page.text, 'html.parser')
    found_id = None

    for paragraph in soup.find_all('p'):
        if IDENTIFIER in str(paragraph).lower():
            found_id = str(paragraph.get_text())
            # Remove excess bio text, if present
            for item in found_id.split():
                if IDENTIFIER in item.lower():
                    found_id = item
                    break

    if found_id is None:
        log.info("Error: no ID found.")
        return 1

    if reddid not in found_id:
        log.info("Error: ID found does not match input provided.")
        return 1

    return "url=" + url, found_id
