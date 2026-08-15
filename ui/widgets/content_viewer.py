"""Read-only scripture content viewer with optional expand and font size."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.theme import tokens as T


class ContentViewer(QWidget):
    def __init__(self, parent=None, *, collapsed_lines: int = 12):
        super().__init__(parent)
        self._full_text = ""
        self._expanded = False
        self._collapsed_lines = collapsed_lines
        self._font_px = T.CONTENT_FONT_MEDIUM

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.editor = QPlainTextEdit()
        self.editor.setObjectName("contentViewer")
        self.editor.setReadOnly(True)
        self.editor.setMinimumHeight(240)
        self.editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.editor, 1)

        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 0, 0, 0)
        bottom.setSpacing(6)
        bottom.addStretch(1)

        self._size_group = QButtonGroup(self)
        self._size_group.setExclusive(True)
        self.btn_small = self._make_size_button("小", T.CONTENT_FONT_SMALL)
        self.btn_medium = self._make_size_button("中", T.CONTENT_FONT_MEDIUM)
        self.btn_large = self._make_size_button("大", T.CONTENT_FONT_LARGE)
        for btn in (self.btn_small, self.btn_medium, self.btn_large):
            self._size_group.addButton(btn)
            bottom.addWidget(btn)

        self.btn_medium.setChecked(True)

        self.btn_more = QPushButton("顯示更多")
        self.btn_more.setObjectName("secondaryButton")
        self.btn_more.setCursor(Qt.PointingHandCursor)
        self.btn_more.clicked.connect(self._toggle)
        bottom.addWidget(self.btn_more)

        layout.addLayout(bottom)
        self._apply_font()

    def _make_size_button(self, label: str, px: int) -> QPushButton:
        btn = QPushButton(label)
        btn.setObjectName("fontSizeButton")
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(30)
        btn.setMinimumWidth(36)
        btn.clicked.connect(lambda _checked=False, size=px: self.set_font_size(size))
        return btn

    def set_font_size(self, px: int):
        self._font_px = int(px)
        self._apply_font()
        if px == T.CONTENT_FONT_SMALL:
            self.btn_small.setChecked(True)
        elif px == T.CONTENT_FONT_MEDIUM:
            self.btn_medium.setChecked(True)
        elif px == T.CONTENT_FONT_LARGE:
            self.btn_large.setChecked(True)

    def set_text(self, text: str):
        self._full_text = text or ""
        self._expanded = False
        self._apply()

    def _toggle(self):
        self._expanded = not self._expanded
        self._apply()

    def _apply_font(self):
        font = self.editor.font()
        font.setPixelSize(self._font_px)
        self.editor.setFont(font)
        self.editor.setStyleSheet(
            f"QPlainTextEdit#contentViewer {{ font-size: {self._font_px}px; }}"
        )

    def _apply(self):
        lines = self._full_text.splitlines()
        needs_toggle = len(lines) > self._collapsed_lines or len(self._full_text) > 480
        self.btn_more.setVisible(needs_toggle)
        if not needs_toggle or self._expanded:
            self.editor.setPlainText(self._full_text)
            self.btn_more.setText("收合")
            self.editor.setMinimumHeight(280)
        else:
            preview = "\n".join(lines[: self._collapsed_lines])
            if len(lines) > self._collapsed_lines:
                preview += "\n…"
            self.editor.setPlainText(preview)
            self.btn_more.setText("顯示更多")
            self.editor.setMinimumHeight(240)
