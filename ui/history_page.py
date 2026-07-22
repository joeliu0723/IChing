"""
==================================================
Project IChing
File : ui/history_page.py
Version : V1.0.0
==================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem

from core.history_manager import HistoryManager
from core.history import HistoryRecord


class HistoryPage:
    """占卜紀錄頁"""

    def __init__(self, window):

        self.window = window
        self.manager = HistoryManager()

        self.list_widget = self.window.listHistory

        self.refresh()

    def refresh(self):
        """重新載入所有紀錄"""

        self.manager.load()

        self.list_widget.clear()

        records = self.manager.get_all()

        for record in records:

            text = (
                f"{record.created_at:%Y-%m-%d %H:%M}   "
                f"{record.main_name}"
            )

            if record.changed_name:
                text += f" → {record.changed_name}"

            if record.question:
                text += f"    【{record.question}】"

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, record.id)

            self.list_widget.addItem(item)

    def refresh_and_keep_selection(self):

        current_id = self.current_record_id()

        self.refresh()

        if current_id is None:
            return

        for row in range(self.list_widget.count()):

            item = self.list_widget.item(row)

            if item.data(Qt.UserRole) == current_id:
                self.list_widget.setCurrentRow(row)
                return

    def current_record_id(self):

        item = self.list_widget.currentItem()

        if item is None:
            return None

        return item.data(Qt.UserRole)

    def current_record(self) -> HistoryRecord | None:

        self.manager.load()

        record_id = self.current_record_id()

        if record_id is None:
            return None

        return self.manager.get(record_id)