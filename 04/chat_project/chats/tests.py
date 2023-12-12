from django.test import TestCase
from openai import OpenAI


def create_test():
    client = OpenAI()
    my_messages = [{"role": "system", "content": "You are a mad scientist."},
                   {"role": "assistant", "content": "여기서 뭐하고 있는거야?"}]
    chat = input()
    while chat != "exit":
        my_messages.append({"role": "user", "content": chat})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=my_messages
        )
        new_message = response.choices[0].message.content
        print(new_message)
        my_messages.append({"role": "assistant", "content": new_message})
        chat = input()