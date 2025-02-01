import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
from pprint import pprint

# 1. [ 환경 변수 로드 ]
load_dotenv()
MY_TTBKEY = os.getenv('ALADIN_API_KEY')
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'


# 2. [ 최대 100개까지 주제별 도서 데이터를 가져오는 함수 정의 ]
def fetch_books_by_topic(topic, max_results=100):
    url = ALADIN_SEARCH_URL
    res = []
    for i in range(max_results // 50):
        params = {
            'TTBKey': MY_TTBKEY,  # API 키 정보
            'Query': topic,  # 검색할 키워드 정보
            'SearchTarget': 'Book',  # 검색 대상 (Book: 도서)
            'Start' : (i+1),
            'MaxResults': max_results,  # 최대 검색 결과 수
            'Output': 'js',  # 응답 형식 (JSON)
            'Version': '20131101',  # API 버전
        }
        data = requests.get(url, params=params)
        data = data.json()
        data = data.get('item', [])
        res.extend(data)
    return res


# 3. '인공지능' 도서 데이터를 처리하는 함수 정의
def process_ai_books():
    # 3.1 [ '인공지능' 관련 도서 검색 ]
    # fetch_books_by_topic()을 호출하여 '인공지능' 관련 도서를 100개 수집합니다.
    all_books = fetch_books_by_topic('인공지능')  

    # 3.2 [ 수집된 데이터에서 가격 정보가 있는 책 필터링 및 가격순 정렬 ]
    all_books.sort(key=lambda x: int(x.get('priceStandard', 0)), reverse=True)

    # 3.3 [ 상위 10개 도서 선택 ]
    pricy_books = all_books[:10]

    # 3.4 [ 상위 10개 도서 정보 출력 ]
    pprint(pricy_books)
    print("*"*50)

    # 3.5 [ JSON 파일로 저장할 데이터 준비 ]
    # output/ai_top10_books.json 파일로 저장
    output_folder = Path('output')
    output_folder.mkdir(exist_ok=True)
    file_path = Path('output/ai_top10_books.json')
    with file_path.open('w', encoding='utf-8') as file:
        json.dump(pricy_books, file, ensure_ascii=False, indent=4)





    # 3.6 [ 완료 메시지를 출력 ]
    print('c01.py 실행 완료!')

# 함수 실행
if __name__ == '__main__':
    process_ai_books()
