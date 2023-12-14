import openai
from decouple import config

from openai import OpenAI

from chatbot.models import Character
from chatbotAPI import settings

class Chatgpt(OpenAI):
    def __init__(self, model='gpt-3.5-turbo'):
        super().__init__(api_key=settings.OPENAI_API_KEY)
        self.model = model
        self.messages = [{'role': 'system', 'content': Character.objects.first().get_character_description()}]

    def ask(self, question):
        self.messages.append({
            'role': 'user',
            'content': question
        })
        res = self.__ask__()
        return res

    def __ask__(self):
        completion = self.chat.completions.create(
            # model 지정
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message.content
        self.messages.append({
            'role': 'assistant',
            'content': response
        })
        return response
