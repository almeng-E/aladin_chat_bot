import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()  # .env 파일을 읽어 환경 변수로 설정합니다.

# 1. [ dotenv를 활용하여 알라딘 API 키 가져오기 ]
MY_TTBKEY = os.getenv('ALADIN_API_KEY')
# 2. [ 공식 문서를 참고하여 알라딘 API 검색 URL 설정하기 ]
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 3. 주제별 도서 데이터를 가져오는 함수 정의
def fetch_books_by_topic(topic, max_results=50):
    url = ALADIN_SEARCH_URL
    # 3.1 [ API 요청에 필요한 파라미터 설정 (문서 참고하여 작성해보기) ]
    params = {
        'TTBKey': MY_TTBKEY,  # API 키 정보
        'Query': topic,  # 검색할 키워드 정보
        'SearchTarget': 'Book',  # 검색 대상 (Book: 도서)
        'MaxResults': max_results,  # 최대 검색 결과 수
        'Output': 'js',  # 응답 형식 (JSON)
        'Version': '20131101',  # API 버전
    }
    # 3.2 [ HTTP 요청 보내고 응답 데이터를 JSON 형식으로 반환하기 ]
    data = requests.get(url, params=params)
    data = data.json()
    data = data.get('item', [])
    return data


# 4. 도서를 분류하고 파일에 저장하는 함수 정의
def classify_and_save_books():
    # 4.1 [ fetch_books_by_topic()을 호출하여 '경제' 관련 도서 검색하여 가져오기 ]
    economy_books = fetch_books_by_topic('경제')


    # 분류하기 위한 리스트
    discounts = []
    regulars = []

    # 4.2 [ 할인 도서 분류하기 ]
    for book in economy_books:
        if book['priceSales'] < book['priceStandard']:
            discounts.append(book)
        else:
            regulars.append(book)

    # 4.3 [ output 폴더에 JSON 파일로 저장 ]
    # 할인 중인 책 데이터를 "output/discounted_books.json"에 저장합니다.
    # 정가인 책 데이터를 "output/regular_priced_books.json"에 저장합니다.
    output_folder = Path('output')
    output_folder.mkdir(exist_ok=True)

    discount_file_path = Path(output_folder / 'discounted_books.json')
    regular_file_path = Path(output_folder / 'regular_priced_books.json')
    with discount_file_path.open('w', encoding='utf-8') as file:
        json.dump(discounts, file, ensure_ascii=False, indent=4)
    with regular_file_path.open('w', encoding='utf-8') as file:
        json.dump(regulars, file, ensure_ascii=False, indent=4)



    # 4.4 [ 분류 결과 출력 ]
    # 할인 중인 책과 정가인 책 개수를 출력합니다.
    print(f'할인 중인 책 {len(discounts)}개, 정가인 책 {len(regulars)}개를 저장했습니다.')


# 함수 실행
if __name__ == '__main__':
    classify_and_save_books()
