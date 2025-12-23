#!/usr/bin/env python3
"""
Figma QA TestCase Generator - 메인 실행 스크립트
"""

import os
import sys
import argparse
from typing import Optional
from dotenv import load_dotenv

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzers.figma_analyzer import FigmaAnalyzer
from src.generators.testcase_generator import TestCaseGenerator
from src.utils.rules_config import DEFAULT_RULES_PATH

def main():
    """메인 실행 함수"""
    # 환경변수 로드
    # - Cursor/샌드박스 환경에서 .env가 ignore 처리되어 읽기 권한이 없을 수 있어 예외를 무시합니다.
    try:
        load_dotenv()
    except PermissionError:
        # .env를 읽을 수 없는 환경에서도 실행되도록 처리 (환경변수는 OS에서 직접 주입 가능)
        pass
    except OSError:
        pass
    
    # 명령행 인자 파싱
    parser = argparse.ArgumentParser(description='Figma QA TestCase Generator')
    parser.add_argument('figma_url', help='분석할 Figma URL')
    parser.add_argument('--output', '-o', default='output/testcases.xlsx', 
                       help='출력 파일 경로 (기본값: output/testcases.xlsx)')
    parser.add_argument('--format', '-f', choices=['excel', 'testrail', 'json'], 
                       default='excel', help='출력 형식 (기본값: excel)')
    parser.add_argument('--analysis', '-a', choices=['basic', 'enhanced'], 
                       default='enhanced', help='분석 유형 (기본값: enhanced)')
    parser.add_argument('--priority', '-p', choices=['P1', 'P2', 'P3', 'P4'],
                       help='최소 우선순위 필터 (예: P1은 P1만, P2는 P1,P2)')
    parser.add_argument('--no-screenshot', action='store_true',
                       help='스크린샷 분석 제외')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='상세 출력')
    parser.add_argument('--rules', default=DEFAULT_RULES_PATH,
                       help=f'룰/템플릿 설정 파일 경로 (기본값: {DEFAULT_RULES_PATH})')
    parser.add_argument('--show-flow-questions', action='store_true',
                       help='유저플로우 신뢰도가 낮으면 확인 질문을 출력')
    
    args = parser.parse_args()
    
    try:
        print("🚀 Figma QA TestCase Generator")
        print("="*50)
        
        # 출력 디렉토리 생성
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Figma 분석기 초기화
        if args.verbose:
            print("🔍 Figma 분석기 초기화 중...")
        
        analyzer = FigmaAnalyzer()
        
        # Figma 분석 실행
        include_screenshot = not args.no_screenshot
        
        if args.analysis == 'basic':
            if args.verbose:
                print("📊 기본 분석 실행 중...")
            result = analyzer.basic_analysis(args.figma_url)
        else:
            if args.verbose:
                print("🔬 향상된 분석 실행 중...")
            result = analyzer.enhanced_analysis(args.figma_url, include_screenshot)
        
        if not result.get("success"):
            print(f"❌ 분석 실패: {result.get('error')}")
            return 1
        
        # 분석 결과 출력
        if args.verbose:
            print_analysis_summary(result)
        
        # 테스트케이스 생성기 초기화
        if args.verbose:
            print("📝 테스트케이스 생성 중...")
        
        generator = TestCaseGenerator(rules_path=args.rules)

        # 유저플로우가 불명확한 경우 질문 출력 (옵션)
        if args.show_flow_questions:
            questions = generator.get_flow_clarification_questions(result)
            if questions:
                print("\n❓ 유저플로우 확인이 필요합니다. 아래 질문에 답변해 주세요:")
                for i, q in enumerate(questions, 1):
                    print(f"  {i}. {q}")
        
        # 테스트케이스 생성
        if args.priority:
            testcases = generator.generate_by_priority(result, args.priority)
        else:
            testcases = generator.generate_from_analysis(result)
        
        if not testcases:
            print("⚠️ 생성된 테스트케이스가 없습니다.")
            return 1
        
        # 파일 저장
        if args.verbose:
            print(f"💾 {len(testcases)}개 테스트케이스를 {args.format} 형식으로 저장 중...")
        
        if args.format == 'excel':
            generator.save_to_excel(testcases, args.output)
        elif args.format == 'testrail':
            generator.save_to_testrail_csv(testcases, args.output)
        elif args.format == 'json':
            generator.save_to_json(testcases, args.output)
        
        # 완료 메시지
        print(f"✅ 완료!")
        print(f"📁 파일: {args.output}")
        print(f"📊 테스트케이스: {len(testcases)}개")
        
        # 우선순위별 통계
        if args.verbose:
            print_testcase_statistics(testcases)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 중단되었습니다.")
        return 1
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def print_analysis_summary(result):
    """분석 결과 요약 출력"""
    print("\n📋 분석 결과 요약:")
    print("-" * 30)
    
    if result.get("analysis_type") == "enhanced":
        summary = result.get("summary", {})
        print(f"  총 요소 수: {summary.get('total_elements', 0)}")
        print(f"  UI 복잡도: {summary.get('ui_complexity', 'unknown')}")
        print(f"  주요 플로우: {summary.get('flow_type', 'unknown')}")
        print(f"  감지된 UI 패턴: {len(summary.get('ui_patterns', []))}")
        
        enhanced = result.get("enhanced_analysis", {})
        ui_structure = enhanced.get("ui_structure", {})
        ui_elements = ui_structure.get("ui_elements", {})
        
        print(f"  버튼: {len(ui_elements.get('buttons', []))}")
        print(f"  입력 필드: {len(ui_elements.get('inputs', []))}")
        print(f"  네비게이션: {len(ui_elements.get('navigation', []))}")
    else:
        basic = result.get("requirements", [])
        print(f"  추출된 요구사항: {len(basic)}개")

def print_testcase_statistics(testcases):
    """테스트케이스 통계 출력"""
    print("\n📈 테스트케이스 통계:")
    print("-" * 30)
    
    # 우선순위별 통계
    priority_counts = {}
    type_counts = {}
    domain_counts = {}
    
    for tc in testcases:
        priority = tc.get("priority", "Unknown")
        test_type = tc.get("type", "Unknown")
        domain = tc.get("domain", "Unknown")
        
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
        type_counts[test_type] = type_counts.get(test_type, 0) + 1
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    
    print("  우선순위별:")
    for priority in ["P1", "P2", "P3", "P4"]:
        count = priority_counts.get(priority, 0)
        if count > 0:
            print(f"    {priority}: {count}개")
    
    print("  타입별:")
    for test_type, count in sorted(type_counts.items()):
        print(f"    {test_type}: {count}개")
    
    print("  도메인별:")
    for domain, count in sorted(domain_counts.items()):
        print(f"    {domain}: {count}개")

if __name__ == "__main__":
    sys.exit(main())

