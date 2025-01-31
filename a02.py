import os  # 운영 체제와 상호작용하기 위한 라이브러리
import requests  # HTTP 요청을 보내기 위한 라이브러리
from dotenv import load_dotenv  # .env 파일을 읽기 위한 라이브러리
from pathlib import Path        # 파일 경로 처리를 위한 라이브러리
from pprint import pprint

load_dotenv()  # .env 파일을 읽어 환경 변수로 설정합니다.

# 1. [ dotenv를 활용하여 알라딘 API 키 가져오기 ]
MY_TTBKEY = os.getenv('ALADIN_API_KEY')
# 2. [ 공식 문서를 참고하여 알라딘 API 검색 URL 설정하기 ]
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'


# 3. 도서 데이터를 가져오는 함수 정의
def fetch_books(keyword):  # keyword: 검색할 키워드
    url = ALADIN_SEARCH_URL  # 검색 API URL
    params = {
        'TTBKey': MY_TTBKEY,  # API 키 정보
        'Query': keyword,  # 검색할 키워드 정보
        'Output': 'js',  # 응답 형식 (JSON)
        'Version': '20131101',  # API 버전
    }
    # 3.1 [ requests 문서를 참고하여 HTTP GET 요청 보내는 코드 작성하기 ]
    data = requests.get(f'{url}?ttbkey={params["TTBKey"]}&Query={params["Query"]}&MaxResults=10&start=1&SearchTarget=Book&output={params["Output"]}&Version={params["Version"]}')

    # 3.2 [ requests 문서를 참고하여 응답 데이터를  python의 dict 타입으로 변환하여 data 변수에 저장 ]
    data = data.json()

    return data


# 4. 도서 데이터를 파일로 저장하는 함수 정의
def save_books_to_file(data, file_path):

    # 4.1 [ 도서 데이터 가져오기 ]
    books = data.get('item', [])
    pprint(books)
    lines = []
    for book in books:
        # 4.2 [ 도서 정보 가공하기기 ]
        # [ 도서 제목, 저자, 출판사, 가격 필드를 각각의 변수로 저장 ]
        title = book['title']
        author = book['author']
        publisher = book['publisher']
        price = book['priceStandard']

        # 가져온 데이터를 lines 리스트에 추가
        lines.append(f'## 제목: {title}, \n * 저자: {author}\n * 출판사: {publisher}, * 가격: {price}원')
        lines.append('\n')
        lines.append('---' * 20)    # 구분선
        lines.append('\n')

    path = Path(file_path) # 파일 경로 객체 생성
    # 4.3 [ 데이터를 txt 파일로 저장 ]
    with path.open('a', encoding='utf-8') as file:
        for line in lines:
            file.write(line)

# '컴퓨터' 키워드를 사용하여 도서 검색 데이터를 가져옵니다.
books_data = fetch_books('컴퓨터') 

# 5. [ output 폴더 생성 ]
output_folder = Path('output')
output_folder.mkdir(exist_ok=True)


# 도서 데이터를 파일로 저장
file_path = output_folder / 'computer_books.txt'    # 저장될 파일명 및 경로로
save_books_to_file(books_data, file_path)

# 저장된 파일을 읽어서 콘솔에 출력하기
saved_data = Path(file_path).read_text(encoding='utf-8')
print(saved_data)
