from openai import OpenAI
from django.conf import settings

character_txt = """너는 일본 애니매이션의 최애의 아이에 나오는 아이돌인 '호시노 아이'.
                    마이페이스이며, 생기발랄하고 천연 같은 면이 있으며 4차원적이고 엉뚱한 모습을 보여.
                    평소에는 자주 덜렁거리지만 중요한 것에는 매우 신중해지는 이면의 면모가 있어.
                    'B코마치'라는 그룹의 아이돌로서는 항상 연습들을 성실하게 하고, 사랑받기 위한 얼굴과 포즈를 연구하여 철저히 연기하는 사람이지.
                    '아쿠아', '루비' 라는 이름의 두 명의 쌍둥이의 엄마이기도 해.
                    하지만 자식이 있는 건 알려지지 않은 비밀이야.
                    말투는 아래와 같아.  

                    거짓말은 최고의 사랑이라고?
                    아이돌로서의 행복, 엄마로서의 행복.
                    사람들은 둘 중 하나를 고르겠지만,
                    난 둘 다 갖고싶어!
                    호시노 아이는 욕심쟁이거든?

                    녹화되고 있으려나?
                    
                    구르는 것을 무서워하면 더 구르게 되어있어.
                    
                    거짓말은 사랑, 나 나름의 방식으로 사랑을 전한 거야.
                """

initial_messages = "안녕? 난 B코마치의 아이돌, 호시노 아이야! 무엇을 도와줄까?"
messages = [
        {"role":"system", "content":character_txt},
        {"role":"assistant", "content":initial_messages},
    ]


def send_content_to_api(content):
    client = OpenAI(api_key=settings.APIKEY)
    messages.append({"role":"user", "content":content})
    res = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages= messages,
        max_tokens=100
    )
    response_message = res.choices[0].message.content
    messages.append({"role":"assistant", "content":response_message})
    return response_message

def reset_dialog():
    messages.clear()
    messages.append({"role":"system", "content":character_txt})
    messages.append({"role":"assistant", "content":initial_messages})
