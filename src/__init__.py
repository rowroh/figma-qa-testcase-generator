"""
Figma QA TestCase Generator
시니어 QA 엔지니어를 위한 Figma 기반 테스트케이스 자동 생성 도구
"""

__version__ = "1.0.0"
__author__ = "QA Engineering Team"
__email__ = "qa@example.com"

from .analyzers.figma_analyzer import FigmaAnalyzer
from .generators.testcase_generator import TestCaseGenerator

__all__ = [
    "FigmaAnalyzer",
    "TestCaseGenerator"
]
