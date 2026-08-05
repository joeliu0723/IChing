import uuid
from datetime import datetime

from core.hexagram import HexagramEngine
from core.history import HistoryRecord, VERIFICATION_RESULTS
from core.history_manager import HistoryManager
from core.session import session
from core.hexagram_lookup import HexagramLookup


VALID_LINE_VALUES = ("少陽", "少陰", "老陽", "老陰")


class HexagramController:

    def __init__(self):
        self.history_manager = HistoryManager()

    def _validate_lines(self, lines):
        if not isinstance(lines, list) or len(lines) != 6:
            raise ValueError("六爻輸入不完整，請選擇全部六爻。")

        for line in lines:
            if line not in VALID_LINE_VALUES:
                raise ValueError(f"無效的爻值：{line}")

    def _validate_number(self, number):
        if not isinstance(number, int) or not 1 <= number <= 64:
            raise ValueError(f"卦序必須為 1 到 64，目前為：{number}")

    def build_result(self, lines, question=""):
        """只計算卦象，不寫入 History。"""

        self._validate_lines(lines)

        engine = HexagramEngine(lines)
        result = engine.calculate()
        result.question = question
        result.lines = lines.copy()

        return result

    def calculate(self, lines, question=""):
        """
        執行排卦

        建立 History
        更新 Session
        """

        result = self.build_result(lines, question)

        record = HistoryRecord()

        record.id = str(uuid.uuid4())
        record.question = question
        record.lines = lines.copy()

        record.main_number = result.main.number
        record.main_name = result.main.name

        record.changed_number = result.changed.number
        record.changed_name = result.changed.name

        record.moving_lines = result.moving_lines.copy()

        self.history_manager.add(record)

        session.set_result(result)
        session.set_record(record)

        return result

    def save_question(self, question: str):
        """儲存目前紀錄的占卜問題。"""

        current = session.record

        if current is None or not current.id:
            raise ValueError("目前沒有可儲存的占卜紀錄，請先起卦或從歷史載入。")

        self.history_manager.load()
        record = self.history_manager.get(current.id)

        if record is None:
            raise ValueError("找不到對應的歷史紀錄。")

        question = (question or "").strip()
        record.question = question
        record.updated_at = datetime.now()
        self.history_manager.update(record)
        session.set_record(record)

        if session.result is not None:
            session.result.question = question

        return record

    def save_notes(self, notes: str):
        """儲存目前紀錄的心得。"""

        current = session.record

        if current is None or not current.id:
            raise ValueError("目前沒有可儲存的占卜紀錄，請先起卦或從歷史載入。")

        self.history_manager.load()
        record = self.history_manager.get(current.id)

        if record is None:
            raise ValueError("找不到對應的歷史紀錄。")

        record.notes = notes
        record.updated_at = datetime.now()
        self.history_manager.update(record)
        session.set_record(record)

        return record

    def set_favorite(self, favorite: bool):
        """設定目前紀錄是否收藏。"""

        current = session.record

        if current is None or not current.id:
            raise ValueError("目前沒有可收藏的占卜紀錄，請先起卦或從歷史載入。")

        self.history_manager.load()
        record = self.history_manager.get(current.id)

        if record is None:
            raise ValueError("找不到對應的歷史紀錄。")

        record.favorite = bool(favorite)
        record.updated_at = datetime.now()
        self.history_manager.update(record)
        session.set_record(record)

        return record

    def save_verification(self, content: str, result: str):
        """儲存目前紀錄的驗證內容與驗證結果。"""

        current = session.record

        if current is None or not current.id:
            raise ValueError("目前沒有可儲存的占卜紀錄，請先起卦或從歷史載入。")

        result = (result or "").strip()
        if result not in VERIFICATION_RESULTS:
            raise ValueError(f"無效的驗證結果：{result}")

        self.history_manager.load()
        record = self.history_manager.get(current.id)

        if record is None:
            raise ValueError("找不到對應的歷史紀錄。")

        record.verification_content = content
        record.verification_result = result
        record.updated_at = datetime.now()
        self.history_manager.update(record)
        session.set_record(record)

        return record

    def delete_record(self, record_id: str):
        """永久刪除歷史紀錄。"""

        self.delete_records([record_id])

    def delete_records(self, record_ids: list[str]):
        """永久刪除多筆歷史紀錄。"""

        ids = [record_id for record_id in record_ids if record_id]

        if not ids:
            raise ValueError("請先選擇要刪除的紀錄。")

        self.history_manager.load()

        missing = [
            record_id
            for record_id in ids
            if self.history_manager.get(record_id) is None
        ]

        if missing:
            raise ValueError("找不到部分要刪除的紀錄。")

        self.history_manager.delete_many(ids)

        if (
            session.record is not None
            and session.record.id in ids
        ):
            session.clear()

    # =======================================================
    # 卦序輸入
    # =======================================================

    def calculate_by_number(self, number, question=""):
        """
        依卦序排卦

        number : 1~64
        """

        self._validate_number(number)

        lines = HexagramLookup.number_to_lines(number)

        return self.calculate(lines, question)

    # =======================================================
    # 卦名輸入
    # =======================================================

    def calculate_by_name(self, name, question=""):
        """
        依卦名排卦
        """

        name = name.strip()

        if not name:
            raise ValueError("請輸入卦名。")

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

        upper = upper.strip()
        lower = lower.strip()

        if not upper or not lower:
            raise ValueError("請選擇上卦與下卦。")

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
