# 🎯 Figma QA TestCase Generator

**시니어 QA 엔지니어를 위한 Figma 기반 테스트케이스 자동 생성 도구**

Figma 디자인을 분석하여 실무 중심의 테스트케이스를 자동으로 생성하는 AI 기반 도구입니다.

![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

---

## 🌟 **주요 기능**

### ✅ **룰세팅 기반 표준화 (NEW)**
- `config/rules_config.json`로 **출력 템플릿 컬럼/우선순위/커버리지/유저플로우 질문 정책**을 고정
- 결과 기록 컬럼을 **Web / (iOS+Android 통합)** 구조로 표준화:
  - `web_result`, `app_result`

### 🧾 **템플릿 기반 Excel 출력 (스타일 유지) (NEW)**
- 기본 템플릿: `templates/QA_Testcase_Template_WebApp.xlsx`
- `save_to_excel()`은 템플릿을 **복제한 뒤 데이터만 채워서** 헤더색/열너비/Freeze pane 등 스타일을 유지합니다.
- 템플릿 2행에는 `web_result/app_result` 작성 예시가 포함되어 있습니다.

### 🚀 **NEW: 고급 5단계 파이프라인** ⭐
- **단계 1**: 체크리스트 생성 (UI요소, 디자인플로우, 유저플로우 분석)
- **단계 2**: 체크리스트 기반 테스트케이스 자동 생성
- **단계 3**: 피그마 요구사항과 교차 검증
- **단계 4**: 불명확한 유저플로우 자동 감지 및 확인 요청
- **단계 5**: 템플릿 기반 CSV/Excel 최종 출력
- **특징**: 요약하지 않은 모든 체크리스트, 완전성 점수, 누락 항목 자동 탐지

### 🔍 **향상된 Figma 분석**
- **키워드 기반 분석**: UI 패턴, 플로우 패턴 자동 인식
- **스크린샷 분석**: 실제 이미지에서 시각적 복잡도 측정
- **유저플로우 추론**: 감지된 패턴 기반 사용자 여정 분석
- **UI 구조 분석**: 컴포넌트, 버튼, 입력필드 등 자동 분류

### 📝 **테스트케이스 자동 생성**
- **시나리오 기반**: 실제 사용자 행동 패턴 반영
- **우선순위 자동 설정**: P1/P2/P3 리스크 기반 분배
- **다양한 출력 형식**: Excel, TestRail CSV, JSON
- **커스터마이징 가능**: 팀별 테스트 표준에 맞춰 조정
- **교차 검증**: 완전성/정확성/중복성 자동 검증

### 🔄 **MCP 서버 통합**
- **도구 체인 통합**: 분석부터 생성까지 원스톱
- **실시간 처리**: 즉시 결과 확인 가능
- **확장 가능**: 새로운 분석 도구 쉽게 추가

### 🎯 **NEW: Notion PRD + Figma 통합 분석** ⭐⭐⭐
- **다중 소스 통합**: Notion PRD와 Figma 디자인을 동시 분석
- **완전한 커버리지**: 비즈니스 로직 + UI/UX + 계산 + 검증 + 에러 처리
- **자동 요구사항 추출**: PRD에서 비즈니스 규칙, 검증 규칙, 계산 로직 자동 추출
- **E2E 시나리오 생성**: 통합 분석 기반 End-to-End 시나리오 자동 생성
- **성과**: 테스트케이스 **173% 증가** (15개 → 41개), P1 케이스 **286% 증가**

---

## 🚀 **빠른 시작**

### **1. 설치**

```bash
# 저장소 클론
git clone https://github.com/rowroh/figma-qa-testcase-generator.git
cd figma-qa-testcase-generator

# 가상환경 생성 및 활성화
python -m venv figma_env
source figma_env/bin/activate  # Windows: figma_env\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### **2. 환경 설정**

```bash
# .env 파일 생성
cp config/env_example.txt .env

# Figma API 토큰 설정
echo "FIGMA_TOKEN=your_figma_token_here" >> .env
```

### **3. 기본 사용**

#### **🎯 NEW: Notion PRD + Figma 통합 (최고 성능)** ⭐⭐⭐

```bash
# Notion PRD와 Figma를 동시 분석하여 완전한 테스트케이스 생성
python generate_integrated_testcases.py

# 스크립트 내에서 설정 필요:
# - Notion PRD URL
# - Figma Design URL

# 결과:
# ✅ 41개 테스트케이스 (Figma만 대비 173% 증가)
# ✅ Notion PRD 기반: 비즈니스 규칙(5), UI 요구사항(5), 검증 규칙(4), 에러 처리(3), 계산 로직(3), 한도(3)
# ✅ Figma 기반: UI/UX 테스트케이스(12)
# ✅ 통합 시나리오: E2E, 비교, 극단값 테스트(3)
# ✅ Excel, TestRail CSV, JSON, 분석 요약 출력
```

**실제 사용 예시 (Fixed Multiplier Mode):**
```bash
# 1. Notion PRD에서 요구사항 추출
- 비즈니스 규칙: Multiplier 범위 (0.01x~100x)
- 계산 로직: Position Size = Multiplier × Master Size
- 검증 규칙: Min/Max 값, 소수점 입력
- 에러 처리: 마진 부족 시 실패

# 2. Figma에서 UI 분석
- UI 요소: 8,833개
- UI 패턴: navigation, form_input, modal, transaction 등

# 3. 통합 결과
- 총 41개 테스트케이스 생성
- P1: 27개 (핵심), P2: 14개 (일반)
- 커버리지: 비즈니스 로직 + UI/UX 완전 커버
```

#### **🚀 고급 5단계 파이프라인 (Figma만)** ⭐

```bash
# 전체 파이프라인 실행
python src/advanced_pipeline.py "https://www.figma.com/design/your-url" \
  --domain "가상화폐거래소" \
  --feature "카피트레이딩 기능" \
  --output "output/copytrading"

# 결과:
# ✅ 체크리스트 (checklist.json)
# ✅ 테스트케이스 초안 (testcases_draft.json)
# ✅ 검증 결과 (validation_result.json)
# ✅ 최종 CSV/Excel 파일
```

```python
# Python API 방식
from src.advanced_pipeline import AdvancedPipeline

pipeline = AdvancedPipeline(
    figma_url="https://www.figma.com/design/...",
    output_dir="output/my_feature"
)

result = pipeline.run(
    domain="가상화폐거래소",
    feature_description="카피트레이딩 기능"
)

print(f"✅ {result['testcase_count']}개 테스트케이스 생성 완료!")
print(f"📂 출력: {result['output_files']['excel_path']}")
```

#### **🔧 기존 CLI 방식 (간단한 케이스)**

```bash
# 기본 Excel 출력
python src/main.py "https://www.figma.com/design/your-figma-url"

# 룰세팅 지정 + 유저플로우 질문 출력
python src/main.py "https://www.figma.com/design/your-figma-url" \
  --rules "config/rules_config.json" \
  --show-flow-questions \
  --output "output/testcases.xlsx" \
  --verbose

# TestRail 가져오기용 CSV
python src/main.py "https://figma.com/design/your-url" \
  --format testrail --output "testrail_import.csv"

# P1 우선순위만 생성
python src/main.py "https://figma.com/design/your-url" \
  --priority P1 --verbose
```

#### **📝 기존 Python API 방식**

```python
from src.analyzers.figma_analyzer import FigmaAnalyzer
from src.generators.testcase_generator import TestCaseGenerator

# Figma 분석
analyzer = FigmaAnalyzer()
analysis = analyzer.enhanced_analysis("https://www.figma.com/design/...")

# 테스트케이스 생성
generator = TestCaseGenerator()
testcases = generator.generate_from_analysis(analysis)

# Excel 저장
generator.save_to_excel(testcases, "output/testcases.xlsx")
```

---

## 📊 **사용 방법 비교**

| 방법 | 데이터 소스 | 테스트케이스 수 | 커버리지 | 추천 시나리오 |
|------|------------|----------------|----------|--------------|
| **Notion + Figma 통합** ⭐⭐⭐ | PRD + 디자인 | **41개** | 비즈니스+UI+계산+검증 | **실제 프로젝트 (최고 성능)** |
| 고급 5단계 파이프라인 | Figma만 | 20~30개 | UI/UX + 체크리스트 | Figma만 있는 경우 |
| 기본 CLI | Figma만 | 15~20개 | UI/UX 기본 | 빠른 프로토타입 |
| Python API | 커스텀 | 변동 | 커스터마이징 가능 | 자동화/통합 |

**💡 추천:**
- ✅ **PRD + Figma 있음** → `generate_integrated_testcases.py` 사용 (**173% 더 많은 케이스**)
- ⚡ **Figma만 있음** → `src/advanced_pipeline.py` 또는 `src/main.py` 사용
- 🔧 **자동화 필요** → Python API 직접 사용

---

## 📖 **사용법**

> **💡 완전한 사용법 가이드: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)**  
> **🚀 빠른 데모: `python quick_demo.py`**

### ✅ 결과 기록 규칙 (web_result / app_result)

- `web_result`: Web 실행 결과 기록
- `app_result`: iOS+Android 결과를 통합 기록
- 권장 포맷 예시:
  - `Pass`
  - `Fail | BUG-1234 | 실제: ... | 기대: ...`
  - `Blocked | DATA | 테스트 데이터 부족`

자세한 규칙은 `docs/USER_GUIDE.md` 및 `config/rules_config.json`의 `result_recording_rules`를 참고하세요.

### **🔍 Figma 분석하기**

```python
# 기본 분석
result = analyzer.basic_analysis(figma_url)

# 향상된 분석 (키워드 + 스크린샷 + 플로우)
result = analyzer.enhanced_analysis(figma_url, include_screenshot=True)

# 분석 결과 확인
print(f"감지된 UI 패턴: {result['ui_patterns']}")
print(f"추론된 플로우: {result['user_flow']['flow_steps']}")
```

### **📝 테스트케이스 생성하기**

```python
# 시나리오 기반 생성
testcases = generator.generate_scenarios({
    "feature_name": "X OAuth 연동",
    "priority": "P1",
    "scenarios": [
        "정상 연동 플로우",
        "앱 미설치 상황",
        "연동 실패 처리"
    ]
})

# 다양한 형식으로 저장
generator.save_to_excel(testcases, "output.xlsx")
generator.save_to_testrail_csv(testcases, "testrail.csv")
generator.save_to_json(testcases, "testcases.json")
```

### **🎯 실제 사용 사례**

```python
# 1. TO-BE vs AS-IS 비교 분석
comparison = analyzer.compare_screens(as_is_url, to_be_url)

# 2. 누락된 테스트케이스 식별
missing_tests = generator.identify_missing_tests(existing_tests, analysis)

# 3. 우선순위 기반 테스트 생성
priority_tests = generator.generate_by_priority(analysis, min_priority="P1")
```

---

## 🏗️ **프로젝트 구조**

```
figma-qa-testcase-generator/
├── src/
│   ├── analyzers/           # Figma 분석 엔진
│   │   ├── figma_analyzer.py
│   ├── generators/          # 테스트케이스 생성 엔진
│   │   ├── testcase_generator.py
│   ├── utils/              # 유틸리티 함수들
│   │   └── rules_config.py
│   ├── advanced_pipeline.py # 5단계 파이프라인
│   └── main.py             # CLI 엔트리포인트
├── config/
│   ├── env_example.txt
│   ├── keywords.json        # 키워드 설정
│   └── rules_config.json    # 룰세팅(템플릿/우선순위/결과기록 규칙)
├── templates/
│   └── QA_Testcase_Template_WebApp.xlsx  # web/app 결과 컬럼 포함 템플릿
├── examples/
│   ├── figma_samples/      # 예제 Figma 링크들
│   ├── output_samples/     # 생성된 테스트케이스 샘플
│   └── tutorials/          # 사용법 튜토리얼
├── docs/                   # 상세 문서
├── tests/                  # 테스트 코드
└── mcp_figma_server.py      # MCP 서버
```

---

## 🎯 **핵심 특징**

### **✅ 거래소 특화 QA 도구**
- 모바일 앱(iOS/Android) 및 웹 기능 테스트에 최적화
- 크로스 플랫폼 호환성 자동 고려
- 접근성 및 사용성 테스트 포함

### **✅ 실무 중심 설계**
- 비즈니스 임팩트 기반 우선순위 설정
- 엣지 케이스 및 오류 상황 자동 커버
- 유저플로우 시나리오 기반 테스트 설계

### **✅ AI 기반 지능형 분석**
- UI 패턴 자동 인식 (navigation, authentication, form_input 등)
- 플로우 패턴 감지 (onboarding, purchasing, verification 등)
- 사용자 행동 패턴 예측 및 잠재적 문제점 식별

---

## 📊 **지원하는 분석 패턴**

### **UI 패턴 (7종)**
- **Navigation**: 네비게이션, 메뉴, 탭
- **Authentication**: 로그인, 회원가입, OAuth
- **Form Input**: 입력 폼, 텍스트 필드
- **Modal/Popup**: 팝업, 다이얼로그
- **Transaction**: 거래, 결제, 주문
- **Social**: 소셜 연동, 공유
- **Settings**: 설정, 프로필 관리

### **플로우 패턴 (6종)**
- **Onboarding**: 온보딩, 튜토리얼
- **Purchasing**: 구매, 결제 플로우
- **Registration**: 회원가입, 계정 생성
- **Verification**: 검증, 확인 프로세스
- **Error Handling**: 오류 처리
- **Success**: 성공 완료 플로우

---

## 🔧 **고급 설정**

### **키워드 커스터마이징**

```json
// config/keywords.json
{
  "requirement_keywords": [
    "거래", "주문", "결제", "인증", "로그인",
    "buy", "sell", "trade", "auth", "login"
  ],
  "ui_patterns": {
    "custom_pattern": {
      "keywords": ["custom", "특별한"],
      "flow_type": "custom_flow"
    }
  }
}
```

### **테스트 템플릿 설정**

룰세팅/템플릿 컬럼/결과 기록 규칙은 `config/rules_config.json`에서 관리합니다.

---

## 📈 **실제 성과**

### **프로젝트 적용 사례**

#### **🎯 Fixed Multiplier Mode (Notion PRD + Figma 통합)** ⭐ NEW
- **데이터 소스**: Notion PRD + Figma 디자인
- **테스트케이스**: Figma만 **15개** → 통합 **41개** (**+173% 증가**)
- **P1 핵심 케이스**: **7개** → **27개** (**+286% 증가**)
- **커버리지**: 
  - Figma만: UI/UX 패턴만
  - 통합: 비즈니스 로직 + UI/UX + 계산 + 검증 + 에러 처리 (**완전 커버**)
- **자동 추출 요구사항**: 비즈니스 규칙(5), UI 요구사항(5), 검증 규칙(4), 에러 처리(3), 계산 로직(3), 한도(3)
- **통합 시나리오**: E2E 플로우, 모드 비교, 극단값 테스트 자동 생성

#### **X OAuth 연동 (Figma만)**
- **테스트케이스**: 24개 → 35개 (중복 제거 + 누락 기능 추가)
- **TO-BE 커버리지**: 30% → 100% 달성
- **테스트 효율성**: 수동 작성 대비 **70% 시간 단축**

### **품질 향상**
- **누락 시나리오 0%**: AI 분석으로 놓치기 쉬운 케이스 자동 발견
- **일관된 우선순위**: 리스크 기반 체계적 분류
- **표준화된 구조**: 팀 간 테스트케이스 품질 균일화
- **다중 소스 통합**: PRD + Figma 통합으로 **완전한 테스트 커버리지** 달성

---

## 🛠️ **개발 환경**

### **요구사항**
- Python 3.8+
- Figma API 토큰
- 최소 4GB RAM (대용량 Figma 파일 분석 시)

### **개발 설정**

```bash
# 개발 의존성 설치
pip install -r requirements-dev.txt

# 테스트 실행
python -m pytest tests/

# 코드 포맷팅
black src/
flake8 src/
```

---

## 🤝 **기여하기**

### **기여 방법**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### **개발 가이드라인**
- 코드 스타일: Black + Flake8
- 테스트 커버리지: 80% 이상 유지
- 문서화: 새로운 기능은 반드시 문서 업데이트

---

## 📝 **라이선스**

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

---

## 📞 **지원 및 문의**

- **GitHub Issues**: 버그 리포트 및 기능 요청
- **Wiki**: 상세 사용법 및 FAQ
- **Discussions**: 커뮤니티 Q&A

---

## 🎉 **시작해보세요!**

```bash
# 프로젝트 클론
git clone https://github.com/rowroh/figma-qa-testcase-generator.git

# 빠른 테스트
cd figma-qa-testcase-generator
python examples/quick_start.py
```

**몇 분 만에 Figma 디자인에서 완전한 테스트케이스 스위트를 생성하세요!** 🚀

---

*Made with ❤️ for QA Engineers*
