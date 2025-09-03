#!/usr/bin/env python3
"""
Figma QA TestCase Generator - API 사용 예제
"""

import os
import sys
from dotenv import load_dotenv

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.analyzers.figma_analyzer import FigmaAnalyzer
from src.generators.testcase_generator import TestCaseGenerator

def api_usage_demo():
    """API 사용 데모"""
    print("🔧 API 사용 예제 실행")
    print("=" * 50)
    
    # 환경변수 로드
    load_dotenv()
    
    # Figma 토큰 확인
    figma_token = os.getenv("FIGMA_TOKEN")
    if not figma_token or figma_token == "your_figma_personal_access_token_here":
        print("⚠️  Figma 토큰이 설정되지 않았습니다.")
        print("    .env 파일에 실제 토큰을 추가하세요:")
        print("    FIGMA_TOKEN=figd_your_actual_token_here")
        print("\n📖 토큰 발급 방법:")
        print("    1. https://www.figma.com/settings 접속")
        print("    2. 'Personal access tokens' 섹션")
        print("    3. 'Create new token' 클릭")
        print("    4. 생성된 토큰을 .env 파일에 추가")
        return
    
    try:
        # 1. 분석기 및 생성기 초기화
        print("🔍 분석기 및 생성기 초기화")
        analyzer = FigmaAnalyzer(figma_token)
        generator = TestCaseGenerator()
        
        # 2. 샘플 Figma URL (실제 URL로 변경하세요)
        figma_url = "https://www.figma.com/design/iZNsaQjAyHxElK9mNXKqXB/X-OAuth?node-id=2-4"
        print(f"📊 Figma URL 분석: {figma_url}")
        
        # 3. 향상된 분석 실행
        print("🔬 향상된 분석 실행 중...")
        result = analyzer.enhanced_analysis(figma_url, include_screenshot=False)
        
        if result.get("success"):
            print("✅ 분석 성공!")
            
            # 4. 분석 결과 확인
            summary = result.get("summary", {})
            print(f"   총 UI 요소: {summary.get('total_elements', 0)}개")
            print(f"   UI 복잡도: {summary.get('ui_complexity', 'unknown')}")
            print(f"   주요 플로우: {summary.get('flow_type', 'unknown')}")
            print(f"   감지된 패턴: {len(summary.get('ui_patterns', []))}개")
            
            # 5. 테스트케이스 생성
            print("📝 테스트케이스 생성 중...")
            testcases = generator.generate_from_analysis(result)
            print(f"   생성된 테스트케이스: {len(testcases)}개")
            
            # 6. 출력 디렉토리 생성
            os.makedirs("demo_output", exist_ok=True)
            
            # 7. 다양한 형식으로 저장
            print("💾 파일 저장 중...")
            generator.save_to_excel(testcases, "demo_output/api_demo.xlsx")
            generator.save_to_testrail_csv(testcases, "demo_output/api_demo.csv")
            generator.save_to_json(testcases, "demo_output/api_demo.json")
            print("   ✅ Excel: demo_output/api_demo.xlsx")
            print("   ✅ TestRail: demo_output/api_demo.csv")
            print("   ✅ JSON: demo_output/api_demo.json")
            
            # 8. 특정 우선순위만 필터링
            print("🎯 우선순위별 필터링...")
            p1_testcases = generator.generate_by_priority(result, "P1")
            print(f"   P1 테스트케이스: {len(p1_testcases)}개")
            
            # 9. 우선순위별 통계
            priority_stats = {}
            for tc in testcases:
                priority = tc.get("priority", "Unknown")
                priority_stats[priority] = priority_stats.get(priority, 0) + 1
            
            print("📊 우선순위별 분포:")
            for priority in ["P1", "P2", "P3", "P4"]:
                count = priority_stats.get(priority, 0)
                if count > 0:
                    print(f"   {priority}: {count}개")
            
            # 10. 커스텀 시나리오 생성
            print("🎨 커스텀 시나리오 생성...")
            custom_config = {
                "feature_name": "사용자 로그인",
                "priority": "P1",
                "scenarios": [
                    "정상 로그인 플로우",
                    "잘못된 비밀번호",
                    "계정 잠금 상황",
                    "소셜 로그인 연동"
                ]
            }
            
            custom_testcases = generator.generate_scenarios(custom_config)
            print(f"   커스텀 테스트케이스: {len(custom_testcases)}개")
            
            # 11. 커스텀 테스트케이스 저장
            generator.save_to_excel(custom_testcases, "demo_output/custom_scenarios.xlsx")
            print("   ✅ 커스텀 시나리오: demo_output/custom_scenarios.xlsx")
            
            print("\n🎉 API 데모 완료!")
            print("📁 생성된 파일들은 demo_output/ 디렉토리에서 확인하세요")
            
        else:
            print(f"❌ 분석 실패: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

def show_basic_usage():
    """기본 사용법 안내"""
    print("\n" + "=" * 60)
    print("📚 기본 사용법 안내")
    print("=" * 60)
    
    print("""
🚀 1. CLI (명령행) 사용법:
    python src/main.py "https://figma.com/your-url"
    python src/main.py "figma-url" --output my_tests.xlsx --verbose
    
🔧 2. Python API 사용법:
    from src.analyzers.figma_analyzer import FigmaAnalyzer
    from src.generators.testcase_generator import TestCaseGenerator
    
    analyzer = FigmaAnalyzer()
    result = analyzer.enhanced_analysis("figma-url")
    
    generator = TestCaseGenerator()
    testcases = generator.generate_from_analysis(result)
    
🎯 3. MCP 서버 사용법:
    cd /Users/rowroh/Documents/testcase
    python mcp_figma_server.py
    
💡 주요 옵션:
    --format excel|testrail|json  # 출력 형식
    --analysis basic|enhanced     # 분석 유형
    --priority P1|P2|P3|P4       # 우선순위 필터
    --no-screenshot              # 스크린샷 분석 제외
    --verbose                    # 상세 출력
    """)

if __name__ == "__main__":
    api_usage_demo()
    show_basic_usage()
