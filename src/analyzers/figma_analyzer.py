#!/usr/bin/env python3
"""
Figma 분석 엔진
- 키워드 기반 분석
- 스크린샷 분석  
- UI 구조 분석
- 유저플로우 추론
"""

import os
import re
import json
import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

class FigmaAnalyzer:
    """향상된 Figma 분석기"""
    
    def __init__(self, figma_token: Optional[str] = None):
        """
        초기화
        
        Args:
            figma_token: Figma API 토큰 (환경변수에서 자동 로드 가능)
        """
        self.figma_token = figma_token or os.getenv("FIGMA_TOKEN")
        if not self.figma_token:
            raise ValueError("FIGMA_TOKEN이 설정되지 않았습니다.")
        
        # UI 패턴 정의
        self.ui_patterns = {
            "navigation": {
                "keywords": ["nav", "menu", "tab", "breadcrumb", "back", "next", "home"],
                "flow_type": "navigation"
            },
            "authentication": {
                "keywords": ["login", "signup", "register", "signin", "oauth", "auth", "password"],
                "flow_type": "auth_flow"
            },
            "form_input": {
                "keywords": ["input", "field", "form", "textfield", "submit", "save", "cancel"],
                "flow_type": "form_interaction"
            },
            "modal_popup": {
                "keywords": ["modal", "popup", "dialog", "overlay", "confirm", "alert"],
                "flow_type": "modal_flow"
            },
            "transaction": {
                "keywords": ["buy", "sell", "trade", "order", "payment", "checkout", "confirm"],
                "flow_type": "transaction_flow"
            },
            "social": {
                "keywords": ["share", "like", "follow", "comment", "social", "connect"],
                "flow_type": "social_interaction"
            },
            "settings": {
                "keywords": ["settings", "preferences", "profile", "account", "config"],
                "flow_type": "settings_flow"
            }
        }
        
        # 플로우 패턴 정의
        self.flow_patterns = {
            "onboarding": ["welcome", "intro", "tutorial", "getting started", "setup"],
            "purchasing": ["add to cart", "checkout", "payment", "order", "buy"],
            "registration": ["sign up", "register", "create account", "join"],
            "verification": ["verify", "confirm", "validate", "check", "code"],
            "error_handling": ["error", "failed", "retry", "oops", "something went wrong"],
            "success": ["success", "complete", "done", "congratulations", "thank you"]
        }
        
        # 요구사항 키워드 (기존 mcp_figma_server.py에서 가져옴)
        self.requirement_keywords = [
            '기능', '요구사항', '사용자', '시스템', '화면', '페이지', '버튼',
            '클릭', '선택', '입력', '검색', '필터', '정렬', '스크롤',
            '로그인', '회원가입', '로그아웃', '프로필', '설정', '알림',
            '목록', '리스트', '카드', '메뉴', '탭', '모달', '팝업',
            '등록', '수정', '삭제', '추가', '업데이트', '동기화',
            # ... (전체 키워드 리스트)
            'login', 'signup', 'setting', 'search', 'filter', 'sort', 'upload', 'download',
            'button', 'click', 'tap', 'swipe', 'scroll'
        ]
    
    def parse_figma_url(self, url: str) -> Dict[str, Any]:
        """Figma URL 파싱"""
        try:
            # URL에서 file_id와 node_id 추출
            pattern = r'figma\.com/design/([a-zA-Z0-9]+)/.*?(?:node-id=([^&]+))?'
            match = re.search(pattern, url)
            
            if not match:
                return {"success": False, "error": "올바른 Figma URL이 아닙니다"}
            
            file_id = match.group(1)
            node_id = match.group(2) if match.group(2) else None
            
            return {
                "success": True,
                "file_id": file_id,
                "node_id": node_id,
                "url": url
            }
        except Exception as e:
            return {"success": False, "error": f"URL 파싱 오류: {str(e)}"}
    
    def fetch_figma_data(self, file_id: str, node_id: Optional[str] = None) -> Dict[str, Any]:
        """Figma API에서 데이터 가져오기"""
        try:
            headers = {"X-Figma-Token": self.figma_token}
            
            if node_id:
                # 특정 노드 데이터 가져오기
                node_id_formatted = node_id.replace('-', ':')
                url = f"https://api.figma.com/v1/files/{file_id}/nodes?ids={node_id_formatted}"
            else:
                # 전체 파일 데이터 가져오기
                url = f"https://api.figma.com/v1/files/{file_id}"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            if 'error' in data:
                return {"success": False, "error": data['error']}
            
            return {"success": True, "data": data}
            
        except requests.RequestException as e:
            return {"success": False, "error": f"API 요청 실패: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"데이터 가져오기 실패: {str(e)}"}
    
    def basic_analysis(self, figma_url: str) -> Dict[str, Any]:
        """기본 키워드 분석"""
        # URL 파싱
        parsed = self.parse_figma_url(figma_url)
        if not parsed.get("success"):
            return parsed
        
        # 데이터 가져오기
        data_result = self.fetch_figma_data(parsed["file_id"], parsed.get("node_id"))
        if not data_result.get("success"):
            return data_result
        
        # 요구사항 키워드 추출
        requirements = self._extract_requirements(data_result["data"])
        
        return {
            "success": True,
            "file_info": parsed,
            "requirements": requirements,
            "analysis_type": "basic"
        }
    
    def enhanced_analysis(self, figma_url: str, include_screenshot: bool = True) -> Dict[str, Any]:
        """향상된 분석 (키워드 + 스크린샷 + 플로우)"""
        try:
            # URL 파싱
            parsed = self.parse_figma_url(figma_url)
            if not parsed.get("success"):
                return parsed
            
            file_id = parsed["file_id"]
            node_id = parsed.get("node_id")
            
            # 데이터 가져오기
            data_result = self.fetch_figma_data(file_id, node_id)
            if not data_result.get("success"):
                return data_result
            
            figma_data = data_result["data"]
            
            # 1. 기본 요구사항 분석
            basic_requirements = self._extract_requirements(figma_data)
            
            # 2. 향상된 키워드 분석
            enhanced_keywords = self._analyze_enhanced_keywords(figma_data)
            
            # 3. UI 구조 분석
            ui_analysis = self._analyze_ui_structure(figma_data)
            
            # 4. 유저플로우 분석
            flow_analysis = self._analyze_user_flow(enhanced_keywords, ui_analysis)
            
            # 5. 스크린샷 분석 (옵션)
            screenshot_analysis = {}
            if include_screenshot:
                screenshot_analysis = self._analyze_screenshot(file_id, node_id)
            
            # 6. 권장사항 생성
            recommendations = self._generate_recommendations(enhanced_keywords, ui_analysis, flow_analysis)
            
            return {
                "success": True,
                "file_info": parsed,
                "basic_analysis": {
                    "requirements_count": len(basic_requirements),
                    "requirements": basic_requirements
                },
                "enhanced_analysis": {
                    "keywords": enhanced_keywords,
                    "ui_structure": ui_analysis,
                    "user_flow": flow_analysis,
                    "screenshot": screenshot_analysis if include_screenshot else None
                },
                "recommendations": recommendations,
                "summary": {
                    "total_elements": enhanced_keywords.get("total_elements", 0),
                    "ui_patterns": list(enhanced_keywords.get("detected_patterns", {}).keys()),
                    "flow_type": flow_analysis.get("primary_flow_type", "unknown"),
                    "confidence": flow_analysis.get("confidence", 0),
                    "ui_complexity": ui_analysis.get("ui_complexity", "medium")
                },
                "analysis_type": "enhanced"
            }
            
        except Exception as e:
            return {"success": False, "error": f"향상된 분석 실패: {str(e)}"}
    
    def _extract_requirements(self, figma_data: Dict) -> List[Dict]:
        """요구사항 텍스트 추출"""
        requirements = []
        
        def traverse_nodes(nodes, depth=0):
            if isinstance(nodes, list):
                for node in nodes:
                    traverse_nodes(node, depth)
            elif isinstance(nodes, dict):
                # 텍스트 노드 처리
                if node.get('type') == 'TEXT' and 'characters' in node:
                    text = node['characters'].strip()
                    if self._is_requirement_text(text):
                        requirements.append({
                            "text": text,
                            "type": "content",
                            "depth": depth
                        })
                
                # 노드 이름 처리
                node_name = node.get('name', '')
                if node_name and self._is_requirement_text(node_name):
                    requirements.append({
                        "text": node_name,
                        "type": "component",
                        "depth": depth
                    })
                
                # 자식 노드 탐색
                if 'children' in node:
                    traverse_nodes(node['children'], depth + 1)
        
        # 문서 루트부터 탐색
        document = figma_data.get('document', {})
        if 'children' in document:
            traverse_nodes(document['children'])
        
        return requirements
    
    def _is_requirement_text(self, text: str) -> bool:
        """텍스트가 요구사항인지 판단"""
        if not text or len(text) < 3 or len(text) > 1000:
            return False
        
        # 제외할 키워드들
        exclude_keywords = [
            'px', 'pt', 'rem', 'color', 'font', 'weight', 'size',
            'margin', 'padding', 'border', 'shadow', 'opacity'
        ]
        
        text_lower = text.lower()
        if any(exclude in text_lower for exclude in exclude_keywords):
            return False
        
        # 요구사항 키워드 포함 여부 확인
        return any(keyword in text for keyword in self.requirement_keywords)
    
    def _analyze_enhanced_keywords(self, figma_data: Dict) -> Dict[str, Any]:
        """향상된 키워드 분석"""
        texts = []
        names = []
        
        def traverse_nodes(nodes, depth=0):
            if isinstance(nodes, list):
                for node in nodes:
                    traverse_nodes(node, depth)
            elif isinstance(nodes, dict):
                node_type = node.get('type')
                node_name = node.get('name', '')
                
                if node_type == 'TEXT' and 'characters' in node:
                    text = node['characters'].strip()
                    if text:
                        texts.append({"text": text, "depth": depth})
                
                if node_type in ['FRAME', 'COMPONENT', 'INSTANCE'] and node_name:
                    names.append({"name": node_name, "type": node_type.lower(), "depth": depth})
                
                if 'children' in node:
                    traverse_nodes(node['children'], depth + 1)
        
        traverse_nodes(figma_data.get('document', {}).get('children', []))
        
        # 모든 텍스트 결합
        all_text = " ".join([t["text"] for t in texts] + [n["name"] for n in names])
        
        # UI 패턴 매칭
        detected_patterns = {}
        for pattern_name, pattern_info in self.ui_patterns.items():
            keywords = pattern_info["keywords"]
            matches = sum(1 for keyword in keywords if keyword.lower() in all_text.lower())
            if matches > 0:
                detected_patterns[pattern_name] = {
                    "matches": matches,
                    "flow_type": pattern_info["flow_type"],
                    "confidence": min(matches * 20, 100)
                }
        
        # 플로우 패턴 매칭
        detected_flows = {}
        for flow_name, flow_keywords in self.flow_patterns.items():
            matches = sum(1 for keyword in flow_keywords if keyword.lower() in all_text.lower())
            if matches > 0:
                detected_flows[flow_name] = {
                    "matches": matches,
                    "confidence": min(matches * 25, 100)
                }
        
        return {
            "texts": texts,
            "names": names,
            "detected_patterns": detected_patterns,
            "detected_flows": detected_flows,
            "total_elements": len(texts) + len(names)
        }
    
    def _analyze_ui_structure(self, figma_data: Dict) -> Dict[str, Any]:
        """UI 구조 분석"""
        ui_elements = {
            "buttons": [],
            "inputs": [],
            "navigation": [],
            "containers": []
        }
        
        layout_info = {
            "depth_levels": 0,
            "max_children": 0,
            "component_count": 0
        }
        
        def analyze_node(node, depth=0):
            if isinstance(node, dict):
                node_type = node.get('type', '')
                node_name = node.get('name', '').lower()
                
                layout_info["depth_levels"] = max(layout_info["depth_levels"], depth)
                
                # UI 요소 분류
                if 'button' in node_name or 'btn' in node_name:
                    ui_elements["buttons"].append({"name": node.get('name', ''), "depth": depth})
                elif any(keyword in node_name for keyword in ['input', 'field', 'textfield']):
                    ui_elements["inputs"].append({"name": node.get('name', ''), "depth": depth})
                elif any(keyword in node_name for keyword in ['nav', 'menu', 'tab']):
                    ui_elements["navigation"].append({"name": node.get('name', ''), "depth": depth})
                elif node_type in ['FRAME', 'GROUP']:
                    ui_elements["containers"].append({"name": node.get('name', ''), "depth": depth})
                
                if node_type in ['COMPONENT', 'INSTANCE']:
                    layout_info["component_count"] += 1
                
                children = node.get('children', [])
                if children:
                    layout_info["max_children"] = max(layout_info["max_children"], len(children))
                    for child in children:
                        analyze_node(child, depth + 1)
        
        for child in figma_data.get('document', {}).get('children', []):
            analyze_node(child)
        
        # UI 복잡도 계산
        total_elements = sum(len(elements) for elements in ui_elements.values())
        complexity_score = total_elements + layout_info["depth_levels"] * 2 + layout_info["component_count"]
        
        if complexity_score < 20:
            ui_complexity = "low"
        elif complexity_score < 50:
            ui_complexity = "medium"
        else:
            ui_complexity = "high"
        
        return {
            "ui_elements": ui_elements,
            "layout_info": layout_info,
            "ui_complexity": ui_complexity
        }
    
    def _analyze_user_flow(self, keyword_analysis: Dict, ui_analysis: Dict) -> Dict[str, Any]:
        """유저플로우 분석"""
        detected_patterns = keyword_analysis.get("detected_patterns", {})
        ui_elements = ui_analysis.get("ui_elements", {})
        
        # 플로우 단계 추론
        flow_steps = []
        
        if "authentication" in detected_patterns:
            flow_steps.append("사용자 인증")
        else:
            flow_steps.append("화면 진입")
        
        if ui_elements.get("inputs"):
            flow_steps.append("정보 입력")
        
        if ui_elements.get("buttons"):
            button_count = len(ui_elements["buttons"])
            if button_count == 1:
                flow_steps.append("액션 실행")
            else:
                flow_steps.append("옵션 선택")
        
        flow_steps.append("결과 확인")
        
        # 주요 플로우 타입 결정
        primary_flow_type = "general"
        max_confidence = 0
        
        for pattern_name, pattern_info in detected_patterns.items():
            if pattern_info["confidence"] > max_confidence:
                max_confidence = pattern_info["confidence"]
                primary_flow_type = pattern_info["flow_type"]
        
        return {
            "flow_steps": flow_steps,
            "primary_flow_type": primary_flow_type,
            "confidence": max_confidence,
            "complexity": ui_analysis.get("ui_complexity", "medium")
        }
    
    def _analyze_screenshot(self, file_id: str, node_id: str = None) -> Dict[str, Any]:
        """스크린샷 분석"""
        try:
            headers = {"X-Figma-Token": self.figma_token}
            
            if node_id:
                node_id_formatted = node_id.replace('-', ':')
                image_url = f"https://api.figma.com/v1/images/{file_id}?ids={node_id_formatted}&format=png&scale=1"
            else:
                return {"success": False, "error": "노드 ID 필요"}
            
            response = requests.get(image_url, headers=headers)
            response.raise_for_status()
            
            image_data = response.json()
            
            if 'images' in image_data and image_data['images']:
                image_urls = list(image_data['images'].values())
                if image_urls and image_urls[0]:
                    image_response = requests.get(image_urls[0])
                    image_response.raise_for_status()
                    
                    image_size = len(image_response.content)
                    
                    return {
                        "success": True,
                        "image_url": image_urls[0],
                        "image_size": image_size,
                        "complexity": "high" if image_size > 500000 else "medium" if image_size > 100000 else "low"
                    }
            
            return {"success": False, "error": "이미지 생성 실패"}
            
        except Exception as e:
            return {"success": False, "error": f"스크린샷 분석 오류: {str(e)}"}
    
    def _generate_recommendations(self, keyword_analysis: Dict, ui_analysis: Dict, flow_analysis: Dict) -> Dict[str, List[str]]:
        """권장사항 생성"""
        recommendations = {
            "ui_improvements": [],
            "testing_priorities": [],
            "user_experience": []
        }
        
        ui_complexity = ui_analysis.get("ui_complexity", "medium")
        detected_patterns = keyword_analysis.get("detected_patterns", {})
        
        # UI 개선 권장사항
        if ui_complexity == "high":
            recommendations["ui_improvements"].append("UI 복잡도 단순화 필요")
        
        button_count = len(ui_analysis.get("ui_elements", {}).get("buttons", []))
        if button_count > 5:
            recommendations["ui_improvements"].append("주요 액션 버튼 우선순위 명확화")
        
        # 테스트 우선순위
        if "authentication" in detected_patterns:
            recommendations["testing_priorities"].append("인증 플로우 테스트 우선 실행")
        if "transaction" in detected_patterns:
            recommendations["testing_priorities"].append("거래 기능 보안 테스트 필수")
        if "form_input" in detected_patterns:
            recommendations["testing_priorities"].append("입력 유효성 검사 테스트")
        
        # 사용자 경험
        if len(flow_analysis.get("flow_steps", [])) > 5:
            recommendations["user_experience"].append("사용자 플로우 단계 단순화 고려")
        
        return recommendations
    
    def compare_screens(self, as_is_url: str, to_be_url: str) -> Dict[str, Any]:
        """AS-IS vs TO-BE 화면 비교 분석"""
        # AS-IS 분석
        as_is_result = self.enhanced_analysis(as_is_url, include_screenshot=False)
        
        # TO-BE 분석
        to_be_result = self.enhanced_analysis(to_be_url, include_screenshot=False)
        
        if not (as_is_result.get("success") and to_be_result.get("success")):
            return {
                "success": False,
                "error": "AS-IS 또는 TO-BE 분석 실패"
            }
        
        # 차이점 분석
        differences = self._analyze_differences(as_is_result, to_be_result)
        
        return {
            "success": True,
            "as_is": as_is_result["summary"],
            "to_be": to_be_result["summary"],
            "differences": differences,
            "recommendations": self._generate_comparison_recommendations(differences)
        }
    
    def _analyze_differences(self, as_is: Dict, to_be: Dict) -> Dict[str, Any]:
        """두 분석 결과의 차이점 분석"""
        as_is_patterns = set(as_is["summary"].get("ui_patterns", []))
        to_be_patterns = set(to_be["summary"].get("ui_patterns", []))
        
        return {
            "new_patterns": list(to_be_patterns - as_is_patterns),
            "removed_patterns": list(as_is_patterns - to_be_patterns),
            "ui_complexity_change": {
                "from": as_is["summary"].get("ui_complexity", "unknown"),
                "to": to_be["summary"].get("ui_complexity", "unknown")
            },
            "flow_type_change": {
                "from": as_is["summary"].get("flow_type", "unknown"),
                "to": to_be["summary"].get("flow_type", "unknown")
            }
        }
    
    def _generate_comparison_recommendations(self, differences: Dict) -> List[str]:
        """비교 분석 기반 권장사항"""
        recommendations = []
        
        if differences["new_patterns"]:
            recommendations.append(f"새로운 UI 패턴 추가 테스트 필요: {', '.join(differences['new_patterns'])}")
        
        if differences["removed_patterns"]:
            recommendations.append(f"제거된 UI 패턴 회귀 테스트: {', '.join(differences['removed_patterns'])}")
        
        complexity_change = differences["ui_complexity_change"]
        if complexity_change["from"] != complexity_change["to"]:
            recommendations.append(f"UI 복잡도 변화: {complexity_change['from']} → {complexity_change['to']}")
        
        return recommendations
