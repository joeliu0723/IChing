"""History list row widget — columns aligned with Layout.png."""

from __future__ import annotations

import re

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from core.history import HistoryRecord
from ui.theme import tokens as T
from ui.widgets.hexagram_glyph import HexagramGlyphWidget, changed_lines_from
from ui.widgets.nav_icons import icon_star, icon_unverified, icon_verified

# 去掉卦名開頭的 Unicode 卦象符號（䷀–䷿ 等），避免與手繪卦象重疊
_HEX_CHAR_RE = re.compile(r"^[\u4DC0-\u4DFF]\s*")


def _display_name(name: str) -> str:
    text = (name or "").strip()
    if not text:
        return "—"
    return _HEX_CHAR_RE.sub("", text).strip() or "—"


class HistoryRecordRow(QWidget):
    favoriteClicked = Signal(str)
    activated = Signal(str)
    selectionToggled = Signal(str, bool)

    def __init__(self, record: HistoryRecord, parent=None, *, row_height: int = 72):
        super().__init__(parent)
        self.record_id = record.id
        self._row_height = max(56, row_height)
        self.setObjectName("historyRecordRow")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(56)
        self.setFixedHeight(self._row_height)

        root = QHBoxLayout(self)
        root.setContentsMargins(10, 6, 10, 6)
        root.setSpacing(10)

        # 解卦時間 + 選取勾選框（手機友善）
        time_col = QVBoxLayout()
        time_col.setSpacing(4)
        time_cap = QLabel("解卦時間")
        time_cap.setObjectName("historyColCaption")
        self.time_label = QLabel(record.created_at.strftime("%Y-%m-%d %H:%M"))
        self.time_label.setObjectName("historyTimeValue")
        self.btn_select = QToolButton()
        self.btn_select.setObjectName("historySelectCheck")
        self.btn_select.setCheckable(True)
        self.btn_select.setCursor(Qt.PointingHandCursor)
        self.btn_select.setFixedSize(28, 28)
        self.btn_select.setToolTip("選取此紀錄")
        self.btn_select.toggled.connect(self._on_select_toggled)
        time_col.addWidget(time_cap)
        time_col.addWidget(self.time_label)
        time_col.addWidget(self.btn_select, 0, Qt.AlignLeft)
        time_col.addStretch(1)
        root.addLayout(time_col, 2)

        # 本卦 / 變卦：標題列放「本卦 豐亨」，下方只留手繪卦象（不再重複 Unicode 符號）
        glyphs = QHBoxLayout()
        glyphs.setSpacing(14)
        lines = list(record.lines or [])
        moving = list(record.moving_lines or [])

        main_wrap = QVBoxLayout()
        main_wrap.setSpacing(4)
        main_title = QHBoxLayout()
        main_title.setSpacing(6)
        main_cap = QLabel("本卦")
        main_cap.setObjectName("historyColCaption")
        self.main_name = QLabel(_display_name(record.main_name))
        self.main_name.setObjectName("historyHexName")
        main_title.addWidget(main_cap)
        main_title.addWidget(self.main_name)
        main_title.addStretch(1)
        self.main_glyph = HexagramGlyphWidget(size="tiny")
        self.main_glyph.set_lines(lines, moving)
        main_wrap.addLayout(main_title)
        main_wrap.addWidget(self.main_glyph, 0, Qt.AlignLeft)
        main_wrap.addStretch(1)
        glyphs.addLayout(main_wrap, 1)

        changed_wrap = QVBoxLayout()
        changed_wrap.setSpacing(4)
        changed_title = QHBoxLayout()
        changed_title.setSpacing(6)
        changed_cap = QLabel("變卦")
        changed_cap.setObjectName("historyColCaption")
        self.changed_name = QLabel(_display_name(record.changed_name))
        self.changed_name.setObjectName("historyHexName")
        changed_title.addWidget(changed_cap)
        changed_title.addWidget(self.changed_name)
        changed_title.addStretch(1)
        self.changed_glyph = HexagramGlyphWidget(size="tiny")
        self.changed_glyph.set_lines(changed_lines_from(lines), [])
        changed_wrap.addLayout(changed_title)
        changed_wrap.addWidget(self.changed_glyph, 0, Qt.AlignLeft)
        changed_wrap.addStretch(1)
        glyphs.addLayout(changed_wrap, 1)
        root.addLayout(glyphs, 3)

        # 占卜問題
        mid = QVBoxLayout()
        mid.setSpacing(2)
        q_cap = QLabel("占卜問題")
        q_cap.setObjectName("historyColCaption")
        self.question_label = QLabel(record.question or "（未填寫問題）")
        self.question_label.setObjectName("historyQuestion")
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        mid.addWidget(q_cap)
        mid.addWidget(self.question_label, 1)
        root.addLayout(mid, 4)

        # 收藏
        fav_col = QVBoxLayout()
        fav_col.setSpacing(2)
        fav_cap = QLabel("收藏")
        fav_cap.setObjectName("historyColCaption")
        fav_cap.setAlignment(Qt.AlignHCenter)
        self.btn_fav = QToolButton()
        self.btn_fav.setObjectName("historyFavButton")
        self.btn_fav.setCursor(Qt.PointingHandCursor)
        self.btn_fav.setAutoRaise(True)
        self.btn_fav.setFixedSize(28, 28)
        self._set_favorite(bool(record.favorite))
        self.btn_fav.clicked.connect(lambda: self.favoriteClicked.emit(self.record_id))
        fav_wrap = QWidget()
        fav_wrap.setFixedWidth(40)
        fav_wrap.setLayout(fav_col)
        fav_col.addWidget(fav_cap)
        fav_col.addWidget(self.btn_fav, 0, Qt.AlignHCenter)
        fav_col.addStretch(1)
        root.addWidget(fav_wrap)

        # 驗證
        ver_col = QVBoxLayout()
        ver_col.setSpacing(2)
        ver_cap = QLabel("驗證")
        ver_cap.setObjectName("historyColCaption")
        ver_cap.setAlignment(Qt.AlignHCenter)
        self.btn_verified = QPushButton()
        self.btn_verified.setObjectName("historyVerifyButton")
        self.btn_verified.setFlat(True)
        self.btn_verified.setEnabled(False)
        self.btn_verified.setFixedSize(28, 28)
        self._set_verified(record.verification_result or "未驗證")
        ver_wrap = QWidget()
        ver_wrap.setFixedWidth(40)
        ver_wrap.setLayout(ver_col)
        ver_col.addWidget(ver_cap)
        ver_col.addWidget(self.btn_verified, 0, Qt.AlignHCenter)
        ver_col.addStretch(1)
        root.addWidget(ver_wrap)

        self.set_checked(False)

    def _on_select_toggled(self, checked: bool):
        self.btn_select.setText("✓" if checked else "")
        self.set_selected(checked)
        self.selectionToggled.emit(self.record_id, checked)

    def _set_favorite(self, favorite: bool):
        self.btn_fav.setIcon(icon_star(T.GOLD, 18, filled=favorite))
        self.btn_fav.setToolTip("已收藏" if favorite else "未收藏")

    def _set_verified(self, result: str):
        verified = result not in ("", "未驗證")
        if verified:
            color = T.WARNING if result == "不符合" else "#2F6B4F"
            self.btn_verified.setIcon(icon_verified(color, 20))
            self.btn_verified.setToolTip(f"已驗證：{result}")
        else:
            self.btn_verified.setIcon(icon_unverified(T.BORDER, 20))
            self.btn_verified.setToolTip("尚未驗證")

    def sizeHint(self):
        return QSize(640, self._row_height)

    def is_checked(self) -> bool:
        return self.btn_select.isChecked()

    def set_checked(self, checked: bool):
        self.btn_select.blockSignals(True)
        self.btn_select.setChecked(checked)
        self.btn_select.setText("✓" if checked else "")
        self.btn_select.blockSignals(False)
        self.set_selected(checked)

    def set_selected(self, selected: bool):
        self.setProperty("selected", "true" if selected else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.activated.emit(self.record_id)
        super().mouseDoubleClickEvent(event)
