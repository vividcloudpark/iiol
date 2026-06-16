#!/bin/bash

# ANSI Color codes for prettier output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}==================================================${NC}"
echo -e "${CYAN}       IIOL (IsInOurLib?) Local Launcher        ${NC}"
echo -e "${CYAN}==================================================${NC}"

# 1. Check for .env file
if [ ! -f .env ]; then
  echo -e "${YELLOW}[!] .env 파일이 존재하지 않습니다. .env.example 복사 중...${NC}"
  cp .env.example .env
fi

# Load env variables (optional, to pass to script context)
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# 2. Spin up Redis and PostgreSQL container
echo -e "${GREEN}[*] Docker Compose를 사용하여 PostgreSQL 및 Redis 컨테이너 기동...${NC}"
docker compose up -d
if [ $? -ne 0 ]; then
  echo -e "${RED}[Error] Docker 컨테이너를 올리지 못했습니다. Docker 데몬이 실행 중인지 확인하세요.${NC}"
  exit 1
fi

# 3. Setup Django virtual environment
echo -e "${GREEN}[*] Python 가상환경(venv) 확인 중...${NC}"
if [ ! -d "venv" ]; then
  echo -e "${YELLOW}[!] 새로운 가상환경 'venv' 생성 중...${NC}"
  python3 -m venv venv
fi

# Activate venv & install deps
source venv/bin/activate
echo -e "${GREEN}[*] pip 업그레이드 및 백엔드 패키지 의존성 설치...${NC}"
pip install --upgrade pip
pip install -r iiol/requirements/common.txt

# 4. Migrate database
echo -e "${GREEN}[*] Django 데이터베이스 마이그레이션 적용...${NC}"
python iiol/manage.py migrate

# 5. Trap function to kill background processes on Exit
BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  echo -e "\n${YELLOW}[*] 로컬 백엔드 및 프론트엔드 프로세스 종료 중...${NC}"
  if [ ! -z "$BACKEND_PID" ]; then
    kill $BACKEND_PID 2>/dev/null
  fi
  if [ ! -z "$FRONTEND_PID" ]; then
    kill $FRONTEND_PID 2>/dev/null
  fi
  
  # 데이터 유실 방지를 위해 DB 컨테이너는 유지하거나 정지
  echo -e "${YELLOW}[*] Docker 컨테이너 정리 (docker compose down)...${NC}"
  docker compose down
  
  echo -e "${GREEN}[✓] 로컬 구동 스크립트 정리 완료.${NC}"
  exit 0
}

# Trap Ctrl+C (SIGINT) and exit signals
trap cleanup INT TERM EXIT

# 6. Start Django Backend Server in background
echo -e "${GREEN}[*] Django 백엔드 API 서버를 백그라운드(8000포트)에서 시작합니다...${NC}"
python iiol/manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!

# 7. Start React Frontend Server (Vite)
echo -e "${GREEN}[*] Vite React 프론트엔드 서버를 백그라운드(5173포트)에서 시작합니다...${NC}"
npm run dev --prefix frontend &
FRONTEND_PID=$!

echo -e "${CYAN}--------------------------------------------------${NC}"
echo -e "${GREEN}[✓] 모든 서버 가동 완료!${NC}"
echo -e "${GREEN}  - 백엔드 API: http://localhost:8000${NC}"
echo -e "${GREEN}  - 프론트엔드 UI: http://localhost:5173${NC}"
echo -e "${CYAN}종료하려면 Ctrl+C를 누르세요. 서버 프로세스 및 컨테이너가 자동 정지됩니다.${NC}"
echo -e "${CYAN}--------------------------------------------------${NC}"

# Keep script alive to allow Trap handling
wait
