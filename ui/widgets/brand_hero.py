"""
BrandHero — 起卦頁主視覺（單一完成稿圖檔）。

資產：assets/ui/hero_banner_desktop.png
山景／太極／八卦／品牌字／飾線皆已烘焙於圖內，不再疊加 SVG 或 Qt 文字。

替換同路徑檔案後，下次顯示／縮放會依 mtime 自動重載，無需改程式。
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPixmapCache
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget


_ASSETS = Path(__file__).resolve().parents[2] / "assets" / "ui"
_HERO_BANNER = _ASSETS / "hero_banner_desktop.png"


class BrandHero(QWidget):
    """單一 Hero 圖：等比例縮放以貼合容器（不裁切、不拉伸）。"""

    TARGET_HEIGHT = 280

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("brandHero")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(self.TARGET_HEIGHT)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("background-color: #0D1B2A;")

        self._source = QPixmap()
        self._mtime_ns: int | None = None

        self._label = QLabel(self)
        self._label.setAlignment(Qt.AlignCenter)
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
        self._apply()

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

        # 避免 Qt 以檔名快取舊圖
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
        scaled = self._source.scaled(
            tw,
            th,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self._label.setPixmap(scaled)
