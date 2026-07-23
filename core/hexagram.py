"""
==================================================
Project IChing
File : core/hexagram.py
Version : V0.8.2
==================================================
"""

import json
from pathlib import Path

from core.trigrams import TRIGRAMS
from core.result import HexagramInfo, HexagramResult


class HexagramEngine:

    def __init__(self, lines):

        self.lines = lines

        json_path = (
            Path(__file__).parent.parent
            / "data"
            / "hexagrams.json"
        )

        with open(json_path, "r", encoding="utf-8") as f:
            self.hexagrams = json.load(f)

        self.version = "V1"

    # -------------------------------------------------
    # 本卦 Binary
    # -------------------------------------------------

    def to_binary(self):

        result = []

        for line in self.lines:

            if line in ("少陽", "老陽"):
                result.append(1)
            else:
                result.append(0)

        return result

    # -------------------------------------------------
    # 變卦 Binary
    # -------------------------------------------------

    def to_changed_binary(self):

        result = []

        for line in self.lines:

            if line == "少陽":
                result.append(1)

            elif line == "少陰":
                result.append(0)

            elif line == "老陽":
                result.append(0)

            elif line == "老陰":
                result.append(1)

            else:
                raise ValueError(f"未知爻值：{line}")

        return result

    # -------------------------------------------------

    def lower_trigram(self):
        return tuple(self.to_binary()[:3])

    def upper_trigram(self):
        return tuple(self.to_binary()[3:])

    def lower_changed_trigram(self):
        return tuple(self.to_changed_binary()[:3])

    def upper_changed_trigram(self):
        return tuple(self.to_changed_binary()[3:])

    # -------------------------------------------------

    def get_trigrams(self):

        return (
            TRIGRAMS[self.lower_trigram()],
            TRIGRAMS[self.upper_trigram()]
        )

    def get_changed_trigrams(self):

        return (
            TRIGRAMS[self.lower_changed_trigram()],
            TRIGRAMS[self.upper_changed_trigram()]
        )

    # -------------------------------------------------

    def _lookup(self, upper_name, lower_name):

        for item in self.hexagrams:

            if (
                item.get("upper") == upper_name
                and item.get("lower") == lower_name
            ):
                return item

        return None

    # -------------------------------------------------

    def get_hexagram(self):

        lower, upper = self.get_trigrams()

        return self._lookup(
            upper["name"],
            lower["name"]
        )

    # -------------------------------------------------

    def get_changed_hexagram(self):

        lower, upper = self.get_changed_trigrams()

        return self._lookup(
            upper["name"],
            lower["name"]
        )

    # -------------------------------------------------

    def _build_info(self, data):

        if data is None:
            return HexagramInfo()

        return HexagramInfo(

            number=data.get("number", 0),

            name=data.get("name", ""),

            title=data.get("title", data.get("name", "")),

            upper=data.get("upper", ""),

            lower=data.get("lower", ""),

            symbol=data.get("symbol", ""),

            gua_text=data.get(
                "gua_text",
                data.get("gua", "")
            ),

            tuan=data.get("tuan", ""),

            xiang=data.get("xiang", ""),

            wenyan=data.get("wenyan", ""),

            translation=data.get(
                "translation",
                data.get(
                    "modern",
                    data.get("description", "")
                )
            ),

            raw=data

        )

    # -------------------------------------------------
    # 動爻
    # -------------------------------------------------

    def get_moving_lines(self):

        result = []

        for index, line in enumerate(self.lines):

            if line in ("老陽", "老陰"):

                result.append(index + 1)

        return result

    # -------------------------------------------------
    # 六爻
    # -------------------------------------------------

    def get_line_text(self, line_no: int):

        info = self._build_info(
            self.get_hexagram()
        )

        return info.line_text(line_no)

    # -------------------------------------------------

    def get_changed_line_text(self, line_no: int):

        info = self._build_info(
            self.get_changed_hexagram()
        )

        return info.line_text(line_no)

    # -------------------------------------------------

    def calculate(self):

        result = HexagramResult()

        result.main = self._build_info(
            self.get_hexagram()
        )

        result.changed = self._build_info(
            self.get_changed_hexagram()
        )

        result.moving_lines = self.get_moving_lines()

        return result

    # -------------------------------------------------

    def debug(self):

        result = self.calculate()

        print()

        print("===================================")

        print("Project IChing")

        print("===================================")

        print()

        print("Database :", self.version)

        print()

        print("Main Binary")

        print(self.to_binary())

        print(result.main.full_name)

        print()

        print("Changed Binary")

        print(self.to_changed_binary())

        print(result.changed.full_name)

        print()

        print("Moving Lines")

        print(result.moving_lines)

        print()

        if result.moving_lines:

            print("Moving Line Text")

            for line in result.moving_lines:

                print(f"{line} :", self.get_line_text(line))

            print()

        print("===================================")