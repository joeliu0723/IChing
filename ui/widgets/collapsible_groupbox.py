# ui/widgets/collapsible_groupbox.py

from PySide6.QtCore import (
    Qt,
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
)
from PySide6.QtWidgets import (
    QFrame,
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
        self.toggleButton.setText(title)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)
        self.toggleButton.setToolButtonStyle(
            self.toggleButton.toolButtonStyle()
        )
        self.toggleButton.setArrowType(Qt.RightArrow)

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

    def setContentWidget(self, widget):
        layout = QVBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(widget)

        self.contentArea.setLayout(layout)

    def expand(self):
        self.toggleButton.setChecked(True)
        self.toggleButton.setArrowType(Qt.DownArrow)

        h = self.contentArea.layout().sizeHint().height()

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