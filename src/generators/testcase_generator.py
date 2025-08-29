#!/usr/bin/env python3
"""
테스트케이스 생성 엔진
- 분석 결과 기반 테스트케이스 자동 생성
- 다양한 출력 형식 지원 (Excel, TestRail, JSON)
- 시나리오 기반 커스터마이징
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
from ..analyzers.figma_analyzer import FigmaAnalyzer

class TestCaseGenerator:
    """테스트케이스 생성기"""
    
    def __init__(self):
        """초기화"""
        # 테스트케이스 템플릿
        self.testcase_template = {
            "domain": "",
            "section": "",
            "component": "",
            "feature": "",
            "title": "",
            "precondition": "",
            "test_steps": "",
            "expected_results": "",
            "priority": "P2",
            "type": "Functional",
            "comment": "",
            "android_result": "",
            "ios_result": ""
        }
        
        # 우선순위 매핑
        self.priority_mapping = {
            "critical": "P1",
            "high": "P2", 
            "medium": "P3",
            "low": "P4"
        }
        
        # 테스트 타입 정의
        self.test_types = {
            "functional": "Functional",
            "ui": "UI",
            "security": "Security",
            "performance": "Performance",
            "accessibility": "Accessibility",
            "usability": "Usability"
        }
    
    def generate_from_analysis(self, analysis_result: Dict[str, Any], 
                             custom_scenarios: Optional[List[Dict]] = None) -> List[Dict]:
        """
        Figma 분석 결과를 기반으로 테스트케이스 생성
        
        Args:
            analysis_result: FigmaAnalyzer.enhanced_analysis() 결과
            custom_scenarios: 커스텀 시나리오 (선택사항)
        
        Returns:
            List[Dict]: 생성된 테스트케이스 목록
        """
        if not analysis_result.get("success"):
            raise ValueError(f"분석 결과 오류: {analysis_result.get('error')}")
        
        testcases = []
        
        # 분석 결과에서 정보 추출
        enhanced_analysis = analysis_result.get("enhanced_analysis", {})
        keywords = enhanced_analysis.get("keywords", {})
        ui_structure = enhanced_analysis.get("ui_structure", {})
        user_flow = enhanced_analysis.get("user_flow", {})
        recommendations = analysis_result.get("recommendations", {})
        
        detected_patterns = keywords.get("detected_patterns", {})
        ui_elements = ui_structure.get("ui_elements", {})
        
        # 1. UI 패턴 기반 테스트케이스 생성
        for pattern_name, pattern_info in detected_patterns.items():
            pattern_testcases = self._generate_pattern_testcases(
                pattern_name, pattern_info, ui_elements
            )
            testcases.extend(pattern_testcases)
        
        # 2. 유저플로우 기반 테스트케이스 생성
        flow_testcases = self._generate_flow_testcases(user_flow, ui_elements)
        testcases.extend(flow_testcases)
        
        # 3. UI 요소 기반 테스트케이스 생성
        ui_testcases = self._generate_ui_testcases(ui_elements, ui_structure)
        testcases.extend(ui_testcases)
        
        # 4. 권장사항 기반 테스트케이스 생성
        recommendation_testcases = self._generate_recommendation_testcases(recommendations)
        testcases.extend(recommendation_testcases)
        
        # 5. 커스텀 시나리오 추가
        if custom_scenarios:
            custom_testcases = self._generate_custom_testcases(custom_scenarios)
            testcases.extend(custom_testcases)
        
        # 6. 우선순위 조정 및 중복 제거
        testcases = self._optimize_testcases(testcases)
        
        return testcases
    
    def _generate_pattern_testcases(self, pattern_name: str, pattern_info: Dict, 
                                  ui_elements: Dict) -> List[Dict]:
        """UI 패턴 기반 테스트케이스 생성"""
        testcases = []
        
        if pattern_name == "authentication":
            testcases.extend(self._generate_auth_testcases(pattern_info, ui_elements))
        elif pattern_name == "form_input":
            testcases.extend(self._generate_form_testcases(pattern_info, ui_elements))
        elif pattern_name == "navigation":
            testcases.extend(self._generate_navigation_testcases(pattern_info, ui_elements))
        elif pattern_name == "modal_popup":
            testcases.extend(self._generate_modal_testcases(pattern_info, ui_elements))
        elif pattern_name == "transaction":
            testcases.extend(self._generate_transaction_testcases(pattern_info, ui_elements))
        elif pattern_name == "social":
            testcases.extend(self._generate_social_testcases(pattern_info, ui_elements))
        elif pattern_name == "settings":
            testcases.extend(self._generate_settings_testcases(pattern_info, ui_elements))
        
        return testcases
    
    def _generate_auth_testcases(self, pattern_info: Dict, ui_elements: Dict) -> List[Dict]:
        """인증 관련 테스트케이스 생성"""
        testcases = []
        
        # 기본 로그인 테스트
        testcases.append({
            **self.testcase_template,
            "domain": "authentication",
            "section": "User Authentication",
            "component": "Login",
            "feature": "Basic Login",
            "title": "정상 로그인 플로우",
            "precondition": "앱이 설치되어 있고 네트워크 연결이 활성화된 상태",
            "test_steps": "1. 앱 실행\n2. 로그인 화면 확인\n3. 유효한 계정 정보 입력\n4. 로그인 버튼 클릭",
            "expected_results": "1. 앱이 정상적으로 실행됨\n2. 로그인 화면이 표시됨\n3. 계정 정보가 정상 입력됨\n4. 메인 화면으로 이동됨",
            "priority": "P1",
            "type": "Functional",
            "comment": "AI 생성 - 인증 패턴"
        })
        
        # 로그인 실패 테스트
        testcases.append({
            **self.testcase_template,
            "domain": "authentication",
            "section": "User Authentication",
            "component": "Login",
            "feature": "Login Error Handling",
            "title": "잘못된 계정 정보 로그인 시도",
            "precondition": "로그인 화면이 표시된 상태",
            "test_steps": "1. 잘못된 이메일 입력\n2. 잘못된 비밀번호 입력\n3. 로그인 버튼 클릭\n4. 에러 메시지 확인",
            "expected_results": "1. 이메일이 입력됨\n2. 비밀번호가 입력됨\n3. 로그인 실패\n4. '계정 정보를 확인해주세요' 에러 메시지 표시",
            "priority": "P1",
            "type": "Functional",
            "comment": "AI 생성 - 에러 처리"
        })
        
        return testcases
    
    def _generate_form_testcases(self, pattern_info: Dict, ui_elements: Dict) -> List[Dict]:
        """폼 입력 관련 테스트케이스 생성"""
        testcases = []
        
        input_count = len(ui_elements.get("inputs", []))
        
        if input_count > 0:
            # 폼 유효성 검사 테스트
            testcases.append({
                **self.testcase_template,
                "domain": "form",
                "section": "Form Input",
                "component": "Input Validation",
                "feature": "Form Validation",
                "title": "필수 입력 필드 유효성 검사",
                "precondition": f"입력 폼이 표시된 상태 (총 {input_count}개 필드)",
                "test_steps": "1. 필수 필드를 빈 상태로 두고 저장 시도\n2. 에러 메시지 확인\n3. 필수 필드 입력 후 저장\n4. 저장 완료 확인",
                "expected_results": "1. 저장 실패\n2. '필수 항목을 입력하세요' 에러 메시지\n3. 정상 저장 시도\n4. 저장 완료 메시지 표시",
                "priority": "P1",
                "type": "Functional",
                "comment": "AI 생성 - 폼 검증"
            })
        
        return testcases
    
    def _generate_navigation_testcases(self, pattern_info: Dict, ui_elements: Dict) -> List[Dict]:
        """네비게이션 관련 테스트케이스 생성"""
        testcases = []
        
        nav_count = len(ui_elements.get("navigation", []))
        
        if nav_count > 0:
            testcases.append({
                **self.testcase_template,
                "domain": "navigation",
                "section": "Navigation",
                "component": "Menu Navigation",
                "feature": "Basic Navigation",
                "title": "메뉴 네비게이션 기본 동작",
                "precondition": f"메인 화면에 네비게이션 메뉴 표시된 상태 (총 {nav_count}개 메뉴)",
                "test_steps": "1. 각 메뉴 항목 클릭\n2. 해당 페이지로 이동 확인\n3. 뒤로가기 버튼 동작 확인\n4. 메뉴 선택 상태 표시 확인",
                "expected_results": "1. 메뉴 클릭이 정상 동작함\n2. 해당 페이지로 정확히 이동됨\n3. 뒤로가기가 정상 동작함\n4. 현재 선택된 메뉴가 하이라이트됨",
                "priority": "P1",
                "type": "Functional",
                "comment": "AI 생성 - 네비게이션"
            })
        
        return testcases
    
    def _generate_modal_testcases(self, pattern_info: Dict, ui_elements: Dict) -> List[Dict]:
        """모달/팝업 관련 테스트케이스 생성"""
        testcases = []
        
        testcases.append({
            **self.testcase_template,
            "domain": "ui",
            "section": "Modal",
            "component": "Popup Dialog",
            "feature": "Modal Interaction", 
            "title": "모달 팝업 기본 동작",
            "precondition": "모달을 띄울 수 있는 액션이 있는 화면",
            "test_steps": "1. 모달 트리거 액션 실행\n2. 모달 팝업 표시 확인\n3. 모달 내 버튼 동작 확인\n4. 모달 닫기 동작 확인",
            "expected_results": "1. 액션이 정상 실행됨\n2. 모달이 중앙에 표시됨\n3. 모달 내 버튼이 정상 동작함\n4. 확인/취소로 모달이 닫힘",
            "priority": "P2",
            "type": "UI",
            "comment": "AI 생성 - 모달 UI"
        })
        
        return testcases
    
    def _generate_transaction_testcases(self, pattern_info: Dict, ui_elements: Dict) -> List[Dict]:
        """거래 관련 테스트케이스 생성"""
        testcases = []
        
        testcases.append({
            **self.testcase_template,
            "domain": "transaction",
            "section": "Trading",
            "component": "Order Execution",
            "feature": "Basic Trading",
            "title": "기본 거래 주문 실행",
            "precondition": "로그인된 상태이고 거래 가능한 자산이 있음",
            "test_steps": "1. 거래 화면 진입\n2. 거래 종목 선택\n3. 주문 정보 입력\n4. 주문 실행\n5. 주문 완료 확인",
            "expected_results": "1. 거래 화면이 정상 로드됨\n2. 종목이 정상 선택됨\n3. 주문 정보가 정상 입력됨\n4. 주문이 정상 실행됨\n5. 주문 완료 메시지 표시",
            "priority": "P1",
            "type": "Functional",
            "comment": "AI 생성 - 거래 기능"
        })
        
        return testcases
    
    def _generate_social_testcases(self, pattern_info: Dict, ui_elements: Dict) -> List[Dict]:
        """소셜 관련 테스트케이스 생성"""
        testcases = []
        
        testcases.append({
            **self.testcase_template,
            "domain": "social",
            "section": "Social Integration",
            "component": "Social Connect",
            "feature": "Social Login",
            "title": "소셜 계정 연동",
            "precondition": "소셜 연동 기능이 활성화된 상태",
            "test_steps": "1. 소셜 연동 버튼 클릭\n2. 해당 앱으로 이동 확인\n3. 인증 완료 후 앱 복귀\n4. 연동 완료 상태 확인",
            "expected_results": "1. 소셜 앱으로 정상 이동됨\n2. OAuth 인증 화면 표시됨\n3. 앱으로 정상 복귀됨\n4. 연동 완료 상태로 표시됨",
            "priority": "P1", 
            "type": "Functional",
            "comment": "AI 생성 - 소셜 연동"
        })
        
        return testcases
    
    def _generate_settings_testcases(self, pattern_info: Dict, ui_elements: Dict) -> List[Dict]:
        """설정 관련 테스트케이스 생성"""
        testcases = []
        
        testcases.append({
            **self.testcase_template,
            "domain": "settings",
            "section": "User Settings",
            "component": "Profile Settings",
            "feature": "Profile Management",
            "title": "프로필 정보 수정",
            "precondition": "프로필 설정 화면에 진입한 상태",
            "test_steps": "1. 기존 프로필 정보 확인\n2. 수정 가능한 필드 편집\n3. 저장 버튼 클릭\n4. 변경사항 적용 확인",
            "expected_results": "1. 기존 정보가 정상 표시됨\n2. 필드 편집이 정상 동작함\n3. 저장이 정상 처리됨\n4. 변경사항이 즉시 반영됨",
            "priority": "P2",
            "type": "Functional",
            "comment": "AI 생성 - 설정 관리"
        })
        
        return testcases
    
    def _generate_flow_testcases(self, user_flow: Dict, ui_elements: Dict) -> List[Dict]:
        """유저플로우 기반 테스트케이스 생성"""
        testcases = []
        
        flow_steps = user_flow.get("flow_steps", [])
        primary_flow_type = user_flow.get("primary_flow_type", "general")
        
        if len(flow_steps) > 2:
            testcases.append({
                **self.testcase_template,
                "domain": "user_flow",
                "section": "User Journey",
                "component": "End-to-End Flow",
                "feature": f"{primary_flow_type.title()} Flow",
                "title": f"전체 {primary_flow_type} 플로우 검증",
                "precondition": "앱이 정상 실행된 상태",
                "test_steps": "\n".join([f"{i+1}. {step}" for i, step in enumerate(flow_steps)]),
                "expected_results": "\n".join([f"{i+1}. {step}이(가) 정상 완료됨" for i, step in enumerate(flow_steps)]),
                "priority": "P1",
                "type": "Functional",
                "comment": f"AI 생성 - {primary_flow_type} 플로우"
            })
        
        return testcases
    
    def _generate_ui_testcases(self, ui_elements: Dict, ui_structure: Dict) -> List[Dict]:
        """UI 요소 기반 테스트케이스 생성"""
        testcases = []
        
        button_count = len(ui_elements.get("buttons", []))
        ui_complexity = ui_structure.get("ui_complexity", "medium")
        
        # 버튼 인터랙션 테스트
        if button_count > 0:
            testcases.append({
                **self.testcase_template,
                "domain": "ui",
                "section": "UI Elements",
                "component": "Button Interaction",
                "feature": "Button Functionality",
                "title": "버튼 인터랙션 기본 동작",
                "precondition": f"UI에 {button_count}개의 버튼이 표시된 상태",
                "test_steps": "1. 각 버튼의 표시 상태 확인\n2. 버튼 클릭 동작 확인\n3. 비활성화 상태 버튼 확인\n4. 버튼 피드백 확인",
                "expected_results": "1. 모든 버튼이 정상 표시됨\n2. 클릭 시 해당 액션 실행됨\n3. 비활성화 버튼은 클릭 불가\n4. 클릭 시 시각적 피드백 제공됨",
                "priority": "P2",
                "type": "UI",
                "comment": "AI 생성 - UI 요소"
            })
        
        # UI 복잡도에 따른 테스트
        if ui_complexity == "high":
            testcases.append({
                **self.testcase_template,
                "domain": "ui",
                "section": "UI Performance",
                "component": "Complex UI",
                "feature": "UI Responsiveness",
                "title": "복잡한 UI 반응성 테스트",
                "precondition": "고복잡도 UI 화면이 로드된 상태",
                "test_steps": "1. UI 로딩 시간 측정\n2. 스크롤 성능 확인\n3. 다중 인터랙션 동시 실행\n4. 메모리 사용량 확인",
                "expected_results": "1. 3초 이내 로딩 완료\n2. 스크롤이 부드럽게 동작함\n3. 인터랙션이 지연되지 않음\n4. 메모리 사용량이 적정 수준 유지",
                "priority": "P2",
                "type": "Performance",
                "comment": "AI 생성 - 성능 테스트"
            })
        
        return testcases
    
    def _generate_recommendation_testcases(self, recommendations: Dict) -> List[Dict]:
        """권장사항 기반 테스트케이스 생성"""
        testcases = []
        
        testing_priorities = recommendations.get("testing_priorities", [])
        
        for priority in testing_priorities:
            if "보안" in priority:
                testcases.append({
                    **self.testcase_template,
                    "domain": "security",
                    "section": "Security",
                    "component": "Security Test",
                    "feature": "Security Validation",
                    "title": "보안 기능 검증",
                    "precondition": "보안이 적용되어야 하는 기능",
                    "test_steps": "1. 인증되지 않은 접근 시도\n2. 권한 없는 액션 실행 시도\n3. 보안 에러 처리 확인",
                    "expected_results": "1. 접근이 차단됨\n2. 권한 오류 메시지 표시\n3. 적절한 보안 처리가 수행됨",
                    "priority": "P1",
                    "type": "Security",
                    "comment": f"AI 생성 - {priority}"
                })
        
        return testcases
    
    def _generate_custom_testcases(self, custom_scenarios: List[Dict]) -> List[Dict]:
        """커스텀 시나리오 기반 테스트케이스 생성"""
        testcases = []
        
        for scenario in custom_scenarios:
            testcase = {**self.testcase_template}
            testcase.update(scenario)
            testcase["comment"] = "사용자 정의 시나리오"
            testcases.append(testcase)
        
        return testcases
    
    def _optimize_testcases(self, testcases: List[Dict]) -> List[Dict]:
        """테스트케이스 최적화 (중복 제거, 우선순위 조정)"""
        # 제목 기반 중복 제거
        seen_titles = set()
        unique_testcases = []
        
        for testcase in testcases:
            title = testcase.get("title", "")
            if title not in seen_titles:
                seen_titles.add(title)
                unique_testcases.append(testcase)
        
        # 우선순위별 정렬 (P1 > P2 > P3 > P4)
        priority_order = {"P1": 1, "P2": 2, "P3": 3, "P4": 4}
        unique_testcases.sort(key=lambda x: priority_order.get(x.get("priority", "P4"), 4))
        
        return unique_testcases
    
    def generate_scenarios(self, feature_config: Dict[str, Any]) -> List[Dict]:
        """시나리오 설정 기반 테스트케이스 생성"""
        feature_name = feature_config.get("feature_name", "Unknown Feature")
        priority = feature_config.get("priority", "P2") 
        scenarios = feature_config.get("scenarios", [])
        
        testcases = []
        
        for i, scenario in enumerate(scenarios, 1):
            testcase = {
                **self.testcase_template,
                "feature": feature_name,
                "title": f"{feature_name} - {scenario}",
                "priority": priority,
                "comment": "시나리오 기반 생성"
            }
            testcases.append(testcase)
        
        return testcases
    
    def identify_missing_tests(self, existing_tests: List[Dict], 
                             analysis_result: Dict[str, Any]) -> List[Dict]:
        """기존 테스트와 분석 결과를 비교하여 누락된 테스트 식별"""
        # 분석 결과에서 생성된 테스트케이스
        generated_tests = self.generate_from_analysis(analysis_result)
        
        # 기존 테스트 제목들
        existing_titles = {test.get("title", "") for test in existing_tests}
        
        # 누락된 테스트케이스 필터링
        missing_tests = [
            test for test in generated_tests 
            if test.get("title", "") not in existing_titles
        ]
        
        return missing_tests
    
    def generate_by_priority(self, analysis_result: Dict[str, Any], 
                           min_priority: str = "P1") -> List[Dict]:
        """우선순위 기반 테스트케이스 생성"""
        all_tests = self.generate_from_analysis(analysis_result)
        
        priority_filter = {"P1": 1, "P2": 2, "P3": 3, "P4": 4}
        min_level = priority_filter.get(min_priority, 2)
        
        filtered_tests = [
            test for test in all_tests
            if priority_filter.get(test.get("priority", "P4"), 4) <= min_level
        ]
        
        return filtered_tests
    
    def save_to_excel(self, testcases: List[Dict], filename: str):
        """Excel 형식으로 저장"""
        df = pd.DataFrame(testcases)
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='TestCases', index=False)
            
            # 워크시트 포맷팅
            worksheet = writer.sheets['TestCases']
            
            # 열 너비 조정
            column_widths = {
                'A': 15,  # domain
                'B': 20,  # section  
                'C': 20,  # component
                'D': 25,  # feature
                'E': 50,  # title
                'F': 40,  # precondition
                'G': 60,  # test_steps
                'H': 60,  # expected_results
                'I': 10,  # priority
                'J': 15,  # type
                'K': 30,  # comment
                'L': 15,  # android_result
                'M': 15   # ios_result
            }
            
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width
    
    def save_to_testrail_csv(self, testcases: List[Dict], filename: str):
        """TestRail 가져오기용 CSV 형식으로 저장"""
        # TestRail 필드로 변환
        testrail_data = []
        
        for testcase in testcases:
            testrail_testcase = {
                "Section": f"{testcase.get('domain', '')}/{testcase.get('section', '')}",
                "Title": testcase.get("title", ""),
                "Type": testcase.get("type", "Functional"),
                "Priority": testcase.get("priority", "P2"),
                "Estimate": "5m",
                "References": "",
                "Preconditions": testcase.get("precondition", ""),
                "Steps": testcase.get("test_steps", ""),
                "Expected Result": testcase.get("expected_results", "")
            }
            testrail_data.append(testrail_testcase)
        
        df = pd.DataFrame(testrail_data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    def save_to_json(self, testcases: List[Dict], filename: str):
        """JSON 형식으로 저장"""
        output_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_testcases": len(testcases),
                "generator_version": "1.0.0"
            },
            "testcases": testcases
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
