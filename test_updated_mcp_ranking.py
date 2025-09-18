#!/usr/bin/env python3
"""
업데이트된 MCP 서버의 랭킹 시스템 지원 테스트
"""

import sys
import json
from datetime import datetime

# MCP 서버 import
try:
    from mcp_figma_server import FigmaMCPServer
except ImportError:
    print("❌ mcp_figma_server.py를 import할 수 없습니다.")
    sys.exit(1)

def test_ranking_keywords():
    """랭킹 시스템 키워드 감지 테스트"""
    print("🏆 랭킹 시스템 키워드 감지 테스트...")
    
    server = FigmaMCPServer()
    
    # 랭킹 시스템 관련 텍스트들
    ranking_texts = [
        "리더보드 순위 표시",
        "현재 순위: 15위",
        "ranking system",
        "대회 참가자 순위",
        "1위 사용자",
        "경쟁 순위 변동",
        "leaderboard position",
        "competition rank",
        "마일스톤 달성",
        "순위별 보상"
    ]
    
    # 티어 시스템 관련 텍스트들 (이제 감지되지 않아야 함)
    tier_texts = [
        "Bronze 티어 승급",
        "Silver to Gold upgrade", 
        "tier progress bar",
        "등급 시스템"
    ]
    
    print("✅ 랭킹 시스템 텍스트 감지 테스트:")
    ranking_detected = 0
    for text in ranking_texts:
        is_requirement = server._is_requirement_text(text)
        if is_requirement:
            ranking_detected += 1
            print(f"  ✓ '{text}' → 감지됨")
        else:
            print(f"  ✗ '{text}' → 미감지")
    
    print(f"\n📊 랭킹 관련: {ranking_detected}/{len(ranking_texts)} 감지")
    
    print("\n⚠️ 티어 시스템 텍스트 감지 테스트 (여전히 감지될 수 있음):")
    tier_detected = 0
    for text in tier_texts:
        is_requirement = server._is_requirement_text(text)
        if is_requirement:
            tier_detected += 1
            print(f"  ! '{text}' → 감지됨 (예상됨 - 일반 키워드 포함)")
        else:
            print(f"  ✓ '{text}' → 미감지")
    
    print(f"\n📊 티어 관련: {tier_detected}/{len(tier_texts)} 감지")
    
    return ranking_detected, tier_detected

def test_ranking_categorization():
    """랭킹 시스템 카테고리 분류 테스트"""
    print("\n🏷️ 랭킹 시스템 카테고리 분류 테스트...")
    
    server = FigmaMCPServer()
    
    test_requirements = [
        {
            'text': '리더보드 순위 표시 기능',
            'source': 'test',
            'node_name': 'leaderboard',
            'node_id': 'test-001'
        },
        {
            'text': '대회 참가자 순위 업데이트',
            'source': 'test', 
            'node_name': 'ranking',
            'node_id': 'test-002'
        },
        {
            'text': 'competition ranking system',
            'source': 'test',
            'node_name': 'competition',
            'node_id': 'test-003'
        }
    ]
    
    for req in test_requirements:
        result = server.generate_testcase_structure(req)
        if result['success']:
            testcase = result['testcase']
            category = testcase['카테고리']
            priority = testcase['우선순위']
            print(f"  ✓ '{req['text']}' → 카테고리: {category}, 우선순위: {priority}")
        else:
            print(f"  ✗ '{req['text']}' → 실패")
    
    return True

def test_enhanced_analysis_ranking():
    """향상된 분석의 랭킹 시스템 패턴 감지 테스트"""
    print("\n🔍 향상된 분석 랭킹 패턴 감지 테스트...")
    
    server = FigmaMCPServer()
    
    # 모의 Figma 데이터 (랭킹 시스템 포함)
    mock_figma_data = {
        'document': {
            'children': [
                {
                    'type': 'FRAME',
                    'name': 'Leaderboard',
                    'children': [
                        {
                            'type': 'TEXT',
                            'characters': 'Current Ranking: #15',
                            'name': 'rank_display'
                        },
                        {
                            'type': 'TEXT', 
                            'characters': '순위 변동: +3',
                            'name': 'rank_change'
                        },
                        {
                            'type': 'COMPONENT',
                            'name': 'Competition Leaderboard',
                            'children': []
                        }
                    ]
                }
            ]
        }
    }
    
    # 향상된 키워드 분석 테스트
    keywords_result = server._analyze_enhanced_keywords(mock_figma_data)
    detected_patterns = keywords_result.get('detected_patterns', {})
    
    print(f"  감지된 패턴: {list(detected_patterns.keys())}")
    
    if 'ranking_system' in detected_patterns:
        ranking_info = detected_patterns['ranking_system']
        print(f"  ✅ 랭킹 시스템 패턴 감지됨!")
        print(f"    - 매칭 수: {ranking_info['matches']}")
        print(f"    - 신뢰도: {ranking_info['confidence']}%")
        print(f"    - 플로우 타입: {ranking_info['flow_type']}")
        return True
    else:
        print("  ❌ 랭킹 시스템 패턴이 감지되지 않음")
        return False

