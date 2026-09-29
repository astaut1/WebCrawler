import bs4
import requests
import tldextract
from bs4 import BeautifulSoup
from collections import deque

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
def links_cleaner(links,domain_name):
    cleaned = set()
    for link in links:
        if link is None:
            continue
        if link.find("http") != -1 and link.find(domain_name) != -1:
            if link.find(".jpg") == -1 and link.find(".png") == -1:
                if link.find("") != -1:
                    link = link.replace(" ", "%20")
                    cleaned.add(link)
    return cleaned

def crawl_one_link(link,domain_name):
    try:
        page = requests.get(link, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        # If the website is down entirely, return an empty list instead of crashing
        print(f"Request failed{e}")
        return []
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("a")
    links = [link.get('href').strip() for link in links]
    cleaned = links_cleaner(links,domain_name)
    return cleaned

def crawl(BASEURL):
    domain_name = tldextract.extract(BASEURL).top_domain_under_public_suffix
    page = requests.get(BASEURL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup.title.string)

    links = soup.find_all('a')
    links = [link.get('href').strip() for link in links]

    links = links_cleaner(links, domain_name)
    base_normalized = normalize_url(BASEURL)
    queue = deque([base_normalized])
    crawled = set()
    for link in links:
        queue.append(link)
    while len(queue) > 0:
        link = queue.popleft()
        if link in crawled:
            continue
        if link is None:
            continue
        crawled.add(link)
        new_links = crawl_one_link(link, domain_name)
        count=0
        for new_link in new_links:
            if new_link not in queue or new_link not in crawled:
                queue.append(new_link)
                count += 1
        print(count)

