#!/usr/bin/env python3
"""
Figma QA TestCase Generator - 빠른 시작 예제
"""

import os
import sys
from dotenv import load_dotenv

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.analyzers.figma_analyzer import FigmaAnalyzer
from src.generators.testcase_generator import TestCaseGenerator

def quick_start_demo():
    """빠른 시작 데모"""
    print("🚀 Figma QA TestCase Generator - 빠른 시작")
    print("="*60)
    
    # 환경변수 로드
    load_dotenv()
    
    # Figma API 토큰 확인
    figma_token = os.getenv("FIGMA_TOKEN")
    if not figma_token:
        print("❌ FIGMA_TOKEN 환경변수가 설정되지 않았습니다.")
        print("   1. .env 파일을 생성하세요")
        print("   2. FIGMA_TOKEN=your_token_here 추가하세요")
        return
    
    # 예제 Figma URL (실제 URL로 변경하세요)
    sample_figma_url = "https://www.figma.com/design/iZNsaQjAyHxElK9mNXKqXB/X-OAuth?node-id=2-4"
    
    try:
        # 1. Figma 분석기 초기화
        print("🔍 1단계: Figma 분석기 초기화")
        analyzer = FigmaAnalyzer(figma_token)
        
        # 2. 기본 분석 실행
        print("📊 2단계: 기본 분석 실행")
        basic_result = analyzer.basic_analysis(sample_figma_url)
        
        if not basic_result.get("success"):
            print(f"❌ 기본 분석 실패: {basic_result.get('error')}")
            return
        
        print(f"   ✅ 요구사항 {len(basic_result.get('requirements', []))}개 추출")
        
        # 3. 향상된 분석 실행
        print("🔬 3단계: 향상된 분석 실행")
        enhanced_result = analyzer.enhanced_analysis(sample_figma_url, include_screenshot=False)
        
        if not enhanced_result.get("success"):
            print(f"❌ 향상된 분석 실패: {enhanced_result.get('error')}")
            return
        
        # 분석 결과 출력
        summary = enhanced_result.get("summary", {})
        print(f"   ✅ 총 요소: {summary.get('total_elements', 0)}개")
        print(f"   ✅ UI 패턴: {len(summary.get('ui_patterns', []))}개")
        print(f"   ✅ 주요 플로우: {summary.get('flow_type', 'unknown')}")
        print(f"   ✅ UI 복잡도: {summary.get('ui_complexity', 'medium')}")
        
        # 4. 테스트케이스 생성기 초기화
        print("📝 4단계: 테스트케이스 생성")
        generator = TestCaseGenerator()
        
        # 5. 테스트케이스 생성
        testcases = generator.generate_from_analysis(enhanced_result)
        print(f"   ✅ 테스트케이스 {len(testcases)}개 생성")
        
        # 6. 우선순위별 통계
        priority_stats = {}
        for tc in testcases:
            priority = tc.get("priority", "Unknown")
            priority_stats[priority] = priority_stats.get(priority, 0) + 1
        
        print("   📊 우선순위별 분포:")
        for priority in ["P1", "P2", "P3", "P4"]:
            count = priority_stats.get(priority, 0)
            if count > 0:
                print(f"      {priority}: {count}개")
        
        # 7. 출력 디렉토리 생성
        output_dir = "examples/output_samples"
        os.makedirs(output_dir, exist_ok=True)
        
        # 8. 다양한 형식으로 저장
        print("💾 5단계: 파일 저장")
        
        # Excel 저장
        excel_file = f"{output_dir}/quick_start_testcases.xlsx"
        generator.save_to_excel(testcases, excel_file)
        print(f"   ✅ Excel: {excel_file}")
        
        # TestRail CSV 저장
        testrail_file = f"{output_dir}/quick_start_testrail.csv"
        generator.save_to_testrail_csv(testcases, testrail_file)
        print(f"   ✅ TestRail: {testrail_file}")
        
        # JSON 저장
        json_file = f"{output_dir}/quick_start_testcases.json"
        generator.save_to_json(testcases, json_file)
        print(f"   ✅ JSON: {json_file}")
        
        # 9. 샘플 테스트케이스 출력
        print("🔍 6단계: 샘플 테스트케이스")
        if testcases:
            sample_tc = testcases[0]
            print("   " + "-" * 50)
            print(f"   제목: {sample_tc.get('title', 'N/A')}")
            print(f"   우선순위: {sample_tc.get('priority', 'N/A')}")
            print(f"   타입: {sample_tc.get('type', 'N/A')}")
            print(f"   도메인: {sample_tc.get('domain', 'N/A')}")
            print("   " + "-" * 50)
        
        print("\n🎉 빠른 시작 데모 완료!")
        print(f"📁 생성된 파일들은 {output_dir}/ 에서 확인하세요")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

def custom_scenario_demo():
    """커스텀 시나리오 데모"""
    print("\n" + "="*60)
    print("🎯 커스텀 시나리오 데모")
    print("="*60)
    
    # 커스텀 시나리오 정의
    custom_scenarios = [
        {
            "domain": "custom",
            "section": "Custom Test",
            "component": "Custom Component",
            "feature": "Custom Feature",
            "title": "커스텀 테스트케이스 1",
            "precondition": "커스텀 전제조건",
            "test_steps": "1. 커스텀 단계 1\n2. 커스텀 단계 2",
            "expected_results": "1. 커스텀 결과 1\n2. 커스텀 결과 2",
            "priority": "P1",
            "type": "Functional"
        }
    ]
    
    generator = TestCaseGenerator()
    
    # 시나리오 기반 생성
    scenario_config = {
        "feature_name": "Custom Feature",
        "priority": "P1",
        "scenarios": [
            "정상 플로우",
            "예외 상황 처리",
            "성능 테스트"
        ]
    }
    
    testcases = generator.generate_scenarios(scenario_config)
    print(f"✅ 시나리오 기반 테스트케이스 {len(testcases)}개 생성")
    
    for i, tc in enumerate(testcases, 1):
        print(f"   {i}. {tc.get('title', 'N/A')}")

if __name__ == "__main__":
    quick_start_demo()
    custom_scenario_demo()
    
    print("\n" + "="*60)
    print("💡 다음 단계:")
    print("   1. 실제 Figma URL로 테스트해보세요")
    print("   2. config/keywords.json에서 키워드를 커스터마이징하세요")
    print("   3. src/main.py로 명령행에서 실행해보세요")
    print("="*60)
