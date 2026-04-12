from feedpoller import FeedPoller 
import json

REUTERS_URL = """
https://news.google.com/rss/search?q=site%3A%20reuters.com&hl=en-US&gl=US&ceid=US%3Aen
""" 

if __name__ == "__main__":
  poller = FeedPoller(REUTERS_URL)
  print(poller.save(poller.get_feed()))
  # feed = poller.get_feed()
  # data = poller.header_entries()
  # has_changed = poller.has_changed(data)
  # if has_changed:
  #   poller.write_to_file(data)