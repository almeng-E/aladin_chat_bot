# a01  
### 배운 점 : 
- dotenv
- getenv로 환경변수 설정하는 이유
- fetch 작성 방법
- get url 일단 무작정 보냈음 
- - 나중에 a03에서 수정, params 파라미터로 딕셔너리 전달
- api 공식 문서 읽는 법
- dict.get() 함수의 목적


# a02 
### 배운 점 : 
- 파일 경로 객체 만드는 이유
- 폴더 생성하는 법과 exist_ok=True
- 파일 생성하는 법
- 파일 읽고 수정하는 법
- 저장된 파일 읽고 출력하는 법
- 파일 수정 방법 
### 파일 읽기 관련하여 더 학습해야함


# a03
### 배운 점 :
- gTTS라는게 있구나


# b01
### 배운 점 :
- API 요청에 필요한 파라미터 직접 작성하기
- 날짜를 전부 계산하기 힘드니 연도만 따로 계산할 수 있는 점


# b02
### 배운 점 : 
- json 파일의 쓰기는 str 작성하는 문법과 다름


# b03
### 배운 점 : 
- enumerate(iterable , start) 형식의 문법사항... start를 지정할 수 있구나
- 여러 층으로 걸쳐 호출하여 따라가야 할 때에는 한 층 한 층 따라가면 이해하기 쉽다
- 에러 디버깅하기 : 천천히 line by line 따라가서 읽다보면 호출 순서와 오류의 위치를 찾을 수 있음
```  File "c:\Users\82104\OneDrive\바탕 화면\SSAFY\관통프로젝트\01-pjt\b03.py", line 74, in process_korean_literature_books
    saved_data = save_books_to_json(raw_data, 'output/korean_literature_books.json')
  File "c:\Users\82104\OneDrive\바탕 화면\SSAFY\관통프로젝트\01-pjt\b03.py", line 51, in save_books_to_json
    with file_path.open('w', encoding='utf-8') as file:
  File "C:\Python310\lib\pathlib.py", line 1117, in open
    return self._accessor.open(self, mode, buffering, encoding, errors,
FileNotFoundError: [Errno 2] No such file or directory: 'output\\output\\korean_literature_books.json' 
```



# c01
### 배운 점 : 
- api는 한번의 호출 당 출력 개수가 제한될 수 있구나,,, 나는 for 문을 통해 두번 호출하는 식으로 해결했는데 더 나은 방법은 없나?
- api에서 제공되지 않는 sort를 구현하려면 일단 받아와서 내가 정리해야하는구나. sorting 알고리즘이 중요한 이유를 알겠다. 100개였으니 list의 .sort() 메서드로 했지 엄청나게 큰 데이터였으면 느렸을 수도 있겠다...





