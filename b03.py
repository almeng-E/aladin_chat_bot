import os
import requests
import json
from pathlib import Path
from gtts import gTTS
from dotenv import load_dotenv


load_dotenv()  # .env 파일을 읽어 환경 변수로 설정합니다.

# 1. [ dotenv를 활용하여 알라딘 API 키 가져오기 ]
MY_TTBKEY = os.getenv('ALADIN_API_KEY')
# 2. [ 공식 문서를 참고하여 알라딘 API 검색 URL 설정하기 ]
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 3. 주제별 도서 데이터를 가져오는 함수 정의
def fetch_books_by_topic(topic, max_results=30):
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


# 4. 도서 정보를 JSON 파일로 저장하는 함수 정의
def save_books_to_json(books, filename, max_save=5):
    
    book_list = []
    for book in books:
        # 4.1 [ 책 정보에서 'description'이 있는 경우 book_list에 총 5개만 추가 ]
        if book['description']:
            book_list.append(book)
        if len(book_list) >= max_save:
            break

    # 4.2 [ 5개의 도서 정보를 JSON 파일로 저장 ]
    # book_list를 'output/korean_literature_books.json' 으로 저장합니다.
    output_folder = Path('output')
    output_folder.mkdir(exist_ok=True)
    file_path = Path(filename)
    with file_path.open('w', encoding='utf-8') as file:
        json.dump(book_list, file, ensure_ascii=False, indent=4)

    # 4.3 [ 저장된 책 정보 반환 ]
    return book_list


# 5. 입력의 text를 음성 파일로 변환하는 함수 정의
def create_tts_file(text, filename):
    # gTTS를 사용하여 입력 받은 text를 MP3 파일로 저장합니다.
    # 파일은 output/book_n.mp3 로 저장한다. (n은 숫자)

    tts = gTTS(text=text, lang='ko', slow=False)
    tts.save(filename)  


# 6. '한국문학' 도서 데이터를 처리하는 함수 정의
def process_korean_literature_books():
    # 6.1 [ fetch_books_by_topic()을 호출하여 '한국문학' 관련 도서를 검색 ]
    raw_data = fetch_books_by_topic('한국문학')
    
    # 6.2 [ save_books_to_json() 를 호출하여 5개의 도서 정보를 JSON으로 저장 및 저장된 데이터 가져오기 ]
    saved_data = save_books_to_json(raw_data, 'output/korean_literature_books.json')

    # 각 책의 제목과 요약을 음성 파일로 저장 
    for i, book in enumerate(saved_data, 1):
        # 6.3 [ create_tts_file 을 호출하여 제목과 요약 정보를 합쳐 음성 파일로 저장 ]
        create_tts_file(book['title'] + book['description'], f'output/book_{i}.mp3')

    # 6.4 [ 처리 완료 메시지 출력하기 ]
    print('한국문학 도서 처리가 완료되었습니다.')  

# 함수 실행
if __name__ == '__main__':
    process_korean_literature_books()
