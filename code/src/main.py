from feedpoller import FeedPoller 
import json

if __name__ == "__main__":
  f = FeedPoller()
  data = f.header_entries()
  print(json.dumps(data, indent=2))