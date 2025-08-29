# 🔧 API 가이드

## FigmaAnalyzer 클래스

### 초기화

```python
from src.analyzers.figma_analyzer import FigmaAnalyzer

# 기본 초기화 (환경변수에서 토큰 로드)
analyzer = FigmaAnalyzer()

# 토큰 직접 지정
analyzer = FigmaAnalyzer(figma_token="your_token_here")
```

### 메소드

#### `basic_analysis(figma_url: str) -> Dict[str, Any]`

기본 키워드 분석 수행

**Parameters:**
- `figma_url`: 분석할 Figma URL

**Returns:**
```python
{
    "success": bool,
    "file_info": {
        "file_id": str,
        "node_id": str,
        "url": str
    },
    "requirements": [
        {
            "text": str,
            "type": str,  # "content" or "component"
            "depth": int
        }
    ],
    "analysis_type": "basic"
}
```

#### `enhanced_analysis(figma_url: str, include_screenshot: bool = True) -> Dict[str, Any]`

향상된 분석 수행 (키워드 + 스크린샷 + 플로우)

**Parameters:**
- `figma_url`: 분석할 Figma URL
- `include_screenshot`: 스크린샷 분석 포함 여부

**Returns:**
```python
{
    "success": bool,
    "file_info": {...},
    "basic_analysis": {
        "requirements_count": int,
        "requirements": [...]
    },
    "enhanced_analysis": {
        "keywords": {
            "detected_patterns": {
                "pattern_name": {
                    "matches": int,
                    "flow_type": str,
                    "confidence": int
                }
            },
            "total_elements": int
        },
        "ui_structure": {
            "ui_elements": {
                "buttons": [...],
                "inputs": [...],
                "navigation": [...],
                "containers": [...]
            },
            "ui_complexity": str  # "low", "medium", "high"
        },
        "user_flow": {
            "flow_steps": [str],
            "primary_flow_type": str,
            "confidence": int
        },
        "screenshot": {
            "success": bool,
            "image_url": str,
            "image_size": int,
            "complexity": str
        }
    },
    "recommendations": {
        "ui_improvements": [str],
        "testing_priorities": [str],
        "user_experience": [str]
    },
    "summary": {
        "total_elements": int,
        "ui_patterns": [str],
        "flow_type": str,
        "confidence": int,
        "ui_complexity": str
    }
}
```

#### `compare_screens(as_is_url: str, to_be_url: str) -> Dict[str, Any]`

AS-IS vs TO-BE 화면 비교 분석

**Parameters:**
- `as_is_url`: 기존 화면 Figma URL
- `to_be_url`: 개선된 화면 Figma URL

**Returns:**
```python
{
    "success": bool,
    "as_is": {...},  # summary
    "to_be": {...},  # summary
    "differences": {
        "new_patterns": [str],
        "removed_patterns": [str],
        "ui_complexity_change": {
            "from": str,
            "to": str
        }
    },
    "recommendations": [str]
}
```

---

## TestCaseGenerator 클래스

### 초기화

```python
from src.generators.testcase_generator import TestCaseGenerator

generator = TestCaseGenerator()
```

### 메소드

#### `generate_from_analysis(analysis_result: Dict, custom_scenarios: List[Dict] = None) -> List[Dict]`

분석 결과를 기반으로 테스트케이스 생성

**Parameters:**
- `analysis_result`: FigmaAnalyzer의 enhanced_analysis() 결과
- `custom_scenarios`: 커스텀 시나리오 (선택사항)

**Returns:**
```python
[
    {
        "domain": str,
        "section": str,
        "component": str,
        "feature": str,
        "title": str,
        "precondition": str,
        "test_steps": str,
        "expected_results": str,
        "priority": str,  # "P1", "P2", "P3", "P4"
        "type": str,      # "Functional", "UI", "Security", etc.
        "comment": str,
        "android_result": str,
        "ios_result": str
    }
]
```

#### `generate_scenarios(feature_config: Dict) -> List[Dict]`

시나리오 설정 기반 테스트케이스 생성

**Parameters:**
```python
feature_config = {
    "feature_name": str,
    "priority": str,
    "scenarios": [str]
}
```

#### `identify_missing_tests(existing_tests: List[Dict], analysis_result: Dict) -> List[Dict]`

누락된 테스트케이스 식별

**Parameters:**
- `existing_tests`: 기존 테스트케이스 목록
- `analysis_result`: Figma 분석 결과

#### `generate_by_priority(analysis_result: Dict, min_priority: str = "P1") -> List[Dict]`

우선순위 기반 테스트케이스 생성

**Parameters:**
- `analysis_result`: Figma 분석 결과
- `min_priority`: 최소 우선순위 ("P1", "P2", "P3", "P4")

### 저장 메소드

#### `save_to_excel(testcases: List[Dict], filename: str)`

Excel 형식으로 저장

#### `save_to_testrail_csv(testcases: List[Dict], filename: str)`

TestRail 가져오기용 CSV 형식으로 저장

#### `save_to_json(testcases: List[Dict], filename: str)`

JSON 형식으로 저장

---

## 사용 예제

### 기본 사용법

```python
from src.analyzers.figma_analyzer import FigmaAnalyzer
from src.generators.testcase_generator import TestCaseGenerator

# 1. 분석
analyzer = FigmaAnalyzer()
result = analyzer.enhanced_analysis("https://www.figma.com/design/...")

# 2. 테스트케이스 생성
generator = TestCaseGenerator()
testcases = generator.generate_from_analysis(result)

# 3. 저장
generator.save_to_excel(testcases, "output.xlsx")
```

### 우선순위 필터링

```python
# P1 테스트케이스만 생성
critical_tests = generator.generate_by_priority(result, "P1")
```

### 커스텀 시나리오

```python
custom_scenarios = [
    {
        "title": "커스텀 테스트",
        "priority": "P1",
        "type": "Functional",
        # ... 기타 필드
    }
]

testcases = generator.generate_from_analysis(result, custom_scenarios)
```

### AS-IS vs TO-BE 비교

```python
comparison = analyzer.compare_screens(
    "https://figma.com/as-is-url",
    "https://figma.com/to-be-url"
)

print(f"새로운 패턴: {comparison['differences']['new_patterns']}")
```

---

## 에러 처리

모든 메소드는 성공/실패 상태를 반환합니다:

```python
result = analyzer.enhanced_analysis(url)

if result.get("success"):
    # 성공 처리
    pass
else:
    # 에러 처리
    print(f"오류: {result.get('error')}")
```

---

## 설정

### 키워드 커스터마이징

`config/keywords.json` 파일을 수정하여 키워드를 커스터마이징할 수 있습니다:

```json
{
  "requirement_keywords": ["custom", "keywords"],
  "ui_patterns": {
    "custom_pattern": {
      "keywords": ["pattern", "keywords"],
      "flow_type": "custom_flow"
    }
  }
}
```

### 환경 변수

`.env` 파일에서 설정:

```
FIGMA_TOKEN=your_token
DEFAULT_PRIORITY=P2
DEFAULT_OUTPUT_FORMAT=excel
```
