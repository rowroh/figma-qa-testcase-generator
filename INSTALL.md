# 🚀 설치 가이드

## 📋 시스템 요구사항

- Python 3.8 이상
- 최소 4GB RAM (대용량 Figma 파일 분석 시)
- 안정적인 인터넷 연결 (Figma API 호출)

## 🔧 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/your-org/figma-qa-testcase-generator.git
cd figma-qa-testcase-generator
```

### 2. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv figma_env

# 가상환경 활성화
# macOS/Linux:
source figma_env/bin/activate

# Windows:
# figma_env\Scripts\activate
```

### 3. 의존성 설치

```bash
# 기본 의존성 설치
pip install -r requirements.txt

# 개발 의존성 설치 (선택사항)
pip install -r requirements-dev.txt
```

### 4. 환경 설정

```bash
# .env 파일 생성
cp config/env_example.txt .env

# .env 파일 편집
nano .env
```

`.env` 파일에 Figma API 토큰 추가:
```
FIGMA_TOKEN=your_figma_personal_access_token_here
```

### 5. Figma API 토큰 발급

1. [Figma 계정 설정](https://www.figma.com/settings) 접속
2. "Personal access tokens" 섹션으로 이동
3. "Create new token" 클릭
4. 토큰 이름 입력 (예: "QA TestCase Generator")
5. 생성된 토큰을 `.env` 파일에 추가

## ✅ 설치 확인

### 빠른 테스트

```bash
# 빠른 시작 예제 실행
python examples/quick_start.py
```

### 명령행 도구 테스트

```bash
# 테스트용 Figma URL로 실행
python src/main.py "https://www.figma.com/design/your-figma-url" --verbose
```

### 단위 테스트 실행

```bash
# 기본 테스트
python -m pytest tests/ -v

# 커버리지 포함
python -m pytest tests/ --cov=src --cov-report=html
```

## 🛠️ 개발 환경 설정

### Pre-commit 훅 설정

```bash
# pre-commit 설치
pip install pre-commit

# 훅 설치
pre-commit install

# 전체 파일에 대해 실행
pre-commit run --all-files
```

### 코드 품질 도구

```bash
# 코드 포맷팅
black src/ tests/

# 린팅
flake8 src/ tests/

# 타입 체크
mypy src/

# Import 정렬
isort src/ tests/
```

## 📁 디렉토리 구조 생성

설치 후 필요한 디렉토리가 자동 생성되지 않는 경우:

```bash
# 출력 디렉토리 생성
mkdir -p output
mkdir -p logs

# 권한 설정 (macOS/Linux)
chmod 755 output logs
```

## 🔍 문제 해결

### 일반적인 문제

#### 1. Figma API 토큰 오류

```
❌ FIGMA_TOKEN이 설정되지 않았습니다.
```

**해결책:**
- `.env` 파일에 올바른 토큰이 설정되었는지 확인
- 토큰이 유효한지 Figma에서 확인

#### 2. 패키지 설치 오류

```
❌ pip install 실패
```

**해결책:**
```bash
# pip 업그레이드
pip install --upgrade pip

# 개별 패키지 설치
pip install requests pandas openpyxl python-dotenv

# 캐시 클리어
pip cache purge
```

#### 3. 권한 오류 (macOS/Linux)

```
❌ Permission denied
```

**해결책:**
```bash
# 실행 권한 부여
chmod +x src/main.py examples/quick_start.py

# 디렉토리 권한 확인
ls -la output/
```

#### 4. Python 버전 호환성

```
❌ Python 3.8+ required
```

**해결책:**
```bash
# Python 버전 확인
python --version

# pyenv 사용 (권장)
pyenv install 3.9.0
pyenv local 3.9.0
```

### 고급 문제

#### 1. 메모리 부족

대용량 Figma 파일 분석 시:

```bash
# 스크린샷 분석 비활성화
python src/main.py "figma-url" --no-screenshot

# 우선순위 필터링으로 테스트케이스 수 제한
python src/main.py "figma-url" --priority P1
```

#### 2. 네트워크 타임아웃

```python
# config/env_example.txt에서 설정 조정
REQUEST_TIMEOUT=60
MAX_RETRY_ATTEMPTS=5
```

#### 3. 로그 확인

```bash
# 로그 파일 확인
tail -f logs/figma_qa_generator.log

# 상세 로그 활성화
export LOG_LEVEL=DEBUG
python src/main.py "figma-url" --verbose
```

## 📦 패키지 설치 (선택사항)

개발 완료 후 패키지로 설치:

```bash
# 개발 모드 설치
pip install -e .

# 명령행 도구 사용
figma-qa "https://figma.com/your-url" -o output.xlsx

# 패키지 제거
pip uninstall figma-qa-testcase-generator
```

## 🔄 업데이트

```bash
# 저장소 업데이트
git pull origin main

# 의존성 업데이트
pip install -r requirements.txt --upgrade

# 설정 파일 업데이트 확인
diff config/env_example.txt .env
```

## 🐳 Docker 사용 (선택사항)

```bash
# Dockerfile 생성 예정
docker build -t figma-qa-generator .
docker run -e FIGMA_TOKEN=your_token figma-qa-generator
```

## 💡 다음 단계

설치 완료 후:

1. **[API 가이드](docs/API_GUIDE.md)** 읽기
2. **[빠른 시작 예제](examples/quick_start.py)** 실행
3. **실제 Figma URL**로 테스트
4. **팀 특화 키워드** 설정 (`config/keywords.json`)

## 📞 지원

설치 관련 문제가 있으면:

- **GitHub Issues**: 버그 리포트
- **Discussions**: 일반적인 질문
- **Wiki**: 상세 가이드

---

*Happy Testing! 🎯*
