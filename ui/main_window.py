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
from ui.widgets.collapsible_groupbox import CollapsibleGroupBox


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
        self.init_start_button()
        self.init_buttons()
        self.init_number_input()
        self.init_name_input()
        self.init_trigrams_input()
        self.init_input_mode_switching()

    def init_interpretation_widgets(self):
        """補充解卦頁欄位，並將各經文區塊改為預設折疊。"""

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
            self._add_collapsible_editor(
                layout,
                insert_at,
                title,
                attr_name,
            )

        designer_groups = [
            (self.ui.grp_txtJudgment, "卦辭"),
            (self.ui.grp_txtTuan, "彖傳"),
            (self.ui.grp_txtXiang, "象傳"),
            (self.ui.grp_txtWenyan, "文言"),
            (self.ui.grp_txtTranslation, "白話翻譯"),
            (self.ui.grp_txtAIAnalysis, "AI分析"),
            (self.ui.grp_txtNotes, "我的心得"),
        ]

        for group_box, title in designer_groups:
            self._wrap_group_as_collapsible(layout, group_box, title)

    def _add_collapsible_editor(self, layout, index, title, attr_name):
        editor = QPlainTextEdit()
        editor.setMinimumHeight(120)
        setattr(self.ui, attr_name, editor)

        collapsible = CollapsibleGroupBox(title)
        collapsible.setContentWidget(editor)
        layout.insertWidget(index, collapsible)

    def _wrap_group_as_collapsible(self, layout, group_box, title):
        index = layout.indexOf(group_box)
        if index < 0:
            return

        editor = group_box.findChild(QPlainTextEdit)
        if editor is None:
            return

        layout.removeWidget(group_box)
        group_box.hide()

        editor.setParent(None)
        editor.setMinimumHeight(120)

        collapsible = CollapsibleGroupBox(title)
        collapsible.setContentWidget(editor)
        layout.insertWidget(index, collapsible)

    def init_start_button(self):
        """在「上下卦」右側新增「開始解卦」按鈕。"""

        # Designer 內 layoutWidget 寬度不足，先加大以容納按鈕
        geo = self.ui.layoutWidget.geometry()
        self.ui.layoutWidget.setGeometry(
            geo.x(),
            geo.y(),
            max(geo.width(), 520),
            geo.height(),
        )

        self.ui.btnStartInterpretation = QPushButton("開始解卦")
        self.ui.horizontalLayout.addWidget(self.ui.btnStartInterpretation)
        self.ui.btnStartInterpretation.clicked.connect(
            self.start_interpretation
        )

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
        """初始化卦序輸入（排卦改由「開始解卦」觸發）。"""

        self.ui.btnNumberCalculate.hide()

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
        """只更新六爻選擇，不自動排卦。"""

        for btn in self.buttons[line]:
            btn.blockSignals(True)
            btn.setChecked(False)
            btn.blockSignals(False)

        button = getattr(self.ui, f"rb{line}{name}")
        button.blockSignals(True)
        button.setChecked(True)
        button.blockSignals(False)

        self.lines[line - 1] = self.values[name]

    def start_interpretation(self):
        """依目前輸入模式排卦並進入解卦頁。"""

        question = self.current_question()

        if self.ui.rbSixLines.isChecked():
            if None in self.lines:
                self.show_input_error("六爻輸入不完整，請選擇全部六爻。")
                return

            lines = self.lines.copy()
            self.run_cast(
                lambda: self.controller.calculate(lines, question)
            )
            return

        if self.ui.rbHexagramNumber.isChecked():
            number = self.ui.spinHexagramNumber.value()
            self.run_cast(
                lambda: self.controller.calculate_by_number(
                    number,
                    question,
                )
            )
            return

        if self.ui.rbHexagramName.isChecked():
            name = self.resolve_hexagram_name()

            if name is None:
                self.show_input_error("請輸入或選擇有效的卦名。")
                return

            self.run_cast(
                lambda: self.controller.calculate_by_name(name, question)
            )
            return

        if self.ui.rbTrigrams.isChecked():
            upper = self.comboUpperTrigram.currentText()
            lower = self.comboLowerTrigram.currentText()
            self.run_cast(
                lambda: self.controller.calculate_by_trigrams(
                    upper,
                    lower,
                    question,
                )
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
