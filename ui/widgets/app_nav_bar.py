"""Bottom app navigation for narrow layouts."""

from __future__ import annotations

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QSizePolicy,
    QToolButton,
    QWidget,
)

from ui.theme import tokens as T
from ui.widgets.nav_icons import NAV_ICON_BUILDERS

NAV_ITEMS = (
    ("cast", "起卦"),
    ("interpretation", "解卦"),
    ("history", "歷史"),
    ("favorites", "收藏"),
)


class AppNavBar(QWidget):
    navigated = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("appNavBar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(62)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._buttons: dict[str, QToolButton] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(0)

        for index, (key, label) in enumerate(NAV_ITEMS):
            if index > 0:
                sep = QFrame()
                sep.setObjectName("appNavSep")
                sep.setFrameShape(QFrame.VLine)
                sep.setFixedWidth(1)
                sep.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
                layout.addWidget(sep)

            button = QToolButton()
            button.setObjectName("appNavButton")
            button.setText(label)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setIcon(NAV_ICON_BUILDERS[key](T.BORDER, 18))
            button.setIconSize(QSize(18, 18))
            button.clicked.connect(lambda checked=False, k=key: self._on_click(k))
            layout.addWidget(button, 1)
            self._buttons[key] = button

        self.set_active("cast")

    def _on_click(self, key: str):
        self.set_active(key)
        self.navigated.emit(key)

    def set_active(self, key: str):
        for k, button in self._buttons.items():
            button.blockSignals(True)
            active = k == key
            button.setChecked(active)
            color = T.GOLD if active else T.BORDER
            if k == "favorites":
                from ui.widgets.nav_icons import icon_star

                button.setIcon(icon_star(color, 18, filled=active))
            else:
                button.setIcon(NAV_ICON_BUILDERS[k](color, 18))
            button.blockSignals(False)
