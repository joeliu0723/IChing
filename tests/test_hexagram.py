"""
==================================================
Project IChing
File : tests/test_hexagram.py
Version : V1.0
==================================================
"""

import sys
from pathlib import Path

# 將專案根目錄加入 Python 搜尋路徑
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.hexagram import HexagramEngine


# ==================================================
# 測試函式
# ==================================================

def run_test(title, lines):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    engine = HexagramEngine(lines)

    result = engine.calculate()

    print("輸入六爻：")
    print(lines)

    print()

    print("本卦")
    print(result.main.full_name)

    print()

    print("變卦")
    print(result.changed.full_name)

    print()

    print("動爻")
    print(result.moving_lines)

    print()

    print("Binary")
    print(engine.to_binary())

    print()

    print("Changed Binary")
    print(engine.to_changed_binary())


# ==================================================
# Main
# ==================================================

if __name__ == "__main__":

    # -----------------------------
    # 測試一
    # 全乾
    # -----------------------------

    run_test(

        "Test 1：全少陽",

        [

            "少陽",
            "少陽",
            "少陽",
            "少陽",
            "少陽",
            "少陽"

        ]

    )

    # -----------------------------
    # 測試二
    # 全坤
    # -----------------------------

    run_test(

        "Test 2：全少陰",

        [

            "少陰",
            "少陰",
            "少陰",
            "少陰",
            "少陰",
            "少陰"

        ]

    )

    # -----------------------------
    # 測試三
    # 初爻老陽
    # -----------------------------

    run_test(

        "Test 3：初爻老陽",

        [

            "老陽",
            "少陽",
            "少陽",
            "少陽",
            "少陽",
            "少陽"

        ]

    )

    # -----------------------------
    # 測試四
    # 初爻老陰
    # -----------------------------

    run_test(

        "Test 4：初爻老陰",

        [

            "老陰",
            "少陰",
            "少陰",
            "少陰",
            "少陰",
            "少陰"

        ]

    )

    print()
    print("=" * 60)
    print("所有測試完成")
    print("=" * 60)