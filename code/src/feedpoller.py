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
    header_entries = {"header":header_dict, "items":entry_dict}  
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
    filename = self.create_filename()
    try: 
      with open(filename, 'x') as file:
        json.dump(header_entries, file, indent=4)
        print(f"File written to {filename}")
    except FileExistsError:
        print(f"File could not be written to {filename}")

  # create path for files
  def create_path(self): 
    cwd = self.format_path()
    data_path = self.out_path
    relative_path = str(cwd) + data_path
    return relative_path

  # get file name
  def get_files(self):
    relative_path = self.create_path()
    path = Path(relative_path)
    filenames = [file.name for file in path.iterdir()]
    return filenames

  # get latest file data
  def latest_file(self):
    filenames = self.get_files()
    filenames_sorted = sorted(filenames, reverse=True)
    full_path = self.create_path() + filenames_sorted[0]
    try: 
      with open(full_path, 'r') as file:
        latest_file = json.load(file)
        return latest_file
    except FileNotFoundError:
        print(f"File could not be found")
  
  # def update_last(self):
  #   data = self.latest_file()
  #   # Store last seen values. Update to retrieve
  #   try:
  #     self.last_etag = data.get('etag') 
  #     self.last_updated = data.get('last_updated')
  #     self.last_hash = "".join(e.get('id') for e in data)
  #   except KeyError:
  #     print("Key can not be found")

  # # Check if feed has changed based on header
  # def has_changed(self, feed:dict) -> bool:
  #   etag = feed.get('etag')
  #   if etag != self.last_etag:
  #     return True
  #   updated = feed.get('updated')
  #   if updated != self.last_updated:
  #     return True
  #   entries = feed.get('entries')
  #   hash = "".join(e.get('id') for e in entries)
  #   if hash != self.last_hash:
  #     return True
  #   return False