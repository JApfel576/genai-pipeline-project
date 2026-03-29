from feedpoller import FeedPoller 
import json

if __name__ == "__main__":
  poller = FeedPoller()
  now_utc = poller.get_now_utc()
  data = poller.header_entries()
  poller.write_to_file(data)