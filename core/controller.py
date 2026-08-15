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

    def calculate(self, lines, question="", cast_method=""):
        """
        執行排卦

        建立 Session 中的暫存 HistoryRecord，但尚不寫入 history.json。
        需於解卦頁「儲存問題」後才會新增歷史紀錄。
        """

        result = self.build_result(lines, question)

        record = HistoryRecord()

        record.id = str(uuid.uuid4())
        record.question = question
        record.lines = lines.copy()
        record.cast_method = (cast_method or "").strip()

        record.main_number = result.main.number
        record.main_name = result.main.name

        record.changed_number = result.changed.number
        record.changed_name = result.changed.name

        record.moving_lines = result.moving_lines.copy()

        result.datetime = record.created_at.strftime("%Y-%m-%d %H:%M")
        result.cast_method = record.cast_method

        session.set_result(result)
        session.set_record(record)

        return result

    def _require_session_record(self) -> HistoryRecord:
        current = session.record

        if current is None or not current.id:
            raise ValueError("目前沒有可儲存的占卜紀錄，請先起卦或從歷史載入。")

        return current

    def _require_persisted_record(self) -> HistoryRecord:
        """取得已寫入歷史檔的紀錄；尚未「儲存問題」則拒絕。"""

        current = self._require_session_record()
        self.history_manager.load()
        record = self.history_manager.get(current.id)

        if record is None:
            raise ValueError("請先按「儲存問題」將此卦寫入歷史後，再儲存其他資料。")

        return record

    def save_question(self, question: str):
        """儲存占卜問題；若尚未寫入歷史則新增一筆。"""

        current = self._require_session_record()
        question = (question or "").strip()

        self.history_manager.load()
        record = self.history_manager.get(current.id)

        if record is None:
            record = current
            record.question = question
            record.updated_at = datetime.now()
            self.history_manager.add(record)
        else:
            record.question = question
            record.updated_at = datetime.now()
            self.history_manager.update(record)

        session.set_record(record)

        if session.result is not None:
            session.result.question = question

        return record

    def save_notes(self, notes: str):
        """儲存目前紀錄的心得。"""

        record = self._require_persisted_record()

        record.notes = notes
        record.updated_at = datetime.now()
        self.history_manager.update(record)
        session.set_record(record)

        return record

    def set_favorite(self, favorite: bool):
        """設定目前紀錄是否收藏。"""

        record = self._require_persisted_record()

        record.favorite = bool(favorite)
        record.updated_at = datetime.now()
        self.history_manager.update(record)
        session.set_record(record)

        return record

    def save_verification(self, content: str, result: str):
        """儲存目前紀錄的驗證內容與驗證結果。"""

        result = (result or "").strip()
        if result not in VERIFICATION_RESULTS:
            raise ValueError(f"無效的驗證結果：{result}")

        record = self._require_persisted_record()

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

    def calculate_by_number(self, number, question="", cast_method=""):
        """
        依卦序排卦

        number : 1~64
        """

        self._validate_number(number)

        lines = HexagramLookup.number_to_lines(number)

        return self.calculate(lines, question, cast_method=cast_method)

    # =======================================================
    # 卦名輸入
    # =======================================================

    def calculate_by_name(self, name, question="", cast_method=""):
        """
        依卦名排卦
        """

        name = name.strip()

        if not name:
            raise ValueError("請輸入卦名。")

        number = HexagramLookup.name_to_number(name)

        if number is None:
            raise ValueError(f"找不到卦名：{name}")

        return self.calculate_by_number(number, question, cast_method=cast_method)

    # =======================================================
    # 上下卦輸入
    # =======================================================

    def calculate_by_trigrams(self, upper, lower, question="", cast_method=""):
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
            question,
            cast_method=cast_method,
        )

    # =======================================================
    # 梅花易數數字卦
    # =======================================================

    def calculate_by_meihua(self, n1, n2, n3, question="", cast_method=""):
        """
        依梅花易數三數起卦。

        n1 → 上卦，n2 → 下卦，n3 → 動爻
        """

        from core.meihua import meihua_numbers_to_lines

        lines = meihua_numbers_to_lines(n1, n2, n3)
        return self.calculate(lines, question, cast_method=cast_method)
