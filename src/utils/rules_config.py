#!/usr/bin/env python3
"""
룰/템플릿 설정 로더

- config/rules_config.json 을 기본으로 로드
- 출력 컬럼 스키마/필드 alias/우선순위 룰/유저플로우 질문 룰 등을 제공
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


DEFAULT_RULES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),  # src/
    "config",
    "rules_config.json",
)


@dataclass(frozen=True)
class RulesConfig:
    raw: Dict[str, Any]

    @property
    def output_columns(self) -> List[str]:
        return list(self.raw.get("output_schema", {}).get("columns", []))

    @property
    def field_aliases(self) -> Dict[str, str]:
        return dict(self.raw.get("output_schema", {}).get("field_aliases", {}))

    @property
    def priority_default(self) -> str:
        return str(self.raw.get("priority_rules", {}).get("default", "P2"))

    @property
    def priority_order(self) -> List[str]:
        return list(self.raw.get("priority_rules", {}).get("order", ["P1", "P2", "P3", "P4"]))

    @property
    def priority_keywords(self) -> Dict[str, List[str]]:
        return dict(self.raw.get("priority_rules", {}).get("keywords", {}))

    @property
    def flow_confidence_threshold(self) -> float:
        return float(self.raw.get("flow_clarification", {}).get("confidence_threshold", 0.55))

    @property
    def flow_default_questions(self) -> List[str]:
        return list(self.raw.get("flow_clarification", {}).get("default_questions", []))

    @property
    def always_include_categories(self) -> List[str]:
        return list(self.raw.get("coverage_rules", {}).get("always_include_categories", []))

    @property
    def platforms(self) -> List[str]:
        return list(self.raw.get("coverage_rules", {}).get("platforms", ["web", "app"]))

    @property
    def excel_formula_enabled(self) -> bool:
        return bool(self.raw.get("excel_formula_output", {}).get("enabled", False))


def load_rules_config(path: Optional[str] = None) -> RulesConfig:
    """룰 설정 로드. path가 없으면 기본 경로를 사용."""
    rules_path = path or DEFAULT_RULES_PATH
    with open(rules_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return RulesConfig(raw=raw)


def normalize_testcase_fields(testcase: Dict[str, Any], field_aliases: Dict[str, str]) -> Dict[str, Any]:
    """
    레거시 키(test_steps/android_result/ios_result 등)를 최신 스키마 키로 정규화.
    """
    out = dict(testcase)
    for src, dst in field_aliases.items():
        if src not in out:
            continue
        src_val = out.get(src)

        # dst가 비어있으면 그대로 채움
        if dst not in out or out.get(dst) in (None, "", []):
            out[dst] = src_val
            continue

        # dst가 이미 있고 src도 값이 있을 때: iOS/Android 결과를 app_result로 "병합" 지원
        dst_val = out.get(dst)
        if src_val in (None, "", []):
            continue

        # 문자열로 병합 (중복 방지)
        dst_s = str(dst_val)
        src_s = str(src_val)
        if src_s.strip() and src_s.strip() not in dst_s:
            # 특별 케이스: android/ios -> app_result는 라벨을 붙여 통합
            if dst == "app_result" and src in ("android_result", "ios_result"):
                label = "Android" if src == "android_result" else "iOS"
                merged = dst_s.rstrip()
                if merged:
                    merged += "\n"
                merged += f"{label}: {src_s}"
                out[dst] = merged
            else:
                out[dst] = (dst_s.rstrip() + "\n" + src_s).strip()
    return out


