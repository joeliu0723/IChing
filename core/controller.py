import uuid

from core.hexagram import HexagramEngine
from core.history import HistoryRecord
from core.history_manager import HistoryManager
from core.session import session


class HexagramController:

    def __init__(self):
        self.history_manager = HistoryManager()

    def calculate(self, lines, question=""):
        """
        執行排卦
        建立 History
        更新 Session
        """

        engine = HexagramEngine(lines)
        result = engine.calculate()

        record = HistoryRecord()

        record.id = str(uuid.uuid4())
        record.question = question
        record.lines = lines.copy()

        record.main_number = result.main.number
        record.main_name = result.main.name

        record.changed_number = result.changed.number
        record.changed_name = result.changed.name

        record.moving_lines = result.moving_lines.copy()

        print("HistoryManager.add()")

        self.history_manager.add(record)

        print("History saved")

        # ===== 更新目前工作階段 =====

        session.set_result(result)
        session.set_record(record)

        return result