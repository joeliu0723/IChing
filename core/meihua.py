"""
梅花易數（邵康節）三數起卦

第 1 數 → 上卦（÷8 取餘，餘 0 作 8）
第 2 數 → 下卦（÷8 取餘，餘 0 作 8）
第 3 數 → 動爻（÷6 取餘，餘 0 作 6；1=初爻 … 6=上爻）

先天八卦序：1乾 2兌 3離 4震 5巽 6坎 7艮 8坤
"""

from __future__ import annotations

from core.hexagram_lookup import HexagramLookup

# 邵雍先天八卦序
MEIHUA_TRIGRAM_ORDER = {
    1: "乾",
    2: "兌",
    3: "離",
    4: "震",
    5: "巽",
    6: "坎",
    7: "艮",
    8: "坤",
}


def _require_positive_int(value, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{label}必須為正整數。")
    if value < 1:
        raise ValueError(f"{label}必須為正整數（≥ 1）。")
    return value


def rem8(n: int) -> int:
    r = n % 8
    return 8 if r == 0 else r


def rem6(n: int) -> int:
    r = n % 6
    return 6 if r == 0 else r


def meihua_numbers_to_lines(n1, n2, n3) -> list[str]:
    """
    三數起卦 → 六爻（含單一動爻，老陽／老陰）。
    """

    n1 = _require_positive_int(n1, "第1數")
    n2 = _require_positive_int(n2, "第2數")
    n3 = _require_positive_int(n3, "第3數")

    upper = MEIHUA_TRIGRAM_ORDER[rem8(n1)]
    lower = MEIHUA_TRIGRAM_ORDER[rem8(n2)]
    moving = rem6(n3)

    number = HexagramLookup.trigrams_to_number(upper, lower)
    if number is None:
        raise ValueError(f"找不到卦：{upper} 上 {lower} 下")

    lines = HexagramLookup.number_to_lines(number)
    index = moving - 1
    current = lines[index]

    if current == "少陽":
        lines[index] = "老陽"
    elif current == "少陰":
        lines[index] = "老陰"
    else:
        # number_to_lines 理論上只有少陰／少陽
        lines[index] = "老陽" if "陽" in current else "老陰"

    return lines
