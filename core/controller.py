import uuid

from core.hexagram import HexagramEngine
from core.history import HistoryRecord
from core.history_manager import HistoryManager
from core.session import session
from core.hexagram_lookup import HexagramLookup


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

    # =======================================================
    # 卦序輸入
    # =======================================================

    def calculate_by_number(self, number, question=""):
        """
        依卦序排卦

        number : 1~64
        """

        lines = HexagramLookup.number_to_lines(number)

        if lines is None:
            raise ValueError(f"無效的卦序：{number}")

        return self.calculate(lines, question)

    # =======================================================
    # 卦名輸入
    # =======================================================

    def calculate_by_name(self, name, question=""):
        """
        依卦名排卦
        """

        number = HexagramLookup.name_to_number(name)

        if number is None:
            raise ValueError(f"找不到卦名：{name}")

        return self.calculate_by_number(number, question)

    # =======================================================
    # 上下卦輸入
    # =======================================================

    def calculate_by_trigrams(self, upper, lower, question=""):
        """
        依上下卦排卦
        """

        number = HexagramLookup.trigrams_to_number(
            upper,
            lower
        )

        if number is None:
            raise ValueError(
                f"找不到卦：{upper} 上 {lower} 下"
            )

        return self.calculate_by_number(
            number,
            question
        )
        