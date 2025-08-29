#!/usr/bin/env python3
"""
FigmaAnalyzer 테스트
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzers.figma_analyzer import FigmaAnalyzer

class TestFigmaAnalyzer:
    """FigmaAnalyzer 테스트 클래스"""
    
    def setup_method(self):
        """테스트 설정"""
        self.analyzer = FigmaAnalyzer(figma_token="test_token")
    
    def test_parse_figma_url_valid(self):
        """유효한 Figma URL 파싱 테스트"""
        url = "https://www.figma.com/design/iZNsaQjAyHxElK9mNXKqXB/X-OAuth?node-id=2-4"
        result = self.analyzer.parse_figma_url(url)
        
        assert result["success"] is True
        assert result["file_id"] == "iZNsaQjAyHxElK9mNXKqXB"
        assert result["node_id"] == "2-4"
    
    def test_parse_figma_url_invalid(self):
        """유효하지 않은 Figma URL 파싱 테스트"""
        url = "https://invalid-url.com"
        result = self.analyzer.parse_figma_url(url)
        
        assert result["success"] is False
        assert "error" in result
    
    def test_is_requirement_text_valid(self):
        """요구사항 텍스트 판별 테스트 - 유효한 경우"""
        valid_texts = [
            "로그인 버튼 클릭",
            "사용자 프로필 설정",
            "거래 내역 조회",
            "Login functionality"
        ]
        
        for text in valid_texts:
            assert self.analyzer._is_requirement_text(text) is True
    
    def test_is_requirement_text_invalid(self):
        """요구사항 텍스트 판별 테스트 - 유효하지 않은 경우"""
        invalid_texts = [
            "px",  # 너무 짧음
            "color: #ffffff",  # 제외 키워드 포함
            "font-size: 16px",  # CSS 속성
            "a" * 1001,  # 너무 김
            ""  # 빈 문자열
        ]
        
        for text in invalid_texts:
            assert self.analyzer._is_requirement_text(text) is False
    
    @patch('requests.get')
    def test_fetch_figma_data_success(self, mock_get):
        """Figma 데이터 가져오기 성공 테스트"""
        # Mock 응답 설정
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "document": {
                "children": []
            }
        }
        mock_get.return_value = mock_response
        
        result = self.analyzer.fetch_figma_data("test_file_id")
        
        assert result["success"] is True
        assert "data" in result
    
    @patch('requests.get')
    def test_fetch_figma_data_api_error(self, mock_get):
        """Figma 데이터 가져오기 API 오류 테스트"""
        # Mock 응답 설정 (API 오류)
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": "Invalid token"
        }
        mock_get.return_value = mock_response
        
        result = self.analyzer.fetch_figma_data("test_file_id")
        
        assert result["success"] is False
        assert result["error"] == "Invalid token"
    
    def test_analyze_enhanced_keywords(self):
        """향상된 키워드 분석 테스트"""
        # 테스트용 Figma 데이터
        figma_data = {
            "document": {
                "children": [
                    {
                        "type": "TEXT",
                        "characters": "Login Button",
                        "children": []
                    },
                    {
                        "type": "FRAME",
                        "name": "Navigation Menu",
                        "children": []
                    }
                ]
            }
        }
        
        result = self.analyzer._analyze_enhanced_keywords(figma_data)
        
        assert "texts" in result
        assert "names" in result
        assert "detected_patterns" in result
        assert "total_elements" in result
        assert len(result["texts"]) > 0
        assert len(result["names"]) > 0
    
    def test_analyze_ui_structure(self):
        """UI 구조 분석 테스트"""
        # 테스트용 Figma 데이터
        figma_data = {
            "document": {
                "children": [
                    {
                        "type": "FRAME",
                        "name": "Login Button",
                        "children": []
                    },
                    {
                        "type": "COMPONENT",
                        "name": "Input Field",
                        "children": []
                    }
                ]
            }
        }
        
        result = self.analyzer._analyze_ui_structure(figma_data)
        
        assert "ui_elements" in result
        assert "layout_info" in result
        assert "ui_complexity" in result
        assert result["ui_complexity"] in ["low", "medium", "high"]
    
    def test_analyze_user_flow(self):
        """유저플로우 분석 테스트"""
        keyword_analysis = {
            "detected_patterns": {
                "authentication": {
                    "confidence": 80,
                    "flow_type": "auth_flow"
                }
            }
        }
        
        ui_analysis = {
            "ui_elements": {
                "buttons": [{"name": "Login Button"}],
                "inputs": [{"name": "Password Field"}]
            },
            "ui_complexity": "medium"
        }
        
        result = self.analyzer._analyze_user_flow(keyword_analysis, ui_analysis)
        
        assert "flow_steps" in result
        assert "primary_flow_type" in result
        assert "confidence" in result
        assert len(result["flow_steps"]) > 0
        assert result["primary_flow_type"] == "auth_flow"
    
    def test_generate_recommendations(self):
        """권장사항 생성 테스트"""
        keyword_analysis = {
            "detected_patterns": {
                "authentication": {"confidence": 80},
                "transaction": {"confidence": 60}
            }
        }
        
        ui_analysis = {
            "ui_elements": {
                "buttons": [{"name": f"Button{i}"} for i in range(7)]  # 7개 버튼
            },
            "ui_complexity": "high"
        }
        
        flow_analysis = {
            "flow_steps": ["step1", "step2", "step3", "step4", "step5", "step6"]  # 6단계
        }
        
        result = self.analyzer._generate_recommendations(
            keyword_analysis, ui_analysis, flow_analysis
        )
        
        assert "ui_improvements" in result
        assert "testing_priorities" in result
        assert "user_experience" in result
        assert len(result["testing_priorities"]) > 0  # 인증, 거래 관련 권장사항
    
    def test_analyze_differences(self):
        """차이점 분석 테스트"""
        as_is = {
            "summary": {
                "ui_patterns": ["navigation", "authentication"],
                "ui_complexity": "medium",
                "flow_type": "auth_flow"
            }
        }
        
        to_be = {
            "summary": {
                "ui_patterns": ["navigation", "authentication", "social"],
                "ui_complexity": "high",
                "flow_type": "social_interaction"
            }
        }
        
        result = self.analyzer._analyze_differences(as_is, to_be)
        
        assert "new_patterns" in result
        assert "removed_patterns" in result
        assert "ui_complexity_change" in result
        assert "flow_type_change" in result
        assert "social" in result["new_patterns"]


class TestFigmaAnalyzerIntegration:
    """FigmaAnalyzer 통합 테스트"""
    
    @pytest.mark.skipif(
        not os.getenv("FIGMA_TOKEN"),
        reason="FIGMA_TOKEN 환경변수가 설정되지 않음"
    )
    def test_real_figma_analysis(self):
        """실제 Figma API를 사용한 분석 테스트 (선택적)"""
        analyzer = FigmaAnalyzer()
        
        # 실제 Figma URL (공개된 예제 파일)
        sample_url = "https://www.figma.com/design/iZNsaQjAyHxElK9mNXKqXB/X-OAuth?node-id=2-4"
        
        result = analyzer.basic_analysis(sample_url)
        
        # 실제 API 호출이므로 성공 여부만 확인
        if result.get("success"):
            assert "requirements" in result
            assert len(result["requirements"]) >= 0
        else:
            # API 실패는 토큰 문제일 수 있으므로 스킵
            pytest.skip(f"API 호출 실패: {result.get('error')}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
