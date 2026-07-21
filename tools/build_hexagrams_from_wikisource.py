"""
Project IChing - 建立易經資料庫工具
用途：
1. 讀取 data/hexagrams.json 的既有 64 卦結構
2. 從維基文庫的 MediaWiki API 下載各卦原文頁面
3. 依常見段落標記嘗試拆分為：
   gua_text / tuan / xiang / wenyan
4. 保留現有 title、上下卦、notes 欄位
5. 產生 data/hexagrams.generated.json，不覆蓋原檔

執行：
    python tools/build_hexagrams_from_wikisource.py
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

import requests

API_URL = "https://zh.wikisource.org/w/api.php"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "hexagrams.json"
OUTPUT_PATH = PROJECT_ROOT / "data" / "hexagrams.generated.json"

HEADERS = {
    "User-Agent": "ProjectIChing/1.0 (personal research tool)"
}


def fetch_page_text(page_title: str) -> str:
    response = requests.get(
        API_URL,
        params={
            "action": "query",
            "prop": "extracts",
            "explaintext": 1,
            "titles": page_title,
            "format": "json",
            "redirects": 1,
        },
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()

    pages = response.json()["query"]["pages"]
    page = next(iter(pages.values()))
    return page.get("extract", "").strip()


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def section_after(text: str, markers: list[str], stop_markers: list[str]) -> str:
    start = -1
    for marker in markers:
        match = re.search(marker, text, flags=re.MULTILINE)
        if match:
            start = match.end()
            break

    if start == -1:
        return ""

    body = text[start:].lstrip("：: \n")
    end = len(body)

    for marker in stop_markers:
        match = re.search(marker, body, flags=re.MULTILINE)
        if match:
            end = min(end, match.start())

    return normalize(body[:end])


def split_iching_text(text: str) -> dict[str, str]:
    """
    來源頁面格式不完全一致，因此使用保守規則：
    - 找不到的欄位保持空字串
    - gua_text 優先取卦名後、彖曰前的內容
    """
    text = normalize(text)

    tuan = section_after(
        text,
        [r"(?m)^彖曰[：:]", r"(?m)^《彖》曰[：:]"],
        [r"(?m)^象曰[：:]", r"(?m)^《象》曰[：:]", r"(?m)^文言曰[：:]", r"(?m)^初[六九]"],
    )

    xiang = section_after(
        text,
        [r"(?m)^象曰[：:]", r"(?m)^《象》曰[：:]"],
        [r"(?m)^文言曰[：:]", r"(?m)^初[六九]", r"(?m)^上[六九]"],
    )

    wenyan = section_after(
        text,
        [r"(?m)^文言曰[：:]", r"(?m)^《文言》曰[：:]"],
        [],
    )

    stops = [m.start() for m in [
        re.search(r"(?m)^彖曰[：:]", text),
        re.search(r"(?m)^《彖》曰[：:]", text),
        re.search(r"(?m)^象曰[：:]", text),
        re.search(r"(?m)^《象》曰[：:]", text),
        re.search(r"(?m)^文言曰[：:]", text),
    ] if m]

    gua_text = normalize(text[:min(stops)]) if stops else text

    return {
        "gua_text": gua_text,
        "tuan": tuan,
        "xiang": xiang,
        "wenyan": wenyan,
    }


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"找不到資料檔：{INPUT_PATH}")

    with INPUT_PATH.open("r", encoding="utf-8") as file:
        database: dict[str, Any] = json.load(file)

    hexagrams: dict[str, dict[str, Any]] = database["hexagrams"]

    for index, (key, record) in enumerate(hexagrams.items(), start=1):
        name = record["name"]
        page_title = f"周易/{name}"

        print(f"[{index:02d}/64] 下載 {page_title}")

        try:
            source_text = fetch_page_text(page_title)
            sections = split_iching_text(source_text)

            record["gua_text"] = sections["gua_text"]
            record["tuan"] = sections["tuan"]
            record["xiang"] = sections["xiang"]
            record["wenyan"] = sections["wenyan"]

            # 白話翻譯不抓第三方現代譯文，保留給 Project IChing 後續自行撰寫。
            record["translation"] = record.get("translation", "")

        except Exception as error:
            print(f"  失敗：{error}")

        time.sleep(0.4)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(database, file, ensure_ascii=False, indent=4)

    print()
    print(f"完成：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
