import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from ui.ui_mainwindow import Ui_MainWindow
from core.controller import HexagramController
from core.presenter import HexagramPresenter
from ui.history_page import HistoryPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setStyleSheet("""
        QPushButton:checked {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        """)

        self.lines = [None] * 6

        self.values = {
            "YoungYang": "少陽",
            "YoungYin": "少陰",
            "OldYang": "老陽",
            "OldYin": "老陰",
        }

        self.buttons = {}

        self.controller = HexagramController()
        self.presenter = HexagramPresenter(self.ui)
        self.history_page = HistoryPage(self.ui)

        self.init_buttons()
        self.init_number_input()

    def init_buttons(self):
        names = ["YoungYang", "YoungYin", "OldYang", "OldYin"]

        for line in range(1, 7):
            group = []

            for name in names:
                button = getattr(self.ui, f"rb{line}{name}")

                button.clicked.connect(
                    lambda checked=False, l=line, n=name: self.select_line(l, n)
                )

                group.append(button)

            self.buttons[line] = group

    def init_number_input(self):
        """
        初始化卦序輸入
        """
        self.ui.btnNumberCalculate.clicked.connect(
            self.calculate_by_number
        )

    def select_line(self, line, name):

        for btn in self.buttons[line]:
            btn.blockSignals(True)
            btn.setChecked(False)
            btn.blockSignals(False)

        button = getattr(self.ui, f"rb{line}{name}")
        button.blockSignals(True)
        button.setChecked(True)
        button.blockSignals(False)

        self.lines[line - 1] = self.values[name]

        if None in self.lines:
            return

        result = self.controller.calculate(
            self.lines,
            self.ui.editQuestion.text().strip()
        )

        self.presenter.show(result)
        self.history_page.refresh()
        self.ui.tabWidget.setCurrentWidget(
            self.ui.tab_interpretation
        )

    def calculate_by_number(self):

        number = self.ui.spinHexagramNumber.value()

        question = self.ui.editQuestion.text().strip()

        result = self.controller.calculate_by_number(
            number,
            question
        )

        self.presenter.show(result)
        self.history_page.refresh()

        self.ui.tabWidget.setCurrentWidget(
            self.ui.tab_interpretation
        )


def run_app():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())