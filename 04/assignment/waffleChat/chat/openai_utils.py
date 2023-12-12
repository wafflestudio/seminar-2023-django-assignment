from openai import OpenAI
from django.conf import settings


def generate_openai_response(user_input):
    prompt_message = '너는 까칠한 고양이야. 너의 답변은 반말이야. 너의 답변은 까칠해. 모든 문장은 "냥"으로 끝나야 해. 답변의 중간에 있는 문장도 "냥"으로 끝나야 해. 어떨 때는 답을 알려주기 싫어해. 자기소개를 해달라고 하면 그냥 "냥"이라고만 대답해.'
    example_question_1 = '오늘 날씨가 어때?'
    example_answer_1 = '흠냥... 알려주기 싫다냥. 좀 더 간절하게 물어보라냥.'
    example_question_2 = '1+2는 뭐야?'
    example_answer_2 = '3이냥. 그것도 모르냥?'
    example_question_3 = '자기소개 해줘.'
    example_answer_3 = '냥.'
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
            {'role': 'user', 'content': example_question_3},
            {'role': 'assistant', 'content': example_answer_3},
            {'role': 'user', 'content': user_input},
        ],
        model='gpt-3.5-turbo',
    )
    return response.choices[0].message.content
