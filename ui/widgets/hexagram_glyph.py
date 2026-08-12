"""Hexagram six-line glyph drawn with QPainter."""

from __future__ import annotations

from PySide6.QtCore import QPointF, QSize, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from ui.theme import tokens as T

# lines[0] = 初爻 (bottom), lines[5] = 上爻 (top)
_YANG = {"少陽", "老陽", "陽"}
_MOVING = {"老陽", "老陰"}


def is_yang(line: str) -> bool:
    return (line or "").strip() in _YANG or "陽" in (line or "")


def is_moving(line: str) -> bool:
    return (line or "").strip() in _MOVING


def flip_line(line: str) -> str:
    mapping = {
        "少陽": "少陽",
        "少陰": "少陰",
        "老陽": "少陰",
        "老陰": "少陽",
        "陽": "陽",
        "陰": "陰",
    }
    key = (line or "").strip()
    return mapping.get(key, key)


def changed_lines_from(main_lines: list[str]) -> list[str]:
    return [flip_line(line) for line in main_lines]


def draw_yao(
    painter: QPainter,
    x: float,
    y: float,
    w: float,
    broken: bool = False,
    moving: bool = False,
    color: QColor | None = None,
    width: float = 2.0,
):
    pen = QPen(color or QColor(T.NAVY))
    pen.setWidthF(width)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)

    if not broken:
        painter.drawLine(QPointF(x, y), QPointF(x + w, y))
    else:
        gap = w * 0.34
        mid = x + w * 0.5
        painter.drawLine(QPointF(x, y), QPointF(mid - gap * 0.5, y))
        painter.drawLine(QPointF(mid + gap * 0.5, y), QPointF(x + w, y))

    if moving:
        mark = QPen(QColor(T.WARNING))
        mark.setWidthF(max(1.2, width - 0.2))
        painter.setPen(mark)
        r = max(2.5, w * 0.06)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(x + w * 0.5, y), r, r)


class HexagramGlyphWidget(QWidget):
    """Renders six yao lines. Size presets: large / small."""

    def __init__(self, parent=None, *, size: str = "large"):
        super().__init__(parent)
        self._lines: list[str] = []
        self._moving: set[int] = set()
        self._size = size
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._apply_size()

    def _apply_size(self):
        if self._size == "small":
            self.setFixedSize(44, 56)
        elif self._size == "tiny":
            self.setFixedSize(36, 48)
        else:
            self.setFixedSize(88, 120)

    def sizeHint(self):
        return QSize(self.width(), self.height())

    def set_lines(self, lines: list[str], moving_lines: list[int] | None = None):
        self._lines = list(lines or [])
        self._moving = set(moving_lines or [])
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(self.rect(), Qt.transparent)

        w = self.width()
        h = self.height()
        margin_x = w * 0.08
        margin_y = h * 0.08
        line_w = w - 2 * margin_x
        usable_h = h - 2 * margin_y
        pen_w = 2.6 if self._size == "large" else 1.6 if self._size == "tiny" else 1.8

        # Display top→bottom as 上爻→初爻; data is bottom→top
        display = list(reversed(self._lines[:6]))
        while len(display) < 6:
            display.append("")

        for i, line in enumerate(display):
            y = margin_y + (i + 0.5) * (usable_h / 6.0)
            # moving_lines are 1-based from 初爻
            data_index = 6 - i  # 1..6
            moving = data_index in self._moving or is_moving(line)
            draw_yao(
                painter,
                margin_x,
                y,
                line_w,
                broken=not is_yang(line) if line else True,
                moving=moving and bool(line),
                color=QColor(T.NAVY),
                width=pen_w,
            )
        painter.end()
