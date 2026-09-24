# 서버 배포와 Nginx Proxy Manager 연결

앱은 컨테이너 안에서 `8000` 포트를 사용하고, Docker 호스트의 `8018` 포트로 연결한다. 브라우저 주소는 NPM이 HTTPS `443`에서 받으므로 포트를 붙일 필요가 없다.

## 배포

1. `.env.example`을 `.env`로 복사하고 `DJANGO_SECRET_KEY`와 `LIBRARY_API_KEY`를 실제 값으로 바꾼다.
2. `docker compose up -d --build`로 앱을 올린다.
3. 서버에서 `curl -I -H 'Host: cloudpark.duckdns.org' -H 'X-Forwarded-Proto: https' http://127.0.0.1:8018/`로 앱 응답을 확인한다.
4. NPM 관리자 화면에서 기존 Proxy Host를 편집하거나 새 Proxy Host를 만든다.

## NPM Proxy Host 값

| 항목 | 값 |
| --- | --- |
| Domain Names | `cloudpark.duckdns.org` |
| Scheme | `http` |
| Forward Hostname / IP | NPM과 Docker 호스트가 공유하는 호스트의 사설 IP (예: `192.168.1.20`) |
| Forward Port | `8018` |
| Block Common Exploits | 켬 |
| Websockets Support | 꺼도 됨 |
| SSL Certificate | 해당 도메인 인증서 선택, Force SSL 켬 |

NPM이 Docker 컨테이너이고 앱 컨테이너와 같은 Docker 네트워크에 연결되어 있으면 `Forward Hostname / IP`에 `iiol-app`, `Forward Port`에 `8000`을 쓸 수 있다. 두 컨테이너가 실제로 같은 네트워크에 있어야 한다.

현재 서버의 NPM 컨테이너 이름은 `npm-app-1`로 확인했다. 위 표의 Docker 호스트 사설 IP 방식으로 연결하면 NPM의 네트워크 이름을 따로 맞추지 않아도 된다.

NPM 공식 안내대로 인터넷에서 서버로 들어오는 HTTP/HTTPS는 NPM의 `80/443`을 유지한다. 여기서 `8018`은 NPM이 앱에 전달할 포트다. 기존 `cloudpark.duckdns.org` Proxy Host를 수정하면 해당 도메인의 기존 서비스가 새 앱으로 바뀐다. 두 앱을 함께 운영하려면 별도 DuckDNS 이름을 등록하거나 NPM의 Custom Locations로 `/iiol/` 경로를 라우팅하고 Django의 경로·정적 파일 설정도 함께 조정해야 한다.

NPM이 Docker에서 `http://127.0.0.1:8018`로 연결하면 `127.0.0.1`은 NPM 컨테이너 자신을 가리킨다. 앱 호스트 IP를 사용하거나 두 컨테이너를 같은 Docker 네트워크에 넣어야 한다.

정보나루 키가 없으면 앱과 계정은 실행되지만 도서관 검색은 설정 안내와 함께 `503`을 반환한다. 실제 외부 사용 전에는 Django secret, API 키, DuckDNS 주소, HTTPS를 확인한다.
