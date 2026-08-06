"""
Project IChing — Data Editor 啟動入口
"""

import sys
from pathlib import Path

# 允許直接 python tools/data_editor/main.py
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PySide6.QtWidgets import QApplication

from tools.data_editor.main_window import DataEditorWindow


def run():
    app = QApplication(sys.argv)
    window = DataEditorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
