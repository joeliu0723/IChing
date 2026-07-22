"""
==================================================
Project IChing
File : core/session.py
Version : V0.9.2
==================================================

工作階段(Session)

保存目前正在使用的占卜結果與相關資料。

用途：
- Presenter 顯示目前卦象
- History 載入紀錄
- Notes 編輯心得
- AI 解卦
- Export 匯出
"""

from core.result import HexagramResult
from core.history import HistoryRecord


class Session:
    """目前工作階段"""

    def __init__(self):
        self.clear()

    def clear(self):
        """清空目前工作階段"""

        self.result: HexagramResult | None = None
        self.record: HistoryRecord | None = None

    def set_result(self, result: HexagramResult):
        """設定目前卦象"""

        self.result = result

    def set_record(self, record: HistoryRecord):
        """設定目前歷史紀錄"""

        self.record = record


# 全域 Session（Singleton）
session = Session()