#!/usr/bin/env python3
"""
🎯 고급 5단계 파이프라인 데모

이 스크립트는 새로운 5단계 파이프라인 기능을 시연합니다.
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.advanced_pipeline import AdvancedPipeline


def main():
    print("=" * 80)
    print("🎯 고급 5단계 파이프라인 데모")
    print("=" * 80)
    print()
    
    # Figma URL (실제 URL로 교체하세요)
    figma_url = "https://www.figma.com/design/YOUR_FILE_ID"
    
    print("📝 입력 정보:")
    print(f"  - Figma URL: {figma_url}")
    print(f"  - 도메인: 가상화폐거래소")
    print(f"  - 기능: 카피트레이딩")
    print()
    
    # 파이프라인 생성
    pipeline = AdvancedPipeline(
        figma_url=figma_url,
        output_dir="output/advanced_demo"
    )
    
    # 전체 파이프라인 실행
    result = pipeline.run(
        domain="가상화폐거래소",
        feature_description="마스터 트레이더의 거래를 따라가는 카피트레이딩 기능"
    )
    
    # 결과 출력
    print()
    print("=" * 80)
    print("📊 실행 결과")
    print("=" * 80)
    print()
    print(f"✅ 성공: {result['success']}")
    print(f"📝 테스트케이스 수: {result['testcase_count']}개")
    print(f"🔍 검증 점수: {result['validation']['completeness_score']}/100")
    print(f"✅ 승인 여부: {result['validation']['approved']}")
    print()
    print("📂 생성된 파일:")
    print(f"  - CSV: {result['output_files']['csv_path']}")
    print(f"  - Excel: {result['output_files']['excel_path']}")
    print()
    print(f"📁 출력 디렉토리: {result['output_directory']}")
    print()
    
    # 단계별 파일도 확인
    print("📋 중간 산출물:")
    print(f"  - figma_analysis.json: Figma 분석 결과")
    print(f"  - checklist.json: 상세 체크리스트")
    print(f"  - testcases_draft.json: 테스트케이스 초안")
    print(f"  - validation_result.json: 검증 결과")
    print()


if __name__ == "__main__":
    main()

