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



# c02
### 배운 점 :
- openai api의 호출 형식과 순서
- role들 : system, user
- json 형태로 출력 요청한 후 parsing 하는 과정
- markdown 형식으로 출력해줘서 ```json ``` 을 제거하는 데에 시간이 걸림 ... 특정 형식으로 반환해달라고 하면 이렇게 코드라고 표시해준다는 것을 알고 있기


# c03
### 궁금한 점 : 
- path는 매번 설정해줘야하나?
- 언제 경로를 지정해주고 언제 안하는거지?
- save_books_info() 에서 book의 정보를 추출하여 문자열로 만들 때, 어떤 방식이 가장 효율적일까 ??



-------

# 도전과제 : 챗봇 만들기
## 플로우차트
![플로우 차트](/asset/chatbot_flowchart.png)

### 배웠던, 실습했던 내용만으로 챗봇을 만들 수 있었다 ! 


### 추가 끄적임
- 아 프레임워크 없이 openai 써보니까 왜 langchain framework를 쓰는지 알겠다.
매번 객체 생성하기도 힘들고
매번 프롬프트 교체하고 하는것도 귀찮다...
LEDC 그립다
  - 가능하다면, langchain 시스템으로 교체하자 나중에...

- DeepSeek R1 모델로 교체하면 분류-요약-포매팅 한번에 될것같기도...?
o1도 되지만 너무 비싼 관계로...







