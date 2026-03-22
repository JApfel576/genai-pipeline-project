import requests
import feedparser

REUTERS_FINANCE_URL = "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15"


# Make request to feed url 
def get_feed(url):
  try:
    response = requests.get(url=url, timeout=10)
    response.raise_for_status()
    return feedparser.parse(url)
  except requests.RequestException as e:
    print(f"Error fetching feed: {e}")
    return None

# ['bozo', 'entries', 'feed', 'headers', 'etag', 'updated', 'updated_parsed', 'href', 'status', 'encoding', 'version', 'namespaces']
feed = get_feed(REUTERS_FINANCE_URL)
print(feed['headers'])
# feed['bozo'], feed['feed'], feed['headers']

# entry keys 
# ['title', 'title_detail', 'links', 'link', 'summary', 'summary_detail', 'published', 'published_parsed', 'authors', 'author', 'author_detail', 'id', 'guidislink']  
# for entry in feed.entries:
#     if entry.title == 'Thomson Reuters Files 2025 Annual Report':
#       print([k for k in entry])