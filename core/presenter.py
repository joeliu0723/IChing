from core.result import HexagramResult


LINE_LABELS = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]


class HexagramPresenter:

    def __init__(self, ui):
        self.ui = ui

    def show(self, result: HexagramResult):

        # ===== 問題 =====
        if hasattr(self.ui, "lblQuestion"):
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

        # ===== 爻辭 =====
        self._set_text("txtLineTexts", self._format_line_texts(result))

        # ===== 心得（僅顯示，V1.4 再編輯） =====
        if hasattr(self.ui, "txtNotes"):
            self.ui.txtNotes.setPlainText(result.notes)

    def _set_text(self, attr, text):
        if hasattr(self.ui, attr):
            getattr(self.ui, attr).setPlainText(text or "")

    def _format_line_texts(self, result: HexagramResult) -> str:
        moving = set(result.moving_lines)
        parts = []
        has_yao_text = False

        for index, label in enumerate(LINE_LABELS, start=1):
            prefix = "【動爻】" if index in moving else ""
            yao_type = ""

            if index - 1 < len(result.lines):
                yao_type = result.lines[index - 1]

            yao_text = result.main.line_text(index)

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
