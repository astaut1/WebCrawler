import bs4
import requests
import tldextract
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin, urlparse, urlunparse


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
def links_cleaner(links,base_url,domain_name):
    cleaned = set()
    for link in links:
        if link is None:
            continue
        if not link or link.startswith(('javascript:', 'mailto:', 'tel:')):
            continue

        absolute_url = urljoin(base_url, link)
        normalized = normalize_url(absolute_url)

        if not normalized:
            continue
        if "itr_print" in normalized.lower():
            continue

        extracted = tldextract.extract(normalized)
        target_domain = f"{extracted.domain}.{extracted.suffix}"

#Only accepts if the target domain is the same as the domain_name and is not a file
        if target_domain == domain_name:
            lower_url = normalized.lower()
            if not any(lower_url.endswith(ext) for ext in ['.jpg', '.png', '.jpeg', '.pdf', '.zip', '.css', '.js']):
                normalized = normalized.replace(" ", "%20")
                cleaned.add(normalized)
    return cleaned

def normalize_url(link):
    parsed = urlparse(link)
#Only URLs with http or https schemes are accepted
    if parsed.scheme not in ('https','http'):
        return None
#URL Query and Fragments are not used
    normalized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc.lower(),
        parsed.path.rstrip('/') if parsed.path != '/' else '/',
        parsed.params,
        '',
        '')
    )
    return normalized

def crawl_one_link(link,domain_name):
    try:
        page = requests.get(link, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        # If the website is down entirely, return an empty list instead of crashing
        print(f"Request failed{e}")
        return []
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    text = soup.get_text()
    links = []
    for tag in soup.find_all("a"):
        href = tag.get('href')
        if href:
            links.append(href.strip())
    cleaned = links_cleaner(links,link,domain_name)
    return cleaned

def crawl(baseurl):
    domain_name = tldextract.extract(baseurl).top_domain_under_public_suffix
    base_normalized = normalize_url(baseurl)
    queue = deque([base_normalized])
    #seen set used for faster "in" check
    seen = {base_normalized}
    crawled = set()

    try:
        page = requests.get(base_normalized, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        if soup.title and soup.title.string:
            print(f"Starting Crawl: {soup.title.string.strip()}")
    except Exception as e:
        print(f"Failed to load base URL: {e}")
        return

    while queue:
        link = queue.popleft()

        crawled.add(link)

        new_links = crawl_one_link(link, domain_name)
        count=0
        for new_link in new_links:
            if new_link not in seen:
                seen.add(new_link)
                queue.append(new_link)
                count += 1
                if count == 1:
                    print(f"adding 1 link:{new_link} ")
        print(f" -> Added {count} new links to queue (Queue size: {len(queue)}, Crawled Size: {len(crawled)})")

#def crawl_with_sitemap(URL):
