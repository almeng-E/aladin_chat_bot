import os
import requests
import json

from pprint import pprint
from pathlib import Path
from dotenv import load_dotenv
from gtts import gTTS


# 모듈 로드
import llm_extract_keyword
import llm_summarize_books
import llm_format_markdown

# 환경 변수 로드
load_dotenv()
MY_TTBKEY = os.getenv('ALADIN_API_KEY')

ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'



# 최대 100개까지 키워드별 도서 데이터를 가져오는 함수 정의
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

# 도서 정보를 텍스트 파일로 저장하는 함수 정의
def save_books_info(searched_books):
    output_folder = Path('chatBot/output')
    output_folder.mkdir(exist_ok=True)
    for keyword, books in searched_books.items():
        file_path = Path(f'{output_folder}/{keyword}_books.json')
        with file_path.open('w', encoding='utf-8') as file:
            json.dump(books, file, ensure_ascii=False, indent=4)    
    return


def save_result(result):
    output_folder = Path('chatBot/output')
    output_folder.mkdir(exist_ok=True)
    file_path = Path(f'{output_folder}/summary.md')
    with file_path.open('w', encoding='utf-8') as file:
        file.write(result)
    print(f"{file_path} 파일이 생성되었습니다.")
    return


# 오디오 파일 생성
def create_audio_file(text_file, audio_file):
    file_path = Path(text_file)
    
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    tts = gTTS(text, lang='ko')
    tts.save(audio_file)
    print(f"{audio_file} 파일이 생성되었습니다.")
    return


# LLM Chain 호출
def process_chain():
    user_input = input("찾고 싶은 도서의 주제, 내용을 입력하세요: ")

    # 1. 키워드 추출
    # output: keywords (list)
    keywords = llm_extract_keyword.extract_keywords(user_input)
    print(f'키워드가 추출 되었습니다 : {keywords}') 

    # 2. 도서 검색
    # output: books (json : list of dicts)
    searched_books = {}
    for keyword in keywords:
        books = fetch_books_by_topic(keyword)
        searched_books[keyword] = books[:5] # for testing
    

    # 3. 도서 정보 저장
    # output: json files
    save_books_info(searched_books)

    # 4. 도서 분류
    # output: summaries (json : list of dicts)
    summaries = llm_summarize_books.summarize_books(keywords)

    # 5. md 형식으로 변환
    # output: result (str - markdown format) 
    result = llm_format_markdown.format_markdown(summaries)
    print('검색한 도서 정보를 정리한 결과입니다.')
    print(result)
    save_result(result)

    # 6. 요약 오디오 파일 생성
    # output: audio_file (mp3)
    create_audio_file('chatBot/output/summary.md', 'chatBot/output/summary.mp3')

    # 7. 결과 출력
    print('모든 작업이 완료되었습니다.')

# 실행 부분
if __name__ == '__main__':
    process_chain()


