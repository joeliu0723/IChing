import sys
from pathlib import Path

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QPushButton

from core.controller import HexagramController
from core.presenter import HexagramPresenter
from ui.history_page import HistoryPage


class MainWindow:

    def __init__(self):

        loader = QUiLoader()

        ui_file = Path(__file__).parent / "main_window.ui"

        file = QFile(str(ui_file))
        if not file.open(QFile.ReadOnly):
            raise RuntimeError(f"無法開啟 {ui_file}")

        self.window = loader.load(file)
        file.close()

        if self.window is None:
            raise RuntimeError("UI 載入失敗")

        # 被選取按鈕樣式
        self.window.setStyleSheet("""
        QPushButton:checked {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        """)

        # 六爻資料（由下往上）
        self.lines = [None] * 6

        self.values = {
            "YoungYang": "少陽",
            "YoungYin": "少陰",
            "OldYang": "老陽",
            "OldYin": "老陰",
        }

        self.buttons = {}

        # Controller / Presenter
        self.controller = HexagramController()
        self.presenter = HexagramPresenter(self.window)

        # History Page
        self.history_page = HistoryPage(self.window)

        self.init_buttons()

    def init_buttons(self):

        names = [
            "YoungYang",
            "YoungYin",
            "OldYang",
            "OldYin",
        ]

        for line in range(1, 7):

            group = []

            for name in names:

                button = self.window.findChild(
                    QPushButton,
                    f"rb{line}{name}",
                )

                if button is None:
                    print(f"找不到 rb{line}{name}")
                    continue

                button.clicked.connect(
                    lambda checked=False, l=line, n=name: self.select_line(l, n)
                )

                group.append(button)

            self.buttons[line] = group

    def select_line(self, line, name):

        # 同一爻取消其它按鈕
        for btn in self.buttons[line]:
            btn.blockSignals(True)
            btn.setChecked(False)
            btn.blockSignals(False)

        # 設定目前按鈕
        button = self.window.findChild(
            QPushButton,
            f"rb{line}{name}",
        )

        if button is not None:
            button.blockSignals(True)
            button.setChecked(True)
            button.blockSignals(False)

        # 更新六爻資料
        self.lines[line - 1] = self.values[name]

        # 六爻尚未輸入完成
        if None in self.lines:

            print("\n========== 六爻 ==========")

            titles = [
                "初爻",
                "二爻",
                "三爻",
                "四爻",
                "五爻",
                "上爻",
            ]

            for i in range(6):
                print(f"{titles[i]}：{self.lines[i]}")

            return

        # ===== 六爻完成，開始排卦 =====

        question = ""

        if hasattr(self.window, "editQuestion"):
            question = self.window.editQuestion.text().strip()

        result = self.controller.calculate(
            self.lines,
            question,
        )

        self.presenter.show(result)

        self.history_page.refresh()

        if (
            hasattr(self.window, "tabWidget")
            and hasattr(self.window, "tab_interpretation")
        ):
            self.window.tabWidget.setCurrentWidget(
                self.window.tab_interpretation
            )

    def show(self):
        self.window.show()


def run_app():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())