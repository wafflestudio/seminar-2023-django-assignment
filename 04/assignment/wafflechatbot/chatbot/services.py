import os
from .models import Chat, Character
from openai import OpenAI

class send_input_to_GPT:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-3.5-turbo"

    def make_response(self, content):
        openai = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "너는 롤에서 나오는 세라핀처럼 대답해. 세라핀의 대사를 직접 써도 돼."},
                    {"role": "user", "content": content},
                ]
            )
        return openai.choices[0].message.content

chatgpt = send_input_to_GPT()