"""
==================================================
Project IChing
File : ui/history_page.py
Version : V1.4.3
==================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QListWidgetItem,
    QPushButton,
)

from core.history_manager import HistoryManager
from core.history import HistoryRecord


class HistoryPage:
    """占卜紀錄頁"""

    def __init__(self, window, on_select=None, on_delete=None):

        self.window = window
        self.manager = HistoryManager()
        self.on_select = on_select
        self.on_delete = on_delete

        self.list_widget = self.window.listHistory
        self.list_widget.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        # 單擊僅選取；雙擊才開啟解卦
        self.list_widget.itemDoubleClicked.connect(
            self._handle_item_double_clicked
        )

        self.btn_delete = QPushButton("刪除選取紀錄")
        self.window.verticalLayout_3.addWidget(self.btn_delete)
        self.btn_delete.clicked.connect(self._handle_delete)

        self.refresh()

    def _handle_item_double_clicked(self, item):
        if self.on_select is None:
            return

        record_id = item.data(Qt.UserRole)
        self.on_select(record_id)

    def _handle_delete(self):
        if self.on_delete is None:
            return

        self.on_delete(self.selected_record_ids())

    def selected_record_ids(self) -> list[str]:
        """回傳目前選取的所有紀錄 id。"""

        ids = []

        for item in self.list_widget.selectedItems():
            record_id = item.data(Qt.UserRole)
            if record_id:
                ids.append(record_id)

        return ids

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

        selected_ids = set(self.selected_record_ids())

        self.refresh()

        if not selected_ids:
            return

        for row in range(self.list_widget.count()):

            item = self.list_widget.item(row)

            if item.data(Qt.UserRole) in selected_ids:
                item.setSelected(True)

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

    def get_record(self, record_id: str) -> HistoryRecord | None:

        self.manager.load()
        return self.manager.get(record_id)
