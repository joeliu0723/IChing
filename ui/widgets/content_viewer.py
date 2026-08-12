"""Read-only scripture content viewer with optional expand."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget


class ContentViewer(QWidget):
    def __init__(self, parent=None, *, collapsed_lines: int = 12):
        super().__init__(parent)
        self._full_text = ""
        self._expanded = False
        self._collapsed_lines = collapsed_lines

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.editor = QPlainTextEdit()
        self.editor.setObjectName("contentViewer")
        self.editor.setReadOnly(True)
        self.editor.setMinimumHeight(240)
        self.editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.editor, 1)

        self.btn_more = QPushButton("顯示更多")
        self.btn_more.setObjectName("secondaryButton")
        self.btn_more.setCursor(Qt.PointingHandCursor)
        self.btn_more.clicked.connect(self._toggle)
        layout.addWidget(self.btn_more, 0, Qt.AlignRight)

    def set_text(self, text: str):
        self._full_text = text or ""
        self._expanded = False
        self._apply()

    def _toggle(self):
        self._expanded = not self._expanded
        self._apply()

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
