# Provides the AI prompt and response services to the MainWindow

import os
from openai import OpenAI
from dotenv import load_dotenv

class AIChatController:
    def __init__(self):
        #get API key from environment variables
        load_dotenv()
        api_key = os.environ.get("OR_API_KEY")
        if api_key == None:
            raise RuntimeError("API_KEY was not assigned.")

        # Create OpenAI API client
        self.AI_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key =api_key,
        )

    def send_message(self, messages: list[dict[str,str]]):
        return self.AI_client.chat.completions.create(
        model = "openrouter/free",
        messages=messages,
    )

