"""
Project IChing — Data Editor

編輯 64 卦解卦資料（hexagrams.json）。
"""

from __future__ import annotations

import json
import re
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any

from core.paths import hexagrams_path, user_data_dir


EDITABLE_FIELDS = (
    ("gua_text", "卦辭"),
    ("tuan", "自定義解釋"),
    ("xiang", "象傳"),
    ("wenyan", "文言"),
    ("translation", "白話翻譯"),
)

LEGACY_SOURCE_FIELDS = (
    ("description", "description（舊說明）"),
    ("fortune", "fortune"),
    ("love", "love"),
    ("career", "career"),
    ("wealth", "wealth"),
    ("gua_text", "gua_text"),
    ("tuan", "tuan"),
    ("xiang", "xiang"),
    ("wenyan", "wenyan"),
    ("translation", "translation"),
)

LINE_LABELS = ("初爻", "二爻", "三爻", "四爻", "五爻", "上爻")


class HexagramStore:
    """載入／儲存／匯入 hexagrams.json。"""

    def __init__(self, path: Path | None = None):
        self.path = path or hexagrams_path()
        self.records: list[dict[str, Any]] = []
        self.load()

    def load(self) -> None:
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            entries = data.get("value", [])
        elif isinstance(data, list):
            entries = data
        else:
            entries = []

        self.records = [
            entry for entry in entries if isinstance(entry, dict)
        ]
        self.records.sort(key=lambda item: item.get("number", 0))
        self._ensure_shape()

    def _ensure_shape(self) -> None:
        for record in self.records:
            for key, _label in EDITABLE_FIELDS:
                record.setdefault(key, "")

            lines = record.get("lines")
            if not isinstance(lines, list):
                lines = []
            while len(lines) < 6:
                lines.append("")
            record["lines"] = [str(item or "") for item in lines[:6]]

    def save(self) -> None:
        self._ensure_shape()
        payload = sorted(
            self.records,
            key=lambda item: item.get("number", 0),
        )
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(
                payload,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def export_backup(self, target: Path) -> None:
        self.save()
        shutil.copy2(self.path, target)

    def get_by_number(self, number: int) -> dict[str, Any] | None:
        for record in self.records:
            if record.get("number") == number:
                return record
        return None

    def list_labels(self) -> list[tuple[int, str]]:
        labels = []
        for record in self.records:
            number = int(record.get("number", 0))
            name = str(record.get("name", "")).strip() or "-"
            labels.append((number, f"{number:02d}. {name}"))
        return labels

    def import_field_from_key(
        self,
        source_key: str,
        target_key: str,
        *,
        force: bool = False,
    ) -> tuple[int, int]:
        """從現有 JSON 鍵匯入到目標欄位。回傳 (寫入數, 略過數)。"""

        written = 0
        skipped = 0

        for record in self.records:
            source_value = record.get(source_key, "")
            if isinstance(source_value, list):
                text = "\n".join(str(item) for item in source_value)
            else:
                text = str(source_value or "").strip()

            if not text:
                skipped += 1
                continue

            if target_key == "lines":
                current = record.get("lines") or []
                has_content = any(str(item).strip() for item in current)
                if has_content and not force:
                    skipped += 1
                    continue
                parts = _split_line_parts(text)
                record["lines"] = parts
                written += 1
                continue

            current = str(record.get(target_key, "") or "").strip()
            if current and not force:
                skipped += 1
                continue

            record[target_key] = text
            written += 1

        return written, skipped

    def import_field_from_texts(
        self,
        texts_by_number: dict[int, str],
        target_key: str,
        *,
        force: bool = False,
    ) -> tuple[int, int]:
        """依卦序對應文字匯入。回傳 (寫入數, 略過數)。"""

        written = 0
        skipped = 0

        for record in self.records:
            number = int(record.get("number", 0))
            text = (texts_by_number.get(number) or "").strip()
            if not text:
                skipped += 1
                continue

            if target_key == "lines":
                current = record.get("lines") or []
                has_content = any(str(item).strip() for item in current)
                if has_content and not force:
                    skipped += 1
                    continue
                record["lines"] = _split_line_parts(text)
                written += 1
                continue

            current = str(record.get(target_key, "") or "").strip()
            if current and not force:
                skipped += 1
                continue

            record[target_key] = text
            written += 1

        return written, skipped

    def clear_imported_text(self) -> int:
        """
        清除全部可匯入文字欄位（卦辭、自定義解釋、象傳、文言、白話、爻辭）。

        保留卦序、卦名、上下卦等結構欄位。回傳受影響的卦數。
        """

        affected = 0
        for record in self.records:
            changed = False
            for key, _label in EDITABLE_FIELDS:
                if str(record.get(key, "") or "").strip():
                    changed = True
                record[key] = ""

            lines = record.get("lines")
            if isinstance(lines, list) and any(str(item or "").strip() for item in lines):
                changed = True
            record["lines"] = [""] * 6

            if changed:
                affected += 1

        return affected


def _split_line_parts(text: str) -> list[str]:
    """將文字拆成六段爻辭。"""

    raw = text.strip()
    if not raw:
        return [""] * 6

    # 以空行分隔優先
    blocks = [block.strip() for block in re.split(r"\n\s*\n", raw) if block.strip()]
    if len(blocks) == 6:
        return blocks

    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if len(lines) >= 6:
        return lines[:6]

    while len(lines) < 6:
        lines.append("")
    return lines


def parse_numbered_text_file(path: Path) -> dict[int, str]:
    """
    解析單一文字檔。

    支援：
    - 以 === 01 === 或 【1】 或 # 1 分隔的 64 段
    - 或以連續空行分成最多 64 段（依序對應 1..n）
    """

    content = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(?m)^\s*(?:===?\s*(\d{1,2})\s*===?|【\s*(\d{1,2})\s*】|#\s*(\d{1,2}))\s*$"
    )
    matches = list(pattern.finditer(content))

    result: dict[int, str] = {}

    if matches:
        for index, match in enumerate(matches):
            number = int(next(group for group in match.groups() if group))
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
            result[number] = content[start:end].strip()
        return result

    blocks = [block.strip() for block in re.split(r"\n\s*\n", content) if block.strip()]
    for index, block in enumerate(blocks[:64], start=1):
        result[index] = block
    return result


def parse_folder_texts(folder: Path) -> dict[int, str]:
    """資料夾內每卦一檔：1.txt / 01.txt / 01_乾.txt。"""

    result: dict[int, str] = {}

    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        match = re.match(r"^(\d{1,2})", path.stem)
        if not match:
            continue
        number = int(match.group(1))
        if 1 <= number <= 64:
            result[number] = path.read_text(encoding="utf-8").strip()

    return result


def deep_copy_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return deepcopy(records)
