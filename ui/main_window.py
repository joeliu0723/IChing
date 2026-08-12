import sys
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, Qt, QRectF
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QCompleter,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QStackedWidget,
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
from ui.widgets.brand_hero import BrandHero
from ui.widgets.collapsible_groupbox import CollapsibleGroupBox
from ui.widgets.mode_selector import ModeSelector


TRIGRAM_NAMES = ["乾", "坤", "震", "巽", "坎", "離", "兌", "艮"]

_ASSETS_UI = Path(__file__).resolve().parents[1] / "assets" / "ui"

CAST_HOME_STYLE = """
QMainWindow, QWidget#castHomeRoot, QWidget#castHomeBody, QWidget#tabDivination {
    background-color: #F7F4EC;
    color: #2B2E34;
}
QTabWidget::pane {
    border: none;
    top: 0px;
    background-color: #F7F4EC;
}
QWidget#brandHero {
    background-color: #0D1B2A;
    border: none;
}
QLabel#brandHeroTitleZh {
    color: #D4AF37;
    background: transparent;
}
QLabel#brandHeroTitleEn {
    color: #D4AF37;
    background: transparent;
    letter-spacing: 4px;
}
QWidget#modeSelector QPushButton#modeSelectButton {
    background-color: #F7F4EC;
    color: #2B2E34;
    border: 1px solid #C9B896;
    border-radius: 4px;
    padding: 0px 8px;
    font-size: 13px;
    font-weight: 500;
}
QWidget#modeSelector QPushButton#modeSelectButton:hover:!checked {
    background-color: #F1E8D6;
    border: 1px solid #D4AF37;
}
QWidget#modeSelector QPushButton#modeSelectButton:checked {
    background-color: #0D1B2A;
    color: #F7F4EC;
    border: 1px solid #D4AF37;
    font-weight: 600;
}
QFrame#questionCard {
    background-color: #F1E6D5;
    border: 1px solid #C9B896;
    border-radius: 8px;
}
QFrame#inputCard {
    background-color: #F7F4EC;
    border: 1px solid #D4C7B0;
    border-radius: 8px;
}
QLabel#sectionLabel, QLabel#inputCardTitle {
    color: #2B2E34;
    font-size: 13px;
    font-weight: 600;
}
QLabel#questionCardTitle {
    color: #0D1B2A;
    font-size: 14px;
    font-weight: 600;
    background: transparent;
}
QLabel#inputCardTitle {
    font-size: 15px;
    color: #2B2E34;
    qproperty-alignment: AlignCenter;
}
QLabel#lineRowLabel {
    color: #2B2E34;
    font-size: 13px;
    font-weight: 600;
    background: transparent;
}
QLineEdit#editQuestionHome {
    background-color: #F7F4EC;
    border: 1px solid #C9B896;
    border-radius: 6px;
    padding: 0px 16px;
    font-size: 13px;
    min-height: 54px;
    max-height: 54px;
    color: #0D1B2A;
    selection-background-color: #0D1B2A;
    selection-color: #F7F4EC;
}
QLineEdit#editQuestionHome::placeholder {
    color: #8A8478;
}
QLineEdit#editQuestionHome:focus {
    border: 1px solid #D4AF37;
    background-color: #F7F4EC;
    outline: none;
}
QLineEdit#editQuestionHome:hover:!focus {
    border: 1px solid #D4C7B0;
    background-color: #F7F4EC;
}
QPushButton#btnStartInterpretation {
    background-color: transparent;
    border: none;
    padding: 0px 24px;
    font-size: 16px;
    font-weight: 700;
    min-height: 52px;
    max-height: 52px;
    color: #F7F4EC;
}
QPushButton#btnStartInterpretation:focus {
    outline: none;
}
QTabBar::tab {
    background: #EFE7DA;
    color: #6B7280;
    padding: 6px 14px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background: #0D1B2A;
    color: #D4AF37;
}
QGroupBox#groupLinesInput {
    border: none;
    margin-top: 0px;
    background: transparent;
}
QGroupBox#groupLinesInput::title {
    height: 0px;
    width: 0px;
    color: transparent;
}
QWidget#sixLinesBody QRadioButton {
    background-color: #F1E8D6;
    color: #2B2E34;
    border: 1px solid #C9B896;
    border-radius: 5px;
    padding: 0px 8px 0px 6px;
    font-size: 13px;
    font-weight: 500;
    min-height: 34px;
    max-height: 34px;
    spacing: 7px;
}
QWidget#sixLinesBody QRadioButton::indicator {
    width: 14px;
    height: 14px;
    border-radius: 8px;
    border: 1.5px solid #B8A88A;
    background-color: #F1E8D6;
    margin-right: 1px;
}
QWidget#sixLinesBody QRadioButton::indicator:unchecked {
    border: 1.5px solid #B8A88A;
    background-color: #F1E8D6;
}
QWidget#sixLinesBody QRadioButton::indicator:unchecked:hover {
    border: 1.5px solid #D4AF37;
    background-color: #EDE4D0;
}
QWidget#sixLinesBody QRadioButton::indicator:checked {
    border: 1.5px solid #D4AF37;
    background-color: #F1E8D6;
    background: qradialgradient(
        cx:0.5, cy:0.5, radius:0.5,
        fx:0.5, fy:0.5,
        stop:0 #0D1B2A,
        stop:0.36 #0D1B2A,
        stop:0.37 #F1E8D6,
        stop:1 #F1E8D6
    );
}
QWidget#sixLinesBody QRadioButton:hover:!checked {
    background-color: #EDE4D0;
    border: 1px solid #D4AF37;
    color: #2B2E34;
}
QWidget#sixLinesBody QRadioButton:checked {
    background-color: #0D1B2A;
    color: #F7F4EC;
    border: 1px solid #D4AF37;
    font-weight: 600;
}
QWidget#sixLinesBody QRadioButton:checked:hover {
    background-color: #152536;
    color: #F7F4EC;
    border: 1px solid #E0C15A;
}
QWidget#sixLinesBody QRadioButton:checked::indicator {
    border: 1.5px solid #D4AF37;
    background-color: #0D1B2A;
    background: qradialgradient(
        cx:0.5, cy:0.5, radius:0.5,
        fx:0.5, fy:0.5,
        stop:0 #F7F4EC,
        stop:0.36 #F7F4EC,
        stop:0.37 #0D1B2A,
        stop:1 #0D1B2A
    );
}
QWidget#sixLinesBody QRadioButton:focus {
    outline: none;
}
QWidget#modeInputBody {
    background: transparent;
}
QWidget#modeInputBody QLabel#fieldLabel {
    color: #2B2E34;
    font-size: 13px;
    font-weight: 600;
    background: transparent;
}
QWidget#modeInputBody QLabel#sectionHint {
    color: #8A8478;
    font-size: 12px;
    font-weight: 400;
    background: transparent;
}
QWidget#modeInputBody QComboBox#modeInputControl,
QWidget#modeInputBody QSpinBox#modeInputControl {
    background-color: #F1E8D6;
    color: #0D1B2A;
    border: 1px solid #C9B896;
    border-radius: 5px;
    padding: 0px 10px;
    font-size: 13px;
    font-weight: 500;
    selection-background-color: #0D1B2A;
    selection-color: #F7F4EC;
}
QWidget#modeInputBody QComboBox#modeInputControl:hover,
QWidget#modeInputBody QSpinBox#modeInputControl:hover {
    background-color: #EDE4D0;
    border: 1px solid #D4C7B0;
}
QWidget#modeInputBody QComboBox#modeInputControl:focus,
QWidget#modeInputBody QSpinBox#modeInputControl:focus {
    border: 1px solid #D4AF37;
    background-color: #F7F4EC;
    outline: none;
}
QWidget#modeInputBody QComboBox#modeInputControl::drop-down {
    border: none;
    width: 22px;
    background: transparent;
}
QWidget#modeInputBody QComboBox#modeInputControl::down-arrow {
    width: 10px;
    height: 10px;
}
QWidget#modeInputBody QSpinBox#modeInputControl::up-button,
QWidget#modeInputBody QSpinBox#modeInputControl::down-button {
    width: 18px;
    border: none;
    background: transparent;
}
QWidget#modeInputBody QSpinBox#modeInputControl::up-arrow,
QWidget#modeInputBody QSpinBox#modeInputControl::down-arrow {
    width: 8px;
    height: 8px;
}
QGroupBox {
    background: transparent;
    border: none;
    margin-top: 4px;
    font-weight: 600;
    color: #2B2E34;
}
"""


