from news_extractor import NewsExtractor
from llm_service import LLMService


news_extractor = NewsExtractor()
llm_service = LLMService()


news = news_extractor.extract()
news1 = news[0]

content = news_extractor.extract_content(news1['link'], news1['title'])
summary = llm_service.summarize_news(content)

print(summary)

