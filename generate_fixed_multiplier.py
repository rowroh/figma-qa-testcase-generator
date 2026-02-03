#!/usr/bin/env python3
"""
Fixed Multiplier Mode 테스트케이스 생성 스크립트
"""

import os
import sys
from dotenv import load_dotenv

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.analyzers.figma_analyzer import FigmaAnalyzer
from src.generators.testcase_generator import TestCaseGenerator

def main():
    """Fixed Multiplier Mode 테스트케이스 생성"""
    print("🚀 Fixed Multiplier Mode 테스트케이스 생성 시작")
    print("="*70)
    
    # 환경변수 로드
    load_dotenv()
    
    # Figma API 토큰 확인
    figma_token = os.getenv("FIGMA_TOKEN")
    if not figma_token:
        print("❌ FIGMA_TOKEN 환경변수가 설정되지 않았습니다.")
        return
    
    # Fixed Multiplier Mode Figma URL
    figma_url = "https://www.figma.com/design/7dnR1hkA7EaEyD6SEGj9Xm/Fixed-Multiplier-Mode?node-id=2-2&p=f&t=ZKN63pR10Wlkl7xO-0"
    
    try:
        # 1. Figma 분석기 초기화
        print("\n🔍 1단계: Figma 분석기 초기화")
        analyzer = FigmaAnalyzer(figma_token)
        print("   ✅ 분석기 초기화 완료")
        
        # 2. 기본 분석 실행 (스크린샷 제외로 빠르게)
        print("\n📊 2단계: 기본 분석 실행")
        basic_result = analyzer.basic_analysis(figma_url)
        
        if not basic_result.get("success"):
            print(f"   ❌ 기본 분석 실패: {basic_result.get('error')}")
            # 기본 분석 실패 시에도 계속 진행
            print("   ⚠️  기본 분석 없이 향상된 분석으로 진행합니다...")
        else:
            print(f"   ✅ 요구사항 {len(basic_result.get('requirements', []))}개 추출")
            # 추출된 요구사항 샘플 출력
            requirements = basic_result.get('requirements', [])
            if requirements:
                print("   📋 추출된 요구사항 샘플:")
                for i, req in enumerate(requirements[:3], 1):
                    req_text = req.get('text', '') if isinstance(req, dict) else str(req)
                    print(f"      {i}. {req_text[:80]}..." if len(req_text) > 80 else f"      {i}. {req_text}")
        
        # 3. 향상된 분석 실행 (스크린샷 제외)
        print("\n🔬 3단계: 향상된 분석 실행 (스크린샷 제외)")
        enhanced_result = analyzer.enhanced_analysis(figma_url, include_screenshot=False)
        
        if not enhanced_result.get("success"):
            print(f"   ❌ 향상된 분석 실패: {enhanced_result.get('error')}")
            print("   ⚠️  수동으로 테스트케이스를 생성합니다...")
            # 실패 시 기본 구조로 테스트케이스 생성
            enhanced_result = {
                "success": True,
                "summary": {
                    "total_elements": 0,
                    "ui_patterns": [],
                    "flow_type": "transaction_flow",
                    "ui_complexity": "medium"
                },
                "basic_analysis": basic_result if basic_result.get("success") else {"requirements": []}
            }
        else:
            # 분석 결과 출력
            summary = enhanced_result.get("summary", {})
            print(f"   ✅ 총 요소: {summary.get('total_elements', 0)}개")
            print(f"   ✅ UI 패턴: {len(summary.get('ui_patterns', []))}개")
            ui_patterns = summary.get('ui_patterns', [])
            if ui_patterns:
                print(f"      패턴: {', '.join(ui_patterns[:5])}")
            print(f"   ✅ 주요 플로우: {summary.get('flow_type', 'unknown')}")
            print(f"   ✅ UI 복잡도: {summary.get('ui_complexity', 'medium')}")
        
        # 4. 테스트케이스 생성기 초기화
        print("\n📝 4단계: 테스트케이스 생성")
        generator = TestCaseGenerator()
        
        # 5. 테스트케이스 생성
        testcases = generator.generate_from_analysis(enhanced_result)
        
        # 테스트케이스가 없으면 기본 시나리오 생성
        if not testcases or len(testcases) == 0:
            print("   ⚠️  분석 기반 테스트케이스가 없습니다. 기본 시나리오를 생성합니다...")
            
            # Fixed Multiplier Mode 기본 시나리오
            scenario_config = {
                "feature_name": "Fixed Multiplier Mode",
                "priority": "P1",
                "scenarios": [
                    "Fixed Multiplier 모드 활성화",
                    "배수 설정 및 변경",
                    "주문 실행 및 검증",
                    "에러 처리 및 예외 상황",
                    "UI/UX 검증"
                ]
            }
            
            testcases = generator.generate_scenarios(scenario_config)
            
            # 도메인 정보 추가
            for tc in testcases:
                tc["domain"] = "가상화폐거래소"
                tc["section"] = "Trading"
                tc["component"] = "Fixed Multiplier Mode"
                tc["feature"] = "Fixed Multiplier"
        
        print(f"   ✅ 테스트케이스 {len(testcases)}개 생성")
        
        # 6. 우선순위별 통계
        priority_stats = {}
        for tc in testcases:
            priority = tc.get("priority", "Unknown")
            priority_stats[priority] = priority_stats.get(priority, 0) + 1
        
        print("\n   📊 우선순위별 분포:")
        for priority in ["P1", "P2", "P3", "P4"]:
            count = priority_stats.get(priority, 0)
            if count > 0:
                print(f"      {priority}: {count}개")
        
        # 7. 출력 디렉토리 생성
        output_dir = "output/fixed_multiplier"
        os.makedirs(output_dir, exist_ok=True)
        
        # 8. 다양한 형식으로 저장
        print("\n💾 5단계: 파일 저장")
        
        # Excel 저장
        excel_file = f"{output_dir}/FixedMultiplier_TestCases.xlsx"
        generator.save_to_excel(testcases, excel_file)
        print(f"   ✅ Excel: {excel_file}")
        
        # TestRail CSV 저장
        testrail_file = f"{output_dir}/FixedMultiplier_TestRail.csv"
        generator.save_to_testrail_csv(testcases, testrail_file)
        print(f"   ✅ TestRail: {testrail_file}")
        
        # JSON 저장
        json_file = f"{output_dir}/FixedMultiplier_TestCases.json"
        generator.save_to_json(testcases, json_file)
        print(f"   ✅ JSON: {json_file}")
        
        # 9. 샘플 테스트케이스 출력
        print("\n🔍 6단계: 샘플 테스트케이스")
        if testcases:
            print("   " + "-" * 60)
            for i, sample_tc in enumerate(testcases[:3], 1):
                print(f"\n   [{i}] {sample_tc.get('title', 'N/A')}")
                print(f"       우선순위: {sample_tc.get('priority', 'N/A')}")
                print(f"       타입: {sample_tc.get('type', 'N/A')}")
                print(f"       도메인: {sample_tc.get('domain', 'N/A')}")
            print("   " + "-" * 60)
        
        print("\n" + "="*70)
        print("🎉 Fixed Multiplier Mode 테스트케이스 생성 완료!")
        print(f"📁 생성된 파일들은 {output_dir}/ 에서 확인하세요")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
