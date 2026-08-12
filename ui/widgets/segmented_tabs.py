"""Segmented tab row (navy/gold), same language as ModeSelector."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget


class SegmentedTabs(QWidget):
    tabSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("segmentedTabs")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(36)
        self._buttons: dict[str, QPushButton] = {}
        self._active = ""
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(6)

    def set_tabs(self, tabs: list[tuple[str, str]], active: str | None = None):
        while self._layout.count():
            item = self._layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self._buttons.clear()

        for key, label in tabs:
            button = QPushButton(label)
            button.setObjectName("segmentTab")
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.setFixedHeight(36)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.clicked.connect(lambda checked=False, k=key: self._on_clicked(k))
            self._layout.addWidget(button, 1)
            self._buttons[key] = button

        if tabs:
            self.set_active(active or tabs[0][0])

    def _on_clicked(self, key: str):
        self.set_active(key)
        self.tabSelected.emit(key)

    def set_active(self, key: str):
        if key not in self._buttons:
            return
        self._active = key
        for mode_key, button in self._buttons.items():
            button.blockSignals(True)
            button.setChecked(mode_key == key)
            button.blockSignals(False)

    def active_key(self) -> str:
        return self._active
