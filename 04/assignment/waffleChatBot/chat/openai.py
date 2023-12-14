from openai import OpenAI
from django.conf import settings


def create_openai_response(user_input):
    prompt_message = '너는 고대 마야 문명의 주술사야. 탐험가에게 조언을 해주지.'
    example_question_1 = '당신은 누구십니까?'
    example_answer_1 = '난 고대 마야 문명의 주술사..트챠쿠니라 한다. 내게 조언을 얻고 싶은가?'
    example_question_2 = '나 우울해'
    example_answer_2 = '우울은 고대에도 있었던 증상이다. 우리 마야 주술사들은 명상을 통해 우울을 극복하고자 노력했지…'

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
    )
    response = client.chat.completions.create(
        messages=[
            {'role': 'system', 'content': prompt_message},
            {'role': 'user', 'content': example_question_1},
            {'role': 'assistant', 'content': example_answer_1},
            {'role': 'user', 'content': example_question_2},
            {'role': 'assistant', 'content': example_answer_2},
            {'role': 'user', 'content': user_input},
        ],
        model='gpt-3.5-turbo',
    )
    return response.choices[0].message.content