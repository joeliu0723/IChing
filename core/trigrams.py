"""
八卦資料

使用三個 bit 表示一個八卦
1 = 陽
0 = 陰

排列順序：
由下往上（初爻 → 三爻）
"""

TRIGRAMS = {

    (1, 1, 1): {
        "name": "乾",
        "symbol": "☰",
        "nature": "天"
    },

    (0, 0, 0): {
        "name": "坤",
        "symbol": "☷",
        "nature": "地"
    },

    (1, 0, 0): {
        "name": "震",
        "symbol": "☳",
        "nature": "雷"
    },

    (0, 1, 1): {
        "name": "巽",
        "symbol": "☴",
        "nature": "風"
    },

    (0, 1, 0): {
        "name": "坎",
        "symbol": "☵",
        "nature": "水"
    },

    (1, 0, 1): {
        "name": "離",
        "symbol": "☲",
        "nature": "火"
    },

    (1, 1, 0): {
        "name": "兌",
        "symbol": "☱",
        "nature": "澤"
    },

    (0, 0, 1): {
        "name": "艮",
        "symbol": "☶",
        "nature": "山"
    }

}