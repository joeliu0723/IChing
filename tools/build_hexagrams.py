from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bs4 import BeautifulSoup
from data.hexagram_map import HEXAGRAM_MAP

HTML_DIR = ROOT / "html"
OUTPUT = ROOT / "data" / "hexagrams.json"


def clean(text: str):
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_summary(text: str):
    result = {
        "fortune": "",
        "love": "",
        "career": "",
        "wealth": ""
    }

    patterns = {
        "fortune": r"諸事\s*：\s*(.*?)\s*愛情\s*：",
        "love": r"愛情\s*：\s*(.*?)\s*事業\s*：",
        "career": r"事業\s*：\s*(.*?)\s*財運\s*：",
        "wealth": r"財運\s*：\s*(.*?)(?:建議：|$)"
    }

    for key, pattern in patterns.items():
        m = re.search(pattern, text, re.S)
        if m:
            result[key] = clean(m.group(1))

    return result


def parse_file(path: Path):

    html = path.read_text(encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("article")
    if article is None:
        return None

    body = article.find(class_="field__item")
    if body is None:
        return None

    paragraphs = body.find_all("p", recursive=False)

    if len(paragraphs) < 5:
        return None

    # ---------- 卦序 ----------
    m = re.match(r"(\d+)", path.stem)
    number = int(m.group(1))

    # ---------- 上下卦 ----------
    upper = ""
    lower = ""

    for (u, l), n in HEXAGRAM_MAP.items():
        if n == number:
            upper = u
            lower = l
            break

    # ---------- 卦辭 ----------
    gua_text = clean(paragraphs[0].get_text(" ", strip=True))

    name = gua_text.split("，")[0].replace("䷀", "").strip()

    # ---------- 諸事 ----------
    summary = parse_summary(
        clean(paragraphs[2].get_text(" ", strip=True))
    )

    # ---------- 解說 ----------
    desc = []

    for p in paragraphs[4:]:

        t = clean(p.get_text(" ", strip=True))

        if not t:
            continue

        if t.startswith("焦林值日"):
            break

        desc.append(t)

    description = "\n\n".join(desc)

    return {
        "number": number,
        "name": name,
        "upper": upper,
        "lower": lower,
        "gua_text": gua_text,
        "description": description,
        "fortune": summary["fortune"],
        "love": summary["love"],
        "career": summary["career"],
        "wealth": summary["wealth"],
    }


def main():

    data = []

    for file in sorted(HTML_DIR.glob("*.html")):

        item = parse_file(file)

        if item:
            data.append(item)

    data.sort(key=lambda x: x["number"])

    OUTPUT.parent.mkdir(exist_ok=True)

    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )

    print(f"完成，共輸出 {len(data)} 卦")
    print(OUTPUT)


if __name__ == "__main__":
    main()