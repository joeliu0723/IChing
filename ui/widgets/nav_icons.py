"""Painted nav / status icons for AppNavBar and history rows."""

from __future__ import annotations

from math import cos, pi, sin

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap, QPolygonF


def _pixmap(size: int, paint_fn) -> QPixmap:
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.Antialiasing, True)
    paint_fn(painter, size)
    painter.end()
    return pm


def icon_taiji(color: str, size: int = 20) -> QIcon:
    c = QColor(color)

    def paint(p: QPainter, s: int):
        m = s * 0.1
        r = QRectF(m, m, s - 2 * m, s - 2 * m)
        cx, cy = r.center().x(), r.center().y()
        rad = r.width() / 2
        eye = max(1.3, s * 0.07)

        # Right (yang) half filled via S-curve path
        path = QPainterPath()
        path.moveTo(cx, cy - rad)
        path.arcTo(QRectF(cx - rad, cy - rad, 2 * rad, 2 * rad), 90, -180)
        path.arcTo(QRectF(cx - rad / 2, cy, rad, rad), 270, 180)
        path.arcTo(QRectF(cx - rad / 2, cy - rad, rad, rad), 270, -180)
        p.setPen(Qt.NoPen)
        p.setBrush(c)
        p.drawPath(path)

        # Outer ring
        p.setPen(QPen(c, max(1.2, s * 0.07)))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(r)

        # Eyes: empty in yang (top), solid in yin (bottom)
        p.setPen(Qt.NoPen)
        # punch empty eye by drawing over with transparent via erase — use bg
        # Draw a paper-colored hole isn't available; use DestinationOut
        p.setCompositionMode(QPainter.CompositionMode_Clear)
        p.drawEllipse(QPointF(cx, cy - rad * 0.5), eye * 1.4, eye * 1.4)
        p.setCompositionMode(QPainter.CompositionMode_SourceOver)
        p.setBrush(c)
        p.drawEllipse(QPointF(cx, cy + rad * 0.5), eye, eye)

    return QIcon(_pixmap(size, paint))


def icon_book(color: str, size: int = 20) -> QIcon:
    c = QColor(color)

    def paint(p: QPainter, s: int):
        pen = QPen(c, max(1.2, s * 0.08))
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        m = s * 0.18
        mid = s / 2
        p.drawLine(QPointF(mid, m), QPointF(mid, s - m))
        p.drawLine(QPointF(m, m + 2), QPointF(mid, m))
        p.drawLine(QPointF(s - m, m + 2), QPointF(mid, m))
        p.drawLine(QPointF(m, m + 2), QPointF(m, s - m - 1))
        p.drawLine(QPointF(s - m, m + 2), QPointF(s - m, s - m - 1))
        p.drawLine(QPointF(m, s - m - 1), QPointF(mid, s - m + 1))
        p.drawLine(QPointF(s - m, s - m - 1), QPointF(mid, s - m + 1))

    return QIcon(_pixmap(size, paint))


def icon_list(color: str, size: int = 20) -> QIcon:
    c = QColor(color)

    def paint(p: QPainter, s: int):
        pen = QPen(c, max(1.2, s * 0.08))
        p.setPen(pen)
        p.setBrush(c)
        m = s * 0.2
        gap = (s - 2 * m) / 2
        for i in range(3):
            y = m + i * gap
            p.drawEllipse(QPointF(m + 1, y), s * 0.06, s * 0.06)
            p.drawLine(QPointF(m + s * 0.22, y), QPointF(s - m, y))

    return QIcon(_pixmap(size, paint))


def icon_star(color: str, size: int = 20, filled: bool = False) -> QIcon:
    c = QColor(color)

    def paint(p: QPainter, s: int):
        cx, cy = s / 2, s / 2
        outer, inner = s * 0.38, s * 0.16
        pts = []
        for i in range(10):
            ang = -pi / 2 + i * pi / 5
            r = outer if i % 2 == 0 else inner
            pts.append(QPointF(cx + r * cos(ang), cy + r * sin(ang)))
        poly = QPolygonF(pts)
        pen = QPen(c, max(1.1, s * 0.07))
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(c if filled else Qt.NoBrush)
        p.drawPolygon(poly)

    return QIcon(_pixmap(size, paint))


def icon_verified(color: str, size: int = 20) -> QIcon:
    c = QColor(color)

    def paint(p: QPainter, s: int):
        m = s * 0.12
        p.setPen(QPen(c, max(1.3, s * 0.09)))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(QRectF(m, m, s - 2 * m, s - 2 * m))
        pen = QPen(c, max(1.4, s * 0.1))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.drawLine(QPointF(s * 0.28, s * 0.52), QPointF(s * 0.44, s * 0.68))
        p.drawLine(QPointF(s * 0.44, s * 0.68), QPointF(s * 0.72, s * 0.34))

    return QIcon(_pixmap(size, paint))


def icon_unverified(color: str, size: int = 20) -> QIcon:
    c = QColor(color)

    def paint(p: QPainter, s: int):
        m = s * 0.12
        p.setPen(QPen(c, max(1.2, s * 0.08)))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(QRectF(m, m, s - 2 * m, s - 2 * m))

    return QIcon(_pixmap(size, paint))


NAV_ICON_BUILDERS = {
    "cast": icon_taiji,
    "interpretation": icon_book,
    "history": icon_list,
    "favorites": lambda color, size=20: icon_star(color, size, filled=False),
}
