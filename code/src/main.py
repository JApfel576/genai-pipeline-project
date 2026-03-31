from feedpoller import FeedPoller 
import json

if __name__ == "__main__":
  poller = FeedPoller()
  feed = poller.get_feed()
  print(feed)
  #data = poller.header_entries()
  #data = poller.latest_file()
  #print(data) #.get('etag') 
  #poller.has_changed()
  # poller.write_to_file(data)
  