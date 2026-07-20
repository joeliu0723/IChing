
from core.result import HexagramResult


class HexagramPresenter:

    def __init__(self, ui):
        self.ui = ui

    def show(self, result: HexagramResult):

        self.ui.lblMainNumber.setText(f"第 {result.main.number} 卦")
        self.ui.lblMainName.setText(result.main.title)

        self.ui.lblChangedNumber.setText(f"第 {result.changed.number} 卦")
        self.ui.lblChangedName.setText(result.changed.title)

        if result.moving_lines:
            self.ui.lblMovingLines.setText("、".join(str(i) for i in result.moving_lines))
        else:
            self.ui.lblMovingLines.setText("無")

        # Optional interpretation controls
        if hasattr(self.ui, "txtJudgment"):
            self.ui.txtJudgment.setPlainText(getattr(result.main, "judgment", ""))

        if hasattr(self.ui, "txtTuan"):
            self.ui.txtTuan.setPlainText(getattr(result.main, "tuan", ""))

        if hasattr(self.ui, "txtXiang"):
            self.ui.txtXiang.setPlainText(getattr(result.main, "xiang", ""))

        if hasattr(self.ui, "txtWenyan"):
            self.ui.txtWenyan.setPlainText(getattr(result.main, "wenyan", ""))

        if hasattr(self.ui, "txtTranslation"):
            self.ui.txtTranslation.setPlainText(getattr(result.main, "translation", ""))
