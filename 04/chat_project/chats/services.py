from openai import OpenAI
import os
from .models import Chat, Character


class GPTService:
    def __init__(self):
        self.myclient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.mymodel = "gpt-3.5-turbo"
        self.current_messages = []

    def make_messages(self):
        my_message = [{"role": "system", "content": "You are a mad scientist."}]
        for chat in Chat.objects.order_by("created_at"):
            my_message += [{"role": chat.role, "content": chat.content}]
        my_message += [{"role": "system", "content": "Remember you are a mad scientist. You are not a kind person."}]
        return my_message

    def make_response(self):
        response = self.myclient.chat.completions.create(
            model=self.mymodel,
            messages=self.make_messages()
        )
        return response.choices[0].message.content


gpt = GPTService()
