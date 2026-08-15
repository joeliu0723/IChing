"""
==================================================
Project IChing
File : ui/history_page.py
Version : V1.4.15
==================================================
History page with card rows, select-all, and pagination.
"""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
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
from ui.theme import tokens as T
from ui.widgets.history_record_row import HistoryRecordRow

_DEFAULT_ASCENDING = {
    SORT_BY_DATE: False,
    SORT_BY_MAIN: True,
    SORT_BY_FAVORITE: False,
    SORT_BY_VERIFICATION: True,
}


class _HistoryViewportFilter(QObject):
    def __init__(self, page: "HistoryPage"):
        super().__init__(page.root)
        self._page = page

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Resize:
            self._page._on_list_resized()
        return False


class HistoryPage:
    """占卜紀錄頁（logic + full-width themed shell）。"""

    def __init__(
        self,
        window,
        on_select=None,
        on_delete=None,
        on_favorite=None,
    ):
        self.window = window
        self.manager = HistoryManager()
        self.on_select = on_select
        self.on_delete = on_delete
        self.on_favorite = on_favorite
        self.sort_ascending = _DEFAULT_ASCENDING[SORT_BY_DATE]
        self._page = 0
        self._page_size = T.HISTORY_PAGE_SIZE_MAX
        self._row_height = T.HISTORY_ROW_HEIGHT_COMFORT
        self._filtered: list[HistoryRecord] = []
        self._row_by_id: dict[str, HistoryRecordRow] = {}
        self._selected_ids: set[str] = set()
        self._fit_guard = False

        self.root = QWidget()
        self.root.setObjectName("historyRoot")
        self._build_ui()
        self._mount_into_tab()
        self.refresh()

    def _mount_into_tab(self):
        tab = self.window.tab_history
        for child in list(tab.children()):
            if isinstance(child, QWidget):
                child.setParent(None)
                child.deleteLater()

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.root)

        # Compatibility aliases used elsewhere
        self.window.listHistory = self.list_widget
        self.window.verticalLayout_3 = self.root_layout

    def _build_ui(self):
        self.root_layout = QVBoxLayout(self.root)
        self.root_layout.setContentsMargins(24, 16, 24, 16)
        self.root_layout.setSpacing(10)

        toolbar = QFrame()
        toolbar.setObjectName("historyToolbar")
        toolbar.setAttribute(Qt.WA_StyledBackground, True)
        tb = QVBoxLayout(toolbar)
        tb.setContentsMargins(12, 10, 12, 10)
        tb.setSpacing(8)

        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("搜尋"))
        self.edit_search = QLineEdit()
        self.edit_search.setObjectName("historySearch")
        self.edit_search.setPlaceholderText("問題、卦名、卦序、收藏、驗證…")
        self.edit_search.textChanged.connect(self._on_search_changed)
        search_row.addWidget(self.edit_search, 1)
        self.btn_clear_search = QPushButton("清除")
        self.btn_clear_search.setObjectName("secondaryButton")
        self.btn_clear_search.clicked.connect(self.clear_search)
        search_row.addWidget(self.btn_clear_search)
        tb.addLayout(search_row)

        sort_row = QHBoxLayout()
        sort_row.addWidget(QLabel("排序"))
        self.combo_sort = QComboBox()
        self.combo_sort.setObjectName("styledCombo")
        for key, label in SORT_OPTIONS:
            self.combo_sort.addItem(label, key)
        self.combo_sort.currentIndexChanged.connect(self._on_sort_changed)
        sort_row.addWidget(self.combo_sort, 1)
        self.btn_sort_order = QPushButton()
        self.btn_sort_order.setObjectName("secondaryButton")
        self.btn_sort_order.clicked.connect(self._toggle_sort_order)
        sort_row.addWidget(self.btn_sort_order)
        self._update_sort_order_button()
        tb.addLayout(sort_row)
        self.root_layout.addWidget(toolbar)

        self.list_widget = QListWidget()
        self.list_widget.setObjectName("historyList")
        self.list_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.list_widget.setFocusPolicy(Qt.NoFocus)
        self.list_widget.setSpacing(2)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.list_widget.setUniformItemSizes(True)
        self.list_widget.itemDoubleClicked.connect(self._handle_item_double_clicked)
        self._viewport_filter = _HistoryViewportFilter(self)
        self.list_widget.viewport().installEventFilter(self._viewport_filter)
        self.root_layout.addWidget(self.list_widget, 1)

        bottom = QHBoxLayout()
        self.chk_select_all = QCheckBox("全選")
        self.chk_select_all.setObjectName("styledCheck")
        self.chk_select_all.toggled.connect(self._on_select_all)
        bottom.addWidget(self.chk_select_all)

        self.btn_delete = QPushButton("刪除選取紀錄")
        self.btn_delete.setObjectName("historyActionButton")
        self.btn_delete.clicked.connect(self._handle_delete)
        bottom.addWidget(self.btn_delete)

        bottom.addStretch(1)

        self.btn_prev = QPushButton("上一頁")
        self.btn_prev.setObjectName("secondaryButton")
        self.btn_prev.clicked.connect(self._prev_page)
        bottom.addWidget(self.btn_prev)
        self.page_label = QLabel("1 / 1")
        self.page_label.setObjectName("mutedLabel")
        bottom.addWidget(self.page_label)
        self.btn_next = QPushButton("下一頁")
        self.btn_next.setObjectName("secondaryButton")
        self.btn_next.clicked.connect(self._next_page)
        bottom.addWidget(self.btn_next)

        self.root_layout.addLayout(bottom)

    def set_favorites_filter(self, enabled: bool):
        if enabled:
            self.edit_search.setText("收藏")
        elif self.edit_search.text().strip() in {"收藏", "★", "favorite"}:
            self.edit_search.clear()

    def _update_sort_order_button(self):
        self.btn_sort_order.setText("小→大" if self.sort_ascending else "大→小")

    def _toggle_sort_order(self):
        self.sort_ascending = not self.sort_ascending
        self._update_sort_order_button()
        self._page = 0
        self.refresh()

    def _on_search_changed(self, _text):
        self._page = 0
        self.refresh()

    def _on_sort_changed(self, _index):
        sort_key = self.current_sort()
        self.sort_ascending = _DEFAULT_ASCENDING.get(sort_key, False)
        self._update_sort_order_button()
        self._page = 0
        self.refresh()

    def clear_search(self):
        self.edit_search.clear()

    def _handle_item_double_clicked(self, item):
        if self.on_select is None:
            return
        record_id = item.data(Qt.UserRole)
        if record_id:
            self.on_select(record_id)

    def _handle_delete(self):
        if self.on_delete is None:
            return
        self.on_delete(self.selected_record_ids())

    def _on_select_all(self, checked: bool):
        self.chk_select_all.blockSignals(True)
        for record_id, row in self._row_by_id.items():
            row.set_checked(checked)
            if checked:
                self._selected_ids.add(record_id)
            else:
                self._selected_ids.discard(record_id)
        self.chk_select_all.blockSignals(False)

    def _on_row_selection_toggled(self, record_id: str, checked: bool):
        if checked:
            self._selected_ids.add(record_id)
        else:
            self._selected_ids.discard(record_id)
        self._sync_select_all_state()

    def _sync_select_all_state(self):
        if not self._row_by_id:
            self.chk_select_all.blockSignals(True)
            self.chk_select_all.setChecked(False)
            self.chk_select_all.blockSignals(False)
            return
        all_checked = all(
            record_id in self._selected_ids for record_id in self._row_by_id
        )
        self.chk_select_all.blockSignals(True)
        self.chk_select_all.setChecked(all_checked)
        self.chk_select_all.blockSignals(False)

    def selected_record_ids(self) -> list[str]:
        # 保持本頁可見順序，方便刪除確認訊息穩定
        ordered = []
        for i in range(self.list_widget.count()):
            record_id = self.list_widget.item(i).data(Qt.UserRole)
            if record_id and record_id in self._selected_ids:
                ordered.append(record_id)
        # 亦包含其他頁曾勾選者
        for record_id in self._selected_ids:
            if record_id not in ordered:
                ordered.append(record_id)
        return ordered

    def _prev_page(self):
        if self._page > 0:
            self._page -= 1
            self._render_page()

    def _next_page(self):
        total_pages = max(1, (len(self._filtered) + self._page_size - 1) // self._page_size)
        if self._page + 1 < total_pages:
            self._page += 1
            self._render_page()

    def current_query(self) -> str:
        return self.edit_search.text().strip()

    def current_sort(self) -> str:
        key = self.combo_sort.currentData()
        return key if key else SORT_BY_DATE

    def refresh(self):
        self.manager.load()
        # 清除已不存在的勾選
        valid_ids = {record.id for record in self.manager.get_all()}
        self._selected_ids &= valid_ids
        records = self.manager.search(self.current_query())
        self._filtered = self.manager.sort_records(
            records,
            self.current_sort(),
            ascending=self.sort_ascending,
        )
        self._apply_fit_metrics(reset_page=False)
        total_pages = max(1, (len(self._filtered) + self._page_size - 1) // self._page_size)
        if self._page >= total_pages:
            self._page = total_pages - 1
        self._render_page()

    def _on_list_resized(self):
        if self._fit_guard:
            return
        old_size = self._page_size
        old_height = self._row_height
        self._apply_fit_metrics(reset_page=False)
        if old_size != self._page_size or old_height != self._row_height:
            self._fit_guard = True
            try:
                self._render_page()
            finally:
                self._fit_guard = False

    def _apply_fit_metrics(self, *, reset_page: bool):
        """依可視高度決定每頁 5–8 筆，並均分行高，盡量不出現直向捲軸。"""

        page_size, row_height = self._compute_fit_metrics()
        self._page_size = page_size
        self._row_height = row_height
        total_pages = max(
            1, (len(self._filtered) + self._page_size - 1) // self._page_size
        )
        if reset_page:
            self._page = 0
        elif self._page >= total_pages:
            self._page = total_pages - 1

    def _compute_fit_metrics(self) -> tuple[int, int]:
        viewport = self.list_widget.viewport()
        available = max(0, viewport.height())
        spacing = max(0, self.list_widget.spacing())
        comfort = T.HISTORY_ROW_HEIGHT_COMFORT

        if available <= 0:
            return T.HISTORY_PAGE_SIZE_MAX, comfort

        # 由大到小：能以舒適列高塞進視窗的最大筆數（5–8）
        chosen = T.HISTORY_PAGE_SIZE_MIN
        for n in range(T.HISTORY_PAGE_SIZE_MAX, T.HISTORY_PAGE_SIZE_MIN - 1, -1):
            need = n * comfort + max(0, n - 1) * spacing
            if need <= available:
                chosen = n
                break

        gaps = max(0, chosen - 1) * spacing
        row_h = (available - gaps) // chosen
        row_h = max(T.HISTORY_ROW_HEIGHT_MIN, min(T.HISTORY_ROW_HEIGHT_MAX, row_h))
        return chosen, row_h

    def _render_page(self, selected_ids: set[str] | None = None):
        if selected_ids is not None:
            self._selected_ids = set(selected_ids)

        self.list_widget.clear()
        self._row_by_id.clear()

        start = self._page * self._page_size
        page_records = self._filtered[start : start + self._page_size]
        visible = len(page_records)

        # 本頁實際筆數均分行高（少於 page_size 時仍鋪滿，避免大片空白＋捲軸）
        spacing = max(0, self.list_widget.spacing())
        available = max(0, self.list_widget.viewport().height())
        if visible > 0 and available > 0:
            gaps = max(0, visible - 1) * spacing
            row_h = (available - gaps) // visible
            row_h = max(T.HISTORY_ROW_HEIGHT_MIN, min(T.HISTORY_ROW_HEIGHT_MAX, row_h))
        else:
            row_h = self._row_height
        self._row_height = row_h

        for record in page_records:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, record.id)
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            row = HistoryRecordRow(record, row_height=row_h)
            row.activated.connect(lambda rid: self.on_select and self.on_select(rid))
            row.favoriteClicked.connect(self._toggle_favorite)
            row.selectionToggled.connect(self._on_row_selection_toggled)
            item.setSizeHint(row.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, row)
            self._row_by_id[record.id] = row
            row.set_checked(record.id in self._selected_ids)

        # 內容剛好貼齊時關掉直向捲軸，避免無意義 bar
        content_h = visible * row_h + max(0, visible - 1) * spacing
        if visible > 0 and content_h <= available + 1:
            self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        else:
            self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        total_pages = max(1, (len(self._filtered) + self._page_size - 1) // self._page_size)
        self.page_label.setText(f"{self._page + 1} / {total_pages}")
        self.btn_prev.setEnabled(self._page > 0)
        self.btn_next.setEnabled(self._page + 1 < total_pages)
        self._sync_select_all_state()

    def _toggle_favorite(self, record_id: str):
        if self.on_favorite:
            self.on_favorite(record_id)
            return
        record = self.manager.get(record_id)
        if record is None:
            return
        record.favorite = not record.favorite
        self.manager.update(record)
        self.refresh()

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
