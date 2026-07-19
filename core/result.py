"""
==================================================
Project IChing
File : core/result.py
Version : V0.8.0
==================================================
"""

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class HexagramInfo:
    number: int = 0
    name: str = ""
    title: str = ""
    upper: str = ""
    lower: str = ""
    symbol: str = ""
    gua_text: str = ""
    tuan: str = ""
    xiang: str = ""
    wenyan: str = ""
    translation: str = ""

    @property
    def full_name(self) -> str:
        return f"第{self.number}卦 {self.title}"


@dataclass(slots=True)
class HexagramResult:
    question: str = ""
    datetime: str = ""

    main: HexagramInfo = field(default_factory=HexagramInfo)
    changed: HexagramInfo = field(default_factory=HexagramInfo)

    moving_lines: List[int] = field(default_factory=list)

    notes: str = ""
    ai_analysis: str = ""