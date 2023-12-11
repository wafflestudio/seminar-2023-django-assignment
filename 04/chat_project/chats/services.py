from openai import OpenAI
from .models import Chat, Character


class GPTService:
    def __init__(self):
        self.myclient = OpenAI()
        self.mymodel = "gpt-3.5-turbo"
        self.current_messages = []

    def make_messages(self):
        my_message = [{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "assistant", "content": Character.objects.first().first_message}
                      ]
        for chat in Chat.objects.order_by("created_at"):
            my_message += {"role": chat.role, "content": chat.content}
        return my_message

    def make_response(self):
        response = self.myclient.chat.completions.create(
            model=self.mymodel,
            messages=self.make_messages()
        )
        return response.choices[0].message.content


gpt = GPTService
