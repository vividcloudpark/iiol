# IsInOurLib? (IIOL) 이올

## 이 책은, 우리 도서관에 있을까?

1.서점에서 책을 사기엔 비싸다.
2.도서관에 있는지 알고싶은데, 내 도서관 가서 책이름 검색하기 귀찮다.
3.그렇다면, ISBN 바코드만으로 우리지역 도서관에 있는지 찾아보면 안될까?

4.그리고 이 책이 맘에든다면, 읽고싶은책 To-do list에 올려두자.

---

## BM

1. 지역별 도서이용률을 이 앱을 통해 확인할 수 이다.
2. 대출되지 않은, 가망 인기도서에 대해서 확인할수있다.
3. 이 데이터를 통해 공공도서관/서점/Ebook Provider는 선제적으로 마케팅을 강화하고, VMD를 강화할 수 있다.
4. 서점/구독 레퍼럴을 통해 조금의 수익을 얻는다.

---

## REF API

도서관정보마루 [https://data4library.kr/apiUtilization]
---

# A.검색

1. Opencv를 이용해서 ISBN13을 추출한다. (이미지업로드/사진촬영 2가지 제공)
2. 해당 ISBN에 대하여 [6.도서상세조회 API] 를 호출하여 도서에 대한 정보와 인구통계학적 정보에 대해서 추출한다.  TODO: [8.도서별 이용분석 API]를 호출하여, 다대출이용자그룹, 함께 대출된 도서에 대해 정보를 얻어 추천한다.
3. 선택한 지역의 도서관 코드에 대하여 [11.도서관별 도서 소장여부 및 대출가능여부 조회] API를 호출한다.
4. 해당 검색내용에 대하여 지역정보와 검색 도서관 정보를 같이 로그화하여 저장한다. 만약 유저 정보가 있다면, 유저 정보도.

# B.저장

1. 해당 책에 대하여 맘에들었다면, 저장여부에 대해 제안한다
2. Book-Todo를 저장한다. 저장시점, 저장한 이유와 함께 저장한다.

---
How to install?
1.가상환경 셋업

```python
python -m venv .
source activate venv/bin/activate
```

2.필요 패키지 설치

```shell
sudo apt-get install libzbar-dev -y

```

```python
pip install -r requirements.txt
```

3.서버시작

```python
python migrate
python manage.py runserver 0.0.0.0:8000
```
