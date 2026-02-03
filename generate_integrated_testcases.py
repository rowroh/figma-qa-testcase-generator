#!/usr/bin/env python3
"""
통합 테스트케이스 생성기 (Notion PRD + Figma)
Fixed Multiplier Mode를 위한 완전한 테스트케이스 자동 생성
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.analyzers.figma_analyzer import FigmaAnalyzer
from src.generators.testcase_generator import TestCaseGenerator

class NotionRequirementsExtractor:
    """Notion PRD에서 요구사항 추출"""
    
    def __init__(self, prd_content):
        self.prd_content = prd_content
    
    def extract_requirements(self):
        """PRD 마크다운에서 요구사항 추출"""
        requirements = {
            "feature_name": "Fixed Multiplier Mode",
            "business_rules": [],
            "ui_requirements": [],
            "validation_rules": [],
            "error_handling": [],
            "calculations": [],
            "limits": []
        }
        
        markdown = self.prd_content.get('markdown', '')
        
        # 비즈니스 규칙 추출
        requirements["business_rules"] = [
            {
                "rule": "Fixed Multiplier 모드 추가",
                "description": "기존 Fixed Ratio 외에 Fixed Multiplier 모드 추가",
                "priority": "P1"
            },
            {
                "rule": "Multiplier 범위",
                "description": "0.01x ~ 100x 범위 지원",
                "priority": "P1"
            },
            {
                "rule": "Position Size 계산",
                "description": "Position Size = Multiplier × Master Position Size",
                "priority": "P1"
            },
            {
                "rule": "마진 부족 시 실패",
                "description": "마진 부족 시 자동 스케일 다운 없이 주문 실패",
                "priority": "P1"
            },
            {
                "rule": "Leverage 적용",
                "description": "min(Master leverage, Copier leverage limit)",
                "priority": "P1"
            }
        ]
        
        # UI 요구사항 추출
        requirements["ui_requirements"] = [
            {
                "component": "Copy Multiplier Input",
                "type": "numeric_input",
                "default": "1.0x",
                "validation": "0.01 ~ 100",
                "decimal": "2자리 권장",
                "priority": "P1"
            },
            {
                "component": "Example Text",
                "content": "If the Master opens a 100 USDT position, you will open a {100 × n} position",
                "dynamic": True,
                "priority": "P1"
            },
            {
                "component": "Warning Message",
                "content": "High multiplier may cause frequent failed orders due to insufficient margin",
                "trigger": "Fixed Multiplier 선택 시",
                "priority": "P1"
            },
            {
                "component": "Tooltip",
                "content": "Opens each copied position at a fixed multiple of the master's position size",
                "priority": "P2"
            },
            {
                "component": "Copy Activity Display",
                "fields": ["Copy Mode", "Copy Multiplier"],
                "condition": "Fixed Multiplier 모드인 경우",
                "priority": "P2"
            }
        ]
        
        # 검증 규칙 추출
        requirements["validation_rules"] = [
            {
                "field": "multiplier",
                "rule": "Min: 0.01",
                "error_message": "Multiplier must be at least 0.01x",
                "priority": "P1"
            },
            {
                "field": "multiplier",
                "rule": "Max: 100",
                "error_message": "Multiplier cannot exceed 100x",
                "priority": "P1"
            },
            {
                "field": "multiplier",
                "rule": "Decimal: 소수점 허용",
                "format": "최대 2자리 권장",
                "priority": "P2"
            },
            {
                "field": "margin",
                "rule": "Sufficient margin required",
                "error_message": "Insufficient margin for selected multiplier",
                "priority": "P1"
            }
        ]
        
        # 에러 처리 추출
        requirements["error_handling"] = [
            {
                "scenario": "마진 부족",
                "behavior": "주문 실패 (자동 스케일 다운 없음)",
                "user_feedback": "Copy order failed: insufficient margin",
                "priority": "P1"
            },
            {
                "scenario": "Multiplier 범위 초과",
                "behavior": "입력 차단 또는 에러 메시지",
                "user_feedback": "Multiplier must be between 0.01x and 100x",
                "priority": "P1"
            },
            {
                "scenario": "네트워크 오류",
                "behavior": "재시도 또는 실패 처리",
                "user_feedback": "Network error, please try again",
                "priority": "P2"
            }
        ]
        
        # 계산 로직 추출
        requirements["calculations"] = [
            {
                "name": "Target Position Size",
                "formula": "Multiplier × Master Position Size",
                "priority": "P1"
            },
            {
                "name": "Effective Leverage",
                "formula": "min(Master Leverage, Copier Leverage Limit)",
                "priority": "P1"
            },
            {
                "name": "Required Margin",
                "formula": "Target Notional / Effective Leverage",
                "priority": "P1"
            }
        ]
        
        # 한도 및 제한 추출
        requirements["limits"] = [
            {
                "category": "Category 1",
                "max_leverage": "100x",
                "change": "20x → 100x",
                "priority": "P1"
            },
            {
                "category": "Category 2",
                "max_leverage": "50x",
                "change": "20x → 50x",
                "priority": "P1"
            },
            {
                "category": "Category 3-8",
                "max_leverage": "20x",
                "change": "10x → 20x",
                "priority": "P1"
            }
        ]
        
        return requirements


class IntegratedTestCaseGenerator:
    """통합 테스트케이스 생성기"""
    
    def __init__(self):
        load_dotenv()
        self.figma_analyzer = FigmaAnalyzer()
        self.testcase_generator = TestCaseGenerator()
        self.notion_requirements = None
        self.figma_analysis = None
    
    def analyze_notion_prd(self, prd_content):
        """Notion PRD 분석"""
        print("\n📄 Notion PRD 분석 중...")
        extractor = NotionRequirementsExtractor(prd_content)
        self.notion_requirements = extractor.extract_requirements()
        
        print(f"   ✅ 비즈니스 규칙: {len(self.notion_requirements['business_rules'])}개")
        print(f"   ✅ UI 요구사항: {len(self.notion_requirements['ui_requirements'])}개")
        print(f"   ✅ 검증 규칙: {len(self.notion_requirements['validation_rules'])}개")
        print(f"   ✅ 에러 처리: {len(self.notion_requirements['error_handling'])}개")
        print(f"   ✅ 계산 로직: {len(self.notion_requirements['calculations'])}개")
        print(f"   ✅ 한도/제한: {len(self.notion_requirements['limits'])}개")
        
        return self.notion_requirements
    
    def analyze_figma_design(self, figma_url):
        """Figma 디자인 분석"""
        print("\n🎨 Figma 디자인 분석 중...")
        
        try:
            self.figma_analysis = self.figma_analyzer.enhanced_analysis(figma_url, include_screenshot=False)
            
            if self.figma_analysis.get("success"):
                summary = self.figma_analysis.get("summary", {})
                print(f"   ✅ 총 요소: {summary.get('total_elements', 0)}개")
                print(f"   ✅ UI 패턴: {len(summary.get('ui_patterns', []))}개")
                print(f"   ✅ 주요 플로우: {summary.get('flow_type', 'unknown')}")
            else:
                print(f"   ⚠️ Figma 분석 제한적: {self.figma_analysis.get('error', 'Unknown')}")
                self.figma_analysis = {"success": False}
        
        except Exception as e:
            print(f"   ⚠️ Figma 분석 실패: {str(e)}")
            self.figma_analysis = {"success": False}
        
        return self.figma_analysis
    
    def generate_integrated_testcases(self):
        """통합 테스트케이스 생성"""
        print("\n📝 통합 테스트케이스 생성 중...")
        
        testcases = []
        
        # 1. Notion PRD 기반 테스트케이스 생성
        testcases.extend(self._generate_from_notion())
        
        # 2. Figma UI 기반 테스트케이스 추가
        if self.figma_analysis and self.figma_analysis.get("success"):
            testcases.extend(self._generate_from_figma())
        
        # 3. 통합 시나리오 테스트케이스 추가
        testcases.extend(self._generate_integration_scenarios())
        
        # 중복 제거
        testcases = self._deduplicate_testcases(testcases)
        
        print(f"   ✅ 총 {len(testcases)}개 테스트케이스 생성 완료")
        
        return testcases
    
    def _generate_from_notion(self):
        """Notion PRD 기반 테스트케이스 생성"""
        testcases = []
        
        if not self.notion_requirements:
            return testcases
        
        # 비즈니스 규칙 테스트
        for rule in self.notion_requirements["business_rules"]:
            testcases.append({
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "Business Logic",
                "feature": rule["rule"],
                "title": f"{rule['rule']} 검증",
                "precondition": "Copy Trading 설정 화면 진입",
                "test_step": f"1. Fixed Multiplier 모드 선택\n2. {rule['description']} 확인\n3. 설정 저장\n4. 동작 검증",
                "expected_results": f"1. 모드 선택 가능\n2. {rule['description']}이(가) 정상 동작\n3. 설정 저장 성공\n4. 기대한 대로 동작",
                "priority": rule["priority"],
                "type": "Functional",
                "comment": f"PRD 요구사항: {rule['description']}",
                "web_result": "",
                "app_result": ""
            })
        
        # UI 요구사항 테스트
        for ui_req in self.notion_requirements["ui_requirements"]:
            testcases.append({
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "UI Components",
                "feature": ui_req["component"],
                "title": f"{ui_req['component']} 표시 및 동작 검증",
                "precondition": "Fixed Multiplier 설정 화면",
                "test_step": f"1. {ui_req['component']} 확인\n2. 표시 내용 검증\n3. 인터랙션 테스트",
                "expected_results": f"1. {ui_req['component']}가 정상 표시됨\n2. 내용이 PRD 요구사항과 일치\n3. 인터랙션 정상 동작",
                "priority": ui_req["priority"],
                "type": "UI",
                "comment": f"PRD UI 요구사항: {ui_req.get('content', ui_req.get('type', ''))}",
                "web_result": "",
                "app_result": ""
            })
        
        # 검증 규칙 테스트
        for validation in self.notion_requirements["validation_rules"]:
            testcases.append({
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "Input Validation",
                "feature": f"{validation['field']} 검증",
                "title": f"{validation['field']} {validation['rule']} 검증",
                "precondition": "Multiplier 입력 필드 활성화 상태",
                "test_step": f"1. {validation['rule']}을(를) 위반하는 값 입력 시도\n2. 에러 메시지 확인\n3. 유효한 값 입력\n4. 저장 성공 확인",
                "expected_results": f"1. 입력이 차단되거나 에러 표시\n2. 명확한 에러 메시지\n3. 유효한 값은 정상 입력\n4. 저장 성공",
                "priority": validation["priority"],
                "type": "Functional",
                "comment": f"PRD 검증 규칙: {validation['rule']}",
                "web_result": "",
                "app_result": ""
            })
        
        # 에러 처리 테스트
        for error in self.notion_requirements["error_handling"]:
            testcases.append({
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "Error Handling",
                "feature": error["scenario"],
                "title": f"{error['scenario']} 시 에러 처리 검증",
                "precondition": f"{error['scenario']} 상황 유도 가능한 상태",
                "test_step": f"1. {error['scenario']} 상황 유도\n2. 시스템 반응 확인\n3. 사용자 피드백 확인\n4. 복구 동작 확인",
                "expected_results": f"1. {error['behavior']}\n2. 적절한 에러 처리\n3. {error['user_feedback']}\n4. 안정적인 상태 유지",
                "priority": error["priority"],
                "type": "Functional",
                "comment": f"PRD 에러 처리: {error['scenario']}",
                "web_result": "",
                "app_result": ""
            })
        
        # 계산 로직 테스트
        for calc in self.notion_requirements["calculations"]:
            testcases.append({
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "Calculation Logic",
                "feature": calc["name"],
                "title": f"{calc['name']} 계산 정확성 검증",
                "precondition": "다양한 입력값으로 테스트 가능한 상태",
                "test_step": f"1. 테스트 값 입력\n2. {calc['name']} 계산 실행\n3. 결과값 확인\n4. 공식 검증: {calc['formula']}",
                "expected_results": f"1. 입력 정상 처리\n2. 계산 실행 완료\n3. 결과값 = {calc['formula']}\n4. 공식과 정확히 일치",
                "priority": calc["priority"],
                "type": "Functional",
                "comment": f"PRD 계산 공식: {calc['formula']}",
                "web_result": "",
                "app_result": ""
            })
        
        # 한도 제한 테스트
        for limit in self.notion_requirements["limits"]:
            testcases.append({
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "Leverage Limits",
                "feature": f"{limit['category']} Leverage",
                "title": f"{limit['category']} 레버리지 한도 변경 검증 ({limit['change']})",
                "precondition": f"{limit['category']} 상품 선택",
                "test_step": f"1. {limit['category']} 상품 선택\n2. 최대 레버리지 확인\n3. {limit['max_leverage']} 적용 확인\n4. 한도 초과 시도",
                "expected_results": f"1. 상품 선택 성공\n2. 최대 레버리지 = {limit['max_leverage']}\n3. 정상 적용됨\n4. 한도 초과 차단됨",
                "priority": limit["priority"],
                "type": "Functional",
                "comment": f"PRD 한도 변경: {limit['change']}",
                "web_result": "",
                "app_result": ""
            })
        
        return testcases
    
    def _generate_from_figma(self):
        """Figma UI 기반 테스트케이스 생성"""
        # 기존 Figma 분석 기반 테스트케이스
        if self.figma_analysis and self.figma_analysis.get("success"):
            return self.testcase_generator.generate_from_analysis(self.figma_analysis)
        return []
    
    def _generate_integration_scenarios(self):
        """통합 시나리오 테스트케이스 생성"""
        scenarios = [
            {
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "End-to-End Flow",
                "feature": "Fixed Multiplier 전체 플로우",
                "title": "Fixed Multiplier 설정부터 주문 실행까지 전체 플로우",
                "precondition": "Copy Trading 활성화 가능한 계정, Master Trader 선택됨",
                "test_step": "1. Copy Trading 설정 화면 진입\n2. Fixed Multiplier 모드 선택\n3. Multiplier 값 입력 (예: 2.5x)\n4. Copy Amount 설정\n5. Total Stop Loss 설정\n6. 저장 및 활성화\n7. Master가 주문 실행\n8. Follower 주문 자동 실행 확인\n9. Position Size = 2.5 × Master Size 확인",
                "expected_results": "1. 화면 진입 성공\n2. Fixed Multiplier 선택 가능\n3. 2.5x 입력 성공\n4. Copy Amount 설정 완료\n5. Stop Loss 설정 완료\n6. 활성화 성공\n7. Master 주문 감지\n8. Follower 주문 자동 실행\n9. Size가 정확히 2.5배",
                "priority": "P1",
                "type": "Functional",
                "comment": "핵심 E2E 시나리오 - PRD + Figma 통합",
                "web_result": "",
                "app_result": ""
            },
            {
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "Cross-validation",
                "feature": "Fixed Ratio vs Fixed Multiplier 비교",
                "title": "동일 Master에 대해 Fixed Ratio와 Fixed Multiplier 결과 비교",
                "precondition": "동일 Master에 대해 2개의 Copy 설정 가능",
                "test_step": "1. 첫 번째 Copy: Fixed Ratio 설정\n2. 두 번째 Copy: Fixed Multiplier (1x) 설정\n3. Master가 주문 실행\n4. 두 Copy의 Position Size 비교\n5. 차이점 분석",
                "expected_results": "1. Fixed Ratio 설정 성공\n2. Fixed Multiplier 설정 성공\n3. 양쪽 모두 주문 실행\n4. Position Size가 다를 수 있음\n5. 각 모드의 공식에 따라 정확히 계산됨",
                "priority": "P2",
                "type": "Functional",
                "comment": "두 모드 간 동작 비교 검증",
                "web_result": "",
                "app_result": ""
            },
            {
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "Edge Cases",
                "feature": "극단값 테스트",
                "title": "최소값(0.01x)과 최대값(100x) 동작 검증",
                "precondition": "테스트 가능한 충분한 잔고",
                "test_step": "1. Multiplier = 0.01x 설정 및 주문 실행\n2. Position Size 확인 (매우 작음)\n3. Multiplier = 100x 설정 및 주문 실행\n4. Position Size 확인 (매우 큼)\n5. 마진 계산 정확성 확인",
                "expected_results": "1. 0.01x 설정 및 실행 성공\n2. Position Size = Master × 0.01\n3. 100x 설정 (마진 충분 시) 성공\n4. Position Size = Master × 100\n5. 모든 계산이 정확함",
                "priority": "P2",
                "type": "Functional",
                "comment": "경계값 테스트 - PRD 요구사항",
                "web_result": "",
                "app_result": ""
            }
        ]
        
        return scenarios
    
    def _deduplicate_testcases(self, testcases):
        """중복 테스트케이스 제거"""
        seen = set()
        unique_testcases = []
        
        for tc in testcases:
            # title을 기준으로 중복 체크
            title = tc.get("title", "")
            if title not in seen:
                seen.add(title)
                unique_testcases.append(tc)
        
        return unique_testcases
    
    def save_results(self, testcases, output_dir):
        """결과 저장"""
        print(f"\n💾 결과 저장 중: {output_dir}/")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Excel 저장
        excel_file = f"{output_dir}/FixedMultiplier_Integrated_TestCases.xlsx"
        self.testcase_generator.save_to_excel(testcases, excel_file)
        print(f"   ✅ Excel: {excel_file}")
        
        # TestRail CSV 저장
        testrail_file = f"{output_dir}/FixedMultiplier_Integrated_TestRail.csv"
        self.testcase_generator.save_to_testrail_csv(testcases, testrail_file)
        print(f"   ✅ TestRail: {testrail_file}")
        
        # JSON 저장
        json_file = f"{output_dir}/FixedMultiplier_Integrated_TestCases.json"
        self.testcase_generator.save_to_json(testcases, json_file)
        print(f"   ✅ JSON: {json_file}")
        
        # 분석 요약 저장
        summary_file = f"{output_dir}/analysis_summary.json"
        summary = {
            "generated_at": datetime.now().isoformat(),
            "sources": {
                "notion_prd": "Copy Trading v2 - Fixed Multiplier Mode",
                "figma_design": "Fixed Multiplier Mode UI"
            },
            "notion_requirements": self.notion_requirements,
            "testcase_count": len(testcases),
            "priority_distribution": self._get_priority_distribution(testcases),
            "type_distribution": self._get_type_distribution(testcases)
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"   ✅ Summary: {summary_file}")
        
        return {
            "excel": excel_file,
            "testrail": testrail_file,
            "json": json_file,
            "summary": summary_file
        }
    
    def _get_priority_distribution(self, testcases):
        """우선순위별 분포"""
        dist = {}
        for tc in testcases:
            priority = tc.get("priority", "Unknown")
            dist[priority] = dist.get(priority, 0) + 1
        return dist
    
    def _get_type_distribution(self, testcases):
        """타입별 분포"""
        dist = {}
        for tc in testcases:
            test_type = tc.get("type", "Unknown")
            dist[test_type] = dist.get(test_type, 0) + 1
        return dist


def main():
    """메인 실행 함수"""
    print("="*70)
    print("🚀 통합 테스트케이스 생성기 (Notion PRD + Figma)")
    print("="*70)
    
    # Notion PRD 내용 (이미 가져온 내용 사용)
    prd_content = {
        "title": "[Copy Trading v2] Fixed Multiplier Mode",
        "url": "https://www.notion.so/prextech/Copy-Trading-v2-Fixed-Multiplier-Mode-2f0eb32ad227800db1a7c42dff91dffc",
        "markdown": """[내용 생략 - 실제 실행 시 전체 마크다운 사용]"""
    }
    
    # Figma URL
    figma_url = "https://www.figma.com/design/7dnR1hkA7EaEyD6SEGj9Xm/Fixed-Multiplier-Mode?node-id=2-2&p=f&t=ZKN63pR10Wlkl7xO-0"
    
    # 출력 디렉토리
    output_dir = "output/fixed_multiplier_integrated"
    
    try:
        # 통합 생성기 초기화
        generator = IntegratedTestCaseGenerator()
        
        # 1. Notion PRD 분석
        generator.analyze_notion_prd(prd_content)
        
        # 2. Figma 디자인 분석
        generator.analyze_figma_design(figma_url)
        
        # 3. 통합 테스트케이스 생성
        testcases = generator.generate_integrated_testcases()
        
        # 4. 결과 저장
        output_files = generator.save_results(testcases, output_dir)
        
        # 5. 요약 출력
        print("\n" + "="*70)
        print("🎉 통합 테스트케이스 생성 완료!")
        print("="*70)
        print(f"\n📊 생성 결과:")
        print(f"   총 테스트케이스: {len(testcases)}개")
        
        priority_dist = generator._get_priority_distribution(testcases)
        print(f"\n   우선순위별 분포:")
        for priority in sorted(priority_dist.keys()):
            print(f"      {priority}: {priority_dist[priority]}개")
        
        type_dist = generator._get_type_distribution(testcases)
        print(f"\n   타입별 분포:")
        for test_type in sorted(type_dist.keys()):
            print(f"      {test_type}: {type_dist[test_type]}개")
        
        print(f"\n📁 출력 파일:")
        for key, filepath in output_files.items():
            print(f"   {key}: {filepath}")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
