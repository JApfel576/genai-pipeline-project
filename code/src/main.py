import requests

URL = "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15"

resp = requests.get(URL)
print(resp)