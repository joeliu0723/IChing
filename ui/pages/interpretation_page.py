"""Interpretation page shell: hex cards + content tabs + notes/verification."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from core.history import VERIFICATION_RESULTS
from ui.theme import tokens as T
from ui.widgets.collapsible_groupbox import CollapsibleGroupBox
from ui.widgets.content_viewer import ContentViewer
from ui.widgets.hexagram_card import HexagramSummaryCard
from ui.widgets.hexagram_glyph import changed_lines_from
from ui.widgets.segmented_tabs import SegmentedTabs

MAIN_TABS = (
    ("judgment", "卦辭"),
    ("tuan", "大帥解釋"),
    ("translation", "白話翻譯"),
    ("lines", "爻辭"),
)

CHANGED_TABS = (
    ("changed_judgment", "卦辭"),
    ("changed_tuan", "大帥解釋"),
    ("changed_translation", "白話翻譯"),
    ("changed_lines", "爻辭"),
)

_TAB_KIND = {
    "judgment": "judgment",
    "tuan": "tuan",
    "translation": "translation",
    "lines": "lines",
    "changed_judgment": "judgment",
    "changed_tuan": "tuan",
    "changed_translation": "translation",
    "changed_lines": "lines",
}


class InterpretationPage(QWidget):
    """Full-width interpretation view mounted into tab_interpretation."""

    saveQuestionRequested = Signal()
    saveNotesRequested = Signal()
    saveVerificationRequested = Signal()
    favoriteToggled = Signal(bool)

    def __init__(self, ui, parent=None):
        super().__init__(parent)
        self.ui = ui
        self.setObjectName("interpretationRoot")
        self._role = "main"
        self._content_key = "judgment"
        self._narrow = False
        self._side_by_side = True
        self._scroll = None
        self._body = None

        self._build()
        self._wire_presenter_targets()
        self._apply_card_layout(side_by_side=True)
        self._apply_chrome_insets(narrow=False)

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        outer.addWidget(scroll, 1)
        self._scroll = scroll

        body = QWidget()
        body.setObjectName("paperBody")
        scroll.setWidget(body)
        self._body = body
        self._body_layout = QVBoxLayout(body)
        self._body_layout.setContentsMargins(24, 16, 24, 16)
        self._body_layout.setSpacing(12)

        # Question card
        q_card = QFrame()
        q_card.setObjectName("paperCard")
        q_card.setAttribute(Qt.WA_StyledBackground, True)
        q_layout = QVBoxLayout(q_card)
        q_layout.setContentsMargins(14, 12, 14, 12)
        q_layout.setSpacing(8)
        title_row = QHBoxLayout()
        q_title = QLabel("占卜問題")
        q_title.setObjectName("questionCardTitle")
        title_row.addWidget(q_title)
        title_row.addStretch(1)

        self.time_cap = QLabel("占卜時間")
        self.time_cap.setObjectName("metaCaption")
        self.time_value = QLabel("—")
        self.time_value.setObjectName("metaValue")
        self.method_cap = QLabel("占卜方式")
        self.method_cap.setObjectName("metaCaption")
        self.method_value = QLabel("—")
        self.method_value.setObjectName("metaValue")

        self.time_pair = QWidget()
        time_row = QHBoxLayout(self.time_pair)
        time_row.setContentsMargins(0, 0, 0, 0)
        time_row.setSpacing(6)
        time_row.addWidget(self.time_cap)
        time_row.addWidget(self.time_value)

        self.method_pair = QWidget()
        method_row = QHBoxLayout(self.method_pair)
        method_row.setContentsMargins(0, 0, 0, 0)
        method_row.setSpacing(6)
        method_row.addWidget(self.method_cap)
        method_row.addWidget(self.method_value)

        self.meta_wrap = QWidget()
        self.meta_wrap.setObjectName("castMetaWrap")
        title_row.addWidget(self.meta_wrap)
        q_layout.addLayout(title_row)
        self._meta_horizontal = None
        self._apply_meta_layout(horizontal=True)

        row = QHBoxLayout()
        self.ui.editInterpretationQuestion = QLineEdit()
        self.ui.editInterpretationQuestion.setObjectName("editInterpretationQuestion")
        self.ui.editInterpretationQuestion.setPlaceholderText("（未填寫）")
        row.addWidget(self.ui.editInterpretationQuestion, 1)
        self.ui.btnSaveQuestion = QPushButton("儲存問題")
        self.ui.btnSaveQuestion.setObjectName("secondaryButton")
        self.ui.btnSaveQuestion.clicked.connect(self.saveQuestionRequested.emit)
        row.addWidget(self.ui.btnSaveQuestion)
        self.ui.chkFavorite = QCheckBox("收藏")
        self.ui.chkFavorite.setObjectName("styledCheck")
        self.ui.chkFavorite.toggled.connect(self.favoriteToggled.emit)
        row.addWidget(self.ui.chkFavorite)
        q_layout.addLayout(row)
        self._body_layout.addWidget(q_card)

        # Hex cards (layout rebuilt on breakpoint)
        self.cards_wrap = QWidget()
        self.cards_wrap.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_card = HexagramSummaryCard("main", "本卦")
        self.changed_card = HexagramSummaryCard("changed", "變卦")
        self.main_card.clicked.connect(self._on_role_clicked)
        self.changed_card.clicked.connect(self._on_role_clicked)
        self._body_layout.addWidget(self.cards_wrap)

        # Content tabs + viewer
        content_card = QFrame()
        content_card.setObjectName("paperCard")
        content_card.setAttribute(Qt.WA_StyledBackground, True)
        c_layout = QVBoxLayout(content_card)
        c_layout.setContentsMargins(14, 12, 14, 12)
        c_layout.setSpacing(10)
        self.content_tabs = SegmentedTabs()
        self.content_tabs.tabSelected.connect(self._on_content_tab)
        c_layout.addWidget(self.content_tabs)
        self.viewer = ContentViewer(collapsed_lines=18)
        self.viewer.editor.setMinimumHeight(280)
        c_layout.addWidget(self.viewer, 1)
        self._body_layout.addWidget(content_card, 1)

        # Notes — 可折疊，預設摺疊
        notes_content = QWidget()
        n_layout = QVBoxLayout(notes_content)
        n_layout.setContentsMargins(0, 0, 0, 0)
        n_layout.setSpacing(8)
        self.ui.txtNotes = QPlainTextEdit()
        self.ui.txtNotes.setObjectName("notesEditor")
        self.ui.txtNotes.setMinimumHeight(100)
        n_layout.addWidget(self.ui.txtNotes)
        self.ui.btnSaveNotes = QPushButton("儲存心得")
        self.ui.btnSaveNotes.setObjectName("secondaryButton")
        self.ui.btnSaveNotes.clicked.connect(self.saveNotesRequested.emit)
        n_layout.addWidget(self.ui.btnSaveNotes, 0, Qt.AlignRight)

        notes_box = CollapsibleGroupBox("我的心得")
        notes_box.setObjectName("paperCard")
        notes_box.setAttribute(Qt.WA_StyledBackground, True)
        notes_box.setContentWidget(notes_content)
        self._notes_box = notes_box
        self._body_layout.addWidget(notes_box)

        # Verification — 可折疊，預設摺疊
        v_content = QWidget()
        v_layout = QVBoxLayout(v_content)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(8)
        result_row = QHBoxLayout()
        result_row.addWidget(QLabel("驗證結果"))
        self.ui.comboVerificationResult = QComboBox()
        self.ui.comboVerificationResult.setObjectName("styledCombo")
        self.ui.comboVerificationResult.addItems(list(VERIFICATION_RESULTS))
        result_row.addWidget(self.ui.comboVerificationResult, 1)
        v_layout.addLayout(result_row)
        v_layout.addWidget(QLabel("驗證內容"))
        self.ui.txtVerificationContent = QPlainTextEdit()
        self.ui.txtVerificationContent.setObjectName("verificationEditor")
        self.ui.txtVerificationContent.setMinimumHeight(90)
        v_layout.addWidget(self.ui.txtVerificationContent)
        self.ui.btnSaveVerification = QPushButton("儲存驗證")
        self.ui.btnSaveVerification.setObjectName("secondaryButton")
        self.ui.btnSaveVerification.clicked.connect(self.saveVerificationRequested.emit)
        v_layout.addWidget(self.ui.btnSaveVerification, 0, Qt.AlignRight)

        v_box = CollapsibleGroupBox("事後驗證")
        v_box.setObjectName("paperCard")
        v_box.setAttribute(Qt.WA_StyledBackground, True)
        v_box.setContentWidget(v_content)
        self._verification_box = v_box
        self._body_layout.addWidget(v_box)

        self.main_card.set_active(True)
        self._refresh_tabs()

    def _wire_presenter_targets(self):
        """Hidden labels + text stores so HexagramPresenter keeps working."""

        self.ui.lblMainName = QLabel()
        self.ui.lblMainNumber = QLabel()
        self.ui.lblChangedName = QLabel()
        self.ui.lblChangedNumber = QLabel()
        self.ui.lblMovingLines = QLabel()
        for attr in (
            "txtJudgment",
            "txtTuan",
            "txtXiang",
            "txtWenyan",
            "txtTranslation",
            "txtChangedJudgment",
            "txtChangedTuan",
            "txtChangedXiang",
            "txtChangedWenyan",
            "txtChangedTranslation",
            "txtLineTexts",
            "txtChangedLineTexts",
            "txtAIAnalysis",
        ):
            editor = QPlainTextEdit()
            editor.hide()
            setattr(self.ui, attr, editor)

    def mount_into_tab(self, tab: QWidget):
        # Clear designer children
        old = tab.layout()
        if old is not None:
            while old.count():
                item = old.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
        else:
            old = QVBoxLayout(tab)
            old.setContentsMargins(0, 0, 0, 0)
            old.setSpacing(0)
        old.setContentsMargins(0, 0, 0, 0)
        old.setSpacing(0)
        old.addWidget(self)

    def _on_role_clicked(self, role: str):
        kind = _TAB_KIND.get(self._content_key, "judgment")
        self._role = role
        self.main_card.set_active(role == "main")
        self.changed_card.set_active(role == "changed")
        self._content_key = kind if role == "main" else f"changed_{kind}"
        self._refresh_tabs()
        self._sync_viewer()

    def _on_content_tab(self, key: str):
        self._content_key = key
        self._sync_viewer()

    def _refresh_tabs(self):
        if self._role == "main":
            tabs = list(MAIN_TABS)
            default = "judgment"
        else:
            tabs = list(CHANGED_TABS)
            default = "changed_judgment"
        keys = {k for k, _ in tabs}
        active = self._content_key if self._content_key in keys else default
        self.content_tabs.set_tabs(tabs, active=active)
        self._content_key = active

    def _text_for_key(self, key: str) -> str:
        mapping = {
            "judgment": "txtJudgment",
            "tuan": "txtTuan",
            "translation": "txtTranslation",
            "lines": "txtLineTexts",
            "changed_judgment": "txtChangedJudgment",
            "changed_tuan": "txtChangedTuan",
            "changed_translation": "txtChangedTranslation",
            "changed_lines": "txtChangedLineTexts",
        }
        attr = mapping.get(key)
        if not attr:
            return ""
        widget = getattr(self.ui, attr, None)
        if widget is None:
            return ""
        return widget.toPlainText()

    def _sync_viewer(self):
        self.viewer.set_text(self._text_for_key(self._content_key))

    def apply_result_visuals(self, result):
        """Update cards after presenter fills text fields."""

        lines = list(result.lines or [])
        moving = list(result.moving_lines or [])
        changed = changed_lines_from(lines)

        main_name = result.main.title or result.main.name
        changed_name = result.changed.title or result.changed.name
        self.main_card.set_hexagram(result.main.number, main_name, lines, moving)
        self.changed_card.set_hexagram(
            result.changed.number, changed_name, changed, moving
        )

        self.set_cast_meta(
            getattr(result, "datetime", "") or "",
            getattr(result, "cast_method", "") or "",
        )

        self._role = "main"
        self.main_card.set_active(True)
        self.changed_card.set_active(False)
        self._refresh_tabs()
        self._sync_viewer()

    def set_cast_meta(self, time_text: str = "", method_text: str = ""):
        """顯示占卜時間與占卜方式（對齊 Layout 解卦頁資訊列）。"""

        self.time_value.setText(time_text.strip() or "—")
        self.method_value.setText(method_text.strip() or "—")

    def _apply_meta_layout(self, *, horizontal: bool):
        """窄屏垂直堆疊；寬屏時間／方式平行並列。"""

        if self._meta_horizontal is horizontal and self.meta_wrap.layout() is not None:
            return
        self._meta_horizontal = horizontal

        old = self.meta_wrap.layout()
        if old is not None:
            while old.count():
                item = old.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
            QWidget().setLayout(old)

        self.time_pair.setParent(None)
        self.method_pair.setParent(None)

        if horizontal:
            layout = QHBoxLayout(self.meta_wrap)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(28)
            layout.addWidget(self.time_pair)
            layout.addWidget(self.method_pair)
        else:
            layout = QVBoxLayout(self.meta_wrap)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(2)
            layout.addWidget(self.time_pair)
            layout.addWidget(self.method_pair)

    def set_narrow(self, narrow: bool):
        """窄屏：本／變卦並排節省垂直空間；底部留白避免被導航遮住。"""

        changed = self._narrow != narrow
        self._narrow = narrow
        self._apply_meta_layout(horizontal=not narrow)
        if changed or not self._side_by_side:
            # 可用高度不足時並排（不上下堆疊），讓心得／驗證標題露在導航上方
            self._apply_card_layout(side_by_side=True)
        self._apply_compact_cards(compact=narrow)
        self._apply_chrome_insets(narrow=narrow)

    def _apply_chrome_insets(self, *, narrow: bool):
        # 窄屏底欄約 56px；額外留白讓摺疊的心得／驗證可捲出導航上方
        side = 16 if narrow else 24
        top = 12 if narrow else 16
        bottom = 72 if narrow else 16
        self._body_layout.setContentsMargins(side, top, side, bottom)
        self._body_layout.setSpacing(10 if narrow else 12)
        if narrow:
            self.viewer.editor.setMinimumHeight(180)
        else:
            self.viewer.editor.setMinimumHeight(280)

    def _apply_compact_cards(self, *, compact: bool):
        height = 120 if compact else 148
        for card in (self.main_card, self.changed_card):
            card.setMinimumHeight(height)
            if compact:
                card.setMaximumHeight(height + 4)
                card.glyph.setFixedSize(64, 88)
            else:
                card.setMaximumHeight(16777215)
                card.glyph.setFixedSize(88, 120)
            card.glyph.update()

    def _apply_card_layout(self, *, side_by_side: bool):
        self._side_by_side = side_by_side
        old = self.cards_wrap.layout()
        if old is not None:
            while old.count():
                item = old.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
            QWidget().setLayout(old)

        layout = QHBoxLayout(self.cards_wrap)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10 if self._narrow else 12)
        layout.addWidget(self.main_card, 1)
        layout.addWidget(self.changed_card, 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_narrow(self.width() < T.BREAKPOINT_WIDE)
