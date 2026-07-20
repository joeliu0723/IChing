
from core.hexagram import HexagramEngine


class HexagramController:

    def calculate(self, lines):
        engine = HexagramEngine(lines)
        return engine.calculate()
