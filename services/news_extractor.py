from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os 


load_dotenv()
NEWS_URL = os.getenv("NEWS_URL")
if not NEWS_URL:
    raise ValueError("NEWS_URL environment variable is not set")


class NewsExtractor:
    def __init__(self, news_url: str = NEWS_URL or ""):
        self.news_url = news_url

    def extract(self)-> list[dict]:
        response = requests.get(self.news_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "xml")
            articles = soup.find_all("item")
            latest_articles = []
            for article in articles:
                title_tag = article.find("title")
                link_tag = article.find("link")
                if title_tag and link_tag:
                    title = title_tag.text
                    link = link_tag.text
                    latest_articles.append({
                        "title": title,
                        "link": link,
                    })
            return latest_articles
        else:
            print(f"Failed to fetch news from {self.news_url}, status code: {response.status_code}")
            return []

    def extract_content(self, article_url: str, title: str) -> str:
        response = requests.get(article_url)
        if(response.status_code == 200):
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            content = "\n\n".join([p.get_text() for p in paragraphs])
            return content
        else:
            print(f"Failed to fetch article from {article_url}, status code: {response.status_code}")
            return ""

# nextractor = NewsExtractor()
# news_data = nextractor.extract()[0]['link']
# content = nextractor.extract_content(news_data, "Sample Title")
# print(content)