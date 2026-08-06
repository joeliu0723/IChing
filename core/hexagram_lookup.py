"""
core/hexagram_lookup.py

Hexagram Lookup

負責各種輸入方式的查詢：

卦序 -> 上下卦
卦序 -> 六爻
卦名 -> 卦序
上下卦 -> 卦序

本模組不負責排卦，
只負責資料查詢。
"""

import json
from pathlib import Path

from data.hexagram_map import HEXAGRAM_MAP
from core.trigrams import TRIGRAMS
from core.paths import hexagrams_path


# -------------------------------------------------
# 建立反向索引
# -------------------------------------------------

NUMBER_TO_TRIGRAM = {}
NAME_TO_NUMBER = {}
NUMBER_TO_NAME = {}

for (upper, lower), number in HEXAGRAM_MAP.items():

    NUMBER_TO_TRIGRAM[number] = (upper, lower)

    NAME = f"{upper}{lower}"

    # 之後可由 hexagrams.json 覆蓋真正卦名
    NAME_TO_NUMBER[NAME] = number

    NUMBER_TO_NAME[number] = NAME


def _short_hexagram_name(full_name: str) -> str:
    """取得卦名簡稱，例如「䷁ 坤」->「坤」。"""

    name = full_name.strip()

    if " " in name:
        return name.split(" ", 1)[1].strip()

    return name


def _load_hexagram_names():
    """以 hexagrams.json 的正式卦名覆蓋暫用的上下卦組合名稱。"""

    data_path = hexagrams_path()

    try:
        with open(data_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, ValueError):
        return

    if isinstance(data, dict):
        entries = data.get("value", [])
    elif isinstance(data, list):
        entries = data
    else:
        return

    for entry in entries:
        if not isinstance(entry, dict):
            continue

        number = entry.get("number")
        name = entry.get("name")

        if not isinstance(number, int) or not isinstance(name, str):
            continue

        full_name = name.strip()
        short_name = _short_hexagram_name(full_name)

        NUMBER_TO_NAME[number] = full_name
        NAME_TO_NUMBER[full_name] = number

        if short_name and short_name not in NAME_TO_NUMBER:
            NAME_TO_NUMBER[short_name] = number


_load_hexagram_names()


# -------------------------------------------------
# 建立 八卦名稱 -> 三爻 bit
# -------------------------------------------------

TRIGRAM_LINES = {}

for bits, info in TRIGRAMS.items():
    TRIGRAM_LINES[info["name"]] = bits


# -------------------------------------------------
# bit -> 六爻文字
# -------------------------------------------------

def bits_to_lines(bits):
    """
    (1,0,1)

    ->

    ["少陽","少陰","少陽"]
    """

    result = []

    for b in bits:
        if b:
            result.append("少陽")
        else:
            result.append("少陰")

    return result


# -------------------------------------------------
# Lookup
# -------------------------------------------------

class HexagramLookup:

    @staticmethod
    def number_to_trigrams(number: int):

        return NUMBER_TO_TRIGRAM.get(number)

    @staticmethod
    def number_to_lines(number: int):

        pair = NUMBER_TO_TRIGRAM.get(number)

        if pair is None:
            raise ValueError(f"找不到卦序：{number}")

        upper_name, lower_name = pair

        lower_bits = TRIGRAM_LINES[lower_name]
        upper_bits = TRIGRAM_LINES[upper_name]

        bits = lower_bits + upper_bits

        return bits_to_lines(bits)

    @staticmethod
    def number_to_name(number: int):

        return NUMBER_TO_NAME.get(number)

    @staticmethod
    def name_to_number(name: str):

        key = name.strip()

        if not key:
            return None

        if ". " in key:
            prefix, suffix = key.split(". ", 1)
            if prefix.isdigit():
                number = int(prefix)
                if 1 <= number <= 64:
                    return number
                key = suffix.strip()

        return NAME_TO_NUMBER.get(key)

    @staticmethod
    def hexagram_names():
        """回傳依卦序排序的正式卦名，供 UI 選擇。"""

        return [
            (number, NUMBER_TO_NAME[number])
            for number in sorted(NUMBER_TO_NAME)
        ]

    @staticmethod
    def trigrams_to_number(upper: str, lower: str):

        return HEXAGRAM_MAP.get((upper, lower))
