# ui/widgets/collapsible_groupbox.py

from PySide6.QtCore import (
    Qt,
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
)
from PySide6.QtWidgets import (
    QFrame,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class CollapsibleGroupBox(QFrame):
    """
    Accordion Widget

    使用方式：

        group = CollapsibleGroupBox("卦辭")
        group.setContentWidget(widget)

    """

    def __init__(self, title="", parent=None):
        super().__init__(parent)

        self.setFrameShape(QFrame.StyledPanel)

        self.toggleButton = QToolButton()
        self.toggleButton.setObjectName("collapseToggle")
        self.toggleButton.setText(title)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)
        self.toggleButton.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )
        self.toggleButton.setArrowType(Qt.RightArrow)
        self.toggleButton.setCursor(Qt.PointingHandCursor)
        self.toggleButton.setStyleSheet("")
        self.toggleButton.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        self.contentArea = QWidget()
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.mainLayout.addWidget(self.toggleButton)
        self.mainLayout.addWidget(self.contentArea)

        self.animation = QParallelAnimationGroup(self)

        self.contentAnimation = QPropertyAnimation(
            self.contentArea,
            b"maximumHeight",
        )
        self.contentAnimation.setDuration(180)
        self.contentAnimation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        self.animation.addAnimation(self.contentAnimation)

        self.toggleButton.clicked.connect(self.toggle)
        # 預設摺疊（不播放動畫）
        self.contentArea.setMaximumHeight(0)

    def setContentWidget(self, widget):
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 0, 12, 12)
        layout.setSpacing(8)
        layout.addWidget(widget)

        self.contentArea.setLayout(layout)

    def expand(self):
        self.toggleButton.setChecked(True)
        self.toggleButton.setArrowType(Qt.DownArrow)

        content_layout = self.contentArea.layout()
        if content_layout is None:
            return

        h = max(content_layout.sizeHint().height(), 80)

        self.contentAnimation.stop()
        self.contentAnimation.setStartValue(
            self.contentArea.maximumHeight()
        )
        self.contentAnimation.setEndValue(h)
        self.animation.start()

    def collapse(self):
        self.toggleButton.setChecked(False)
        self.toggleButton.setArrowType(Qt.RightArrow)

        self.contentAnimation.stop()
        self.contentAnimation.setStartValue(
            self.contentArea.maximumHeight()
        )
        self.contentAnimation.setEndValue(0)
        self.animation.start()

    def toggle(self):
        if self.toggleButton.isChecked():
            self.expand()
        else:
            self.collapse()

    def isExpanded(self) -> bool:
        return self.toggleButton.isChecked()