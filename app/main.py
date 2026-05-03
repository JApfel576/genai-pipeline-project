from fastapi import FastAPI, Query
from enum import Enum
from typing import Annotated
import re 
from pydantic import AfterValidator


class DefaultStr(str, Enum):
  URL = "https://news.google.com/search?q=site%3A%20bbc.com&hl=en-US&gl=US&ceid=US%3Aen" 


app = FastAPI()

# Ensure url matches format for google news site search
def check_url(url_input):
  pattern = r"^https?:\/\/news\.google\.com\/search\?q=site(\:|%3A)(?:%20|\s)?[a-z0-9.-]+\.com(&.*)?$"
  url_input=str(url_input)
  value_error_str = f"Malformed input...returning default url: {DefaultStr.URL.value}"
  if not url_input:
    raise ValueError(value_error_str)
  if not re.match(pattern, url_input):
    raise ValueError(value_error_str)
  return True

# Create url from one given for rss feed
def create_url(url_input):
  pattern = r"\.com"
  match = re.search(pattern, url_input)
  idx = match.end()
  insert_str = "/rss"
  return f"{url_input[:idx]}{insert_str}{url_input[idx:]}"

# Check app health
@app.get("/health")
def health_check():
  return {"status": "ok"}

# If url is not provided or without proper format return default
@app.get("/url")
def url_provider(url_input: Annotated[str | None
, AfterValidator(check_url)
, Query(
  description= "Url for google news search"
) ] = None
):
  if check_url(url_input):
    return create_url(url_input)    


print(url_provider(DefaultStr.URL.value))