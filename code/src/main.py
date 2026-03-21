import requests

URL = "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15"

response = requests.get(url=URL)
xml_data = response.content

print(xml_data)