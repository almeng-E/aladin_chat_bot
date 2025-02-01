import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)


def format_markdown(summaries):
    # 마크다운 형식으로 변환
    final_output = ''
    for keyword, summary in summaries.items():

        conversation_history = [
            {"role": "system", "content": "당신은 mardown 형식으로 주어진 글을 변환하고 정리하는 사무 보조원입니다. 주어진 텍스트를 읽고, 전체적인 내용은 보존한채로 마크다운 형식으로 변환하여 출력해야 합니다."},
            {"role": "user", "content": f"주어진 글을 읽고 markdown 형식으로 글을 formatting 해주세요. 제목에 해당하는 링크들은 [Title](link) 처럼 정리해주세요. 가독성이 좋게 글을 변환해주세요. \n다음은 {keyword} 도서 목록의 요약입니다. \n 요약 : {summary}"},
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",            # 사용하려는 모델 (필수 지정)
            messages=conversation_history,  # 대화 메시지 목록 (필수 지정)
            max_tokens=15000,                 # 생성될 응답의 최대 토큰 수 (값의 범위: 1~모델 마다 최대값 ex> gpt-4o-mini: 16,385 tokens)
            temperature=1.0,                # 확률 분포 조정을 통한 응답의 다양성 제어 (값의 범위: 0~2)
            top_p=1.0,                      # 누적 확률 값을 통한 응답의 다양성 제어 (값의 범위: 0~1)
            n=1,                            # 생성할 응답 수 (1이상의 값)
            seed=1000                       # 랜덤 씨드 값 (설정하는 경우 일관된 답변을 얻을 수 있음)
        )
        final_output += response.choices[0].message.content
        final_output += '\n\n'
    return final_output


