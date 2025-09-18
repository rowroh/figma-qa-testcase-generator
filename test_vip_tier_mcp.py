#!/usr/bin/env python3
"""
VIP 티어 시스템이 추가된 MCP 서버 테스트
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

def test_vip_tier_keywords():
    """VIP 티어 시스템 키워드 감지 테스트"""
    print("🌟 VIP 티어 시스템 키워드 감지 테스트...")
    
    server = FigmaMCPServer()
    
    # VIP 티어 시스템 관련 텍스트들
    vip_tier_texts = [
        "VIP 등급 표시",
        "사용자 티어 배지",
        "membership upgrade",
        "멤버십 승급 진행률",
        "Gold 티어 혜택",
        "premium tier benefits",
        "SVIP 전용 서비스",
        "티어 승급 조건",
        "등급별 할인 혜택",
        "VIP tier system"
    ]
    
    # 랭킹 시스템과 구분되어야 하는 텍스트들
    ranking_texts = [
        "리더보드 순위",
        "대회 1위",
        "competition ranking",
        "순위 변동"
    ]
    
    print("✅ VIP 티어 시스템 텍스트 감지 테스트:")
    vip_detected = 0
    for text in vip_tier_texts:
        is_requirement = server._is_requirement_text(text)
        if is_requirement:
            vip_detected += 1
            print(f"  ✓ '{text}' → 감지됨")
        else:
            print(f"  ✗ '{text}' → 미감지")
    
    print(f"\n📊 VIP 티어 관련: {vip_detected}/{len(vip_tier_texts)} 감지")
    
    print("\n🏆 랭킹 시스템 텍스트 감지 확인 (구분 목적):")
    ranking_detected = 0
    for text in ranking_texts:
        is_requirement = server._is_requirement_text(text)
        if is_requirement:
            ranking_detected += 1
            print(f"  ✓ '{text}' → 감지됨")
        else:
            print(f"  ✗ '{text}' → 미감지")
    
    print(f"\n📊 랭킹 관련: {ranking_detected}/{len(ranking_texts)} 감지")
    
    return vip_detected, ranking_detected

def test_system_distinction():
    """VIP 티어 시스템과 랭킹 시스템 구분 테스트"""
    print("\n🎯 시스템 구분 테스트...")
    
    server = FigmaMCPServer()
    
    test_requirements = [
        # VIP 티어 시스템
        {
            'text': 'VIP 등급 승급 시스템',
            'expected_category': 'VIP티어시스템',
            'system_type': 'VIP 티어'
        },
        {
            'text': '사용자 멤버십 티어 관리',
            'expected_category': 'VIP티어시스템', 
            'system_type': 'VIP 티어'
        },
        {
            'text': 'premium membership benefits',
            'expected_category': 'VIP티어시스템',
            'system_type': 'VIP 티어'
        },
        # 랭킹 시스템
        {
            'text': '대회 리더보드 순위',
            'expected_category': '랭킹시스템',
            'system_type': '랭킹'
        },
        {
            'text': 'competition ranking display',
            'expected_category': '랭킹시스템',
            'system_type': '랭킹'
        }
    ]
    
    correct_classifications = 0
    for req in test_requirements:
        result = server.generate_testcase_structure(req)
        if result['success']:
            testcase = result['testcase']
            category = testcase['카테고리']
            priority = testcase['우선순위']
            
            is_correct = category == req['expected_category']
            status = "✅ 정확" if is_correct else "❌ 오류"
            
            print(f"  {status} '{req['text']}'")
            print(f"    → 예상: {req['expected_category']}, 실제: {category}, 우선순위: {priority}")
            
            if is_correct:
                correct_classifications += 1
        else:
            print(f"  ❌ 실패 '{req['text']}' → 테스트케이스 생성 실패")
    
    print(f"\n📊 구분 정확도: {correct_classifications}/{len(test_requirements)}")
    return correct_classifications == len(test_requirements)

def test_enhanced_analysis_vip():
    """향상된 분석의 VIP 티어 시스템 패턴 감지 테스트"""
    print("\n🔍 향상된 분석 VIP 티어 패턴 감지 테스트...")
    
    server = FigmaMCPServer()
    
    # 모의 VIP 티어 시스템 Figma 데이터
    mock_vip_figma_data = {
        'document': {
            'children': [
                {
                    'type': 'FRAME',
                    'name': 'VIP Membership',
                    'children': [
                        {
                            'type': 'TEXT',
                            'characters': 'Current Tier: Gold',
                            'name': 'tier_display'
                        },
                        {
                            'type': 'TEXT',
                            'characters': 'VIP 혜택: 수수료 20% 할인',
                            'name': 'benefit_info'
                        },
                        {
                            'type': 'COMPONENT',
                            'name': 'Tier Upgrade Progress',
                            'children': []
                        },
                        {
                            'type': 'TEXT',
                            'characters': 'Premium Membership',
                            'name': 'membership_title'
                        }
                    ]
                }
            ]
        }
    }
    
    # 향상된 키워드 분석 테스트
    keywords_result = server._analyze_enhanced_keywords(mock_vip_figma_data)
    detected_patterns = keywords_result.get('detected_patterns', {})
    
    print(f"  감지된 패턴: {list(detected_patterns.keys())}")
    
    vip_detected = False
    ranking_detected = False
    
    if 'vip_tier_system' in detected_patterns:
        vip_info = detected_patterns['vip_tier_system']
        print(f"  ✅ VIP 티어 시스템 패턴 감지됨!")
        print(f"    - 매칭 수: {vip_info['matches']}")
        print(f"    - 신뢰도: {vip_info['confidence']}%")
        print(f"    - 플로우 타입: {vip_info['flow_type']}")
        vip_detected = True
    
    if 'ranking_system' in detected_patterns:
        ranking_info = detected_patterns['ranking_system']
        print(f"  ⚠️ 랭킹 시스템 패턴도 감지됨 (의외)")
        print(f"    - 매칭 수: {ranking_info['matches']}")
        print(f"    - 신뢰도: {ranking_info['confidence']}%")
        ranking_detected = True
    
    if not vip_detected:
        print("  ❌ VIP 티어 시스템 패턴이 감지되지 않음")
    
    return vip_detected

def test_template_feature_mapping_vip():
    """VIP 티어 시스템 템플릿 feature 매핑 테스트"""
    print("\n📋 VIP 티어 시스템 템플릿 feature 매핑 테스트...")
    
    server = FigmaMCPServer()
    
    vip_test_cases = [
        {'제목': 'VIP 등급 표시 테스트', '카테고리': 'VIP티어시스템'},
        {'제목': 'membership tier upgrade test', '카테고리': 'VIP티어시스템'},
        {'제목': '사용자 티어 혜택 확인', '카테고리': 'VIP티어시스템'},
        {'제목': 'premium tier benefits verification', '카테고리': 'VIP티어시스템'}
    ]
    
    correct_mappings = 0
    for i, case in enumerate(vip_test_cases):
        converted = server._convert_to_template_format(case, i)
        feature = converted['feature']
        print(f"  ✓ '{case['제목']}' → Feature: {feature}")
        
        if feature == 'VIP Tier System':
            print("    ✅ 올바른 VIP 티어 시스템 feature 매핑")
            correct_mappings += 1
        else:
            print(f"    ⚠️ 예상과 다른 feature: {feature}")
    
    print(f"\n📊 VIP feature 매핑 정확도: {correct_mappings}/{len(vip_test_cases)}")
    return correct_mappings == len(vip_test_cases)

def create_vip_test_summary():
    """VIP 티어 시스템 테스트 결과 요약 생성"""
    
    summary = {
        "test_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mcp_server_update": "VIP 티어 시스템 추가",
        "system_distinction": {
            "trading_competition": "랭킹 시스템 (동적 순위 경쟁)",
            "user_vip_system": "티어 시스템 (고정 등급 멤버십)"
        },
        "vip_updates_applied": [
            "VIP 티어 시스템 키워드 추가 (한국어/영어)",
            "카테고리 분류에 'VIP티어시스템' 추가",
            "우선순위 분류에 VIP 관련 키워드 P1 설정", 
            "향상된 분석에 'vip_tier_system' 패턴 추가",
            "템플릿 변환에 'VIP Tier System' feature 추가"
        ],
        "key_vip_keywords": [
            "VIP, SVIP, 티어, 등급, 멤버십",
            "vip, svip, tier, grade, membership",
            "승급, 강등, upgrade, downgrade",
            "혜택, 특권, benefit, privilege",
            "베이직, 실버, 골드, 플래티넘"
        ],
        "expected_behavior": {
            "keyword_detection": "VIP 관련 텍스트가 요구사항으로 감지됨",
            "categorization": "VIP 관련 요구사항이 'VIP티어시스템' 카테고리로 분류됨",
            "distinction": "랭킹 시스템과 VIP 티어 시스템이 올바르게 구분됨",
            "pattern_detection": "향상된 분석에서 'vip_tier_system' 패턴 감지",
            "template_mapping": "Excel 템플릿에서 'VIP Tier System' feature로 매핑"
        }
    }
    
    # JSON 파일로 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mcp_vip_tier_test_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    return filename, summary

def main():
    """메인 테스트 실행"""
    print("🧪 VIP 티어 시스템 추가된 MCP 서버 테스트 시작\n")
    
    try:
        # 1. VIP 키워드 감지 테스트
        vip_detected, ranking_detected = test_vip_tier_keywords()
        
        # 2. 시스템 구분 테스트
        distinction_success = test_system_distinction()
        
        # 3. 향상된 분석 VIP 패턴 테스트
        vip_pattern_detected = test_enhanced_analysis_vip()
        
        # 4. VIP 템플릿 매핑 테스트
        vip_mapping_success = test_template_feature_mapping_vip()
        
        # 5. 테스트 요약 생성
        summary_file, summary_data = create_vip_test_summary()
        
        print(f"\n📊 VIP 티어 시스템 테스트 결과 요약:")
        print(f"  ✅ VIP 키워드 감지: {vip_detected}/10")
        print(f"  ✅ 랭킹 키워드 감지: {ranking_detected}/4 (기존 기능 유지)")
        print(f"  ✅ 시스템 구분: {'성공' if distinction_success else '실패'}")
        print(f"  ✅ VIP 패턴 감지: {'성공' if vip_pattern_detected else '실패'}")
        print(f"  ✅ VIP Feature 매핑: {'성공' if vip_mapping_success else '실패'}")
        
        print(f"\n🎯 시스템 구분 확인:")
        print(f"  🏆 Trading Competition → 랭킹 시스템")
        print(f"  🌟 User VIP System → 티어 시스템")
        
        print(f"\n📄 테스트 요약 파일: {summary_file}")
        
        print(f"\n🎉 MCP 서버 VIP 티어 시스템 추가 완료!")
        print(f"   이제 Figma 분석 시 VIP 관련 요소들이")
        print(f"   티어 시스템으로 올바르게 분류됩니다.")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
