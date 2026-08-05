import sys

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from ui.ui_mainwindow import Ui_MainWindow
from core.controller import HexagramController
from core.presenter import HexagramPresenter
from core.hexagram_lookup import HexagramLookup
from ui.history_page import HistoryPage


TRIGRAM_NAMES = ["乾", "坤", "震", "巽", "坎", "離", "兌", "艮"]


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
        self.history_page = HistoryPage(
            self.ui,
            on_select=self.show_history_record,
        )

        self.init_interpretation_widgets()
        self.init_buttons()
        self.init_number_input()
        self.init_name_input()
        self.init_trigrams_input()
        self.init_input_mode_switching()

    def init_interpretation_widgets(self):
        """補充解卦頁：問題、變卦經文、爻辭。"""

        layout = self.ui.verticalLayoutInterpretation

        self.ui.lblQuestion = QLabel("占卜問題：（未填寫）")
        self.ui.lblQuestion.setWordWrap(True)
        layout.insertWidget(0, self.ui.lblQuestion)

        insert_at = layout.indexOf(self.ui.grp_txtAIAnalysis)
        groups = [
            ("txtChangedJudgment", "變卦卦辭"),
            ("txtChangedTuan", "變卦彖傳"),
            ("txtChangedXiang", "變卦象傳"),
            ("txtChangedWenyan", "變卦文言"),
            ("txtLineTexts", "爻辭"),
        ]

        for attr_name, title in reversed(groups):
            self._add_interpretation_group(
                layout,
                insert_at,
                title,
                attr_name,
            )

    def _add_interpretation_group(self, layout, index, title, attr_name):
        group = QGroupBox(title)
        box_layout = QVBoxLayout(group)
        editor = QPlainTextEdit()
        box_layout.addWidget(editor)
        layout.insertWidget(index, group)
        setattr(self.ui, attr_name, editor)

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
        """初始化卦序輸入"""

        self.ui.btnNumberCalculate.clicked.connect(
            self.calculate_by_number
        )

    def init_name_input(self):
        """初始化卦名輸入"""

        group = QGroupBox("卦名輸入", self.ui.widget)
        layout = QHBoxLayout(group)

        layout.addWidget(QLabel("選擇卦名"))

        self.comboHexagramName = QComboBox()
        self.comboHexagramName.setEditable(True)

        for number, name in HexagramLookup.hexagram_names():
            self.comboHexagramName.addItem(
                f"{number}. {name}",
                number,
            )

        layout.addWidget(self.comboHexagramName, 1)

        button = QPushButton("依卦名排卦")
        button.clicked.connect(self.calculate_by_name)
        layout.addWidget(button)

        self.ui.verticalLayout_2.addWidget(group)
        self.groupNameInput = group

    def init_trigrams_input(self):
        """初始化上下卦輸入"""

        group = QGroupBox("上下卦輸入", self.ui.widget)
        layout = QHBoxLayout(group)

        layout.addWidget(QLabel("上卦"))
        self.comboUpperTrigram = QComboBox()
        self.comboUpperTrigram.addItems(TRIGRAM_NAMES)
        layout.addWidget(self.comboUpperTrigram)

        layout.addWidget(QLabel("下卦"))
        self.comboLowerTrigram = QComboBox()
        self.comboLowerTrigram.addItems(TRIGRAM_NAMES)
        layout.addWidget(self.comboLowerTrigram)

        button = QPushButton("依上下卦排卦")
        button.clicked.connect(self.calculate_by_trigrams)
        layout.addWidget(button)
        layout.addStretch()

        self.ui.verticalLayout_2.addWidget(group)
        self.groupTrigramsInput = group

    def init_input_mode_switching(self):
        """依 RadioButton 切換輸入方式，僅顯示目前輸入區塊。"""

        self.mode_groups = {
            "six_lines": self.ui.groupLinesInput,
            "name": self.groupNameInput,
            "number": self.ui.horizontalLayoutWidget_8,
            "trigrams": self.groupTrigramsInput,
        }

        self.ui.rbSixLines.toggled.connect(
            lambda checked: checked and self.show_input_mode("six_lines")
        )
        self.ui.rbHexagramName.toggled.connect(
            lambda checked: checked and self.show_input_mode("name")
        )
        self.ui.rbHexagramNumber.toggled.connect(
            lambda checked: checked and self.show_input_mode("number")
        )
        self.ui.rbTrigrams.toggled.connect(
            lambda checked: checked and self.show_input_mode("trigrams")
        )

        self.show_input_mode("six_lines")

    def show_input_mode(self, mode):
        for name, group in self.mode_groups.items():
            group.setVisible(name == mode)

    def current_question(self):
        return self.ui.editQuestion.text().strip()

    def run_cast(self, calculate):
        """共用起卦流程：計算、錯誤提示、顯示結果。"""

        try:
            result = calculate()
        except ValueError as error:
            self.show_input_error(str(error))
            return

        self.show_result(result)

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

        lines = self.lines.copy()
        question = self.current_question()

        self.run_cast(
            lambda: self.controller.calculate(lines, question)
        )

    def calculate_by_number(self):
        number = self.ui.spinHexagramNumber.value()
        question = self.current_question()

        self.run_cast(
            lambda: self.controller.calculate_by_number(number, question)
        )

    def calculate_by_name(self):
        name = self.resolve_hexagram_name()

        if name is None:
            self.show_input_error("請輸入或選擇有效的卦名。")
            return

        question = self.current_question()

        self.run_cast(
            lambda: self.controller.calculate_by_name(name, question)
        )

    def resolve_hexagram_name(self):
        selected_text = self.comboHexagramName.currentText().strip()

        if not selected_text:
            return None

        selected_index = self.comboHexagramName.findText(selected_text)

        if selected_index >= 0:
            number = self.comboHexagramName.itemData(selected_index)
            return HexagramLookup.number_to_name(number)

        if HexagramLookup.name_to_number(selected_text) is not None:
            return selected_text

        return None

    def calculate_by_trigrams(self):
        upper = self.comboUpperTrigram.currentText()
        lower = self.comboLowerTrigram.currentText()
        question = self.current_question()

        self.run_cast(
            lambda: self.controller.calculate_by_trigrams(
                upper,
                lower,
                question,
            )
        )

    def show_history_record(self, record_id):
        record = self.history_page.get_record(record_id)

        if record is None:
            return

        try:
            result = self.controller.build_result(
                record.lines,
                record.question,
            )
        except ValueError as error:
            self.show_input_error(str(error))
            return

        result.notes = record.notes
        self.show_result(result, refresh_history=False)

    def show_result(self, result, refresh_history=True):
        self.presenter.show(result)

        if refresh_history:
            self.history_page.refresh()

        self.ui.tabWidget.setCurrentWidget(
            self.ui.tab_interpretation
        )

    def show_input_error(self, message):
        QMessageBox.warning(self, "輸入錯誤", message)


def run_app():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
