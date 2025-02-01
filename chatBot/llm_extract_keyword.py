import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)



def extract_keywords(user_input):
    # 키워드 추출 페르소나 설정
    conversation_history = [
        {"role": "system", "content": "당신은 학생들의 질문에 답하기 위해 관련 정보를 추출하는 사서입니다. 사용자의 입력에 맞추어 도서 정보 검색에 용이한 가장 중요한 키워드(주제) 2개를 추출하고 정리하여 출력해야 합니다."},
        {"role": "system", "content": "답변은 사용자가 읽고 이해하기 쉽도록 키워드를 쉼표(,) 로 구분하여 출력해야합니다.\n 예를 들어 : 인공지능, 머신러닝 \n 주의사항 1. '등'으로 끝나는 키워드는 제외해주세요.\n 주의사항 2. '무엇'과 같은 의문사는 제외해주세요. \n 주의사항 3. '추천'과 같이 주제가 아닌 단어는 제외해주세요."},
    ]
    # 질문
    conversation_history.append(
        {
            "role": "user",
            "content": f"다음은 사용자의 질문입니다. 사용자의 질문 내용을 토대로 도서 정보 검색에 용이한 가장 중요한 키워드 2개를 추출해주세요. \n 사용자 질문 : {user_input} \n 출력 형태 : 쉼표(,)로 구분된 키워드",
        } 
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",            # 사용하려는 모델 (필수 지정)
        messages=conversation_history,  # 대화 메시지 목록 (필수 지정)
        max_tokens=500,                 # 생성될 응답의 최대 토큰 수 (값의 범위: 1~모델 마다 최대값 ex> gpt-4o-mini: 16,385 tokens)
        temperature=1.0,                # 확률 분포 조정을 통한 응답의 다양성 제어 (값의 범위: 0~2)
        top_p=1.0,                      # 누적 확률 값을 통한 응답의 다양성 제어 (값의 범위: 0~1)
        n=1,                            # 생성할 응답 수 (1이상의 값)
        seed=1000                       # 랜덤 씨드 값 (설정하는 경우 일관된 답변을 얻을 수 있음)
    )

    # 키워드 추출
    keywords = response.choices[0].message.content
    keywords = keywords.split(',')
    keywords = [keyword.strip() for keyword in keywords]
    return keywords







