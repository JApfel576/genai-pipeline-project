from fastapi import FastAPI
from enum import Enum


class DefaultStr(str, Enum):
  URL = "https://news.google.com/rss/searchq=site%3A%20reuters.com&hl=en-US&gl=US&ceid=US%3Aen" 


app = FastAPI()

@app.get("/health")
def health_check():
  return {"status": "ok"}

@app.get("/url")
@app.get("/url/{url}")
def url_provider(url: str | None = None):
  return url or DefaultStr.URL.value