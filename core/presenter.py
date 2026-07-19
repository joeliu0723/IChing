"""
==================================================
Project IChing
File : core/presenter.py
Version : V1.0.0
==================================================
"""

from core.result import HexagramResult


class HexagramPresenter:

    def __init__(self, ui):

        self.ui = ui

    def show(self, result: HexagramResult):

        # 本卦
        self.ui.lblMainNumber.setText(
            f"第 {result.main.number} 卦"
        )

        self.ui.lblMainName.setText(
            result.main.title
        )

        # 變卦
        self.ui.lblChangedNumber.setText(
            f"第 {result.changed.number} 卦"
        )

        self.ui.lblChangedName.setText(
            result.changed.title
        )

        # 動爻
        if result.moving_lines:

            text = "、".join(
                str(i) for i in result.moving_lines
            )

        else:

            text = "無"

        self.ui.lblMovingLines.setText(text)