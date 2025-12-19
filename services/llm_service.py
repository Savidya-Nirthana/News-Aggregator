import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()


class LLMService:
    def __init__(self):
        self.__api_key = os.getenv("GOOGLE_KEY")
        if not self.__api_key:
            raise ValueError("GOOGLE_KEY environment variable is not set")
        self.model_name = "gemini-3-pro-preview"
        self.client = genai.Client(api_key=self.__api_key)


    def summarize_news(self, content: str) -> str:
        prompt = f"Please summarize the following news article: \n\n{content}"

        try: 
            response = self.client.models.generate_content(
                model=self.model_name,
                contents = prompt,
                config = types.GenerateContentConfig(
                    system_instruction="You are a professional news editor. Summarize articles in a concise, neutral tone. Use 3-5 bullet points for the key facts.",
                    temperature=0.3
                )
            )
            return response.text
        except Exception as e:
            print(f"Error during LLM summarization: {e}")
            return "Error: Unable to summarize the article at this time."

    

