import requests
import feedparser

ITEM_CNT = 15 # item count stays the same
REUTERS_FINANCE_URL = f"""
https://ir.thomsonreuters.com/rss/news-releases.xml?items={ITEM_CNT}
"""
HEADER_KEYS = ['etag','updated', 'updated_parsed', 'href']
ENTRY_KEYS = ['title', 'summary', 'published', 'published_parsed', 'id'
              , 'link']

class FeedPoller():
  def __init__(self, url = REUTERS_FINANCE_URL):
    self.item_cnt = 15
    self.url = url
    self.header_keys = HEADER_KEYS
    self.entry_keys = ENTRY_KEYS

  # Make request to feed url 
  def get_feed(self) -> dict | None:
    try:
      response = requests.get(self.url, timeout=10)
      response.raise_for_status()
      return feedparser.parse(response.content)
    except requests.RequestException as e:
      print(f"Error fetching feed: {e}")
      return None

  # Extract header details
  def process_header(self, feed: dict, key_list: list[str]) -> dict:
    if not feed.get('bozo'):
      new_dict = {k:v for (k,v) in feed.items() if k in key_list}
    else:
      raise Exception("Feed is marked bozo")
    return new_dict

  # Extract entry details
  def process_entries(self, feed: dict, key_list: list[str]) -> list:
    processed_entries = [
      {key: entry.get(key) for key in key_list}
      for entry in feed.entries
      ]
    return processed_entries

  # Merge headers with entries
  def header_entries(self) -> dict:
    feed = self.get_feed()
    header_dict = self.process_header(feed, self.header_keys)
    entry_dict = self.process_entries(feed, self.entry_keys)
    merged_dict = {**header_dict, "items":entry_dict}  
    return merged_dict