"""
BrandHero — 起卦頁主視覺（單一完成稿圖檔）。

資產：assets/ui/hero_banner_desktop.png
山景／太極／八卦／品牌字／飾線皆已烘焙於圖內，不再疊加 SVG 或 Qt 文字。

顯示策略（Cover 滿版，不留深藍硬邊）：
- 寬屏提高 Hero 高度（接近原圖比例），避免太極頂緣被裁切
- 頂部深藍呼吸空間以垂直漸層融入圖面，避免藍條硬切
- 較窄／較寬 → 等比放大後裁切；裁切錨點對準品牌焦點
  （太極＋「易經占卜」）

替換同路徑檔案後，下次顯示／縮放會依 mtime 自動重載，無需改程式。
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPixmap, QPixmapCache
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from core.paths import assets_ui_dir


_HERO_BANNER = assets_ui_dir() / "hero_banner_desktop.png"

# 原圖 2400×560；太極圖中心（相對座標）
_SRC_W = 2400
_SRC_H = 560
_ASPECT = _SRC_W / _SRC_H  # ≈ 4.286
_FOCAL_X = 1175 / _SRC_W  # ≈ 0.4896
_FOCAL_Y = 110 / _SRC_H   # ≈ 0.1964
# 顯示座標微調：正值＝太極／品牌往右移（縮小 crop_x）
_NUDGE_X_PX = 14
# 太極中心距視窗頂的目標距離（避免頂緣貼齊視窗）
_FOCAL_TOP_PAD = 72
# 寬屏額外頂部留白（深藍），讓八卦圈與視窗邊緣有呼吸空間
_TOP_BREATHING = 36

_HEIGHT_MIN = 200
_HEIGHT_BASE = 280
_HEIGHT_MAX = 448 + _TOP_BREATHING


class BrandHero(QWidget):
    """單一 Hero 圖：Cover 滿版；寬屏加高；裁切對準太極焦點。"""

    TARGET_HEIGHT = _HEIGHT_BASE

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("brandHero")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(self.TARGET_HEIGHT)
        self.setMinimumWidth(0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("background-color: #0D1B2A;")

        self._source = QPixmap()
        self._mtime_ns: int | None = None

        self._label = QLabel(self)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setMinimumWidth(0)
        self._label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._label.setScaledContents(False)
        self._label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._label)

        self._apply()

    def showEvent(self, event):
        super().showEvent(event)
        self._apply()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._sync_height_for_width(self.width())
        self._apply()

    @staticmethod
    def preferred_height_for_width(width: int) -> int:
        """寬屏接近原圖比例加高，並加頂部呼吸空間。"""

        w = max(1, width)
        natural = int(round(w / _ASPECT)) + _TOP_BREATHING
        if w >= 1600:
            return max(_HEIGHT_BASE, min(_HEIGHT_MAX, natural))
        if w >= 1100:
            t = (w - 1100) / (1600 - 1100)
            target = int(
                round(_HEIGHT_BASE + t * (min(_HEIGHT_MAX, natural) - _HEIGHT_BASE))
            )
            return max(_HEIGHT_BASE, min(_HEIGHT_MAX, target))
        if w >= 600:
            return _HEIGHT_BASE
        return max(_HEIGHT_MIN, min(_HEIGHT_BASE, int(round(_HEIGHT_BASE * w / 600))))

    def _sync_height_for_width(self, width: int):
        target = self.preferred_height_for_width(width)
        if self.height() != target:
            self.setFixedHeight(target)

    def _reload_source_if_needed(self) -> None:
        """從固定路徑重讀；檔案被覆蓋後依 mtime 自動置換。"""
        path = _HERO_BANNER
        try:
            mtime_ns = path.stat().st_mtime_ns
        except OSError:
            self._source = QPixmap()
            self._mtime_ns = None
            return

        if (
            mtime_ns == self._mtime_ns
            and not self._source.isNull()
        ):
            return

        key = str(path.resolve())
        QPixmapCache.remove(key)
        QPixmapCache.remove(str(path))

        pm = QPixmap()
        if not pm.load(key):
            pm = QPixmap()
        self._source = pm
        self._mtime_ns = mtime_ns

    def _apply(self):
        self._reload_source_if_needed()
        if self._source.isNull():
            self._label.clear()
            return

        tw = max(1, self.width())
        th = max(1, self.height())
        top_pad = _TOP_BREATHING if tw >= 1100 else 0
        avail_h = max(1, th - top_pad)

        # Cover：放大蓋滿可用區域（頂部可留深藍呼吸空間）
        scaled = self._source.scaled(
            tw,
            avail_h,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )

        target_x = tw * 0.5
        target_y = min(_FOCAL_TOP_PAD, avail_h * 0.28)
        x = int(round(scaled.width() * _FOCAL_X - target_x - _NUDGE_X_PX))
        y = int(round(scaled.height() * _FOCAL_Y - target_y))
        x = max(0, min(x, scaled.width() - tw))
        y = max(0, min(y, scaled.height() - avail_h))

        cropped = scaled.copy(x, y, tw, avail_h)

        canvas = QPixmap(tw, th)
        canvas.fill(Qt.transparent)

        navy = QColor("#0D1B2A")
        painter = QPainter(canvas)
        painter.fillRect(0, 0, tw, th, navy)
        painter.drawPixmap(0, top_pad, cropped)

        # 頂部深藍 → 透明漸層（加長距離、放緩透明度曲線，減少接界痕跡）
        fade_extra = 72 if top_pad > 0 else 48
        fade_h = top_pad + fade_extra
        fade_h = min(fade_h, th)
        if fade_h > 0:
            grad = QLinearGradient(0, 0, 0, fade_h)
            grad.setColorAt(0.0, navy)
            grad.setColorAt(0.25, QColor(13, 27, 42, 235))
            grad.setColorAt(0.55, QColor(13, 27, 42, 140))
            grad.setColorAt(0.8, QColor(13, 27, 42, 55))
            grad.setColorAt(1.0, QColor(13, 27, 42, 0))
            painter.fillRect(0, 0, tw, fade_h, QBrush(grad))

        painter.end()
        self._label.setPixmap(canvas)
