"""
Project IChing — Data Editor 主視窗
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from core.paths import user_data_dir
from tools.data_editor.store import (
    EDITABLE_FIELDS,
    LEGACY_SOURCE_FIELDS,
    LINE_LABELS,
    HexagramStore,
    parse_folder_texts,
    parse_numbered_text_file,
)


def trigger_windows_voice_typing() -> bool:
    """模擬 Win+H，喚起 Windows 語音輸入。成功送出按鍵回傳 True。"""

    if sys.platform != "win32":
        return False

    import ctypes

    user32 = ctypes.windll.user32
    VK_LWIN = 0x5B
    VK_H = 0x48
    KEYEVENTF_KEYUP = 0x0002

    user32.keybd_event(VK_LWIN, 0, 0, 0)
    user32.keybd_event(VK_H, 0, 0, 0)
    user32.keybd_event(VK_H, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0)
    return True


class ImportDialog(QDialog):
    """依欄位分類一鍵匯入。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("依欄位匯入")
        self.resize(480, 280)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.combo_target = QComboBox()
        for key, label in EDITABLE_FIELDS:
            self.combo_target.addItem(label, key)
        self.combo_target.addItem("爻辭（lines）", "lines")
        form.addRow("目標欄位", self.combo_target)

        self.combo_source_type = QComboBox()
        self.combo_source_type.addItem("現有 JSON 欄位", "json_key")
        self.combo_source_type.addItem("單一文字檔（64 段）", "text_file")
        self.combo_source_type.addItem("資料夾（每卦一檔）", "folder")
        self.combo_source_type.currentIndexChanged.connect(self._sync_source_ui)
        form.addRow("來源類型", self.combo_source_type)

        self.combo_source_key = QComboBox()
        for key, label in LEGACY_SOURCE_FIELDS:
            self.combo_source_key.addItem(label, key)
        form.addRow("來源欄位", self.combo_source_key)

        path_row = QHBoxLayout()
        self.edit_path = QLabel("（未選擇）")
        self.edit_path.setWordWrap(True)
        self.btn_browse = QPushButton("瀏覽…")
        self.btn_browse.clicked.connect(self._browse)
        path_row.addWidget(self.edit_path, 1)
        path_row.addWidget(self.btn_browse)
        form.addRow("來源路徑", path_row)

        self.chk_force = QCheckBox("強制覆蓋已有內容")
        form.addRow("", self.chk_force)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._source_path: Path | None = None
        self._sync_source_ui()

    def _sync_source_ui(self):
        is_key = self.combo_source_type.currentData() == "json_key"
        self.combo_source_key.setEnabled(is_key)
        self.btn_browse.setEnabled(not is_key)
        if is_key:
            self.edit_path.setText("（使用 JSON 現有欄位）")

    def _browse(self):
        source_type = self.combo_source_type.currentData()
        if source_type == "folder":
            path = QFileDialog.getExistingDirectory(self, "選擇資料夾")
            if path:
                self._source_path = Path(path)
                self.edit_path.setText(path)
            return

        path, _ = QFileDialog.getOpenFileName(
            self,
            "選擇文字檔",
            "",
            "Text (*.txt *.md);;All (*.*)",
        )
        if path:
            self._source_path = Path(path)
            self.edit_path.setText(path)

    def values(self):
        return {
            "target": self.combo_target.currentData(),
            "source_type": self.combo_source_type.currentData(),
            "source_key": self.combo_source_key.currentData(),
            "source_path": self._source_path,
            "force": self.chk_force.isChecked(),
        }


class FocusAwarePlainTextEdit(QPlainTextEdit):
    """記住焦點，供語音輸入鎖定目標欄位。"""

    def __init__(self, on_focus=None, parent=None):
        super().__init__(parent)
        self._on_focus = on_focus

    def focusInEvent(self, event):
        if self._on_focus is not None:
            self._on_focus(self)
        super().focusInEvent(event)


class DataEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IChing Data Editor")
        self.resize(1100, 720)

        self.store = HexagramStore()
        self._current_number: int | None = None
        self._dirty = False
        self._last_editor: QPlainTextEdit | None = None

        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)

        toolbar = QHBoxLayout()
        self.lbl_path = QLabel(str(self.store.path))
        self.lbl_path.setTextInteractionFlags(Qt.TextSelectableByMouse)
        toolbar.addWidget(QLabel("資料檔："))
        toolbar.addWidget(self.lbl_path, 1)

        self.btn_reload = QPushButton("重新載入")
        self.btn_reload.clicked.connect(self.reload)
        toolbar.addWidget(self.btn_reload)

        self.btn_save = QPushButton("儲存")
        self.btn_save.clicked.connect(self.save)
        toolbar.addWidget(self.btn_save)

        self.btn_backup = QPushButton("匯出備份")
        self.btn_backup.clicked.connect(self.export_backup)
        toolbar.addWidget(self.btn_backup)

        self.btn_voice = QPushButton("語音輸入")
        self.btn_voice.setToolTip(
            "喚起 Windows 語音輸入（Win+H）。\n"
            "請先在系統安裝「中文（台灣）」語音；也可手動按 Win+H。"
        )
        self.btn_voice.clicked.connect(self.start_voice_input)
        toolbar.addWidget(self.btn_voice)

        self.btn_import = QPushButton("依欄位匯入")
        self.btn_import.clicked.connect(self.open_import)
        toolbar.addWidget(self.btn_import)
        # 暫不使用，保留程式碼方便日後恢復
        self.btn_import.hide()

        self.btn_clear_all = QPushButton("清除全部資訊")
        self.btn_clear_all.setToolTip(
            "一鍵清空全部卦的卦辭、自定義解釋、象傳、文言、白話翻譯與爻辭。\n"
            "不會刪除卦名／上下卦等結構資料。寫入目前資料檔。"
        )
        self.btn_clear_all.clicked.connect(self.clear_all_imported_text)
        toolbar.addWidget(self.btn_clear_all)

        outer.addLayout(toolbar)

        splitter = QSplitter()
        outer.addWidget(splitter, 1)

        self.list_hexagrams = QListWidget()
        self.list_hexagrams.currentItemChanged.connect(self._on_select)
        splitter.addWidget(self.list_hexagrams)

        editor_panel = QWidget()
        editor_layout = QVBoxLayout(editor_panel)
        editor_layout.setContentsMargins(8, 0, 8, 8)

        self.lbl_title = QLabel("請選擇卦")
        editor_layout.addWidget(self.lbl_title)

        self.editors: dict[str, QPlainTextEdit] = {}
        for key, label in EDITABLE_FIELDS:
            editor_layout.addWidget(QLabel(label))
            editor = FocusAwarePlainTextEdit(on_focus=self._remember_editor)
            editor.setMinimumHeight(70)
            editor.textChanged.connect(self._mark_dirty)
            self.editors[key] = editor
            editor_layout.addWidget(editor)

        editor_layout.addWidget(QLabel("爻辭（初爻→上爻）"))
        self.line_editors: list[QPlainTextEdit] = []
        for label in LINE_LABELS:
            editor_layout.addWidget(QLabel(label))
            editor = FocusAwarePlainTextEdit(on_focus=self._remember_editor)
            editor.setMaximumHeight(60)
            editor.textChanged.connect(self._mark_dirty)
            self.line_editors.append(editor)
            editor_layout.addWidget(editor)

        editor_layout.addWidget(QLabel("舊欄對照（唯讀）"))
        self.txt_legacy = QPlainTextEdit()
        self.txt_legacy.setReadOnly(True)
        self.txt_legacy.setMaximumHeight(120)
        editor_layout.addWidget(self.txt_legacy)
        editor_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidget(editor_panel)
        splitter.addWidget(scroll)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage(
            "語音：點欄位後按「語音輸入」或 Win+H（需中文台灣語音套件）"
        )

        self._populate_list()
        if self.list_hexagrams.count():
            self.list_hexagrams.setCurrentRow(0)

    def _remember_editor(self, editor: QPlainTextEdit):
        self._last_editor = editor

    def _mark_dirty(self):
        self._dirty = True

    def _editable_editors(self) -> list[QPlainTextEdit]:
        return list(self.editors.values()) + list(self.line_editors)

    def _focus_voice_target(self) -> QPlainTextEdit | None:
        focused = QApplication.focusWidget()
        if isinstance(focused, QPlainTextEdit) and not focused.isReadOnly():
            if focused in self._editable_editors():
                self._last_editor = focused
                return focused

        if self._last_editor is not None:
            self._last_editor.setFocus(Qt.OtherFocusReason)
            return self._last_editor

        for editor in self._editable_editors():
            editor.setFocus(Qt.OtherFocusReason)
            self._last_editor = editor
            return editor

        return None

    def start_voice_input(self):
        target = self._focus_voice_target()
        if target is None:
            QMessageBox.information(
                self,
                "語音輸入",
                "請先選擇可編輯的欄位。",
            )
            return

        QApplication.processEvents()

        if not trigger_windows_voice_typing():
            QMessageBox.information(
                self,
                "語音輸入",
                "目前僅支援 Windows。\n"
                "請手動按下 Win+H，並確認已安裝「中文（台灣）」語音。",
            )
            return

        self.statusBar().showMessage(
            "已喚起 Windows 語音輸入（Win+H）。請用中文（台灣）開始說話。",
            5000,
        )

    def _populate_list(self):
        self.list_hexagrams.blockSignals(True)
        self.list_hexagrams.clear()
        for number, label in self.store.list_labels():
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, number)
            self.list_hexagrams.addItem(item)
        self.list_hexagrams.blockSignals(False)

    def _on_select(self, current, _previous):
        if current is None:
            return

        if self._dirty and self._current_number is not None:
            self._apply_editors_to_store()

        number = current.data(Qt.UserRole)
        self._load_record(number)

    def _load_record(self, number: int):
        record = self.store.get_by_number(number)
        if record is None:
            return

        self._current_number = number
        name = record.get("name", "")
        self.lbl_title.setText(f"第 {number} 卦　{name}")

        for key, editor in self.editors.items():
            editor.blockSignals(True)
            editor.setPlainText(str(record.get(key, "") or ""))
            editor.blockSignals(False)

        lines = record.get("lines") or []
        for index, editor in enumerate(self.line_editors):
            text = lines[index] if index < len(lines) else ""
            editor.blockSignals(True)
            editor.setPlainText(str(text or ""))
            editor.blockSignals(False)

        legacy_parts = []
        for key in ("description", "fortune", "love", "career", "wealth"):
            value = str(record.get(key, "") or "").strip()
            if value:
                legacy_parts.append(f"【{key}】\n{value}")
        self.txt_legacy.setPlainText("\n\n".join(legacy_parts))

        self._dirty = False

    def _apply_editors_to_store(self):
        if self._current_number is None:
            return

        record = self.store.get_by_number(self._current_number)
        if record is None:
            return

        for key, editor in self.editors.items():
            record[key] = editor.toPlainText()

        record["lines"] = [
            editor.toPlainText().strip()
            for editor in self.line_editors
        ]
        self._dirty = False

    def reload(self):
        if self._dirty:
            reply = QMessageBox.question(
                self,
                "重新載入",
                "有未儲存變更，確定放棄並重新載入？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

        try:
            self.store.load()
        except Exception as error:
            QMessageBox.warning(self, "載入失敗", str(error))
            return

        self._dirty = False
        self.lbl_path.setText(str(self.store.path))
        current = self._current_number
        self._populate_list()
        if current is not None:
            for row in range(self.list_hexagrams.count()):
                item = self.list_hexagrams.item(row)
                if item.data(Qt.UserRole) == current:
                    self.list_hexagrams.setCurrentRow(row)
                    break
        QMessageBox.information(self, "完成", "已重新載入。")

    def save(self):
        self._apply_editors_to_store()
        try:
            self.store.save()
        except Exception as error:
            QMessageBox.warning(self, "儲存失敗", str(error))
            return
        QMessageBox.information(self, "儲存成功", f"已寫入：\n{self.store.path}")

    def export_backup(self):
        self._apply_editors_to_store()
        default = str(user_data_dir() / "hexagrams_backup.json")
        path, _ = QFileDialog.getSaveFileName(
            self,
            "匯出備份",
            default,
            "JSON (*.json)",
        )
        if not path:
            return
        try:
            self.store.export_backup(Path(path))
        except Exception as error:
            QMessageBox.warning(self, "匯出失敗", str(error))
            return
        QMessageBox.information(self, "完成", f"已匯出：\n{path}")

    def clear_all_imported_text(self):
        reply = QMessageBox.warning(
            self,
            "清除全部資訊",
            "將清空全部 64 卦的卦辭、自定義解釋、象傳、文言、白話翻譯與爻辭，"
            "並立即寫入資料檔。\n\n"
            f"資料檔：\n{self.store.path}\n\n"
            "此操作無法復原（建議先「匯出備份」）。確定繼續？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        self._apply_editors_to_store()
        try:
            affected = self.store.clear_imported_text()
            self.store.save()
        except Exception as error:
            QMessageBox.warning(self, "清除失敗", str(error))
            return

        if self._current_number is not None:
            self._load_record(self._current_number)
        else:
            self._dirty = False

        QMessageBox.information(
            self,
            "清除完成",
            f"已清空 {affected} 卦的匯入文字，並寫入：\n{self.store.path}",
        )

    def open_import(self):
        dialog = ImportDialog(self)
        if dialog.exec() != QDialog.Accepted:
            return

        values = dialog.values()
        self._apply_editors_to_store()

        target = values["target"]
        force = values["force"]
        source_type = values["source_type"]

        try:
            if source_type == "json_key":
                written, skipped = self.store.import_field_from_key(
                    values["source_key"],
                    target,
                    force=force,
                )
            elif source_type == "text_file":
                path = values["source_path"]
                if path is None:
                    QMessageBox.warning(self, "匯入", "請先選擇文字檔。")
                    return
                texts = parse_numbered_text_file(path)
                written, skipped = self.store.import_field_from_texts(
                    texts,
                    target,
                    force=force,
                )
            else:
                path = values["source_path"]
                if path is None:
                    QMessageBox.warning(self, "匯入", "請先選擇資料夾。")
                    return
                texts = parse_folder_texts(path)
                written, skipped = self.store.import_field_from_texts(
                    texts,
                    target,
                    force=force,
                )
        except Exception as error:
            QMessageBox.warning(self, "匯入失敗", str(error))
            return

        if self._current_number is not None:
            self._load_record(self._current_number)

        reply = QMessageBox.question(
            self,
            "匯入完成",
            f"已寫入 {written} 卦，略過 {skipped} 卦。\n是否立即儲存到檔案？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        if reply == QMessageBox.Yes:
            self.save()
        else:
            self._dirty = True
