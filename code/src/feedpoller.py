import requests
import feedparser
from datetime import datetime, timezone
from pathlib import Path
import platform
import json


ITEM_CNT = 15 # item count stays the same
REUTERS_FINANCE_URL = f"""
https://ir.thomsonreuters.com/rss/news-releases.xml?items={ITEM_CNT}
"""
HEADER_KEYS = ['etag','updated', 'updated_parsed', 'href']
ENTRY_KEYS = ['title', 'summary', 'published', 'published_parsed', 'id'
              , 'link']
OUT_PATH = '/code/output/data/'


class FeedPoller():
  def __init__(self, url = REUTERS_FINANCE_URL):
    self.item_cnt = 15
    self.url = url
    self.header_keys = HEADER_KEYS
    self.entry_keys = ENTRY_KEYS
    self.out_path = OUT_PATH
    # Store last seen values. Update to retrieve
    self.last_etag = None 
    self.last_updated = None
    self.last_hash = None 
  
  # Check if feed has changed based on header
  def has_changed(self, feed:dict) -> bool:
    etag = feed.get('etag')
    if etag != self.last_etag:
      return True
    updated = feed.get('updated')
    if updated != self.last_updated:
      return True
    entries = feed.entries
    hash = "".join(e.get('id') for e in entries)
    if hash != self.last_hash:
      return True
    return False

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
    header_entries = {**header_dict, "items":entry_dict}  
    return header_entries
  
  # Get current datetime and format
  def get_now_utc(self) -> str:
    now_utc = datetime.now(timezone.utc)\
      .strftime('%Y%m%d_%H%M%S')
    return now_utc
  
  # format path for windows machine
  def format_path(self):
    cwd = Path.cwd()
    if platform.system() == "Windows":
      cwd = str(cwd).replace('\\', '/')
    return cwd
  
  # create file name using current working dir and current time 
  def create_filename(self, ext='.json'):
    cwd = self.format_path()
    now_utc = self.get_now_utc()
    filename = str(cwd) + self.out_path + now_utc + ext 
    return filename
  
  # Append changes to existing file or create new
  def write_to_file(self, header_entries:dict):
    data = self.header_entries()
    filename = self.create_filename()
    try: 
      with open(filename, 'x') as file:
        json.dump(data, file, indent=4)
        print(f"File written to {filename}")
    except FileExistsError:
        print(f"File could not be written to {filename}")