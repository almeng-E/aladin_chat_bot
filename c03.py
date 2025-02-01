import os
import requests
from pathlib import Path
from gtts import gTTS
from dotenv import load_dotenv

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


# 3. [ 도서 정보를 텍스트 파일로 저장하는 함수 정의 ]
# 책 정보를 "제목, 저자, 소개" 형식으로 변환하여 txt 파일로 저장
def save_books_info(books, filename):
    result = ''
    for book in books:
        title = book.get('title', '미상')
        author = book.get('author', '미상')
        description = book.get('description', '미상')
        text = f"제목 : {title}\n저자 : {author}\n소개 : {description}\n\n"
        result += text
    output_folder = Path('output')
    output_folder.mkdir(exist_ok=True)  
    file_path = Path(filename)
    with file_path.open('w', encoding='utf-8') as file:
        file.write(result)

    print(f"{filename} 파일이 생성되었습니다.")
    return

# 5. [ 텍스트 파일을 오디오 파일로 변환하는 함수 정의 ]
def create_audio_file(text_file, audio_file):
    file_path = Path(text_file)
    
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    tts = gTTS(text, lang='ko', slow=False)
    tts.save(audio_file)
    print(f"{audio_file} 파일이 생성되었습니다.")
    return


# 6. [ 음악 관련 도서 데이터를 처리하는 함수 정의 ]
def process_music_books():
    # 6.1 [ '음악' 주제의 도서 데이터 수집 ]
    searched_books = fetch_books_by_topic('음악')

    # 6.2 [ 도서 정보를 텍스트 파일로 저장 ]
    save_books_info(searched_books, 'output/music_books_info.txt')

    # 6.3 [ 텍스트 파일을 오디오 파일로 변환 ]
    create_audio_file('output/music_books_info.txt', 'output/music_books_info.mp3')

    print("모든 작업이 완료되었습니다.")


# 함수 실행
if __name__ == '__main__':
    process_music_books()
