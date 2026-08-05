"""
==================================================
Project IChing
File : ui/history_page.py
Version : V1.4.9
==================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidgetItem,
    QPushButton,
    QWidget,
)

from core.history_manager import (
    HistoryManager,
    SORT_BY_DATE,
    SORT_BY_FAVORITE,
    SORT_BY_MAIN,
    SORT_BY_VERIFICATION,
    SORT_OPTIONS,
)
from core.history import HistoryRecord


# 各排序欄位的預設方向（維持既有行為）
_DEFAULT_ASCENDING = {
    SORT_BY_DATE: False,
    SORT_BY_MAIN: True,
    SORT_BY_FAVORITE: False,
    SORT_BY_VERIFICATION: True,
}


class HistoryPage:
    """占卜紀錄頁"""

    def __init__(self, window, on_select=None, on_delete=None):

        self.window = window
        self.manager = HistoryManager()
        self.on_select = on_select
        self.on_delete = on_delete
        self.sort_ascending = _DEFAULT_ASCENDING[SORT_BY_DATE]

        self.list_widget = self.window.listHistory
        self.list_widget.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        # 單擊僅選取；雙擊才開啟解卦
        self.list_widget.itemDoubleClicked.connect(
            self._handle_item_double_clicked
        )

        self._init_search_bar()
        self._init_sort_bar()

        self.btn_delete = QPushButton("刪除選取紀錄")
        self.window.verticalLayout_3.addWidget(self.btn_delete)
        self.btn_delete.clicked.connect(self._handle_delete)

        self.refresh()

    def _init_search_bar(self):
        bar = QWidget()
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("搜尋"))

        self.edit_search = QLineEdit()
        self.edit_search.setPlaceholderText(
            "問題、卦名、卦序、收藏、驗證…"
        )
        self.edit_search.textChanged.connect(self._on_search_changed)
        layout.addWidget(self.edit_search, 1)

        self.btn_clear_search = QPushButton("清除")
        self.btn_clear_search.clicked.connect(self.clear_search)
        layout.addWidget(self.btn_clear_search)

        self.window.verticalLayout_3.insertWidget(0, bar)

    def _init_sort_bar(self):
        bar = QWidget()
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("排序"))

        self.combo_sort = QComboBox()
        for key, label in SORT_OPTIONS:
            self.combo_sort.addItem(label, key)

        self.combo_sort.currentIndexChanged.connect(self._on_sort_changed)
        layout.addWidget(self.combo_sort, 1)

        self.btn_sort_order = QPushButton()
        self.btn_sort_order.clicked.connect(self._toggle_sort_order)
        layout.addWidget(self.btn_sort_order)
        self._update_sort_order_button()

        self.window.verticalLayout_3.insertWidget(1, bar)

    def _update_sort_order_button(self):
        if self.sort_ascending:
            self.btn_sort_order.setText("小→大")
        else:
            self.btn_sort_order.setText("大→小")

    def _toggle_sort_order(self):
        self.sort_ascending = not self.sort_ascending
        self._update_sort_order_button()
        self.refresh()

    def _on_search_changed(self, _text):
        self.refresh()

    def _on_sort_changed(self, _index):
        sort_key = self.current_sort()
        self.sort_ascending = _DEFAULT_ASCENDING.get(sort_key, False)
        self._update_sort_order_button()
        self.refresh()

    def clear_search(self):
        self.edit_search.clear()

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

    def current_query(self) -> str:
        return self.edit_search.text().strip()

    def current_sort(self) -> str:
        key = self.combo_sort.currentData()
        return key if key else SORT_BY_DATE

    def refresh(self):
        """重新載入紀錄（套用目前搜尋與排序）。"""

        selected_ids = set(self.selected_record_ids())

        self.manager.load()
        self.list_widget.clear()

        records = self.manager.search(self.current_query())
        records = self.manager.sort_records(
            records,
            self.current_sort(),
            ascending=self.sort_ascending,
        )

        for record in records:

            prefix = "★ " if record.favorite else ""

            text = (
                f"{prefix}"
                f"{record.created_at:%Y-%m-%d %H:%M}   "
                f"{record.main_name}"
            )

            if record.changed_name:
                text += f" → {record.changed_name}"

            if record.question:
                text += f"    【{record.question}】"

            result = record.verification_result or "未驗證"
            if result != "未驗證":
                text += f"    [{result}]"

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, record.id)

            self.list_widget.addItem(item)

            if record.id in selected_ids:
                item.setSelected(True)

    def refresh_and_keep_selection(self):
        self.refresh()

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
