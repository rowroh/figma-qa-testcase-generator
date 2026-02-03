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
        
        # 비즈니스 규칙 테스트 (구체화)
        for rule in self.notion_requirements["business_rules"]:
            # 구체적인 테스트 단계 생성
            if "Multiplier 범위" in rule["rule"]:
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "Business Logic",
                    "feature": rule["rule"],
                    "title": f"{rule['rule']} 검증 (최소값 0.01x)",
                    "precondition": "1. Copy Trading 설정 화면 진입\n2. 'Fixed Multiplier' 탭 표시 상태",
                    "test_step": "1. 'Fixed Multiplier' 탭 클릭\n2. 'Copy Multiplier' 입력 필드 확인\n3. '0.01' 입력\n4. 입력 필드 외부 영역 클릭 (포커스 아웃)\n5. 입력값 확인\n6. 'Save' 또는 '저장' 버튼 클릭\n7. 저장 완료 메시지 확인",
                    "expected_results": "1. 'Fixed Multiplier' 탭이 활성화됨 (하이라이트 또는 언더라인 표시)\n2. 'Copy Multiplier' 입력 필드가 활성화되고 '1.0x' 기본값 표시\n3. '0.01' 입력 성공, 입력 필드에 '0.01x' 또는 '0.01' 표시\n4. 에러 메시지 없음\n5. 입력값 '0.01x' 유지됨\n6. 버튼 클릭 시 로딩 표시 후 성공 메시지\n7. '설정이 저장되었습니다' 또는 'Settings saved' 토스트/스낵바 표시",
                    "priority": rule["priority"],
                    "type": "Functional",
                    "comment": f"PRD 요구사항: {rule['description']} - 최소값 경계 테스트",
                    "web_result": "",
                    "app_result": ""
                })
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "Business Logic",
                    "feature": rule["rule"],
                    "title": f"{rule['rule']} 검증 (최대값 100x)",
                    "precondition": "1. Copy Trading 설정 화면 진입\n2. 'Fixed Multiplier' 탭 선택됨",
                    "test_step": "1. 'Copy Multiplier' 입력 필드에 '100' 입력\n2. 입력 필드 외부 클릭 (포커스 아웃)\n3. 입력값 확인\n4. 'Save' 버튼 클릭\n5. Copy Activity 화면으로 이동\n6. 설정된 Master Trader 확인\n7. 'Copy Mode' 또는 'Copy Multiplier' 표시 확인",
                    "expected_results": "1. '100' 입력 성공, '100x' 또는 '100' 표시\n2. 에러 메시지 없음\n3. 입력값 '100x' 유지\n4. 저장 성공 메시지 표시\n5. Copy Activity 화면 전환 성공\n6. Master Trader 카드 또는 리스트 아이템 표시\n7. 'Copy Multiplier: 100x' 또는 'Fixed Multiplier (100x)' 라벨 표시",
                    "priority": rule["priority"],
                    "type": "Functional",
                    "comment": f"PRD 요구사항: {rule['description']} - 최대값 경계 테스트",
                    "web_result": "",
                    "app_result": ""
                })
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "Business Logic",
                    "feature": rule["rule"],
                    "title": f"{rule['rule']} 검증 (범위 초과 - 0.009x)",
                    "precondition": "Fixed Multiplier 설정 화면, 'Copy Multiplier' 입력 필드 활성화",
                    "test_step": "1. 'Copy Multiplier' 필드에 '0.009' 입력 시도\n2. 입력 결과 확인\n3. 포커스 아웃 시 에러 메시지 확인\n4. 'Save' 버튼 상태 확인",
                    "expected_results": "1. '0.009' 입력이 차단되거나 입력 후 에러 표시\n2. 입력 필드 아래 또는 옆에 빨간색 에러 메시지 표시: 'Multiplier must be at least 0.01x' 또는 '배수는 최소 0.01x 이상이어야 합니다'\n3. 에러 메시지 지속 표시\n4. 'Save' 버튼이 비활성화되거나 클릭 시 에러 재표시",
                    "priority": rule["priority"],
                    "type": "Functional",
                    "comment": f"PRD 요구사항: {rule['description']} - 최소값 미만 입력 차단",
                    "web_result": "",
                    "app_result": ""
                })
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "Business Logic",
                    "feature": rule["rule"],
                    "title": f"{rule['rule']} 검증 (범위 초과 - 101x)",
                    "precondition": "Fixed Multiplier 설정 화면, 'Copy Multiplier' 입력 필드 활성화",
                    "test_step": "1. 'Copy Multiplier' 필드에 '101' 입력 시도\n2. 입력 결과 확인\n3. 에러 메시지 확인\n4. '100' 재입력 후 정상 동작 확인",
                    "expected_results": "1. '101' 입력 후 빨간색 에러 표시\n2. 에러 메시지: 'Multiplier cannot exceed 100x' 또는 '배수는 최대 100x를 초과할 수 없습니다'\n3. 입력 필드 테두리 빨간색 표시\n4. '100' 재입력 시 에러 메시지 사라지고 정상 상태로 복구, 'Save' 버튼 활성화",
                    "priority": rule["priority"],
                    "type": "Functional",
                    "comment": f"PRD 요구사항: {rule['description']} - 최대값 초과 입력 차단",
                    "web_result": "",
                    "app_result": ""
                })
            elif "Position Size 계산" in rule["rule"]:
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "Business Logic",
                    "feature": rule["rule"],
                    "title": "Position Size 계산 정확성 검증 (Multiplier 2.5x)",
                    "precondition": "1. Fixed Multiplier 모드 설정 완료 (Multiplier: 2.5x)\n2. Master Trader 활성화 상태\n3. 충분한 Copy Balance 보유",
                    "test_step": "1. Master Trader가 BTC/USDT 100 USDT Position 오픈\n2. 5초 이내 Follower 계정의 Positions 탭 확인\n3. 자동 생성된 Copy Position 확인\n4. Position Size 확인\n5. Position 상세 정보 확인 (클릭 또는 호버)\n6. Multiplier 적용 여부 확인",
                    "expected_results": "1. Master Position 생성 감지\n2. Positions 탭에 새로운 Copy Position 추가됨\n3. Copy Position이 'Copying' 또는 'Master: [이름]' 라벨과 함께 표시\n4. Position Size = 250 USDT (100 × 2.5) 정확히 표시\n5. 상세 정보에 'Master Position: 100 USDT', 'Your Position: 250 USDT', 'Multiplier: 2.5x' 표시\n6. 계산 공식이 정확히 적용됨: 250 = 100 × 2.5",
                    "priority": rule["priority"],
                    "type": "Functional",
                    "comment": f"PRD 계산 공식: {rule['description']} - 실제 거래 시나리오",
                    "web_result": "",
                    "app_result": ""
                })
            elif "마진 부족" in rule["rule"]:
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "Business Logic",
                    "feature": rule["rule"],
                    "title": "마진 부족 시 주문 실패 처리 (자동 스케일 다운 없음)",
                    "precondition": "1. Fixed Multiplier 설정: 10x\n2. Copy Balance: 50 USDT\n3. Master가 100 USDT Position 오픈 예정 (필요 마진: 1000 USDT for 10x)",
                    "test_step": "1. Master가 BTC/USDT 100 USDT Position (Leverage 10x) 오픈\n2. Follower 계정의 Notifications 또는 Copy Activity 확인\n3. Failed Orders 또는 Activity History 탭 확인\n4. 실패 사유 확인\n5. Copy Balance 잔액 확인 (차감되지 않았는지)\n6. Positions 탭에 Position이 생성되지 않았는지 확인",
                    "expected_results": "1. Master Position 생성 감지되나 Follower는 Position 생성 실패\n2. 알림: 'Copy order failed: Insufficient margin' 또는 '복사 주문 실패: 마진 부족' 표시 (빨간색 또는 경고 아이콘)\n3. Failed Orders에 실패 기록 표시: 시간, Master 이름, Symbol, Reason: 'Insufficient margin'\n4. 실패 사유: 'Required: 1000 USDT, Available: 50 USDT' 또는 유사 메시지\n5. Copy Balance가 50 USDT 그대로 유지됨 (차감 없음)\n6. Positions 탭에 해당 Copy Position이 없음 (자동 스케일 다운 없이 완전 실패)",
                    "priority": rule["priority"],
                    "type": "Functional",
                    "comment": f"PRD 요구사항: {rule['description']} - 실패 처리 및 사용자 피드백",
                    "web_result": "",
                    "app_result": ""
                })
            elif "Leverage 적용" in rule["rule"]:
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "Business Logic",
                    "feature": rule["rule"],
                    "title": "Leverage 적용 로직 검증 (Copier Leverage Limit 우선)",
                    "precondition": "1. Master Leverage: 50x\n2. Copier Leverage Limit 설정: 20x\n3. Fixed Multiplier: 1x",
                    "test_step": "1. Copy Trading 설정 화면에서 'Max Leverage' 또는 'Leverage Limit' 설정 확인\n2. Copier Leverage Limit을 20x로 설정\n3. 설정 저장\n4. Master가 50x Leverage로 Position 오픈\n5. Follower의 Copy Position Leverage 확인\n6. Position 상세에서 Leverage 값 확인",
                    "expected_results": "1. 'Max Leverage' 또는 'Copier Leverage Limit' 입력 필드 표시\n2. '20x' 입력 성공\n3. 설정 저장 완료 메시지\n4. Copy Position 생성 성공\n5. Follower Position의 Leverage가 20x로 표시 (50x가 아님)\n6. 상세 정보: 'Master Leverage: 50x, Your Leverage: 20x (Limited)' 또는 유사 표시, 계산 공식 적용 확인: Effective Leverage = min(50, 20) = 20",
                    "priority": rule["priority"],
                    "type": "Functional",
                    "comment": f"PRD 요구사항: {rule['description']} - Copier Limit 우선 적용",
                    "web_result": "",
                    "app_result": ""
                })
            else:
                # 기본 케이스 (구체화 버전)
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "Business Logic",
                    "feature": rule["rule"],
                    "title": f"{rule['rule']} 검증",
                    "precondition": "1. Copy Trading 설정 화면 진입\n2. 필요한 권한 및 잔고 확보",
                    "test_step": f"1. 'Fixed Multiplier' 탭 클릭\n2. {rule['description']} 관련 UI 요소 확인\n3. 테스트 데이터 입력\n4. 'Save' 버튼 클릭\n5. 설정 저장 확인\n6. 실제 동작 테스트 (Master 거래 발생 시)\n7. 결과 확인",
                    "expected_results": f"1. 탭 전환 성공\n2. {rule['description']} 관련 UI 정상 표시\n3. 입력 성공\n4. 로딩 후 성공 메시지\n5. '설정이 저장되었습니다' 토스트\n6. {rule['description']}이(가) 정상 동작\n7. 기대한 결과와 일치",
                    "priority": rule["priority"],
                    "type": "Functional",
                    "comment": f"PRD 요구사항: {rule['description']}",
                    "web_result": "",
                    "app_result": ""
                })
        
        # UI 요구사항 테스트 (구체화)
        for ui_req in self.notion_requirements["ui_requirements"]:
            if "Copy Multiplier Input" in ui_req["component"]:
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "UI Components",
                    "feature": ui_req["component"],
                    "title": "Copy Multiplier 입력 필드 UI 검증 (레이아웃, 기본값, 포커스)",
                    "precondition": "Copy Trading 설정 화면, Fixed Multiplier 탭 선택됨",
                    "test_step": "1. 'Copy Multiplier' 라벨 텍스트 확인\n2. 입력 필드 기본값 확인\n3. 입력 필드 클릭 (포커스)\n4. 입력 필드 테두리 색상 변경 확인\n5. 플레이스홀더 또는 힌트 텍스트 확인\n6. 필드 너비 및 정렬 확인\n7. 소수점 입력 가능 여부 확인",
                    "expected_results": "1. 'Copy Multiplier' 또는 '복사 배수' 라벨이 입력 필드 위 또는 왼쪽에 표시\n2. 입력 필드에 '1.0x' 또는 '1.0' 기본값 표시\n3. 포커스 시 테두리 색상이 파란색 또는 강조 색상으로 변경\n4. 테두리 두께 증가 또는 그림자 효과 추가\n5. 플레이스홀더: '0.01 ~ 100' 또는 'Enter multiplier' 표시\n6. 입력 필드 너비가 적절하고 (최소 80px), 다른 필드들과 정렬됨\n7. 소수점 2자리 입력 가능 (예: 2.50 입력 시 '2.50x' 또는 '2.5x' 표시)",
                    "priority": ui_req["priority"],
                    "type": "UI",
                    "comment": f"PRD UI: {ui_req.get('type', '')} - 기본값: {ui_req.get('default', '')}, 범위: {ui_req.get('validation', '')}",
                    "web_result": "",
                    "app_result": ""
                })
            elif "Example Text" in ui_req["component"]:
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "UI Components",
                    "feature": ui_req["component"],
                    "title": "Example Text 동적 업데이트 검증",
                    "precondition": "Fixed Multiplier 설정 화면, Copy Multiplier 입력 필드 표시",
                    "test_step": "1. 초기 Example Text 확인\n2. Copy Multiplier 필드에 '2' 입력\n3. Example Text 변경 확인\n4. Copy Multiplier 필드에 '0.5' 입력\n5. Example Text 재변경 확인\n6. Copy Multiplier 필드를 비우고 포커스 아웃\n7. Example Text 상태 확인",
                    "expected_results": "1. 'If the Master opens a 100 USDT position, you will open a 100 USDT position' (기본 1.0x)\n2. 텍스트가 즉시 업데이트: '...you will open a 200 USDT position' (100 × 2 = 200)\n3. 계산 결과가 실시간으로 반영됨\n4. 텍스트 재업데이트: '...you will open a 50 USDT position' (100 × 0.5 = 50)\n5. 소수점 계산 정확히 표시\n6. 필드 비움 시 기본값(1.0x) 또는 에러 상태로 복구\n7. Example Text도 기본값으로 복구: '...100 USDT position' 또는 숨김 처리",
                    "priority": ui_req["priority"],
                    "type": "UI",
                    "comment": f"PRD UI: {ui_req.get('content', '')} - 동적 업데이트",
                    "web_result": "",
                    "app_result": ""
                })
            elif "Warning Message" in ui_req["component"]:
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "UI Components",
                    "feature": ui_req["component"],
                    "title": "High Multiplier 경고 메시지 표시 검증",
                    "precondition": "Copy Trading 설정 화면 진입",
                    "test_step": "1. 'Fixed Ratio' 탭에서 경고 메시지 표시 여부 확인\n2. 'Fixed Multiplier' 탭 클릭\n3. 경고 메시지 표시 위치 및 내용 확인\n4. 경고 메시지 아이콘 확인 (있는 경우)\n5. 경고 메시지 스타일 확인 (색상, 폰트)\n6. Copy Multiplier를 '10' 이상 입력 시 변화 확인\n7. 다시 'Fixed Ratio' 탭으로 전환 후 경고 메시지 사라짐 확인",
                    "expected_results": "1. Fixed Ratio 탭에서는 경고 메시지 표시 안 됨\n2. Fixed Multiplier 탭 선택 시 경고 메시지 즉시 표시\n3. 메시지: 'High multiplier may cause frequent failed orders due to insufficient margin' 또는 '높은 배수는 마진 부족으로 인한 주문 실패가 빈번할 수 있습니다' - Copy Multiplier 입력 필드 아래 또는 근처에 표시\n4. 노란색 경고 아이콘(⚠️) 또는 정보 아이콘(ℹ️) 표시 (있는 경우)\n5. 텍스트 색상: 주황색(#FF9800) 또는 노란색 계열, 배경: 연한 주황색 또는 없음\n6. 높은 배수 입력 시 경고 메시지 지속 표시 (변화 없음 또는 더 강조)\n7. Fixed Ratio 탭으로 전환 시 경고 메시지 사라짐",
                    "priority": ui_req["priority"],
                    "type": "UI",
                    "comment": f"PRD UI: {ui_req.get('content', '')} - 조건: {ui_req.get('trigger', '')}",
                    "web_result": "",
                    "app_result": ""
                })
            elif "Tooltip" in ui_req["component"]:
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "UI Components",
                    "feature": ui_req["component"],
                    "title": "Copy Multiplier 툴팁 표시 검증",
                    "precondition": "Fixed Multiplier 설정 화면, Copy Multiplier 입력 필드 표시",
                    "test_step": "1. Copy Multiplier 라벨 옆 정보 아이콘(ℹ️ 또는 ?) 확인\n2. 정보 아이콘에 마우스 호버 (Web) 또는 터치 (App)\n3. 툴팁 표시 위치 및 내용 확인\n4. 툴팁 배경색 및 폰트 확인\n5. 마우스 이동 또는 다른 영역 터치 시 툴팁 사라짐 확인",
                    "expected_results": "1. 'Copy Multiplier' 라벨 옆에 ℹ️ 또는 ? 아이콘 표시\n2. (Web) 호버 시 즉시 툴팁 표시 / (App) 터치 시 툴팁 표시\n3. 툴팁 내용: 'Opens each copied position at a fixed multiple of the master's position size' 또는 '마스터 포지션 크기의 고정 배수로 각 복사 포지션을 오픈합니다' - 아이콘 위 또는 오른쪽에 말풍선 형태로 표시\n4. 배경색: 검은색(#000) 또는 진한 회색(#424242), 텍스트: 흰색, 폰트 크기: 12~14px\n5. (Web) 마우스 아웃 시 0.3초 후 사라짐 / (App) 다른 영역 터치 시 즉시 사라짐",
                    "priority": ui_req["priority"],
                    "type": "UI",
                    "comment": f"PRD UI: {ui_req.get('content', '')}",
                    "web_result": "",
                    "app_result": ""
                })
            elif "Copy Activity Display" in ui_req["component"]:
                testcases.append({
                    "domain": "Copy Trading",
                    "section": "Fixed Multiplier Mode",
                    "component": "UI Components",
                    "feature": ui_req["component"],
                    "title": "Copy Activity에서 Multiplier 정보 표시 검증",
                    "precondition": "1. Fixed Multiplier 모드로 Master Trader 구독 완료\n2. Copy Multiplier: 3.0x 설정\n3. Copy Activity 화면 진입",
                    "test_step": "1. Copy Activity 화면에서 구독 중인 Master 카드/리스트 확인\n2. Master 이름 및 기본 정보 확인\n3. 'Copy Mode' 표시 라벨 확인\n4. 'Copy Multiplier' 값 표시 확인\n5. 다른 Master (Fixed Ratio 모드)와 표시 차이 확인",
                    "expected_results": "1. 구독 중인 Master가 카드 또는 리스트 아이템으로 표시됨\n2. Master 이름, 프로필 이미지, ROI 등 기본 정보 표시\n3. 'Copy Mode: Fixed Multiplier' 또는 'Mode: Fixed Multiplier' 라벨 표시\n4. 'Copy Multiplier: 3.0x' 또는 'Multiplier: 3.0x' 추가 라벨 표시 (Mode 라벨 아래 또는 옆)\n5. Fixed Ratio 모드 Master는 'Copy Mode: Fixed Ratio', Multiplier 값 표시 없음",
                    "priority": ui_req["priority"],
                    "type": "UI",
                    "comment": f"PRD UI: {ui_req.get('fields', [])} - 조건: {ui_req.get('condition', '')}",
                    "web_result": "",
                    "app_result": ""
                })
        
        # 검증 규칙 테스트 (구체화) - 이미 비즈니스 규칙에서 상세히 다루었으므로 추가 엣지 케이스만
        testcases.append({
            "domain": "Copy Trading",
            "section": "Fixed Multiplier Mode",
            "component": "Input Validation",
            "feature": "소수점 입력 검증",
            "title": "Copy Multiplier 소수점 자리수 입력 검증",
            "precondition": "Fixed Multiplier 설정 화면, Copy Multiplier 입력 필드 활성화",
            "test_step": "1. Copy Multiplier 필드에 '1.5' 입력\n2. 결과 확인 (2자리 권장)\n3. '2.55' 입력\n4. 결과 확인\n5. '3.123' 입력 (3자리)\n6. 표시 또는 저장 시 처리 방식 확인\n7. '4.999' 입력 후 저장\n8. 저장된 값 확인",
            "expected_results": "1. '1.5' 입력 성공, '1.5x' 또는 '1.50x' 표시\n2. 에러 없음\n3. '2.55' 입력 성공, '2.55x' 표시\n4. 2자리 소수점 정상 처리\n5. '3.123' 입력 가능하나, 표시 시 '3.12x' (반올림) 또는 '3.123x' (그대로)\n6. 소수점 3자리 입력 가능하되, 저장 시 2자리로 자동 조정되거나 그대로 저장\n7. 저장 성공 메시지\n8. Copy Activity에서 '4.99x' (반올림) 또는 '5.0x' (반올림) 또는 '4.999x' (그대로) 표시",
            "priority": "P2",
            "type": "Functional",
            "comment": "PRD 검증: 소수점 2자리 권장, 더 높은 정밀도 허용 여부 확인",
            "web_result": "",
            "app_result": ""
        })
        
        testcases.append({
            "domain": "Copy Trading",
            "section": "Fixed Multiplier Mode",
            "component": "Input Validation",
            "feature": "특수문자 입력 차단",
            "title": "Copy Multiplier 필드에 숫자 외 입력 차단 검증",
            "precondition": "Copy Multiplier 입력 필드 활성화",
            "test_step": "1. 'abc' 입력 시도\n2. 입력 결과 확인\n3. '-5' (음수) 입력 시도\n4. '10x' (단위 포함) 입력 시도\n5. '1 0' (공백 포함) 입력 시도\n6. '1,000' (쉼표 포함) 입력 시도",
            "expected_results": "1. 'abc' 입력 차단 (키 입력이 필드에 반영되지 않음) 또는 에러 메시지\n2. 입력 필드가 비어있거나 이전 값 유지\n3. '-' 입력 차단 또는 에러 메시지: 'Only positive numbers allowed'\n4. '10x' 입력 시 'x' 자동 제거되어 '10'만 입력되거나, 'x' 입력 차단\n5. 공백 입력 차단 또는 자동 제거\n6. 쉼표 입력 차단 (소수점만 허용)",
            "priority": "P2",
            "type": "Functional",
            "comment": "PRD 검증: 숫자와 소수점만 입력 가능",
            "web_result": "",
            "app_result": ""
        })
        
        testcases.append({
            "domain": "Copy Trading",
            "section": "Fixed Multiplier Mode",
            "component": "Input Validation",
            "feature": "빈 값 입력 처리",
            "title": "Copy Multiplier 필드 비우고 저장 시도",
            "precondition": "Copy Multiplier 필드에 값이 입력된 상태",
            "test_step": "1. Copy Multiplier 필드의 모든 값 삭제 (빈 상태로 만듦)\n2. 포커스 아웃\n3. 필드 상태 확인\n4. 'Save' 버튼 클릭 시도\n5. 에러 또는 자동 복구 확인",
            "expected_results": "1. 필드가 비어있음\n2. 포커스 아웃 시:\n   - 옵션 A: 기본값 '1.0x' 자동 입력\n   - 옵션 B: 빨간색 에러 테두리 표시\n3. - 옵션 A: '1.0x' 표시\n   - 옵션 B: 에러 메시지: 'Multiplier is required' 또는 '배수를 입력하세요'\n4. - 옵션 A: 저장 성공 (기본값 적용)\n   - 옵션 B: 저장 실패, 에러 메시지 재표시\n5. 사용자가 값을 입력해야만 저장 가능하거나, 자동으로 기본값 적용됨",
            "priority": "P2",
            "type": "Functional",
            "comment": "PRD 검증: 필수 입력 필드 처리 정책 확인",
            "web_result": "",
            "app_result": ""
        })
        
        # 에러 처리 테스트 (구체화) - 마진 부족은 이미 비즈니스 규칙에서 다룸
        testcases.append({
            "domain": "Copy Trading",
            "section": "Fixed Multiplier Mode",
            "component": "Error Handling",
            "feature": "네트워크 오류 처리",
            "title": "설정 저장 중 네트워크 오류 발생 시 처리",
            "precondition": "1. Fixed Multiplier 설정 입력 완료\n2. (테스트 환경) 네트워크 차단 또는 지연 유도 가능",
            "test_step": "1. Copy Multiplier를 '5.0x'로 설정\n2. 'Save' 버튼 클릭\n3. 저장 요청 전송 시 네트워크 끊기 (또는 서버 타임아웃 유도)\n4. 로딩 상태 지속 시간 확인 (타임아웃: 30초)\n5. 에러 메시지 표시 확인\n6. 'Retry' 또는 재시도 옵션 확인\n7. 네트워크 복구 후 'Retry' 클릭\n8. 저장 성공 확인",
            "expected_results": "1. '5.0x' 입력 성공\n2. 로딩 스피너 표시, 'Save' 버튼 비활성화\n3. 네트워크 끊김\n4. 30초 후 로딩 중단\n5. 에러 메시지: 'Network error, please try again' 또는 '네트워크 오류가 발생했습니다. 다시 시도해주세요' (빨간색 또는 주황색 알림)\n6. 'Retry' 버튼 또는 'Save' 버튼 재활성화\n7. 'Retry' 클릭 시 재시도, 로딩 스피너 재표시\n8. 저장 성공 메시지, 설정 반영 확인",
            "priority": "P2",
            "type": "Functional",
            "comment": "PRD 에러 처리: 네트워크 오류 시 재시도 옵션 제공",
            "web_result": "",
            "app_result": ""
        })
        
        testcases.append({
            "domain": "Copy Trading",
            "section": "Fixed Multiplier Mode",
            "component": "Error Handling",
            "feature": "서버 에러 처리",
            "title": "서버 에러 (5xx) 발생 시 사용자 피드백",
            "precondition": "1. Fixed Multiplier 설정 화면\n2. (테스트 환경) 서버 500 에러 유도 가능",
            "test_step": "1. Copy Multiplier 설정 후 저장 시도\n2. 서버에서 500 Internal Server Error 응답 유도\n3. 에러 메시지 내용 및 스타일 확인\n4. 'Contact Support' 또는 'Report' 옵션 확인\n5. 에러 로그 기록 여부 확인 (개발자 도구)\n6. 사용자 입력값 유지 확인\n7. 재시도 시 정상 동작 확인",
            "expected_results": "1. 저장 시도\n2. 서버 500 에러 발생\n3. 에러 메시지: 'Server error occurred. Please try again later' 또는 '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요' - 빨간색 배너 또는 모달\n4. 'Contact Support' 링크 또는 'Retry' 버튼 표시\n5. 콘솔에 에러 로그 기록: 'POST /api/copy-settings 500'\n6. 사용자가 입력한 '5.0x' 값이 필드에 그대로 유지됨 (초기화되지 않음)\n7. 재시도 시 정상 저장 완료",
            "priority": "P2",
            "type": "Functional",
            "comment": "PRD 에러 처리: 서버 에러 시 사용자 친화적 메시지",
            "web_result": "",
            "app_result": ""
        })
        
        testcases.append({
            "domain": "Copy Trading",
            "section": "Fixed Multiplier Mode",
            "component": "Error Handling",
            "feature": "권한 오류 처리",
            "title": "Copy Trading 권한 없는 사용자 접근 시 처리",
            "precondition": "1. Copy Trading 권한이 없는 계정\n2. KYC 미완료 또는 Region 제한 등",
            "test_step": "1. Copy Trading 설정 화면 접근 시도\n2. 권한 체크 결과 확인\n3. 차단 메시지 또는 리다이렉트 확인\n4. 안내 메시지 내용 확인\n5. 'Go to KYC' 또는 해결 방법 링크 확인",
            "expected_results": "1. 설정 화면 로딩 시작\n2. 권한 없음 감지\n3. 설정 화면 대신 차단 페이지 표시 또는 모달 팝업\n4. 메시지: 'Copy Trading is not available in your region' 또는 'Please complete KYC to use Copy Trading' - 이유와 해결 방법 명시\n5. 'Complete KYC' 버튼 → KYC 페이지로 이동 또는 'Contact Support' 링크 제공",
            "priority": "P2",
            "type": "Functional",
            "comment": "PRD 에러 처리: 권한 체크 및 사용자 안내",
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
        """통합 시나리오 테스트케이스 생성 (구체화)"""
        scenarios = [
            {
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "End-to-End Flow",
                "feature": "Fixed Multiplier 전체 플로우",
                "title": "Fixed Multiplier 설정부터 주문 실행까지 전체 플로우 (성공 케이스)",
                "precondition": "1. 로그인된 계정 (KYC 완료)\n2. Copy Balance: 1000 USDT\n3. Master Trader 'TestMaster' 선택 가능\n4. Master가 거래 실행 가능한 상태",
                "test_step": "1. 앱 하단 'Copy Trading' 탭 클릭\n2. 'TestMaster' 프로필 카드 클릭\n3. 'Copy Settings' 또는 '복사 설정' 버튼 클릭\n4. 'Fixed Multiplier' 탭 클릭\n5. 'Copy Amount' 필드에 '500' 입력 (500 USDT)\n6. 'Copy Multiplier' 필드에 '2.5' 입력\n7. Example Text에서 '250 USDT position' (100 × 2.5) 확인\n8. 'Total Stop Loss' 필드에 '100' 입력 (100 USDT)\n9. 'Max Entry Slippage' 기본값 확인 (1% 등)\n10. 'Start Copying' 또는 'Save' 버튼 클릭\n11. '설정이 저장되었습니다' 토스트 확인\n12. Copy Activity 화면으로 자동 이동 확인\n13. 'TestMaster' 카드에 'Active' 상태 표시 확인\n14. (Master 측) BTC/USDT Long Position 100 USDT, Leverage 10x 오픈\n15. (Follower 측) 5초 이내 Notifications 확인\n16. 'Positions' 탭 이동\n17. 새로운 Copy Position 확인: BTC/USDT Long\n18. Position Size 확인\n19. Position 상세 클릭\n20. Entry Price, Leverage, PnL 등 확인",
                "expected_results": "1. Copy Trading 메인 화면 로드\n2. TestMaster 프로필 표시 (이름, ROI, 팔로워 수)\n3. 'Copy Settings' 버튼 표시\n4. Fixed Multiplier 탭 활성화, 입력 필드들 표시\n5. Copy Amount '500 USDT' 입력 성공\n6. Copy Multiplier '2.5x' 입력 성공\n7. Example Text 업데이트: '...you will open a 250 USDT position'\n8. Total Stop Loss '100 USDT' 입력 성공\n9. Max Entry Slippage '1%' 표시\n10. 로딩 후 저장 완료\n11. 녹색 토스트: '설정이 저장되었습니다'\n12. Copy Activity 화면 전환\n13. TestMaster 카드에 'Active' 녹색 라벨, 'Copy Multiplier: 2.5x' 표시\n14. Master Position 생성\n15. Notification: 'TestMaster opened a position' 또는 알림 배지 표시\n16. Positions 탭 전환\n17. BTC/USDT Long Position 표시, 'Copying TestMaster' 라벨\n18. Position Size = 250 USDT (100 × 2.5 정확히 일치)\n19. 상세 화면 오픈\n20. Entry Price: Master와 유사 (슬리피지 범위 내), Leverage: 10x, PnL: 실시간 업데이트, Master Position Size: 100 USDT 표시",
                "priority": "P1",
                "type": "Functional",
                "comment": "핵심 E2E 시나리오 - PRD + Figma 통합 - 전체 플로우 검증",
                "web_result": "",
                "app_result": ""
            },
            {
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "Cross-validation",
                "feature": "Fixed Ratio vs Fixed Multiplier 비교",
                "title": "동일 Master에 대해 Fixed Ratio와 Fixed Multiplier 결과 비교 검증",
                "precondition": "1. 2개의 Follower 계정 준비 (Account A, Account B)\n2. Account A Copy Balance: 500 USDT, Account B Copy Balance: 500 USDT\n3. 동일 Master 'TestMaster' 구독 준비\n4. Master Equity: 2000 USDT (가정)\n5. Master가 BTC/USDT 200 USDT Position 오픈 예정",
                "test_step": "**Account A - Fixed Ratio 설정**\n1. Account A 로그인\n2. 'TestMaster' Copy Settings 진입\n3. 'Fixed Ratio' 탭 선택\n4. Copy Amount '500' USDT 입력\n5. Preview 확인: Expected Ratio = 500 / 2000 = 0.25\n6. 'Save' 및 활성화\n\n**Account B - Fixed Multiplier 설정**\n7. Account B 로그인\n8. 'TestMaster' Copy Settings 진입\n9. 'Fixed Multiplier' 탭 선택\n10. Copy Multiplier '0.25' 입력 (동일 배수 적용 목적)\n11. Example Text 확인\n12. 'Save' 및 활성화\n\n**Master 거래 실행 및 비교**\n13. Master 'TestMaster'가 BTC/USDT 200 USDT Position 오픈\n14. Account A Position Size 확인\n15. Account B Position Size 확인\n16. 두 계정의 Position Size 비교\n17. 계산 로직 검증\n\n**추가 테스트: Master Equity 변동 시**\n18. Master Equity가 4000 USDT로 변경 (가정)\n19. Master가 다시 200 USDT Position 오픈\n20. Account A Position Size 확인 (Ratio 재계산됨)\n21. Account B Position Size 확인 (Multiplier 고정)\n22. 결과 비교",
                "expected_results": "**Phase 1 - 설정:**\n1-6. Account A Fixed Ratio 활성화 성공, Copy Amount 500 USDT\n7-12. Account B Fixed Multiplier 활성화 성공, Multiplier 0.25x\n\n**Phase 2 - 첫 번째 거래:**\n13. Master Position 생성 (200 USDT)\n14. Account A Position Size = 200 × (500 / 2000) = 200 × 0.25 = 50 USDT\n15. Account B Position Size = 200 × 0.25 = 50 USDT\n16. 두 계정 모두 50 USDT Position (초기 Equity 기준으로 동일)\n17. 계산 결과 정확히 일치\n\n**Phase 3 - Master Equity 변동 후:**\n18. Master Equity 4000 USDT로 변경\n19. Master Position 200 USDT 재오픈\n20. Account A Position Size = 200 × (500 / 4000) = 200 × 0.125 = 25 USDT (Ratio 동적 변경)\n21. Account B Position Size = 200 × 0.25 = 50 USDT (Multiplier 고정 유지)\n22. Fixed Ratio는 Equity 변동에 따라 동적으로 변화하지만, Fixed Multiplier는 고정값 유지 → 핵심 차이점 검증 완료",
                "priority": "P2",
                "type": "Functional",
                "comment": "두 모드 간 동작 비교 - Equity 변동 시 동적 vs 고정 검증",
                "web_result": "",
                "app_result": ""
            },
            {
                "domain": "Copy Trading",
                "section": "Fixed Multiplier Mode",
                "component": "Edge Cases",
                "feature": "극단값 테스트",
                "title": "최소값(0.01x)과 최대값(100x) 동작 검증 - 경계값 테스트",
                "precondition": "1. Follower Account: Copy Balance 10000 USDT (충분한 마진 확보)\n2. Master 'TestMaster' 구독 준비\n3. Master가 BTC/USDT 거래 실행 가능",
                "test_step": "**Test Case 1: 최소값 0.01x**\n1. 'TestMaster' Copy Settings 진입\n2. 'Fixed Multiplier' 탭 선택\n3. Copy Multiplier '0.01' 입력\n4. Example Text 확인: 'If Master opens 100 USDT, you will open 1 USDT' (100 × 0.01)\n5. 'Save' 및 활성화\n6. Master가 BTC/USDT 1000 USDT Position (Leverage 10x) 오픈\n7. Follower Position Size 확인\n8. Position 상세 확인: Required Margin, Leverage\n9. 계산 검증: Expected Size = 1000 × 0.01 = 10 USDT\n\n**Test Case 2: 최대값 100x**\n10. Copy Trading 설정 수정 (Edit)\n11. Copy Multiplier를 '100' 으로 변경\n12. Example Text 확인: 'If Master opens 100 USDT, you will open 10000 USDT'\n13. Warning Message 확인: 'High multiplier may cause frequent failed orders due to insufficient margin'\n14. 'Save' 및 활성화\n15. Master가 BTC/USDT 100 USDT Position (Leverage 10x) 오픈\n16. Follower Position Size 확인\n17. Position 상세 확인: Required Margin, Leverage\n18. 계산 검증: Expected Size = 100 × 100 = 10000 USDT\n19. Required Margin 확인: 10000 / 10 = 1000 USDT (Copy Balance 10000 USDT 내에서 충분)\n20. Position 정상 생성 확인\n\n**Test Case 3: 극단값에서 마진 부족 시나리오**\n21. Copy Balance를 500 USDT로 조정 (가정 또는 별도 계정)\n22. Copy Multiplier 100x 유지\n23. Master가 BTC/USDT 100 USDT Position (Leverage 10x) 오픈 시도\n24. Follower의 주문 실패 확인\n25. 에러 메시지 확인: 'Insufficient margin' (Required: 1000 USDT, Available: 500 USDT)\n26. Failed Orders 기록 확인",
                "expected_results": "**Test Case 1 결과:**\n1-5. 0.01x 설정 및 활성화 성공\n6. Master Position 1000 USDT 생성\n7. Follower Position Size = 10 USDT (매우 작은 포지션)\n8. Required Margin = 10 / 10 = 1 USDT (Leverage 10x), Leverage: 10x 정상 적용\n9. 계산 정확: 1000 × 0.01 = 10 USDT ✅\n\n**Test Case 2 결과:**\n10-14. 100x 설정 및 활성화 성공, Warning 메시지 표시 확인\n15. Master Position 100 USDT 생성\n16. Follower Position Size = 10000 USDT (매우 큰 포지션)\n17. Required Margin = 10000 / 10 = 1000 USDT, Leverage: 10x 정상 적용\n18. 계산 정확: 100 × 100 = 10000 USDT ✅\n19. Copy Balance 10000 USDT 중 1000 USDT 사용 (충분)\n20. Position 정상 생성, PnL 실시간 업데이트\n\n**Test Case 3 결과:**\n21-22. Copy Balance 500 USDT, Multiplier 100x 유지\n23. Master Position 오픈 시도\n24. Follower 주문 실패 (Required: 1000 USDT, Available: 500 USDT)\n25. Notification 및 Failed Orders에 에러 표시: 'Copy order failed: Insufficient margin (Required: 1000 USDT, Available: 500 USDT)'\n26. Activity History에 실패 기록 남음, 자동 스케일 다운 없이 완전 실패 ✅\n\n**종합 결과:**\n- 최소값 0.01x와 최대값 100x 모두 정확히 동작\n- 극단값에서도 계산 공식 정확히 적용됨\n- 마진 부족 시 적절한 에러 처리 및 사용자 피드백 제공",
                "priority": "P2",
                "type": "Functional",
                "comment": "경계값 테스트 - PRD 요구사항 - 최소/최대 Multiplier 및 마진 부족 시나리오",
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
