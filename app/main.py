from fastapi import FastAPI, Query
from enum import Enum
from typing import Annotated
import re 


class DefaultStr(str, Enum):
  URL = "https://news.google.com/rss/search?q=site%3A%20reuters.com&hl=en-US&gl=US&ceid=US%3Aen" 


app = FastAPI()

@app.get("/health")
def health_check():
  return {"status": "ok"}

# if url is not provided or without proper format return default
@app.get("/url")
def url_provider(url_input: Annotated[str | None
, Query(
  description= "Google News RSS site: url"  
)] = None
):
  pattern = r"^https?:\/\/news\.google\.com\/search\?q=site(\:|%3A)(?:%20|\s)?[a-z0-9.-]+\.com(&.*)?$"
  url_input=str(url_input)
  if url_input and re.match(pattern, url_input):
    return url_input
  return f"Malformed input...returning default url: {DefaultStr.URL.value}"