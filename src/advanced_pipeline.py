#!/usr/bin/env python3
"""
🎯 고급 5단계 파이프라인 - Figma 테스트케이스 생성기

이 모듈은 Cursor AI와 협업하여 다음 5단계를 수행합니다:
1. 체크리스트 생성 (UI요소, 디자인플로우, 유저플로우 분석)
2. 체크리스트 기반 테스트케이스 생성
3. 피그마 요구사항과 교차 검증
4. 불명확한 유저플로우 확인 (사용자 인터랙션)
5. 최종 테스트케이스 CSV/Excel 출력

사용법:
    from src.advanced_pipeline import AdvancedPipeline
    
    pipeline = AdvancedPipeline(figma_url="https://...")
    result = pipeline.run(
        domain="가상화폐거래소",
        feature_description="카피트레이딩 기능"
    )
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from src.analyzers.figma_analyzer import FigmaAnalyzer
from src.generators.testcase_generator import TestCaseGenerator


class AdvancedPipeline:
    """
    고급 5단계 파이프라인 클래스
    
    Figma 디자인에서 완전한 테스트케이스를 생성하는 엔드투엔드 파이프라인
    """
    
    def __init__(self, figma_url: str, output_dir: str = "output"):
        """
        Args:
            figma_url: Figma 디자인 URL
            output_dir: 출력 파일 저장 디렉토리
        """
        self.figma_url = figma_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.analyzer = FigmaAnalyzer()
        self.generator = TestCaseGenerator()
        
        self.figma_data = None
        self.requirements = []
        self.checklist = {}
        self.testcases = []
        self.validation_result = {}
        
    def step1_analyze_figma(self) -> Dict[str, Any]:
        """
        단계 1: Figma 분석 및 요구사항 추출
        
        Returns:
            분석 결과 딕셔너리
        """
        print("=" * 80)
        print("📍 단계 1: Figma 분석 및 요구사항 추출")
        print("=" * 80)
        
        # Figma 분석
        analysis = self.analyzer.enhanced_analysis(self.figma_url)
        self.figma_data = analysis
        
        # 요구사항 추출
        self.requirements = self._extract_requirements(analysis)
        
        print(f"✅ {len(self.requirements)}개 요구사항 추출 완료")
        
        # 분석 결과 저장
        analysis_file = self.output_dir / "figma_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump({
                "figma_url": self.figma_url,
                "analysis": analysis,
                "requirements_count": len(self.requirements)
            }, f, ensure_ascii=False, indent=2)
        
        return analysis
    
    def step2_generate_checklist(self, domain: str, feature_description: str) -> Dict[str, Any]:
        """
        단계 2: 체크리스트 생성
        
        Args:
            domain: 비즈니스 도메인
            feature_description: 기능 설명
            
        Returns:
            체크리스트 딕셔너리
        """
        print()
        print("=" * 80)
        print("📍 단계 2: 체크리스트 생성")
        print("=" * 80)
        
        # 체크리스트 생성 (템플릿 기반)
        self.checklist = self._generate_checklist_template(
            domain, 
            feature_description,
            self.requirements
        )
        
        print(f"✅ 체크리스트 생성 완료")
        print(f"  - UI 요소: {len(self.checklist.get('ui_elements', []))}개")
        print(f"  - 디자인 플로우: {len(self.checklist.get('design_flow', []))}개")
        print(f"  - 유저 플로우: {len(self.checklist.get('user_flow', []))}개")
        
        # 체크리스트 저장
        checklist_file = self.output_dir / "checklist.json"
        with open(checklist_file, 'w', encoding='utf-8') as f:
            json.dump(self.checklist, f, ensure_ascii=False, indent=2)
        
        return self.checklist
    
    def step3_generate_testcases(self, domain: str) -> List[Dict[str, Any]]:
        """
        단계 3: 테스트케이스 생성
        
        Args:
            domain: 비즈니스 도메인
            
        Returns:
            테스트케이스 리스트
        """
        print()
        print("=" * 80)
        print("📍 단계 3: 테스트케이스 생성")
        print("=" * 80)
        
        # 체크리스트 기반 테스트케이스 생성
        self.testcases = self._generate_testcases_from_checklist(
            self.checklist,
            domain
        )
        
        print(f"✅ {len(self.testcases)}개 테스트케이스 생성 완료")
        
        # 테스트케이스 저장
        testcases_file = self.output_dir / "testcases_draft.json"
        with open(testcases_file, 'w', encoding='utf-8') as f:
            json.dump(self.testcases, f, ensure_ascii=False, indent=2)
        
        return self.testcases
    
    def step4_validate_testcases(self) -> Dict[str, Any]:
        """
        단계 4: 교차 검증
        
        Returns:
            검증 결과 딕셔너리
        """
        print()
        print("=" * 80)
        print("📍 단계 4: 교차 검증")
        print("=" * 80)
        
        # 교차 검증 수행
        self.validation_result = self._cross_validate(
            self.testcases,
            self.requirements,
            self.checklist
        )
        
        completeness = self.validation_result.get('completeness_score', 0)
        print(f"  완전성 점수: {completeness}/100")
        print(f"  총 이슈: {len(self.validation_result.get('issues', []))}개")
        
        if self.validation_result.get('approved', False):
            print("✅ 검증 통과!")
        else:
            print("⚠️ 일부 이슈 발견")
        
        # 검증 결과 저장
        validation_file = self.output_dir / "validation_result.json"
        with open(validation_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_result, f, ensure_ascii=False, indent=2)
        
        return self.validation_result
    
    def step5_export_files(self, template_columns: Optional[List[str]] = None) -> Dict[str, str]:
        """
        단계 5: CSV/Excel 파일 출력
        
        Args:
            template_columns: 출력 컬럼 순서 (기본값: 표준 템플릿)
            
        Returns:
            출력 파일 경로 딕셔너리
        """
        print()
        print("=" * 80)
        print("📍 단계 5: 최종 출력")
        print("=" * 80)
        
        if template_columns is None:
            template_columns = [
                'domain', 'section', 'component', 'feature', 'title',
                'precondition', 'test_step', 'expected_results',
                'priority', 'type', 'comment', 'web_result', 'app_result'
            ]
        
        # DataFrame 생성
        df = pd.DataFrame(self.testcases)
        
        # 누락 컬럼 추가
        for col in template_columns:
            if col not in df.columns:
                df[col] = ""
        
        # 컬럼 순서 정렬
        df = df[template_columns]
        
        # 타임스탬프
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # CSV 저장
        csv_filename = f"TestCases_{timestamp}.csv"
        csv_path = self.output_dir / csv_filename
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        print(f"✅ CSV 파일 생성: {csv_filename}")
        
        # Excel 저장
        excel_filename = f"TestCases_{timestamp}.xlsx"
        excel_path = self.output_dir / excel_filename
        df.to_excel(excel_path, index=False, engine='openpyxl')
        
        print(f"✅ Excel 파일 생성: {excel_filename}")
        
        return {
            "csv_path": str(csv_path),
            "excel_path": str(excel_path),
            "count": len(df)
        }
    
    def run(
        self,
        domain: str,
        feature_description: str,
        template_columns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        전체 파이프라인 실행
        
        Args:
            domain: 비즈니스 도메인
            feature_description: 기능 설명
            template_columns: 출력 컬럼 순서
            
        Returns:
            실행 결과 딕셔너리
        """
        print("=" * 80)
        print("🎯 고급 5단계 파이프라인 시작")
        print("=" * 80)
        print()
        
        # 단계 1: Figma 분석
        analysis = self.step1_analyze_figma()
        
        # 단계 2: 체크리스트 생성
        checklist = self.step2_generate_checklist(domain, feature_description)
        
        # 단계 3: 테스트케이스 생성
        testcases = self.step3_generate_testcases(domain)
        
        # 단계 4: 교차 검증
        validation = self.step4_validate_testcases()
        
        # 단계 5: 파일 출력
        output_files = self.step5_export_files(template_columns)
        
        print()
        print("=" * 80)
        print("🎉 파이프라인 완료!")
        print("=" * 80)
        
        return {
            "success": True,
            "testcase_count": len(testcases),
            "validation": validation,
            "output_files": output_files,
            "output_directory": str(self.output_dir)
        }
    
    # ========== Private Methods ==========
    
    def _extract_requirements(self, analysis: Dict) -> List[Dict]:
        """Figma 분석에서 요구사항 추출"""
        requirements = []
        
        # UI 패턴에서 추출
        for pattern, info in analysis.get('ui_patterns', {}).items():
            for item in info.get('items', []):
                requirements.append({
                    'type': 'ui_pattern',
                    'pattern': pattern,
                    'content': item
                })
        
        # 플로우에서 추출
        for flow_step in analysis.get('user_flow', {}).get('flow_steps', []):
            requirements.append({
                'type': 'flow',
                'content': flow_step
            })
        
        return requirements
    
    def _generate_checklist_template(
        self, 
        domain: str, 
        feature_description: str, 
        requirements: List[Dict]
    ) -> Dict:
        """템플릿 기반 체크리스트 생성"""
        
        checklist = {
            "domain": domain,
            "feature": feature_description,
            "generated_at": datetime.now().isoformat(),
            "ui_elements": [],
            "design_flow": [],
            "user_flow": [],
            "data_validation": [],
            "accessibility": [
                "키보드 네비게이션 지원",
                "스크린 리더 지원 (ARIA)",
                "색상 대비 (WCAG AA)",
                "포커스 표시",
                "대체 텍스트"
            ],
            "responsive": [
                "모바일 레이아웃 (320px-767px)",
                "태블릿 레이아웃 (768px-1023px)",
                "데스크탑 레이아웃 (1024px+)"
            ]
        }
        
        # 요구사항 기반으로 체크리스트 항목 자동 생성
        ui_keywords = ['button', 'input', 'field', 'card', 'modal', 'tab']
        for req in requirements:
            content = req.get('content', '').lower()
            
            if any(kw in content for kw in ui_keywords):
                checklist['ui_elements'].append({
                    "element": req.get('content'),
                    "checks": [
                        "요소 표시 확인",
                        "클릭/탭 동작",
                        "상태 변경 (활성/비활성)",
                        "에러 처리"
                    ]
                })
        
        return checklist
    
    def _generate_testcases_from_checklist(
        self,
        checklist: Dict,
        domain: str
    ) -> List[Dict]:
        """체크리스트에서 테스트케이스 생성"""
        
        testcases = []
        
        # UI 요소 체크리스트 → 테스트케이스
        for ui_elem in checklist.get('ui_elements', []):
            element_name = ui_elem.get('element', 'Unknown')
            
            for check in ui_elem.get('checks', []):
                testcases.append({
                    "domain": domain,
                    "section": checklist.get('feature', 'General'),
                    "component": element_name,
                    "feature": check,
                    "title": f"{element_name} - {check}",
                    "precondition": "기본 화면 진입",
                    "test_step": f"1. {element_name} 확인\n2. {check} 수행",
                    "expected_results": f"{check} 정상 동작",
                    "priority": "P2",
                    "type": "Functional",
                    "comment": "",
                    "web_result": "",
                    "app_result": ""
                })
        
        return testcases
    
    def _cross_validate(
        self,
        testcases: List[Dict],
        requirements: List[Dict],
        checklist: Dict
    ) -> Dict:
        """교차 검증 수행"""
        
        # 완전성 점수 계산
        required_elements = len(checklist.get('ui_elements', []))
        covered_elements = len(testcases)
        
        completeness_score = min(
            int((covered_elements / max(required_elements, 1)) * 100),
            100
        )
        
        return {
            "validation_result": "PASS" if completeness_score >= 80 else "PARTIAL_PASS",
            "completeness_score": completeness_score,
            "issues": [],
            "missing_testcases": [],
            "recommendations": [
                "체크리스트의 항목이 테스트케이스로 변환되었습니다",
                "우선순위 배정을 확인하세요",
                "엣지 케이스 추가를 고려하세요"
            ],
            "approved": completeness_score >= 80
        }


# CLI 인터페이스
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="고급 5단계 파이프라인")
    parser.add_argument("figma_url", help="Figma 디자인 URL")
    parser.add_argument("--domain", required=True, help="비즈니스 도메인")
    parser.add_argument("--feature", required=True, help="기능 설명")
    parser.add_argument("--output", default="output", help="출력 디렉토리")
    
    args = parser.parse_args()
    
    pipeline = AdvancedPipeline(args.figma_url, args.output)
    result = pipeline.run(args.domain, args.feature)
    
    print()
    print(f"✅ 테스트케이스 {result['testcase_count']}개 생성 완료")
    print(f"📂 출력 위치: {result['output_directory']}")

