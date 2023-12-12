import os
from .models import Chat, Character
from openai import OpenAI

class GPTService:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-3.5-turbo"

    def make_response(self, content):
        openai = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are Groot in Guardians of the Galaxy."},
                    {"role": "user", "content": content},
                    {"role": "system", "content": "Remember, you are Groot. However, Please say your feeling in English using ( and ) after your 'I am Groot'"}
                ]
            )
        return openai.choices[0].message.content

chatgpt = GPTService()