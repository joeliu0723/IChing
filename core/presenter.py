from core.result import HexagramResult


class HexagramPresenter:

    def __init__(self, ui):
        self.ui = ui

    def show(self, result: HexagramResult):

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

        # ===== 卦辭 =====
        if hasattr(self.ui, "txtJudgment"):
            self.ui.txtJudgment.setPlainText(result.main.gua_text)

        # ===== 彖傳 =====
        if hasattr(self.ui, "txtTuan"):
            self.ui.txtTuan.setPlainText(result.main.tuan)

        # ===== 象傳 =====
        if hasattr(self.ui, "txtXiang"):
            self.ui.txtXiang.setPlainText(result.main.xiang)

        # ===== 文言 =====
        if hasattr(self.ui, "txtWenyan"):
            self.ui.txtWenyan.setPlainText(result.main.wenyan)

        # ===== 白話翻譯 =====
        if hasattr(self.ui, "txtTranslation"):
            self.ui.txtTranslation.setPlainText(result.main.translation)