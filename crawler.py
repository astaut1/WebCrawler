import requests
from bs4 import BeautifulSoup
from crawl_utils import *
import tldextract

URL = "https://ku.edu.np/"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

URL = "https://ku.edu.np/news-app/kathmandu-university-inaugurated-the-thrangu-rinpoche-academia-industry-block?search_category=2&search_school=10&show_on_home=0&search_site_name=kuhome"
URL = "https://www.inspiredtaste.net/"
domain_name = tldextract.extract(URL).top_domain_under_public_suffix

print(domain_name)

page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")
print(soup.title.string)


links = soup.find_all('a')
links = [link.get('href').strip() for link in links]

links = links_cleaner(links,domain_name)
queue = []
crawled = set()
print(len(links))
for link in links:
    queue.append(link)
    # print(link)# = link.get('href')

while len(queue) > 0:
    link = queue.pop(0)
    if link in crawled:
        continue
    if link is None:
        continue
    crawled.add(link)
    new_links = crawl_one_link(link,crawled,domain_name)
    count = 0
    print(len(new_links))
    for new_link in new_links:
        queue.append(new_link)
    print(f"Queue length:{len(queue)}")
    print(f"Crwaled Set Length:{len(crawled)}")
