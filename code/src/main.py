import requests
import feedparser

URL = "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15"

def get_feed_data(url):
  try:
    response = requests.get(url=url, timeout=10)
    response.raise_for_status()
    return feedparser.parse(url)
  except requests.RequestException as e:
    print(f"Error fetching feed: {e}")
    return None

print(get_feed_data(URL))
  
  # for entry in feed_var.entries:
  #   if entry.title == 'Thomson Reuters Files 2025 Annual Report':
  #   print([k for k in entry])