class _PrimaryCtaButton(QPushButton):
    """Primary CTA with gold border inset 3px from the outer edge."""

    _OUTER_RADIUS = 8
    _INSET = 3
    _BORDER_WIDTH = 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg, text_color, border_color = self._palette_for_state()
        outer = QRectF(self.rect()).adjusted(0.5, 0.5, -1.0, -1.0)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(bg))
        painter.drawRoundedRect(outer, self._OUTER_RADIUS, self._OUTER_RADIUS)

        inner = outer.adjusted(self._INSET, self._INSET, -self._INSET, -self._INSET)
        inner_radius = max(0.0, self._OUTER_RADIUS - self._INSET + 0.5)
        pen = QPen(QColor(border_color), self._BORDER_WIDTH)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(inner, inner_radius, inner_radius)

        font = self.font()
        font.setPixelSize(16)
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor(text_color))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        painter.end()

    def _palette_for_state(self):
        if not self.isEnabled():
            return "#1A2838", "#8A8478", "#8A7A50"
        if self.isDown():
            return "#081018", "#F7F4EC", "#C9A032"
        if self.underMouse():
            return "#122233", "#FFFDF7", "#E8C96A"
        if self.hasFocus():
            return "#0D1B2A", "#F7F4EC", "#E8C96A"
        return "#0D1B2A", "#F7F4EC", "#D4AF37"


