import os

from typing import Optional, Literal, List, Dict

from dotenv import load_dotenv

from google import genai
from google.genai import types
from groq import Groq


load_dotenv()


class LLMService:
    def __init__(self, provider: Literal["google", "groq", "openai"],model: str, max_retries: Optional[int] = None, backoff_base: Optional[float] = None,backoff_jitter: Optional[float] = None, hard_prompt_cap: Optional[int] = None):
        self.provider = provider
        self.model = model
        self.max_retries = max_retries if max_retries is not None else 2
        self.backoff_base = backoff_base if backoff_base is not None else 1.2
        self.backoff_jitter = backoff_jitter if backoff_jitter is not None else 0.2
        self.hard_prompt_cap = hard_prompt_cap if hard_prompt_cap is not None else 1000

        self._init_client()

    def _init_client(self) -> None:
        if self.provider == "google":
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key is None:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            self.client = genai.Client(api_key=api_key)
            
        elif self.provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if api_key is None:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            self.client = Groq(api_key=api_key)

        elif self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key is None:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            # self.client = genai.Client(api_key=api_key)
        else:
            raise ValueError(f"Invalid provider: {self.provider}")



    def Chat(self, messages: List[Dict[str, str]], context_strs: Optional[List[str]]=None, temperature: Optional[float] = None, max_tokens: Optional[int] = None, **kwargs):
        if self.provider == "google":
            return self._call_google(messages, context_strs, temperature, max_tokens, **kwargs)
        elif self.provider == "groq":
            return self._call_groq(messages, context_strs, temperature, max_tokens, **kwargs)
        elif self.provider == "openai":
            return self._call_openai(messages, context_strs, temperature, max_tokens, **kwargs)
        else:
            raise ValueError(f"Invalid provider: {self.provider}")




    def _call_google(self, 
                    messages: List[Dict[str, str]], 
                    context_strs: Optional[List[str]]=None, 
                    temperature: Optional[float] = None, 
                    max_tokens: Optional[int] = None, 
                    **kwargs)-> Dict[str, str]:
        
        gemini_content = []
        system_instruction = None

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                system_instruction = content    
            elif role == "user":
                gemini_content.append(types.Content(role="user", parts=[types.Part.from_text(text=content)]))
            elif role == "assistant":
                gemini_content.append(types.Content(role="model", parts=[types.Part.from_text(text=content)]))

        config_params = {}
        if temperature is not None:
            config_params["temperature"] = temperature
        if max_tokens is not None:
            config_params["max_output_tokens"] = max_tokens
        if system_instruction is not None:
            config_params["system_instruction"] = system_instruction
        
        generation_config = types.GenerateContentConfig(**config_params) if config_params else None

        response = self.client.models.generate_content(
            model=self.model,
            contents=gemini_content,
            config=generation_config
        )
        return {"text" : response.text}
    
    def _call_groq(self, 
                    messages: List[Dict[str, str]], 
                    context_strs: Optional[List[str]]=None, 
                    temperature: Optional[float] = None, 
                    max_tokens: Optional[int] = None, 
                    **kwargs):
        pass


    def _call_openai(self, 
                    messages: List[Dict[str, str]], 
                    context_strs: Optional[List[str]]=None, 
                    temperature: Optional[float] = None, 
                    max_tokens: Optional[int] = None, 
                    **kwargs):
        pass




    

