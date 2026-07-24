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

from data.hexagram_map import HEXAGRAM_MAP
from core.trigrams import TRIGRAMS


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

        return NAME_TO_NUMBER.get(name)

    @staticmethod
    def trigrams_to_number(upper: str, lower: str):

        return HEXAGRAM_MAP.get((upper, lower))