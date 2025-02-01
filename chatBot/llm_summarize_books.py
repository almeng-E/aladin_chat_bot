import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv



# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)




def read_and_sort(keywords):
    # 키워드에 해당하는 문서 읽어오기
    output_folder = Path('chatBot/output')
    result = {}
    for keyword in keywords:
        file_path = Path(f'{output_folder}/{keyword}_books.json')
        with file_path.open('r', encoding='utf-8') as file:
            books = json.load(file)
        
        # book 을 판매량으로 정렬
        books.sort(key=lambda x: int(x.get('salesPoint', 0)), reverse=True)
        books = books[:15]
        
        # 도서 정보를 텍스트로 변환
        book_data_string = ''
        for book in books:
            title = book.get('title', '미상')
            link = book.get('link', '미상')
            description = book.get('description', '미상')
            salesPoint = book.get('salesPoint', '미상')
            book_data_string += f"[제목 : {title} \n 링크 : {link} \n 소개 : {description} \n 판매량 : {salesPoint}] \n\n"

        result[keyword] = book_data_string
    return result
        

def summarize_books(keywords):
    datas = read_and_sort(keywords)
    summaries = {}
    for keyword in keywords:
        data_arg = datas[keyword]
        # LLM 호출
        conversation_history = [
            {"role": "system", "content": "당신은 주어진 책 정보들을 토대로 도서들의 내용을 요약하는 사서입니다. 책의 소개글 작성을 위해 주어진 도서 정보를 차근차근 읽고, 이해하고, 전체 목록을 하나의 문단으로 요약해야 합니다."},
            {"role": "user", "content": f"다음은 요약할 도서의 정보입니다. 도서의 제목, 저자, 소개, 판매량 정보가 하나의 텍스트로, [ ]로 묶여 전달되었습니다. \n 판매량 순서대로 정리된 도서 정보 데이터를 차근차근 읽고, 이해하고, 대표 도서를 세개 언급하고, 제시된 도서 목록 전체의 내용은 주로 어떤 내용인지 3 문장으로 요약하여 하나의 문단으로 출력해주세요. \n 도서의 제목을 언급 할 때에는 항상 해당 도서의 링크를 옆에 (link : link) 형태로 제시해주세요.\n 출력 형태 : 문자열 \n 요약 시작 문구 : '다음은 {keyword} 도서 목록의 요약입니다! :) \n 도서 정보 : {data_arg}"},
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
        # 요약 결과 저장
        summary = response.choices[0].message.content
        summaries[keyword] = summary
    return summaries
    





