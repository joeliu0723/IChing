"""Application stylesheet assembled from shared tokens."""

from ui.theme import tokens as T


def build_app_stylesheet() -> str:
    return f"""
QMainWindow, QWidget#castHomeRoot, QWidget#castHomeBody, QWidget#tabDivination,
QWidget#tab_interpretation, QWidget#tab_history,
QWidget#interpretationRoot, QWidget#historyRoot, QWidget#paperBody {{
    background-color: {T.PAPER};
    color: {T.INK};
}}
QTabWidget::pane {{
    border: none;
    top: 0px;
    background-color: {T.PAPER};
}}
QWidget#brandHero {{
    background-color: {T.NAVY};
    border: none;
}}
QLabel#brandHeroTitleZh, QLabel#brandHeroTitleEn {{
    color: {T.GOLD};
    background: transparent;
}}
QLabel#brandHeroTitleEn {{
    letter-spacing: 4px;
}}
QWidget#modeSelector QPushButton#modeSelectButton,
QWidget#segmentedTabs QPushButton#segmentTab {{
    background-color: {T.PAPER};
    color: {T.INK};
    border: 1px solid {T.BORDER};
    border-radius: {T.RADIUS_PILL}px;
    padding: 0px 8px;
    font-size: 15px;
    font-weight: 500;
}}
QWidget#modeSelector QPushButton#modeSelectButton:hover:!checked,
QWidget#segmentedTabs QPushButton#segmentTab:hover:!checked {{
    background-color: {T.PAPER_SOFT};
    border: 1px solid {T.GOLD};
}}
QWidget#modeSelector QPushButton#modeSelectButton:checked,
QWidget#segmentedTabs QPushButton#segmentTab:checked {{
    background-color: {T.NAVY};
    color: {T.IVORY};
    border: 1px solid {T.GOLD};
    font-weight: 600;
}}
QFrame#questionCard, QFrame#paperCard, QFrame#historyToolbar {{
    background-color: {T.PAPER_WARM};
    border: 1px solid {T.BORDER};
    border-radius: {T.RADIUS_CARD}px;
}}
QFrame#paperCard QToolButton#collapseToggle {{
    background: transparent;
    border: none;
    color: {T.NAVY};
    font-size: 16px;
    font-weight: 600;
    padding: 10px 12px;
    text-align: left;
}}
QFrame#paperCard QToolButton#collapseToggle:hover {{
    color: {T.GOLD};
}}
QFrame#inputCard {{
    background-color: {T.PAPER};
    border: 1px solid {T.BORDER_SOFT};
    border-radius: {T.RADIUS_CARD}px;
}}
QFrame#hexCard {{
    background-color: {T.PAPER};
    border: 1px solid {T.BORDER};
    border-radius: {T.RADIUS_CARD}px;
}}
QFrame#hexCard[active="true"] {{
    border: 1px solid {T.GOLD};
    background-color: {T.PAPER_WARM};
}}
QLabel#sectionLabel, QLabel#inputCardTitle, QLabel#cardTitle, QLabel#fieldLabel {{
    color: {T.INK};
    font-size: 15px;
    font-weight: 600;
    background: transparent;
}}
QLabel#questionCardTitle, QLabel#hexCardTitle {{
    color: {T.NAVY};
    font-size: 16px;
    font-weight: 600;
    background: transparent;
}}
QLabel#inputCardTitle {{
    font-size: 17px;
    color: {T.INK};
    qproperty-alignment: AlignCenter;
}}
QLabel#lineRowLabel, QLabel#metaLabel, QLabel#mutedLabel {{
    color: {T.INK};
    font-size: 15px;
    font-weight: 600;
    background: transparent;
}}
QLabel#mutedLabel {{
    color: {T.INK_MUTED};
    font-weight: 400;
}}
QLabel#metaCaption {{
    color: {T.INK_MUTED};
    font-size: 13px;
    font-weight: 600;
}}
QLabel#metaValue {{
    color: {T.INK};
    font-size: 14px;
    font-weight: 500;
}}
QLabel#historyColCaption {{
    color: {T.INK_MUTED};
    font-size: 12px;
    font-weight: 600;
}}
QLabel#historyTimeValue {{
    color: {T.INK};
    font-size: 14px;
    font-weight: 600;
}}
QLabel#historyHexName {{
    color: {T.INK};
    font-size: 14px;
    font-weight: 600;
}}
QLabel#historyQuestion {{
    color: {T.INK};
    font-size: 15px;
}}
QListWidget#historyList {{
    background: transparent;
    border: none;
    outline: none;
}}
QListWidget#historyList::item {{
    margin: 0px;
    padding: 0px;
}}
QToolButton#historyFavButton {{
    border: none;
    background: transparent;
    padding: 2px;
}}
QPushButton#historyVerifyButton {{
    border: none;
    background: transparent;
    padding: 0px;
}}
QLabel#hexCardName {{
    color: {T.NAVY};
    font-size: 20px;
    font-weight: 700;
    background: transparent;
}}
QLabel#hexCardNumber {{
    color: {T.NAVY};
    font-size: 14px;
    font-weight: 600;
    background: transparent;
}}
QLineEdit#editQuestionHome, QLineEdit#styledLineEdit, QLineEdit#editInterpretationQuestion,
QLineEdit#historySearch {{
    background-color: {T.PAPER};
    border: 1px solid {T.BORDER};
    border-radius: {T.RADIUS_CONTROL}px;
    padding: 0px 16px;
    font-size: 15px;
    min-height: 40px;
    color: {T.NAVY};
    selection-background-color: {T.NAVY};
    selection-color: {T.IVORY};
}}
QLineEdit#editQuestionHome {{
    min-height: 54px;
    max-height: 54px;
}}
QLineEdit#editQuestionHome::placeholder, QLineEdit#styledLineEdit::placeholder,
QLineEdit#editInterpretationQuestion::placeholder, QLineEdit#historySearch::placeholder {{
    color: {T.INK_MUTED};
}}
QLineEdit#editQuestionHome:focus, QLineEdit#styledLineEdit:focus,
QLineEdit#editInterpretationQuestion:focus, QLineEdit#historySearch:focus {{
    border: 1px solid {T.GOLD};
    background-color: {T.PAPER};
    outline: none;
}}
QLineEdit#editQuestionHome:hover:!focus, QLineEdit#styledLineEdit:hover:!focus,
QLineEdit#editInterpretationQuestion:hover:!focus, QLineEdit#historySearch:hover:!focus {{
    border: 1px solid {T.BORDER_SOFT};
}}
QPushButton#btnStartInterpretation {{
    background-color: transparent;
    border: none;
    padding: 0px 24px;
    font-size: 18px;
    font-weight: 700;
    min-height: 52px;
    max-height: 52px;
    color: {T.IVORY};
}}
QPushButton#btnStartInterpretation:focus {{
    outline: none;
}}
QPushButton#secondaryButton, QPushButton#historyActionButton {{
    background-color: {T.PAPER};
    color: {T.NAVY};
    border: 1px solid {T.GOLD};
    border-radius: {T.RADIUS_CONTROL}px;
    padding: 6px 14px;
    font-size: 15px;
    font-weight: 600;
    min-height: 34px;
}}
QPushButton#secondaryButton:hover, QPushButton#historyActionButton:hover {{
    background-color: {T.PAPER_SOFT};
    border: 1px solid {T.GOLD_BRIGHT};
}}
QPushButton#secondaryButton:pressed, QPushButton#historyActionButton:pressed {{
    background-color: {T.PAPER_WARM};
}}
QPushButton#primaryNavButton {{
    background-color: {T.NAVY};
    color: {T.IVORY};
    border: 1px solid {T.GOLD};
    border-radius: {T.RADIUS_CONTROL}px;
    padding: 8px 16px;
    font-size: 15px;
    font-weight: 700;
    min-height: 40px;
}}
QPushButton#primaryNavButton:hover {{
    background-color: {T.NAVY_HOVER};
    border: 1px solid {T.GOLD_BRIGHT};
}}
QPlainTextEdit#contentViewer, QPlainTextEdit#notesEditor, QPlainTextEdit#verificationEditor {{
    background-color: {T.PAPER};
    color: {T.INK};
    border: 1px solid {T.BORDER};
    border-radius: {T.RADIUS_CONTROL}px;
    padding: 10px;
    font-size: 15px;
}}
QPlainTextEdit#contentViewer {{
    font-size: 16px;
}}
QTabBar {{
    background: {T.NAVY};
    border: none;
}}
QTabBar::tab {{
    background: transparent;
    color: {T.BORDER};
    padding: 8px 18px;
    margin-right: 0px;
    border: none;
    border-right: 1px solid rgba(201, 184, 150, 0.35);
    min-width: 88px;
    font-size: 15px;
    font-weight: 500;
}}
QTabBar::tab:selected {{
    background: rgba(212, 175, 55, 0.12);
    color: {T.GOLD};
    font-size: 15px;
    font-weight: 700;
}}
QTabBar::tab:hover:!selected {{
    color: {T.GOLD_BRIGHT};
}}
QTabBar::tab:last {{
    border-right: none;
}}
QGroupBox#groupLinesInput {{
    border: none;
    margin-top: 0px;
    background: transparent;
}}
QGroupBox#groupLinesInput::title {{
    height: 0px;
    width: 0px;
    color: transparent;
}}
QWidget#sixLinesBody QPushButton#yaoOption {{
    background-color: {T.PAPER_SOFT};
    color: {T.INK};
    border: 1px solid {T.BORDER};
    border-radius: 5px;
    padding: 0px 14px 0px 12px;
    font-size: 15px;
    font-weight: 500;
    min-height: 40px;
    max-height: 40px;
    min-width: 96px;
}}
QWidget#sixLinesBody QPushButton#yaoOption:hover:!checked {{
    background-color: #EDE4D0;
    border: 1px solid {T.GOLD};
    color: {T.INK};
}}
QWidget#sixLinesBody QPushButton#yaoOption:checked {{
    background-color: {T.NAVY};
    color: {T.IVORY};
    border: 1px solid {T.GOLD};
    font-weight: 600;
}}
QWidget#sixLinesBody QPushButton#yaoOption:checked:hover {{
    background-color: {T.NAVY_HOVER};
    color: {T.IVORY};
    border: 1px solid {T.GOLD_BRIGHT};
}}
QWidget#sixLinesBody QPushButton#yaoOption:pressed,
QWidget#sixLinesBody QPushButton#yaoOption:checked:pressed {{
    background-color: {T.NAVY_PRESSED};
    color: {T.IVORY};
}}
QWidget#sixLinesBody QPushButton#yaoOption:focus {{
    outline: none;
}}
QWidget#modeInputBody {{
    background: transparent;
}}
QWidget#modeInputBody QLabel#fieldLabel {{
    color: {T.INK};
    font-size: 15px;
    font-weight: 600;
    background: transparent;
}}
QWidget#modeInputBody QLabel#sectionHint {{
    color: {T.INK_MUTED};
    font-size: 14px;
    font-weight: 400;
    background: transparent;
}}
QWidget#modeInputBody QComboBox#modeInputControl,
QWidget#modeInputBody QSpinBox#modeInputControl,
QComboBox#styledCombo {{
    background-color: {T.PAPER};
    color: {T.INK};
    border: 1px solid {T.BORDER};
    border-radius: 5px;
    padding: 0px 10px;
    font-size: 15px;
    font-weight: 500;
    min-height: 34px;
    selection-background-color: {T.PAPER_WARM};
    selection-color: {T.INK};
}}
QWidget#modeInputBody QComboBox#modeInputControl:hover,
QWidget#modeInputBody QSpinBox#modeInputControl:hover,
QComboBox#styledCombo:hover {{
    background-color: {T.PAPER_SOFT};
    border: 1px solid {T.GOLD};
}}
QWidget#modeInputBody QComboBox#modeInputControl:focus,
QWidget#modeInputBody QSpinBox#modeInputControl:focus,
QComboBox#styledCombo:focus,
QWidget#modeInputBody QComboBox#modeInputControl:on,
QComboBox#styledCombo:on {{
    border: 1px solid {T.GOLD};
    background-color: {T.PAPER_WARM};
    outline: none;
}}
QWidget#modeInputBody QComboBox#modeInputControl QAbstractItemView,
QComboBox#styledCombo QAbstractItemView {{
    background-color: {T.PAPER};
    color: {T.INK};
    border: 1px solid {T.BORDER};
    outline: none;
    selection-background-color: {T.PAPER_WARM};
    selection-color: {T.INK};
}}
QWidget#modeInputBody QComboBox#modeInputControl::drop-down,
QComboBox#styledCombo::drop-down {{
    border: none;
    width: 22px;
    background: transparent;
}}
QWidget#modeInputBody QSpinBox#modeInputControl::up-button,
QWidget#modeInputBody QSpinBox#modeInputControl::down-button {{
    width: 18px;
    border: none;
    background: transparent;
}}
QGroupBox {{
    background: transparent;
    border: none;
    margin-top: 4px;
    font-weight: 600;
    color: {T.INK};
}}
QListWidget#historyList {{
    background-color: {T.PAPER};
    border: 1px solid {T.BORDER};
    border-radius: {T.RADIUS_CARD}px;
    padding: 4px;
    outline: none;
}}
QListWidget#historyList::item {{
    border: none;
    margin: 4px 2px;
    padding: 0px;
}}
QListWidget#historyList::item:selected {{
    background: transparent;
}}
QWidget#historyRecordRow {{
    background-color: {T.PAPER};
    border: 1px solid {T.BORDER};
    border-radius: 6px;
}}
QWidget#historyRecordRow[selected="true"] {{
    border: 1px solid {T.GOLD};
    background-color: {T.PAPER_WARM};
}}
QLabel#verificationBadge {{
    color: {T.NAVY};
    background-color: {T.PAPER_SOFT};
    border: 1px solid {T.GOLD};
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 13px;
    font-weight: 600;
}}
QLabel#verificationBadge[tone="warn"] {{
    color: {T.WARNING};
    border: 1px solid {T.WARNING};
}}
QWidget#appNavBar {{
    background-color: {T.NAVY};
    border-top: 1px solid {T.GOLD};
}}
QFrame#appNavSep {{
    background-color: rgba(201, 184, 150, 0.35);
    border: none;
    max-width: 1px;
    margin: 10px 0px;
}}
QWidget#appNavBar QToolButton#appNavButton {{
    background: transparent;
    color: {T.BORDER};
    border: none;
    border-radius: 4px;
    padding: 4px 2px;
    font-size: 13px;
    font-weight: 500;
}}
QWidget#appNavBar QToolButton#appNavButton:checked {{
    color: {T.GOLD};
    font-size: 13px;
    font-weight: 700;
}}
QWidget#appNavBar QToolButton#appNavButton:hover {{
    color: {T.GOLD_BRIGHT};
}}
QCheckBox#styledCheck {{
    color: {T.INK};
    spacing: 8px;
}}

QPushButton#fontSizeButton {{
    background-color: {T.PAPER};
    color: {T.INK};
    border: 1px solid {T.BORDER};
    border-radius: {T.RADIUS_CONTROL}px;
    padding: 0px 10px;
    font-size: 15px;
    font-weight: 500;
    min-height: 30px;
    max-height: 30px;
}}
QPushButton#fontSizeButton:hover:!checked {{
    background-color: {T.PAPER_SOFT};
    border: 1px solid {T.GOLD};
}}
QPushButton#fontSizeButton:checked {{
    background-color: {T.NAVY};
    color: {T.IVORY};
    border: 1px solid {T.GOLD};
    font-weight: 600;
}}
"""
