"""
==================================================
Project IChing
File : tests/test_controller.py
==================================================
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.controller import HexagramController


controller = HexagramController()

result = controller.calculate(

    [

        "老陽",
        "少陽",
        "少陽",
        "少陰",
        "少陰",
        "少陰"

    ]

)

print(result.main.full_name)

print(result.changed.full_name)

print(result.moving_lines)