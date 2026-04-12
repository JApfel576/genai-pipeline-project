from feedpoller import FeedPoller 
import json

REUTERS_URL = """
https://news.google.com/rss/search?q=site%3A%20reuters.com&hl=en-US&gl=US&ceid=US%3Aen
""" 

if __name__ == "__main__":
  poller = FeedPoller(REUTERS_URL)
  changed = poller.poll()
  if changed:
      print("Feed changed — new file saved")
  else:
      print("No change")