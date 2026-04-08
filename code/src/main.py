from feedpoller import FeedPoller 
import json

if __name__ == "__main__":
  poller = FeedPoller()
  feed = poller.get_feed()
  data = poller.header_entries()
  has_changed = poller.has_changed(data)
  if has_changed:
    poller.write_to_file(data)
