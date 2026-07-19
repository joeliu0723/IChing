"""
==================================================
Project IChing
File : core/controller.py
Version : V0.9.0
==================================================
"""

from core.hexagram import HexagramEngine


class HexagramController:

    def __init__(self):
        pass

    def calculate(self, lines):

        engine = HexagramEngine(lines)

        return engine.calculate()