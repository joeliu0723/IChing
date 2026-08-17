from core.result import HexagramResult


LINE_LABELS = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]

_LINE_FLIP = {
    "少陽": "少陽",
    "少陰": "少陰",
    "老陽": "少陰",
    "老陰": "少陽",
}


def _changed_line_types(lines):
    return [_LINE_FLIP.get(line, line) for line in (lines or [])]


class HexagramPresenter:

    def __init__(self, ui):
        self.ui = ui

    def show(self, result: HexagramResult):

        # ===== 問題（解卦頁可編輯欄位由 MainWindow 同步） =====
        if hasattr(self.ui, "editInterpretationQuestion"):
            self.ui.editInterpretationQuestion.setText(result.question)
        elif hasattr(self.ui, "lblQuestion"):
            question = result.question.strip()
            if question:
                self.ui.lblQuestion.setText(f"占卜問題：{question}")
            else:
                self.ui.lblQuestion.setText("占卜問題：（未填寫）")

        # ===== 本卦 =====
        self.ui.lblMainNumber.setText(f"第 {result.main.number} 卦")
        self.ui.lblMainName.setText(result.main.title)

        # ===== 變卦 =====
        self.ui.lblChangedNumber.setText(f"第 {result.changed.number} 卦")
        self.ui.lblChangedName.setText(result.changed.title)

        # ===== 動爻 =====
        if result.moving_lines:
            self.ui.lblMovingLines.setText(
                "、".join(str(i) for i in result.moving_lines)
            )
        else:
            self.ui.lblMovingLines.setText("無")

        # ===== 本卦經文 =====
        self._set_text("txtJudgment", result.main.gua_text)
        self._set_text("txtTuan", result.main.tuan)
        self._set_text("txtXiang", result.main.xiang)
        self._set_text("txtWenyan", result.main.wenyan)
        self._set_text("txtTranslation", result.main.translation)

        # ===== 變卦經文 =====
        self._set_text("txtChangedJudgment", result.changed.gua_text)
        self._set_text("txtChangedTuan", result.changed.tuan)
        self._set_text("txtChangedXiang", result.changed.xiang)
        self._set_text("txtChangedWenyan", result.changed.wenyan)
        self._set_text("txtChangedTranslation", result.changed.translation)

        # ===== 爻辭 =====
        self._set_text("txtLineTexts", self._format_line_texts(result, result.main, result.lines))
        self._set_text(
            "txtChangedLineTexts",
            self._format_line_texts(
                result,
                result.changed,
                _changed_line_types(result.lines),
                mark_moving=False,
            ),
        )

        # ===== 心得 =====
        if hasattr(self.ui, "txtNotes"):
            self.ui.txtNotes.setPlainText(result.notes)

    def _set_text(self, attr, text):
        if hasattr(self.ui, attr):
            getattr(self.ui, attr).setPlainText(text or "")

    def _format_line_texts(self, result: HexagramResult, info, line_types, *, mark_moving: bool = True) -> str:
        moving = set(result.moving_lines) if mark_moving else set()
        parts = []
        has_yao_text = False
        types = list(line_types or [])

        for index, label in enumerate(LINE_LABELS, start=1):
            prefix = "【動爻】" if index in moving else ""
            yao_type = types[index - 1] if index - 1 < len(types) else ""
            yao_text = info.line_text(index) if info is not None else ""

            if yao_text:
                has_yao_text = True

            if yao_type and yao_text:
                parts.append(f"{prefix}{label}（{yao_type}）\n{yao_text}")
            elif yao_type:
                parts.append(f"{prefix}{label}（{yao_type}）")
            elif yao_text:
                parts.append(f"{prefix}{label}\n{yao_text}")

        if not parts:
            return ""

        if not has_yao_text:
            parts.append("（目前資料庫尚無爻辭原文，以上僅顯示各爻陰陽與動爻標記。）")

        return "\n\n".join(parts)
