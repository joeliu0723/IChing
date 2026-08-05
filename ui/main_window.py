import sys

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.ui_mainwindow import Ui_MainWindow
from core.controller import HexagramController
from core.presenter import HexagramPresenter
from core.hexagram_lookup import HexagramLookup
from core.history import VERIFICATION_RESULTS
from core.session import session
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
            on_delete=self.delete_history_record,
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

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.ui.lblQuestion = QLabel("占卜問題：（未填寫）")
        self.ui.lblQuestion.setWordWrap(True)
        header_layout.addWidget(self.ui.lblQuestion, 1)

        self.ui.chkFavorite = QCheckBox("收藏")
        self.ui.chkFavorite.toggled.connect(self.on_favorite_toggled)
        header_layout.addWidget(self.ui.chkFavorite)

        layout.insertWidget(0, header)

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
        ]

        for group_box, title in designer_groups:
            self._wrap_group_as_collapsible(layout, group_box, title)

        self._wrap_notes_as_collapsible(layout, self.ui.grp_txtNotes)
        self._add_verification_section(layout)

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

    def _wrap_notes_as_collapsible(self, layout, group_box):
        """心得區塊：可編輯文字 + 儲存按鈕，預設折疊。"""

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
        self.ui.txtNotes = editor

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(editor)

        self.ui.btnSaveNotes = QPushButton("儲存心得")
        self.ui.btnSaveNotes.clicked.connect(self.save_notes)
        content_layout.addWidget(self.ui.btnSaveNotes)

        collapsible = CollapsibleGroupBox("我的心得")
        collapsible.setContentWidget(content)
        layout.insertWidget(index, collapsible)

    def _add_verification_section(self, layout):
        """事後驗證：驗證結果 + 驗證內容 + 儲存。"""

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        result_row = QHBoxLayout()
        result_row.addWidget(QLabel("驗證結果"))
        self.ui.comboVerificationResult = QComboBox()
        self.ui.comboVerificationResult.addItems(list(VERIFICATION_RESULTS))
        result_row.addWidget(self.ui.comboVerificationResult, 1)
        content_layout.addLayout(result_row)

        content_layout.addWidget(QLabel("驗證內容"))
        self.ui.txtVerificationContent = QPlainTextEdit()
        self.ui.txtVerificationContent.setMinimumHeight(100)
        content_layout.addWidget(self.ui.txtVerificationContent)

        self.ui.btnSaveVerification = QPushButton("儲存驗證")
        self.ui.btnSaveVerification.clicked.connect(self.save_verification)
        content_layout.addWidget(self.ui.btnSaveVerification)

        collapsible = CollapsibleGroupBox("事後驗證")
        collapsible.setContentWidget(content)
        layout.addWidget(collapsible)

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
        session.set_result(result)
        session.set_record(record)
        self.show_result(result, refresh_history=False)

    def sync_favorite_checkbox(self):
        favorite = bool(session.record and session.record.favorite)

        self.ui.chkFavorite.blockSignals(True)
        self.ui.chkFavorite.setChecked(favorite)
        self.ui.chkFavorite.blockSignals(False)

    def sync_verification_fields(self):
        if session.record is None:
            content = ""
            result = "未驗證"
        else:
            content = session.record.verification_content
            result = session.record.verification_result or "未驗證"

        self.ui.txtVerificationContent.setPlainText(content)

        index = self.ui.comboVerificationResult.findText(result)
        if index < 0:
            index = 0

        self.ui.comboVerificationResult.blockSignals(True)
        self.ui.comboVerificationResult.setCurrentIndex(index)
        self.ui.comboVerificationResult.blockSignals(False)

    def on_favorite_toggled(self, checked):
        try:
            self.controller.set_favorite(checked)
        except ValueError as error:
            self.ui.chkFavorite.blockSignals(True)
            self.ui.chkFavorite.setChecked(False)
            self.ui.chkFavorite.blockSignals(False)
            self.show_input_error(str(error))
            return

        self.history_page.refresh_and_keep_selection()

    def save_notes(self):
        notes = self.ui.txtNotes.toPlainText()

        try:
            self.controller.save_notes(notes)
        except ValueError as error:
            self.show_input_error(str(error))
            return

        self.history_page.refresh_and_keep_selection()
        QMessageBox.information(self, "儲存成功", "心得已儲存。")

    def save_verification(self):
        content = self.ui.txtVerificationContent.toPlainText()
        result = self.ui.comboVerificationResult.currentText()

        try:
            self.controller.save_verification(content, result)
        except ValueError as error:
            self.show_input_error(str(error))
            return

        self.history_page.refresh_and_keep_selection()
        QMessageBox.information(self, "儲存成功", "驗證資料已儲存。")

    def delete_history_record(self, record_ids):
        if isinstance(record_ids, str):
            record_ids = [record_ids]

        if not record_ids:
            self.show_input_error("請先選擇要刪除的紀錄。")
            return

        count = len(record_ids)

        if count == 1:
            message = "確定要永久刪除此占卜紀錄？此操作無法復原。"
        else:
            message = (
                f"確定要永久刪除 {count} 筆占卜紀錄？"
                "此操作無法復原。"
            )

        reply = QMessageBox.question(
            self,
            "確認刪除",
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:
            self.controller.delete_records(record_ids)
        except ValueError as error:
            self.show_input_error(str(error))
            return

        self.history_page.refresh()
        self.sync_favorite_checkbox()
        self.sync_verification_fields()

    def show_result(self, result, refresh_history=True):
        self.presenter.show(result)
        self.sync_favorite_checkbox()
        self.sync_verification_fields()

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
