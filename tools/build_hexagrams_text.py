"""
Project IChing
用途：從公開《周易》原文來源下載全文，將卦辭、彖傳、象傳、文言寫入 data/hexagrams.json。

使用方式（在專案根目錄執行）：
    python tools/build_hexagrams_text.py

執行前請確認專案結構：
    ProjectIChing/
    ├─ data/
    │  └─ hexagrams.json
    └─ tools/
       └─ build_hexagrams_text.py
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from urllib.request import Request, urlopen


SOURCE_URL = (
    "https://gist.githubusercontent.com/sui1491/"
    "52e8214c8e5f4a189b94f5ea2b8bdb05/raw/"
    "d628f824a90d7b41b5149199e0fa0767e030b3af/"
    "%25E6%2598%2593%25E7%25BB%258F%25E5%2585%25A8%25E6%2596%2587"
)

HEXAGRAM_NAMES = [
    "乾", "坤", "屯", "蒙", "需", "訟", "師", "比",
    "小畜", "履", "泰", "否", "同人", "大有", "謙", "豫",
    "隨", "蠱", "臨", "觀", "噬嗑", "賁", "剝", "復",
    "無妄", "大畜", "頤", "大過", "坎", "離", "咸", "恆",
    "遯", "大壯", "晉", "明夷", "家人", "睽", "蹇", "解",
    "損", "益", "夬", "姤", "萃", "升", "困", "井",
    "革", "鼎", "震", "艮", "漸", "歸妹", "豐", "旅",
    "巽", "兌", "渙", "節", "中孚", "小過", "既濟", "未濟",
]

# 原始資料中可能使用「无」與「恆」等不同字形；統一比對用。
NAME_ALIASES = {
    "无妄": "無妄",
    "恒": "恆",
    "遁": "遯",
}


def project_root() -> Path:
    """由 tools/ 目錄回推專案根目錄。"""
    return Path(__file__).resolve().parent.parent


def download_source_text() -> str:
    """下載公開原始文本。"""
    request = Request(
        SOURCE_URL,
        headers={"User-Agent": "Project-IChing/1.0"},
    )

    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def normalize_text(text: str) -> str:
    """清理文字格式，但保留原文內容。"""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u3000", " ")
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def canonical_name(name: str) -> str:
    """將來源卦名轉換為專案採用的名稱。"""
    return NAME_ALIASES.get(name, name)


def find_hexagram_sections(source_text: str) -> dict[str, str]:
    """
    依「1 乾，...」「2 坤，...」等標題切出 64 卦段落。
    回傳：{卦名: 該卦完整段落}
    """
    heading_pattern = re.compile(
        r"(?m)(?:^|\n)\s*(?P<number>[1-9]|[1-5]\d|6[0-4])\s*[\.、 ]+\s*(?P<name>[^，,\n\s]+)[，,]"
    )

    matches = list(heading_pattern.finditer(source_text))
    sections: dict[str, str] = {}

    for index, match in enumerate(matches):
        name = canonical_name(match.group("name"))
        if name not in HEXAGRAM_NAMES:
            continue

        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source_text)
        sections[name] = source_text[start:end].strip()

    return sections


def clean_piece(text: str) -> str:
    """整理欄位內容。"""
    text = text.strip()
    text = re.sub(r"\n[ \t]*", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip(" \n")


def parse_hexagram_section(section: str) -> dict[str, str]:
    """
    從單一卦段落解析：
    - gua_text：卦辭
    - tuan：彖傳
    - xiang：象傳（包含卦象與各爻象）
    - wenyan：文言（只有乾、坤通常有內容）
    """
    section = normalize_text(section)

    title_match = re.match(
        r"\s*(?:[1-9]|[1-5]\d|6[0-4])\s*[\.、 ]+\s*[^，,\n\s]+[，,]\s*(.*)",
        section,
        re.S,
    )
    if not title_match:
        return {
            "gua_text": "",
            "tuan": "",
            "xiang": "",
            "wenyan": "",
        }

    body = title_match.group(1).strip()

    tuan_match = re.search(r"《彖》曰：", body)
    xiang_matches = list(re.finditer(r"《象》曰：", body))
    wenyan_match = re.search(r"(?:《文言》曰：|文言曰：)", body)

    gua_text_end = tuan_match.start() if tuan_match else len(body)
    gua_text = clean_piece(body[:gua_text_end])

    tuan = ""
    if tuan_match:
        tuan_end_candidates = [m.start() for m in xiang_matches if m.start() > tuan_match.start()]
        if wenyan_match and wenyan_match.start() > tuan_match.start():
            tuan_end_candidates.append(wenyan_match.start())

        tuan_end = min(tuan_end_candidates) if tuan_end_candidates else len(body)
        tuan = clean_piece(body[tuan_match.end():tuan_end])

    xiang = ""
    if xiang_matches:
        xiang_parts: list[str] = []
        for index, xiang_match in enumerate(xiang_matches):
            start = xiang_match.end()
            end = xiang_matches[index + 1].start() if index + 1 < len(xiang_matches) else len(body)

            if wenyan_match and start < wenyan_match.start() < end:
                end = wenyan_match.start()

            piece = clean_piece(body[start:end])
            if piece:
                xiang_parts.append(piece)

        xiang = "\n\n".join(xiang_parts)

    wenyan = ""
    if wenyan_match:
        wenyan = clean_piece(body[wenyan_match.end():])

    return {
        "gua_text": gua_text,
        "tuan": tuan,
        "xiang": xiang,
        "wenyan": wenyan,
    }


def main() -> None:
    root = project_root()
    json_path = root / "data" / "hexagrams.json"
    backup_path = root / "data" / "hexagrams.backup.json"

    if not json_path.exists():
        print(f"找不到檔案：{json_path}")
        sys.exit(1)

    print("下載《周易》原始文本...")
    source_text = download_source_text()

    print("解析 64 卦資料...")
    sections = find_hexagram_sections(source_text)

    if len(sections) != 64:
        print(f"解析失敗：預期 64 卦，實際找到 {len(sections)} 卦。")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as file:
        project_data = json.load(file)

    hexagrams = project_data.get("hexagrams", {})
    if len(hexagrams) != 64:
        print(f"資料庫格式異常：預期 64 卦，實際找到 {len(hexagrams)} 卦。")
        sys.exit(1)

    shutil.copy2(json_path, backup_path)

    updated_count = 0
    unmatched_names: list[str] = []

    for key, record in hexagrams.items():
        name = canonical_name(record.get("name", ""))

        if name not in sections:
            unmatched_names.append(f"{key}（{name}）")
            continue

        parsed = parse_hexagram_section(sections[name])

        record["gua_text"] = parsed["gua_text"]
        record["tuan"] = parsed["tuan"]
        record["xiang"] = parsed["xiang"]
        record["wenyan"] = parsed["wenyan"]

        # 白話翻譯保持空白，避免直接複製有版權的現代譯文。
        record["translation"] = record.get("translation", "")

        updated_count += 1

    if unmatched_names:
        print("以下卦名未能對應來源資料：")
        for item in unmatched_names:
            print(f" - {item}")
        print("已停止，原始 hexagrams.json 保留不寫入。")
        sys.exit(1)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(project_data, file, ensure_ascii=False, indent=4)
        file.write("\n")

    print(f"完成：已更新 {updated_count} 卦。")
    print(f"備份檔：{backup_path}")


if __name__ == "__main__":
    main()
