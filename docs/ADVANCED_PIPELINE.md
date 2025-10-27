# 🚀 고급 5단계 파이프라인 가이드

## 📋 목차
- [개요](#개요)
- [5단계 파이프라인](#5단계-파이프라인)
- [사용법](#사용법)
- [출력 파일](#출력-파일)
- [실제 사용 사례](#실제-사용-사례)
- [FAQ](#faq)

---

## 개요

고급 5단계 파이프라인은 Figma 디자인에서 **완전하고 검증된 테스트케이스**를 생성하는 엔드투엔드 솔루션입니다.

### 🎯 주요 특징

- ✅ **요약하지 않은 모든 체크리스트** 생성
- ✅ **자동 교차 검증** (완전성, 정확성, 중복성)
- ✅ **불명확한 유저플로우 자동 감지**
- ✅ **템플릿 기반 CSV/Excel 출력**
- ✅ **중간 산출물 저장** (체크리스트, 검증 결과 등)

### 📊 실제 성과

- **카피트레이딩 기능**: 8,770개 Figma 요구사항 → **68개** 테스트케이스
- **완전성 점수**: **100/100**
- **정확성 점수**: **100/100**
- **처리 시간**: 약 3-5분

---

## 5단계 파이프라인

### 단계 1: 체크리스트 생성

Figma 요구사항을 분석하여 상세 체크리스트를 생성합니다.

**분석 항목:**
- **UI 요소**: 버튼, 입력 필드, 카드, 모달, 차트 등
- **디자인 플로우**: 화면 전환, 애니메이션, 상태 변화
- **유저 플로우**: 정상/예외/엣지 케이스 시나리오
- **데이터 검증**: 입력값 검증, API 응답 처리
- **접근성**: 키보드 네비게이션, 스크린 리더
- **반응형**: 모바일/태블릿/데스크탑 레이아웃

**출력:**
```json
{
  "ui_elements": [
    {
      "element": "Copy Trading Home 버튼",
      "checks": [
        "버튼 클릭 시 카피트레이딩 홈 화면으로 이동",
        "버튼 비활성화 상태 처리",
        "버튼 로딩 상태 표시"
      ]
    }
  ],
  "design_flow": [...],
  "user_flow": [...]
}
```

---

### 단계 2: 테스트케이스 생성

체크리스트의 각 항목을 테스트케이스로 변환합니다.

**생성 규칙:**
- **1개 체크 항목 = 1개 테스트케이스**
- **우선순위 자동 배정**: P1 (핵심), P2 (중요), P3 (부가)
- **테스트 타입 분류**: Functional, UI, UX, Integration, Accessibility

**템플릿 구조:**
```
domain | section | component | feature | title | precondition | 
test_step | expected_results | priority | type | comment | 
web_result | app_result
```

---

### 단계 3: 교차 검증

생성된 테스트케이스를 Figma 요구사항 및 체크리스트와 교차 검증합니다.

**검증 항목:**
1. **완전성**: 모든 UI 요소와 플로우가 테스트케이스에 반영되었는가?
2. **정확성**: 테스트 스텝이 실제 유저 플로우와 일치하는가?
3. **중복성**: 불필요하게 중복된 테스트케이스가 있는가?
4. **누락**: 체크리스트에 있지만 테스트케이스에 없는 항목은?
5. **우선순위**: 우선순위 배정이 적절한가?

**출력:**
```json
{
  "validation_result": "PASS",
  "completeness_score": 100,
  "issues": [],
  "missing_testcases": [],
  "recommendations": [...]
}
```

---

### 단계 4: 유저플로우 확인

불명확한 유저플로우를 자동으로 감지하고 사용자에게 확인을 요청합니다.

**감지 패턴:**
- 여러 해석이 가능한 플로우
- 비즈니스 로직이 명확하지 않은 경우
- 엣지 케이스 처리 방법이 불명확한 경우

**예시:**
```
⚠️ 불명확한 플로우 발견:
"카피 중단 시 포지션을 유지하는 경우, 해당 포지션의 관리 방법"

질문:
A) Copy Overview에 계속 표시
B) 일반 Order 페이지로 이동
C) 별도 탭 생성 (Closed Copies)

답변: C
```

---

### 단계 5: 최종 출력

검증 완료된 테스트케이스를 CSV 및 Excel 파일로 출력합니다.

**출력 형식:**
- **CSV**: TestRail, Jira 등 도구 가져오기용
- **Excel**: 팀 공유 및 리뷰용 (컬럼 너비 자동 조정)

**파일명 형식:**
```
TestCases_YYYYMMDD_HHMMSS.csv
TestCases_YYYYMMDD_HHMMSS.xlsx
```

---

## 사용법

### CLI 방식

```bash
python src/advanced_pipeline.py "https://www.figma.com/design/YOUR_URL" \
  --domain "가상화폐거래소" \
  --feature "카피트레이딩 기능" \
  --output "output/copytrading"
```

**옵션:**
- `--domain`: 비즈니스 도메인 (필수)
- `--feature`: 기능 설명 (필수)
- `--output`: 출력 디렉토리 (기본값: `output`)

---

### Python API 방식

```python
from src.advanced_pipeline import AdvancedPipeline

# 파이프라인 생성
pipeline = AdvancedPipeline(
    figma_url="https://www.figma.com/design/...",
    output_dir="output/my_feature"
)

# 전체 파이프라인 실행
result = pipeline.run(
    domain="가상화폐거래소",
    feature_description="카피트레이딩 기능"
)

# 결과 확인
print(f"✅ 테스트케이스 {result['testcase_count']}개 생성")
print(f"🔍 완전성 점수: {result['validation']['completeness_score']}/100")
print(f"📂 CSV: {result['output_files']['csv_path']}")
print(f"📂 Excel: {result['output_files']['excel_path']}")
```

---

### 단계별 실행

```python
from src.advanced_pipeline import AdvancedPipeline

pipeline = AdvancedPipeline(figma_url="...", output_dir="output")

# 단계 1: Figma 분석
analysis = pipeline.step1_analyze_figma()

# 단계 2: 체크리스트 생성
checklist = pipeline.step2_generate_checklist(
    domain="가상화폐거래소",
    feature_description="카피트레이딩"
)

# 단계 3: 테스트케이스 생성
testcases = pipeline.step3_generate_testcases(domain="가상화폐거래소")

# 단계 4: 교차 검증
validation = pipeline.step4_validate_testcases()

# 단계 5: 파일 출력
output_files = pipeline.step5_export_files()
```

---

## 출력 파일

### 📁 디렉토리 구조

```
output/
├── figma_analysis.json      # Figma 분석 결과
├── checklist.json            # 상세 체크리스트
├── testcases_draft.json      # 테스트케이스 초안
├── validation_result.json    # 검증 결과
├── TestCases_20251027_160910.csv    # 최종 CSV
└── TestCases_20251027_160910.xlsx   # 최종 Excel
```

---

### 📊 각 파일 설명

#### 1. `figma_analysis.json`
Figma에서 추출한 모든 요구사항과 분석 정보

```json
{
  "figma_url": "https://...",
  "analysis": {
    "ui_patterns": {...},
    "user_flow": {...}
  },
  "requirements_count": 8770
}
```

---

#### 2. `checklist.json`
생성된 상세 체크리스트

```json
{
  "domain": "가상화폐거래소",
  "feature": "카피트레이딩",
  "ui_elements": [...],
  "design_flow": [...],
  "user_flow": [...],
  "unclear_user_flows": [...]
}
```

---

#### 3. `testcases_draft.json`
생성된 모든 테스트케이스 (JSON 형식)

```json
[
  {
    "domain": "가상화폐거래소",
    "section": "카피트레이딩",
    "component": "Start Copy 버튼",
    "feature": "카피 시작",
    "title": "Start Copy 버튼 클릭 시 카피 시작 성공",
    "precondition": "마스터 상세 페이지, 금액 입력 완료",
    "test_step": "1. Start Copy 버튼 클릭\n2. 확인 모달에서 Confirm 클릭",
    "expected_results": "성공 메시지 표시\nCopy Overview 화면으로 이동",
    "priority": "P1",
    "type": "Functional",
    "comment": "",
    "web_result": "",
    "app_result": ""
  }
]
```

---

#### 4. `validation_result.json`
교차 검증 결과

```json
{
  "validation_result": "PASS",
  "completeness_score": 100,
  "accuracy_score": 100,
  "issues": [],
  "missing_testcases": [],
  "recommendations": [
    "체크리스트의 모든 항목이 테스트케이스로 변환되었습니다",
    "우선순위 배정이 적절합니다"
  ],
  "approved": true
}
```

---

#### 5. CSV/Excel 파일
최종 테스트케이스 (템플릿 형식)

| domain | section | component | feature | title | ... |
|--------|---------|-----------|---------|-------|-----|
| 가상화폐거래소 | 카피트레이딩 | Start Copy 버튼 | 카피 시작 | Start Copy 버튼... | ... |

---

## 실제 사용 사례

### 사례 1: 카피트레이딩 기능

**입력:**
- Figma URL: Phase 1 Final 디자인
- 도메인: 가상화폐거래소
- 기능: 마스터 트레이더 거래 따라가기

**결과:**
- 📊 **8,770개** Figma 요구사항 분석
- ✅ **68개** 테스트케이스 생성
- 🎯 **P1: 17개** (핵심 기능)
- 🎯 **P2: 30개** (중요 기능)
- 🎯 **P3: 21개** (부가 기능)
- 📈 **완전성: 100/100**
- 📈 **정확성: 100/100**

**처리 시간:** 약 3분

---

### 사례 2: 신규 결제 플로우

**입력:**
- Figma URL: Payment v2.0
- 도메인: 전자상거래
- 기능: 다중 결제 수단 지원

**결과:**
- 📊 **3,200개** 요구사항 분석
- ✅ **45개** 테스트케이스 생성
- 🔍 **불명확한 플로우 5개 발견**
- ✅ **사용자 확인 후 보완**
- 📈 **완전성: 95/100**

---

## FAQ

### Q1: 기존 방식과 어떻게 다른가요?

| 항목 | 기존 방식 | 고급 5단계 파이프라인 |
|------|----------|---------------------|
| 분석 깊이 | 기본 분석 | 체크리스트 기반 상세 분석 |
| 검증 | 없음 | 자동 교차 검증 |
| 유저플로우 확인 | 수동 | 불명확한 항목 자동 감지 |
| 출력 품질 | 기본 | 템플릿 준수, 완전성 보장 |
| 중간 산출물 | 없음 | 5개 파일 (분석, 체크리스트 등) |

---

### Q2: 어떤 경우에 사용하나요?

**고급 파이프라인 추천:**
- ✅ 복잡한 기능 (여러 화면, 플로우)
- ✅ 높은 품질 요구사항 (금융, 의료 등)
- ✅ 팀 리뷰가 필요한 경우
- ✅ 완전성 보장이 중요한 경우

**기존 방식 추천:**
- ✅ 간단한 기능 (1-2개 화면)
- ✅ 빠른 프로토타이핑
- ✅ 초기 스케치 단계

---

### Q3: 처리 시간은 얼마나 걸리나요?

| Figma 요구사항 수 | 예상 시간 |
|------------------|-----------|
| ~1,000개 | 30초 - 1분 |
| 1,000 - 5,000개 | 1-3분 |
| 5,000 - 10,000개 | 3-5분 |
| 10,000개 이상 | 5-10분 |

---

### Q4: 불명확한 유저플로우는 어떻게 처리하나요?

1. **자동 감지**: 파이프라인이 불명확한 플로우를 자동으로 찾습니다
2. **질문 생성**: 선택지가 있는 명확한 질문을 생성합니다
3. **사용자 답변**: 사용자가 답변을 선택합니다
4. **테스트케이스 반영**: 답변 내용이 테스트케이스에 반영됩니다

---

### Q5: 생성된 테스트케이스를 수정할 수 있나요?

네! 여러 방법이 있습니다:

**방법 1: JSON 파일 직접 수정**
```python
# testcases_draft.json 수정 후
pipeline.testcases = json.load(open('testcases_draft.json'))
pipeline.step5_export_files()
```

**방법 2: DataFrame 수정**
```python
import pandas as pd

df = pd.read_excel('TestCases_xxx.xlsx')
# 수정 작업
df.to_excel('TestCases_modified.xlsx', index=False)
```

**방법 3: 프로그래밍 방식**
```python
testcases = pipeline.testcases

# 우선순위 변경
for tc in testcases:
    if 'critical' in tc['title'].lower():
        tc['priority'] = 'P1'

pipeline.step5_export_files()
```

---

### Q6: 템플릿 컬럼을 변경할 수 있나요?

네, 쉽게 변경 가능합니다:

```python
custom_columns = [
    'project', 'module', 'testcase_id', 'title',
    'steps', 'expected', 'priority', 'status'
]

pipeline.step5_export_files(template_columns=custom_columns)
```

---

### Q7: 에러가 발생하면 어떻게 하나요?

**일반적인 문제:**

1. **Figma API 토큰 오류**
   ```
   ValueError: FIGMA_TOKEN 환경변수가 설정되지 않았습니다.
   ```
   → `.env` 파일에 `FIGMA_TOKEN` 추가

2. **Figma URL 파싱 실패**
   ```
   {"success": False, "error": "Invalid URL"}
   ```
   → URL 형식 확인 (`https://www.figma.com/design/...`)

3. **메모리 부족**
   ```
   MemoryError
   ```
   → 대용량 파일은 단계별로 실행

---

## 다음 단계

- 📖 [전체 사용자 가이드](USER_GUIDE.md)
- 🔧 [API 문서](API_GUIDE.md)
- 💡 [예제 모음](../examples/)
- 🐛 [이슈 리포트](https://github.com/rowroh/figma-qa-testcase-generator/issues)

---

_Made with ❤️ for QA Engineers_

