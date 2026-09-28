from operator import truediv
def extract_url_from_link(link):
    if link.find("http") >= 0:
        start = link.find("://")
        link = link[start+3:]
        start = link.find("/")
        if start >= 0:
            link = link[:start]
        print("link:"+link)
        return link
    else:
        print("Link not found")
        return False

def links_cleaner(links):
    cleaned = set()
    for link in links:
        link = link.get('href').strip()
        print(link)
        if link.find("http") != -1:
            if link.find(".jpg") == -1 and link.find(".png") == -1:
                cleaned.add(link)
    return cleaned
