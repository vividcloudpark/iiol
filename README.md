# 이올 (IIOL)

서점에서 책의 ISBN-13을 스캔하고, 선택한 지역의 참여 도서관 소장 정보를 찾는 모바일 우선 웹앱입니다. 비회원 검색을 지원하며 회원은 가입 때 기본 지역을 저장하고 프로필에서 수정할 수 있습니다.

## 로컬 실행

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
npm ci
npm run build
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

`http://127.0.0.1:8000`에서 화면과 계정 흐름을 확인할 수 있습니다. 도서관 검색은 `LIBRARY_API_KEY` 환경 변수에 도서관 정보나루 키를 설정해야 합니다. 카메라 테스트는 HTTPS 환경에서 진행해야 하며, localhost는 브라우저가 로컬 보안 컨텍스트로 허용합니다.

## 배포

Docker 배포와 Nginx Proxy Manager의 도메인·포트 연결은 [DEPLOYMENT.md](DEPLOYMENT.md)에 있습니다. 현재 Compose 설정은 앱 컨테이너의 `8000`을 호스트 `8018`로 연결합니다.

## 구현 범위

- EAN-13 카메라 인식: 브라우저 `BarcodeDetector` 우선, 미지원 또는 읽기 실패 시 ZXing 브라우저 디코더
- 사진 촬영/선택과 ISBN 직접 입력 대체 경로
- ISBN 접두어·검사 숫자 검증, 결과 확인 후 지역 도서관 검색
- 필수 지역 선택을 포함한 가입, 로그인, 로그아웃, 프로필 수정, 비밀번호 변경
- 지역 내 소장 도서관과 전일 기준 대출 가능 정보 조회

지역 코드 파일은 기존 프로젝트를 시작점으로 정리했습니다. 운영 전에 정보나루 API 키로 광역시·시군구 코드 응답을 검증해야 합니다. 카메라 접근은 실기기 Android/iPhone에서 HTTPS로 따로 확인해야 합니다.
