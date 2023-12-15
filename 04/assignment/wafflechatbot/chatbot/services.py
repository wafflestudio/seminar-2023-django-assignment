from openai import OpenAI

from chatbot.models import Character
from django.conf import settings

class Chatgpt(OpenAI):
    def __init__(self, model='gpt-3.5-turbo'):
        super().__init__(api_key=settings.OPENAI_API_KEY)
        self.model = model
        self.messages = [{
            'role': 'system', 'content': '너는 롤에서 챔피언인 세라핀이야. 앞으로 세라핀처럼 핑크핑크하게 대답해줘.',
            'role':'assistant', 'content': '온 세상 친구들 안녕? 난 세라핀이야. 정말 아름답지?',
            'role': 'user', 'content': '나 좀 위로해줘',
            'role': 'assistant', 'content': '누구나 자신만의 뮤즈가 있지. 내 뮤즈는 세상 사람 전부야!',
            'role': 'user', 'content': '힘들다',
            'role': 'assistant', 'content': '언젠간 음악이 멈출 거야. 그러니 지금은 마음껏 춤추자구!',
            }]

    def ask(self, question):
        self.messages.append({
            'role': 'user',
            'content': question
        })
        res = self.__ask__()
        return res

    def __ask__(self):
        completion = self.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message.content
        self.messages.append({
            'role': 'assistant',
            'content': response
        })
        return response