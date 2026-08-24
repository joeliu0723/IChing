# CLAUDE.md / AI 交接

Project IChing：Python + PySide6 本機易經研究工作台。資料為 JSON。

Current Version：**V1.4.15**（2026-08-24 文件對齊）

## 現況摘要

- 五種起卦（含梅花三數）
- 解卦頁經文（含象傳／文言／爻辭）與折疊
- 歷史：搜尋、排序、刪除；「儲存問題」才寫入 `history.json`
- Data Editor：`python -m tools.data_editor`
- 可攜執行檔：`packaging/build_exes.ps1` → `dist/IChing/`

待辦：設定頁、備份 ZIP、AI 串接、Inno 正式發行驗證。資料補齊用 Data Editor。

## 目錄

```
main.py
core/                 Engine、Controller、Presenter、History、paths、meihua
ui/                   main_window、history_page、pages、widgets、theme
data/                 hexagrams.json、hexagram_map.py、history.json
tools/data_editor/
assets/ui/            hero_banner_desktop.png、ornamental_divider.svg
packaging/
tests/
docs/                 規格與狀態（產品 SPEC 只在此）
ForAI/                DEVELOPMENT_LOG、DECISIONS、本檔、PROJECT_HANDOVER
```

規格請讀 `docs/PRODUCT_SPEC.md`，不要在 ForAI 再放一份 PRODUCT_SPEC。

## 架構

UI → Controller → HexagramEngine → Presenter → UI

Engine 不可操作 UI。Presenter 不可運算。Controller 不可存取 Widget。

## Tabs

起卦、解卦、歷史。無設定頁。

## 原則

一次一項功能；不要重寫 MVC；不要刪 JSON 欄位。完成後更新 `ForAI/DEVELOPMENT_LOG.md` 與 `docs/PROJECT_STATUS.md`。

## Out of Scope（V1）

六親、納甲、世應、八字、紫微、奇門、雲端、SQLite、Web、Mobile。  
梅花三數起卦已做；傳統梅花體例不做。
