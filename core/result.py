"""
==================================================
Project IChing
File : core/result.py
Version : V0.8.1
==================================================
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(slots=True)
class HexagramInfo:
    number: int = 0
    name: str = ""
    title: str = ""
    upper: str = ""
    lower: str = ""
    symbol: str = ""

    # 卦辭
    gua_text: str = ""

    # 十翼
    tuan: str = ""
    xiang: str = ""
    wenyan: str = ""

    # 白話翻譯
    translation: str = ""

    # 保留完整 JSON 資料
    raw: Dict[str, Any] = field(default_factory=dict)

    @property
    def full_name(self) -> str:
        return f"第{self.number}卦 {self.title}"

    @property
    def lines(self) -> List[str]:
        """
        六爻爻辭
        """
        if not self.raw:
            return []

        value = (
            self.raw.get("lines")
            or self.raw.get("yao")
            or self.raw.get("yaoci")
            or []
        )

        return value if isinstance(value, list) else []

    def line_text(self, line_no: int) -> str:
        """
        取得指定爻辭 (1~6)
        """
        if line_no < 1:
            return ""

        lines = self.lines

        if line_no > len(lines):
            return ""

        return lines[line_no - 1]


@dataclass(slots=True)
class HexagramResult:
    question: str = ""
    datetime: str = ""

    main: HexagramInfo = field(default_factory=HexagramInfo)
    changed: HexagramInfo = field(default_factory=HexagramInfo)

    moving_lines: List[int] = field(default_factory=list)

    notes: str = ""
    ai_analysis: str = ""