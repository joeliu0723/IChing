"""
ModeSelector — 五種起卦模式選擇列。

只負責 UI 與 modeSelected(str) 訊號；
不負責 Controller／Engine／起卦計算。
圖示以統一線條風格程式繪製（不新增圖片資產檔）。
"""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget


# (mode_key, label)
MODE_OPTIONS = (
    ("six_lines", "六爻輸入"),
    ("name", "卦名"),
    ("number", "卦序"),
    ("trigrams", "上下卦"),
    ("meihua", "數字卦"),
)

_ICON_SIZE = 16
_BTN_HEIGHT = 40
_COLOR_INK = QColor("#2B2E34")
_COLOR_ACTIVE_ICON = QColor("#F7F4EC")


def _pen(color: QColor, width: float = 1.2) -> QPen:
    pen = QPen(color)
    pen.setWidthF(width)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    return pen


def _draw_yao(painter: QPainter, x: float, y: float, w: float, broken: bool = False):
    """畫一爻：陽＝實線，陰＝中斷線。"""
    if not broken:
        painter.drawLine(QPointF(x, y), QPointF(x + w, y))
        return
    gap = w * 0.36
    mid = x + w * 0.5
    painter.drawLine(QPointF(x, y), QPointF(mid - gap * 0.5, y))
    painter.drawLine(QPointF(mid + gap * 0.5, y), QPointF(x + w, y))


def _make_icon(mode: str, color: QColor, size: int = _ICON_SIZE) -> QIcon:
    """統一細線風格的模式圖示（向量式 QPainter，非 Unicode／點陣資產）。"""

    dpr = 2
    px = size * dpr
    pm = QPixmap(px, px)
    pm.fill(Qt.transparent)
    pm.setDevicePixelRatio(dpr)

    painter = QPainter(pm)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setPen(_pen(color, 1.25))
    painter.setBrush(Qt.NoBrush)

    m = 2.0
    x0 = m
    y0 = m
    w = size - 2 * m
    h = size - 2 * m

    if mode == "six_lines":
        # 六爻：完整六爻卦象（陰陽相間）
        pattern = (False, True, False, True, False, True)
        for i, broken in enumerate(pattern):
            y = y0 + 1.2 + i * ((h - 2.4) / 5.0)
            _draw_yao(painter, x0 + 0.5, y, w - 1.0, broken)

    elif mode == "name":
        # 卦名：書冊／名標 — 左卦象、右標籤線
        fold = x0 + w * 0.50
        painter.drawRoundedRect(QRectF(x0, y0, w, h), 1.2, 1.2)
        painter.drawLine(QPointF(fold, y0 + 1.2), QPointF(fold, y0 + h - 1.2))
        lw = fold - x0 - 2.2
        for i, broken in enumerate((False, True, False, True)):
            y = y0 + 2.4 + i * ((h - 4.8) / 3.0)
            _draw_yao(painter, x0 + 1.4, y, lw, broken)
        rx = fold + 1.6
        rw = x0 + w - rx - 1.4
        painter.drawLine(QPointF(rx, y0 + h * 0.36), QPointF(rx + rw, y0 + h * 0.36))
        painter.drawLine(QPointF(rx, y0 + h * 0.64), QPointF(rx + rw, y0 + h * 0.64))

    elif mode == "number":
        # 卦序：左側完整微卦＋右側 1→3 序位階梯
        gw = w * 0.46
        for i, broken in enumerate((False, True, False, True, False, True)):
            y = y0 + 1.0 + i * ((h - 2.0) / 5.0)
            _draw_yao(painter, x0, y, gw, broken)
        sx = x0 + w * 0.58
        for i in range(3):
            y = y0 + 2.2 + i * ((h - 4.4) / 2.0)
            length = w * 0.14 + i * w * 0.12
            painter.drawLine(QPointF(sx, y), QPointF(sx + length, y))
            # 左側小豎標，強化「序」感
            painter.drawLine(
                QPointF(sx - 1.6, y - 1.1),
                QPointF(sx - 1.6, y + 1.1),
            )

    elif mode == "trigrams":
        # 上下卦：上乾（三陽）／下坤（三陰），中縫拉開
        gap = 3.2
        block = (h - gap) / 2.0
        upper = (False, False, False)
        lower = (True, True, True)
        for y_base, pattern in ((y0, upper), (y0 + block + gap, lower)):
            for i, broken in enumerate(pattern):
                y = y_base + (i + 0.5) * (block / 3.0)
                _draw_yao(painter, x0 + 0.5, y, w - 1.0, broken)

    elif mode == "meihua":
        # 數字卦：三欄計數點（1／2／3）表數占輸入
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        r = 1.05
        cols = (
            (x0 + w * 0.20, 1),
            (x0 + w * 0.50, 2),
            (x0 + w * 0.80, 3),
        )
        for cx, count in cols:
            top = y0 + 1.5
            bottom = y0 + h - 3.2
            if count == 1:
                ys = ((top + bottom) * 0.5,)
            else:
                ys = tuple(
                    top + (bottom - top) * i / (count - 1) for i in range(count)
                )
            for y in ys:
                painter.drawEllipse(QPointF(cx, y), r, r)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(_pen(color, 1.2))
        painter.drawLine(
            QPointF(x0 + 0.8, y0 + h - 0.8),
            QPointF(x0 + w - 0.8, y0 + h - 0.8),
        )

    painter.end()
    return QIcon(pm)


class ModeSelector(QWidget):
    """模式選擇列；點選後發出 modeSelected(mode_key)。"""

    modeSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modeSelector")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(_BTN_HEIGHT)

        self._buttons: dict[str, QPushButton] = {}
        self._active = "six_lines"

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        for key, label in MODE_OPTIONS:
            button = QPushButton(label)
            button.setObjectName("modeSelectButton")
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.setFixedHeight(_BTN_HEIGHT)
            button.setMinimumWidth(0)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setIconSize(QSize(_ICON_SIZE, _ICON_SIZE))
            button.setLayoutDirection(Qt.LeftToRight)
            button.clicked.connect(lambda checked=False, k=key: self._on_clicked(k))
            layout.addWidget(button, 1)
            self._buttons[key] = button

        self.set_active("six_lines")

    def _on_clicked(self, key: str):
        self.set_active(key)
        self.modeSelected.emit(key)

    def set_active(self, key: str):
        if key not in self._buttons:
            return
        self._active = key
        for mode_key, button in self._buttons.items():
            active = mode_key == key
            button.blockSignals(True)
            button.setChecked(active)
            button.blockSignals(False)
            color = _COLOR_ACTIVE_ICON if active else _COLOR_INK
            button.setIcon(_make_icon(mode_key, color))

    def active_mode(self) -> str:
        return self._active