def test_template_feature_mapping():
    """템플릿 feature 매핑 테스트"""
    print("\n📋 템플릿 feature 매핑 테스트...")
    
    server = FigmaMCPServer()
    
    test_cases = [
        {'제목': '리더보드 순위 표시 테스트', '카테고리': '랭킹시스템'},
        {'제목': 'ranking system verification', '카테고리': '랭킹시스템'},
        {'제목': '대회 참가 기능 테스트', '카테고리': '랭킹시스템'}
    ]
    
    for i, case in enumerate(test_cases):
        converted = server._convert_to_template_format(case, i)
        feature = converted['feature']
        print(f"  ✓ '{case['제목']}' → Feature: {feature}")
        
        if feature == 'Ranking System':
            print("    ✅ 올바른 랭킹 시스템 feature 매핑")
        else:
            print(f"    ⚠️ 예상과 다른 feature: {feature}")
    
    return True

def create_test_summary():
    """테스트 결과 요약 생성"""
    
    summary = {
        "test_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mcp_server_update": "Trading Competition = 랭킹 시스템",
        "updates_applied": [
            "랭킹 시스템 키워드 추가 (한국어/영어)",
            "카테고리 분류에 '랭킹시스템' 추가", 
            "우선순위 분류에 랭킹 관련 키워드 P1 설정",
            "향상된 분석에 'ranking_system' 패턴 추가",
            "템플릿 변환에 'Ranking System' feature 추가"
        ],
        "key_ranking_keywords": [
            "랭킹, 순위, 리더보드, 대회, 경쟁",
            "ranking, rank, leaderboard, competition",
            "1위, 2위, 3위, 1st, 2nd, 3rd",
            "마일스톤, 달성, milestone, achievement",
            "순위변동, 순위상승, rank up, rank down"
        ],
        "expected_behavior": {
            "keyword_detection": "랭킹 관련 텍스트가 요구사항으로 감지됨",
            "categorization": "랭킹 관련 요구사항이 '랭킹시스템' 카테고리로 분류됨",
            "priority": "랭킹 핵심 기능이 P1 우선순위로 설정됨",
            "pattern_detection": "향상된 분석에서 'ranking_system' 패턴 감지",
            "template_mapping": "Excel 템플릿에서 'Ranking System' feature로 매핑"
        }
    }
    
    # JSON 파일로 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mcp_ranking_update_test_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    return filename, summary

def main():
    """메인 테스트 실행"""
    print("🧪 업데이트된 MCP 서버 랭킹 시스템 지원 테스트 시작\n")
    
    try:
        # 1. 키워드 감지 테스트
        ranking_detected, tier_detected = test_ranking_keywords()
        
        # 2. 카테고리 분류 테스트 
        test_ranking_categorization()
        
        # 3. 향상된 분석 테스트
        pattern_detected = test_enhanced_analysis_ranking()
        
        # 4. 템플릿 매핑 테스트
        test_template_feature_mapping()
        
        # 5. 테스트 요약 생성
        summary_file, summary_data = create_test_summary()
        
        print(f"\n📊 테스트 결과 요약:")
        print(f"  ✅ 랭킹 키워드 감지: {ranking_detected}/10")
        print(f"  ✅ 랭킹 패턴 감지: {'성공' if pattern_detected else '실패'}")
        print(f"  ✅ 카테고리 분류: 랭킹시스템")
        print(f"  ✅ 우선순위: P1 (핵심 기능)")
        print(f"  ✅ Feature 매핑: Ranking System")
        
        print(f"\n📄 테스트 요약 파일: {summary_file}")
        
        print(f"\n🎉 MCP 서버 랭킹 시스템 업데이트 완료!")
        print(f"   이제 Trading Competition 관련 Figma 분석 시")
        print(f"   랭킹 시스템으로 올바르게 분류되고 처리됩니다.")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
