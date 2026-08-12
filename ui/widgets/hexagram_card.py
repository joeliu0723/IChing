"""Clickable hexagram summary card (本卦 / 變卦)."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout

from ui.widgets.hexagram_glyph import HexagramGlyphWidget


class HexagramSummaryCard(QFrame):
    clicked = Signal(str)

    def __init__(self, role: str, title: str, parent=None):
        super().__init__(parent)
        self.role = role
        self.setObjectName("hexCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(148)

        root = QHBoxLayout(self)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(14)

        self.glyph = HexagramGlyphWidget(size="large")
        root.addWidget(self.glyph, 0, Qt.AlignVCenter)

        col = QVBoxLayout()
        col.setSpacing(4)
        self.role_label = QLabel(title)
        self.role_label.setObjectName("hexCardTitle")
        self.number_label = QLabel("第 — 卦")
        self.number_label.setObjectName("hexCardNumber")
        self.name_label = QLabel("—")
        self.name_label.setObjectName("hexCardName")
        self.moving_label = QLabel("動爻：—")
        self.moving_label.setObjectName("mutedLabel")
        col.addWidget(self.role_label)
        col.addWidget(self.number_label)
        col.addWidget(self.name_label)
        col.addWidget(self.moving_label)
        col.addStretch(1)
        root.addLayout(col, 1)

        self.set_active(False)

    def set_active(self, active: bool):
        self.setProperty("active", "true" if active else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def set_hexagram(
        self,
        number: int,
        name: str,
        lines: list[str],
        moving_lines: list[int] | None = None,
    ):
        self.number_label.setText(f"第 {number} 卦" if number else "第 — 卦")
        self.name_label.setText(name or "—")
        moving = moving_lines or []
        if moving:
            self.moving_label.setText("動爻：" + "、".join(str(i) for i in moving))
        else:
            self.moving_label.setText("動爻：無")
        # Only highlight moving on 本卦 card
        highlight = moving if self.role == "main" else []
        self.glyph.set_lines(lines, highlight)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.role)
        super().mousePressEvent(event)