class _CtaElevationFilter(QObject):
    """Primary CTA hover elevation without layout movement."""

    def __init__(self, button: QPushButton):
        super().__init__(button)
        self._button = button
        self._rest_shadow = self._make_shadow(12, 2, 52)
        self._hover_shadow = self._make_shadow(18, 4, 88)
        button.setGraphicsEffect(self._rest_shadow)

    @staticmethod
    def _make_shadow(blur: int, offset_y: int, alpha: int) -> QGraphicsDropShadowEffect:
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, offset_y)
        shadow.setColor(QColor(212, 175, 55, alpha))
        return shadow

    def eventFilter(self, obj, event):
        if obj is self._button:
            if event.type() == QEvent.Type.Enter:
                self._button.setGraphicsEffect(self._hover_shadow)
            elif event.type() in (QEvent.Type.Leave, QEvent.Type.Hide):
                self._button.setGraphicsEffect(self._rest_shadow)
        return super().eventFilter(obj, event)


class _PaperBody(QWidget):
    """Hero 以下內容區：宣紙米白底（#F7F4EC）。

    paper_texture.svg 含 feTurbulence，Qt Svg 會渲成灰塊，
    故此處採用資產色票實心米白，避免 CTA 下方出現 #A19F9A。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("castHomeBody")
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAutoFillBackground(False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#F7F4EC"))
        painter.end()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("易經占卜 — I Ching")
        self.setStyleSheet(CAST_HOME_STYLE)

        self.lines = [None] * 6

        self.values = {
            "YoungYang": "少陽",
            "YoungYin": "少陰",
            "OldYang": "老陽",
            "OldYin": "老陰",
        }

        self.buttons = {}
        self.mode_selector = None
        self._input_card_title = None
        self._input_scroll = None

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
        self.init_meihua_input()
        self.init_input_mode_switching()
        self.init_cast_home_redesign()
        self.init_cast_page_navigation()

    def init_interpretation_widgets(self):
        """補充解卦頁欄位，並將各經文區塊改為預設折疊。"""

        layout = self.ui.verticalLayoutInterpretation

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        header_layout.addWidget(QLabel("占卜問題"))

        self.ui.editInterpretationQuestion = QLineEdit()
        self.ui.editInterpretationQuestion.setPlaceholderText("（未填寫）")
        header_layout.addWidget(self.ui.editInterpretationQuestion, 1)

        self.ui.btnSaveQuestion = QPushButton("儲存問題")
        self.ui.btnSaveQuestion.clicked.connect(self.save_question)
        header_layout.addWidget(self.ui.btnSaveQuestion)

        self.ui.chkFavorite = QCheckBox("收藏")
        self.ui.chkFavorite.toggled.connect(self.on_favorite_toggled)
        header_layout.addWidget(self.ui.chkFavorite)

        layout.insertWidget(0, header)

        insert_at = layout.indexOf(self.ui.grp_txtAIAnalysis)
        groups = [
            ("txtChangedJudgment", "變卦卦辭"),
            ("txtChangedTuan", "變卦大帥解釋"),
            ("txtChangedXiang", "變卦象傳"),
            ("txtChangedWenyan", "變卦文言"),
            ("txtChangedTranslation", "變卦白話翻譯"),
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
            (self.ui.grp_txtTuan, "大帥解釋"),
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

        # Designer 內 layoutWidget 寬度不足，先加大以容納按鈕與「數字卦」
        geo = self.ui.layoutWidget.geometry()
        self.ui.layoutWidget.setGeometry(
            geo.x(),
            geo.y(),
            max(geo.width(), 620),
            geo.height(),
        )

        self.ui.rbMeihuaNumbers = QRadioButton("數字卦")
        self.ui.rbMeihuaNumbers.setObjectName("rbMeihuaNumbers")
        # 插在「開始解卦」之前（若尚未加入則加在末尾）
        self.ui.horizontalLayout.addWidget(self.ui.rbMeihuaNumbers)

        self.ui.btnStartInterpretation = _PrimaryCtaButton("開始解卦")
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

        # 從絕對座標改掛入 GroupBox，稍後與其他模式一併放入 Stack
        number_widget = self.ui.horizontalLayoutWidget_8
        number_widget.setParent(None)

        group = QGroupBox("卦序輸入")
        layout = QHBoxLayout(group)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(number_widget)
        layout.addStretch()

        self.groupNumberInput = group

    def init_name_input(self):
        """初始化卦名輸入"""

        group = QGroupBox("卦名輸入")
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

        self.groupNameInput = group

    def init_trigrams_input(self):
        """初始化上下卦輸入"""

        group = QGroupBox("上下卦輸入")
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

        self.groupTrigramsInput = group

    def init_meihua_input(self):
        """初始化梅花易數數字卦輸入（三數）。"""

        group = QGroupBox("數字卦（梅花易數）")
        layout = QVBoxLayout(group)

        hint = QLabel(
            "第1數→上卦（÷8 餘）、第2數→下卦（÷8 餘）、"
            "第3數→動爻（÷6 餘；餘0作8／6）"
        )
        hint.setWordWrap(True)
        layout.addWidget(hint)

        row = QHBoxLayout()
        row.addWidget(QLabel("第1數"))
        self.spinMeihua1 = QSpinBox()
        self.spinMeihua1.setRange(1, 99999)
        self.spinMeihua1.setValue(1)
        row.addWidget(self.spinMeihua1)

        row.addWidget(QLabel("第2數"))
        self.spinMeihua2 = QSpinBox()
        self.spinMeihua2.setRange(1, 99999)
        self.spinMeihua2.setValue(1)
        row.addWidget(self.spinMeihua2)

        row.addWidget(QLabel("第3數"))
        self.spinMeihua3 = QSpinBox()
        self.spinMeihua3.setRange(1, 99999)
        self.spinMeihua3.setValue(1)
        row.addWidget(self.spinMeihua3)
        row.addStretch()
        layout.addLayout(row)

        self.groupMeihuaInput = group

    def init_input_mode_switching(self):
        """依 RadioButton 切換輸入方式；固定區域高度避免跳動。"""

        layout = self.ui.verticalLayout_2

        # 六爻原本在 layout 內，先取出再放入 stack
        lines_group = self.ui.groupLinesInput
        layout.removeWidget(lines_group)

        self.input_mode_stack = QStackedWidget()
        self.input_mode_stack.setMinimumHeight(420)

        pages = [
            ("six_lines", lines_group),
            ("name", self.groupNameInput),
            ("number", self.groupNumberInput),
            ("trigrams", self.groupTrigramsInput),
            ("meihua", self.groupMeihuaInput),
        ]

        self.mode_page_index = {}
        for key, page in pages:
            index = self.input_mode_stack.addWidget(page)
            self.mode_page_index[key] = index

        # 插在「輸入模式」Radio 區塊正下方
        mode_index = layout.indexOf(self.ui.groupInputMode)
        if mode_index < 0:
            layout.insertWidget(0, self.input_mode_stack)
        else:
            layout.insertWidget(mode_index + 1, self.input_mode_stack)

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
        self.ui.rbMeihuaNumbers.toggled.connect(
            lambda checked: checked and self.show_input_mode("meihua")
        )

        self.show_input_mode("six_lines")

    @staticmethod
    def _prepare_mode_group(group: QGroupBox):
        """清空 GroupBox 外框，供 modeInputBody 重掛控件。"""

        group.setTitle("")
        group.setFlat(True)
        group.setStyleSheet(
            "QGroupBox { border: none; margin-top: 0; background: transparent; }"
        )
        if group.layout() is None:
            return
        layout = group.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            sub = item.layout()
            if sub is not None:
                while sub.count():
                    sub_item = sub.takeAt(0)
                    sub_widget = sub_item.widget()
                    if sub_widget is not None:
                        sub_widget.setParent(None)

    def _build_mode_input_body(self, control_width: int = 200):
        """置中 modeInputBody + grid（左標籤欄 + 右控件欄）。"""

        body = QWidget()
        body.setObjectName("modeInputBody")
        body_outer = QVBoxLayout(body)
        body_outer.setContentsMargins(0, 4, 0, 4)
        body_outer.setSpacing(0)
        body_outer.addStretch(1)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.addStretch(1)

        grid_host = QWidget()
        grid_host.setObjectName("modeInputContent")
        grid = QGridLayout(grid_host)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)
        grid.setColumnMinimumWidth(0, 72)
        grid.setColumnStretch(0, 0)
        grid.setColumnMinimumWidth(1, control_width)
        grid.setColumnStretch(1, 0)

        row.addWidget(grid_host, 0, Qt.AlignHCenter)
        row.addStretch(1)
        body_outer.addLayout(row)
        body_outer.addStretch(1)
        return body, grid

    @staticmethod
    def _add_field_label(grid: QGridLayout, row: int, text: str, height: int = 34):
        label = QLabel(text)
        label.setObjectName("fieldLabel")
        label.setFixedWidth(72)
        label.setFixedHeight(height)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        grid.addWidget(label, row, 0, Qt.AlignVCenter)
        return label

    @staticmethod
    def _style_mode_spin(spin: QSpinBox, width: int = 140, height: int = 34):
        spin.setObjectName("modeInputControl")
        spin.setFixedSize(width, height)
        spin.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        spin.setAlignment(Qt.AlignCenter)
        spin.setButtonSymbols(QSpinBox.UpDownArrows)

    @staticmethod
    def _style_mode_combo(combo: QComboBox, width: int, height: int = 34):
        combo.setObjectName("modeInputControl")
        combo.setFixedSize(width, height)
        combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        combo.setCursor(Qt.PointingHandCursor)

    def _mount_mode_group(self, group: QGroupBox, body: QWidget):
        if group.layout() is None:
            group_layout = QVBoxLayout(group)
        else:
            group_layout = group.layout()
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(0)
        group_layout.addWidget(body)
        group.setMinimumHeight(0)
        group.setMaximumHeight(16777215)
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def _restyle_name_input(self):
        """卦名：置中單列 ComboBox。"""

        group = self.groupNameInput
        self._prepare_mode_group(group)

        combo = self.comboHexagramName
        combo.setParent(None)
        self._style_mode_combo(combo, width=520, height=54)
        combo.setInsertPolicy(QComboBox.NoInsert)
        completer = QCompleter(combo.model(), combo)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        combo.setCompleter(completer)

        body, grid = self._build_mode_input_body(control_width=520)
        self._add_field_label(grid, 0, "卦名", height=54)
        grid.addWidget(combo, 0, 1, Qt.AlignVCenter)
        self._mount_mode_group(group, body)

    def _restyle_number_input(self):
        """卦序：置中單列 SpinBox。"""

        group = self.groupNumberInput
        self._prepare_mode_group(group)

        spin = self.ui.spinHexagramNumber
        spin.setParent(None)
        self._style_mode_spin(spin, width=140, height=34)

        body, grid = self._build_mode_input_body(control_width=140)
        self._add_field_label(grid, 0, "卦序")
        grid.addWidget(spin, 0, 1, Qt.AlignVCenter)
        self._mount_mode_group(group, body)

    def _restyle_trigrams_input(self):
        """上下卦：置中兩列 ComboBox。"""

        group = self.groupTrigramsInput
        self._prepare_mode_group(group)

        upper = self.comboUpperTrigram
        lower = self.comboLowerTrigram
        upper.setParent(None)
        lower.setParent(None)
        self._style_mode_combo(upper, width=200, height=34)
        self._style_mode_combo(lower, width=200, height=34)

        body, grid = self._build_mode_input_body(control_width=200)
        self._add_field_label(grid, 0, "上卦")
        grid.addWidget(upper, 0, 1, Qt.AlignVCenter)
        self._add_field_label(grid, 1, "下卦")
        grid.addWidget(lower, 1, 1, Qt.AlignVCenter)
        self._mount_mode_group(group, body)

    def _restyle_meihua_input(self):
        """數字卦：hint + 三列 SpinBox。"""

        group = self.groupMeihuaInput
        self._prepare_mode_group(group)

        for spin in (self.spinMeihua1, self.spinMeihua2, self.spinMeihua3):
            spin.setParent(None)
            self._style_mode_spin(spin, width=140, height=34)

        body = QWidget()
        body.setObjectName("modeInputBody")
        body_outer = QVBoxLayout(body)
        body_outer.setContentsMargins(0, 4, 0, 4)
        body_outer.setSpacing(0)
        body_outer.addStretch(1)

        center_row = QHBoxLayout()
        center_row.setContentsMargins(0, 0, 0, 0)
        center_row.addStretch(1)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(6)

        hint = QLabel(
            "第1數→上卦（÷8 餘）、第2數→下卦（÷8 餘）、"
            "第3數→動爻（÷6 餘；餘0作8／6）"
        )
        hint.setObjectName("sectionHint")
        hint.setWordWrap(True)
        hint.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(hint)

        grid_host = QWidget()
        grid = QGridLayout(grid_host)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)
        grid.setColumnMinimumWidth(0, 72)
        grid.setColumnStretch(0, 0)
        grid.setColumnMinimumWidth(1, 140)
        grid.setColumnStretch(1, 0)

        for row, (label_text, spin) in enumerate(
            (
                ("第1數", self.spinMeihua1),
                ("第2數", self.spinMeihua2),
                ("第3數", self.spinMeihua3),
            )
        ):
            self._add_field_label(grid, row, label_text)
            grid.addWidget(spin, row, 1, Qt.AlignVCenter)

        content_layout.addWidget(grid_host)
        center_row.addWidget(content, 0, Qt.AlignHCenter)
        center_row.addStretch(1)
        body_outer.addLayout(center_row)
        body_outer.addStretch(1)
        self._mount_mode_group(group, body)

    def _restyle_six_lines_input(self):
        """六爻選項卡片網格：左欄爻名＋四欄置中選項，保留既有按鈕綁定。"""

        group = self.ui.groupLinesInput
        group.setTitle("")
        group.setFlat(True)

        line_defs = (
            (6, "上爻"),
            (5, "五爻"),
            (4, "四爻"),
            (3, "三爻"),
            (2, "二爻"),
            (1, "初爻"),
        )
        value_keys = ("YoungYang", "YoungYin", "OldYang", "OldYin")
        self._yao_option_labels = {
            "YoungYang": "少陽",
            "YoungYin": "少陰",
            "OldYang": "老陽",
            "OldYin": "老陰",
        }
        _opt_w = 128
        _opt_h = 34
        _col_gap = 12
        _row_gap = 8

        body = QWidget()
        body.setObjectName("sixLinesBody")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(0, 4, 0, 4)
        body_layout.setSpacing(0)

        grid_row = QHBoxLayout()
        grid_row.setContentsMargins(0, 0, 0, 0)
        grid_row.setSpacing(0)

        grid_host = QWidget()
        grid_host.setObjectName("sixLinesContent")
        grid_host.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        grid = QGridLayout(grid_host)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(_col_gap)
        grid.setVerticalSpacing(_row_gap)
        grid.setColumnMinimumWidth(0, 52)
        grid.setColumnStretch(0, 0)
        for col in range(1, 5):
            grid.setColumnMinimumWidth(col, _opt_w)
            grid.setColumnStretch(col, 0)

        for row_idx, (line_no, line_label) in enumerate(line_defs):
            label = QLabel(line_label)
            label.setObjectName("lineRowLabel")
            label.setFixedWidth(52)
            label.setFixedHeight(_opt_h)
            label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
            grid.addWidget(label, row_idx, 0, Qt.AlignVCenter)

            for col_idx, key in enumerate(value_keys, start=1):
                button = getattr(self.ui, f"rb{line_no}{key}")
                button.setParent(None)
                button.setAutoExclusive(False)
                button.setFixedSize(_opt_w, _opt_h)
                button.setCursor(Qt.PointingHandCursor)
                button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                button.setAttribute(Qt.WA_StyledBackground, True)
                button.setStyleSheet("")
                self._refresh_yao_option_label(button, key, checked=button.isChecked())
                grid.addWidget(button, row_idx, col_idx, Qt.AlignVCenter)

        grid_row.addStretch(1)
        grid_row.addWidget(grid_host, 0, Qt.AlignHCenter)
        grid_row.addStretch(1)
        body_layout.addLayout(grid_row)

        for attr in (
            "horizontalLayoutWidget",
            "horizontalLayoutWidget_2",
            "horizontalLayoutWidget_3",
            "horizontalLayoutWidget_4",
            "horizontalLayoutWidget_5",
            "horizontalLayoutWidget_6",
        ):
            widget = getattr(self.ui, attr, None)
            if widget is not None:
                widget.hide()
                widget.setParent(None)

        if group.layout() is None:
            group_layout = QVBoxLayout(group)
        else:
            group_layout = group.layout()
            while group_layout.count():
                item = group_layout.takeAt(0)
                child = item.widget()
                if child is not None:
                    child.setParent(None)

        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(0)
        group_layout.addWidget(body)
        group.setMinimumHeight(0)
        group.setMaximumHeight(16777215)
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def _refresh_yao_option_label(self, button, key: str, checked: bool):
        """選項卡片文字；圓點由 QRadioButton::indicator 呈現。"""

        del checked
        label = self._yao_option_labels.get(key, button.text())
        button.setText(label)
    def _sync_yao_option_labels(self, line: int):
        value_keys = ("YoungYang", "YoungYin", "OldYang", "OldYin")
        for key in value_keys:
            button = getattr(self.ui, f"rb{line}{key}")
            self._refresh_yao_option_label(button, key, button.isChecked())

    def init_cast_home_redesign(self):
        """
        Phase 1B / V4：依參考圖重建 Hero／Mode／六爻 Card 視覺。

        Hero → Mode → Input Card → Question → CTA
        Mode Button → 既有 Radio → stack → start_interpretation
        """

        self._mode_radios = {
            "six_lines": self.ui.rbSixLines,
            "name": self.ui.rbHexagramName,
            "number": self.ui.rbHexagramNumber,
            "trigrams": self.ui.rbTrigrams,
            "meihua": self.ui.rbMeihuaNumbers,
        }
        self._mode_titles = {
            "six_lines": "六爻輸入",
            "name": "卦名",
            "number": "卦序",
            "trigrams": "上下卦",
            "meihua": "數字卦",
        }

        self.ui.groupInputMode.hide()
        self._restyle_six_lines_input()
        self._restyle_name_input()
        self._restyle_number_input()
        self._restyle_trigrams_input()
        self._restyle_meihua_input()

        self.input_mode_stack.setParent(None)
        self.input_mode_stack.setMinimumHeight(0)
        self.input_mode_stack.setMaximumHeight(228)
        self.input_mode_stack.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred,
        )

        self.ui.editQuestion.setParent(None)
        self.ui.editQuestion.setObjectName("editQuestionHome")
        self.ui.editQuestion.setPlaceholderText("請輸入您想占卜的問題......")
        self.ui.editQuestion.setFixedHeight(54)
        self.ui.editQuestion.setAttribute(Qt.WA_StyledBackground, True)
        self.ui.editQuestion.setCursor(Qt.IBeamCursor)

        self.ui.btnStartInterpretation.setParent(None)
        self.ui.btnStartInterpretation.setObjectName("btnStartInterpretation")
        self.ui.btnStartInterpretation.setFixedHeight(54)
        self.ui.btnStartInterpretation.setFixedWidth(300)
        self.ui.btnStartInterpretation.setCursor(Qt.PointingHandCursor)
        self._style_cta_button()

        self.ui.horizontalLayoutWidget_7.hide()
        self.ui.widget.hide()
        self.ui.tabDivination.setAttribute(Qt.WA_StyledBackground, True)
        self.ui.tabDivination.setAutoFillBackground(True)

        central_layout = self.centralWidget().layout()
        if central_layout is not None:
            central_layout.setContentsMargins(0, 0, 0, 0)
            central_layout.setSpacing(0)
        self.ui.tabWidget.setDocumentMode(True)
        self.ui.tabWidget.setContentsMargins(0, 0, 0, 0)

        tab = self.ui.tabDivination
        shell = QWidget()
        shell.setObjectName("castHomeRoot")
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        self.brand_hero = BrandHero()
        shell_layout.addWidget(self.brand_hero, 0)

        body = _PaperBody()
        body.setObjectName("castHomeBody")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(32, 2, 32, 2)
        body_layout.setSpacing(0)

        self.mode_selector = ModeSelector()
        self.mode_selector.modeSelected.connect(self._on_mode_button_selected)
        body_layout.addWidget(self.mode_selector, 0)
        body_layout.addSpacing(4)

        input_card = QFrame()
        input_card.setObjectName("inputCard")
        input_card.setAttribute(Qt.WA_StyledBackground, True)
        input_card.setFixedHeight(270)
        input_card_layout = QVBoxLayout(input_card)
        input_card_layout.setContentsMargins(16, 8, 16, 13)
        input_card_layout.setSpacing(8)

        title_row = QHBoxLayout()
        title_row.setSpacing(10)
        left_div = QSvgWidget(str(_ASSETS_UI / "ornamental_divider.svg"))
        left_div.setFixedSize(72, 14)
        left_div.setStyleSheet("background: transparent;")
        right_div = QSvgWidget(str(_ASSETS_UI / "ornamental_divider.svg"))
        right_div.setFixedSize(72, 14)
        right_div.setStyleSheet("background: transparent;")
        self._input_card_title = QLabel("六爻輸入")
        self._input_card_title.setObjectName("inputCardTitle")
        self._input_card_title.setAlignment(Qt.AlignCenter)
        self._input_card_title.setFixedHeight(22)
        title_row.addStretch(1)
        title_row.addWidget(left_div, 0, Qt.AlignVCenter)
        title_row.addWidget(self._input_card_title, 0, Qt.AlignVCenter)
        title_row.addWidget(right_div, 0, Qt.AlignVCenter)
        title_row.addStretch(1)
        input_card_layout.addLayout(title_row)
        input_card_layout.addWidget(self.input_mode_stack, 1)

        input_card_wrap = QWidget()
        input_card_wrap.setObjectName("inputCardWrap")
        input_card_wrap.setFixedHeight(270)
        input_card_wrap.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        wrap_layout = QVBoxLayout(input_card_wrap)
        wrap_layout.setContentsMargins(0, 0, 0, 0)
        wrap_layout.setSpacing(0)
        wrap_layout.addWidget(input_card)

        body_layout.addWidget(input_card_wrap, 0)
        body_layout.addSpacing(16)

        question_card = QFrame()
        question_card.setObjectName("questionCard")
        question_card.setAttribute(Qt.WA_StyledBackground, True)
        question_card.setFixedHeight(108)
        question_layout = QVBoxLayout(question_card)
        question_layout.setContentsMargins(16, 12, 16, 12)
        question_layout.setSpacing(8)
        q_label = QLabel("占卜問題")
        q_label.setObjectName("questionCardTitle")
        q_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        q_label.setFixedHeight(20)
        question_layout.addWidget(q_label)
        question_layout.addWidget(self.ui.editQuestion)

        question_card_wrap = QWidget()
        question_card_wrap.setObjectName("questionCardWrap")
        question_card_wrap.setFixedHeight(108)
        question_card_wrap.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        q_wrap_layout = QVBoxLayout(question_card_wrap)
        q_wrap_layout.setContentsMargins(0, 0, 0, 0)
        q_wrap_layout.setSpacing(0)
        q_wrap_layout.addWidget(question_card)

        body_layout.addWidget(question_card_wrap, 0)
        body_layout.addSpacing(10)

        cta_row = QHBoxLayout()
        cta_row.setContentsMargins(0, 0, 0, 0)
        cta_row.addStretch(1)
        cta_row.addWidget(self.ui.btnStartInterpretation)
        cta_row.addStretch(1)
        body_layout.addLayout(cta_row)

        shell_layout.addWidget(body, 1)

        if tab.layout() is None:
            tab_layout = QVBoxLayout(tab)
            tab_layout.setContentsMargins(0, 0, 0, 0)
            tab_layout.setSpacing(0)
        else:
            tab_layout = tab.layout()
            while tab_layout.count():
                item = tab_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        tab_layout.addWidget(shell)

        self.ui.tabWidget.setTabText(
            self.ui.tabWidget.indexOf(self.ui.tabDivination),
            "起卦",
        )

        self.mode_selector.set_active("six_lines")
        self.ui.rbSixLines.setChecked(True)
        self.show_input_mode("six_lines")
        self._flatten_mode_groups()

    @staticmethod
    def _apply_subtle_card_shadow(widget: QWidget):
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(8)
        shadow.setOffset(0, 1)
        shadow.setColor(QColor(43, 46, 52, 16))
        widget.setGraphicsEffect(shadow)

    @staticmethod
    def _apply_card_shadow(widget: QWidget):
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 1)
        shadow.setColor(QColor(43, 46, 52, 22))
        widget.setGraphicsEffect(shadow)

    def _style_cta_button(self):
        btn = self.ui.btnStartInterpretation
        btn.setAttribute(Qt.WA_StyledBackground, True)
        elevation = _CtaElevationFilter(btn)
        btn.installEventFilter(elevation)
        btn._cta_elevation_filter = elevation

    def init_cast_page_navigation(self):
        """
        首頁不顯示導航（無底欄、無頂部 Tab）。
        進入解卦／歷史後才顯示 Tab，以便返回起卦。
        """

        self.ui.tabWidget.tabBar().hide()
        self.ui.tabWidget.currentChanged.connect(self._sync_cast_tab_bar)
        self._sync_cast_tab_bar()

    def _sync_cast_tab_bar(self, *_args):
        on_home = self.ui.tabWidget.currentWidget() is self.ui.tabDivination
        bar = self.ui.tabWidget.tabBar()
        bar.setVisible(not on_home)
        bar.setMaximumHeight(0 if on_home else 16777215)

    def _flatten_mode_groups(self):
        """其他模式輸入區去掉傳統 GroupBox 外框感。"""

        for group in (
            self.groupNameInput,
            self.groupNumberInput,
            self.groupTrigramsInput,
            self.groupMeihuaInput,
        ):
            group.setFlat(True)
            group.setTitle("")
            group.setStyleSheet(
                "QGroupBox { border: none; margin-top: 0; background: transparent; }"
            )

    def _on_mode_button_selected(self, mode: str):
        """新按鈕 → 同步既有 Radio（由 Radio toggled 驅動 stack）。"""

        radio = self._mode_radios.get(mode)
        if radio is None:
            return

        if not radio.isChecked():
            radio.setChecked(True)
        else:
            self.show_input_mode(mode)

    def show_input_mode(self, mode):
        index = self.mode_page_index.get(mode)
        if index is None:
            return
        self.input_mode_stack.setCurrentIndex(index)
        if self.mode_selector is not None:
            self.mode_selector.set_active(mode)
        if self._input_card_title is not None:
            self._input_card_title.setText(
                self._mode_titles.get(mode, "起卦輸入")
            )

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
        self._sync_yao_option_labels(line)

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
            return

        if self.ui.rbMeihuaNumbers.isChecked():
            n1 = self.spinMeihua1.value()
            n2 = self.spinMeihua2.value()
            n3 = self.spinMeihua3.value()
            self.run_cast(
                lambda: self.controller.calculate_by_meihua(
                    n1,
                    n2,
                    n3,
                    question,
                )
            )

    def resolve_hexagram_name(self):
        selected_text = self.comboHexagramName.currentText().strip()

        if not selected_text:
            return None

        combo = self.comboHexagramName
        exact_index = combo.findText(selected_text, Qt.MatchExactly)
        if exact_index >= 0:
            number = combo.itemData(exact_index)
            if isinstance(number, int):
                return HexagramLookup.number_to_name(number)

        if HexagramLookup.name_to_number(selected_text) is not None:
            return selected_text

        contains_index = combo.findText(selected_text, Qt.MatchContains)
        if contains_index >= 0:
            number = combo.itemData(contains_index)
            if isinstance(number, int):
                return HexagramLookup.number_to_name(number)

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

    def sync_question_field(self):
        if session.record is not None:
            question = session.record.question
        elif session.result is not None:
            question = session.result.question
        else:
            question = ""

        self.ui.editInterpretationQuestion.setText(question)

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

    def save_question(self):
        question = self.ui.editInterpretationQuestion.text()

        try:
            self.controller.save_question(question)
        except ValueError as error:
            self.show_input_error(str(error))
            return

        self.history_page.refresh_and_keep_selection()
        QMessageBox.information(self, "儲存成功", "占卜問題已儲存。")

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
        self.sync_question_field()
        self.sync_favorite_checkbox()
        self.sync_verification_fields()

    def show_result(self, result, refresh_history=True):
        self.presenter.show(result)
        self.sync_question_field()
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
