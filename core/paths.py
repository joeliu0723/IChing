"""
Project IChing — 資料路徑

開發：專案根目錄 data/
打包後：%APPDATA%\\IChing\\data\\（首次從安裝目錄預設檔複製）
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

APP_NAME = "IChing"
HEXAGRAMS_FILENAME = "hexagrams.json"
HISTORY_FILENAME = "history.json"


def project_root() -> Path:
    """開發時的專案根目錄。"""

    return Path(__file__).resolve().parent.parent


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def resource_root() -> Path:
    """開發時為專案根目錄；打包後為 PyInstaller _MEIPASS。"""

    if is_frozen():
        return Path(sys._MEIPASS)

    return project_root()


def bundled_data_dir() -> Path:
    """
    內建唯讀預設資料目錄。

    開發：專案 data/
    PyInstaller：_MEIPASS/data/
    """

    return resource_root() / "data"


def assets_ui_dir() -> Path:
    """UI 圖檔／SVG（Hero、飾線）。"""

    return resource_root() / "assets" / "ui"


def user_data_dir() -> Path:
    """可寫入的使用者資料目錄。"""

    if is_frozen():
        base = os.environ.get("APPDATA") or str(Path.home())
        path = Path(base) / APP_NAME / "data"
    else:
        path = project_root() / "data"

    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_user_file(filename: str) -> Path:
    """
    確保使用者目錄有指定檔案。

    若不存在且安裝包有預設檔，則複製過去。
    """

    target = user_data_dir() / filename

    if target.exists():
        return target

    source = bundled_data_dir() / filename

    if source.exists():
        shutil.copy2(source, target)

    return target


def hexagrams_path() -> Path:
    """hexagrams.json 可讀寫路徑。"""

    return ensure_user_file(HEXAGRAMS_FILENAME)


def history_path() -> Path:
    """history.json 可讀寫路徑（不強制從內建複製）。"""

    path = user_data_dir() / HISTORY_FILENAME
    return path


def export_backup_path(filename: str) -> Path:
    """匯出備份建議路徑（使用者資料目錄）。"""

    return user_data_dir() / filename
