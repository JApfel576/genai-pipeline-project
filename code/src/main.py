import requests
import feedparser

REUTERS_FINANCE_URL = "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15"


# Make request to feed url 
def get_feed(url: str) -> dict:
  try:
    response = requests.get(url=url, timeout=10)
    response.raise_for_status()
    return feedparser.parse(url)
  except requests.RequestException as e:
    print(f"Error fetching feed: {e}")
    return None


def create_dict(key_list: list[str]) -> list:
  new_dict = {k:v for (k,v) in feed.items() if k in key_list}
  return new_dict


feed = get_feed(REUTERS_FINANCE_URL)
key_list = ['etag','updated', 'updated_parsed', 'href'] 
print(create_dict(key_list))

