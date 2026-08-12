# CLAUDE.md

# Project IChing

## Project

Project IChing 是一套使用 Python + PySide6 開發的本機易經研究工作台。

目的不是算命，而是建立一套可以長期累積易經研究資料的桌面工具。

所有資料皆保存於本機 JSON。

---

# Development Stage

Current Version

V1.4.13

Current Progress

- ✓ V1.1 四種輸入方式
- ✓ V1.2 共用起卦流程、輸入驗證
- ✓ V1.3 解卦頁（變卦經文、爻辭、History 詳情）
- ✓ V1.3.1 解卦欄位折疊、「開始解卦」按鈕
- ✓ 歷史紀錄（自動儲存、列表、雙擊開啟、多選刪除）
- ✓ V1.4 心得編輯與儲存
- ✓ V1.4 驗證內容與驗證結果
- ✓ V1.4 編輯（問題／心得／驗證／收藏）
- ✓ V1.4 排序
- ✓ V1.4.9 UX 修正（排序升降、大帥解釋、變卦白話、輸入模式固定）
- ✓ V1.4.10 Data Editor（64 卦編輯／欄位匯入）
- ✓ V1.4.11 Data Editor UX（捲動、Win+H 語音、隱藏匯入）
- ✓ V1.4.12 數字卦（梅花易數三數起卦）
- ✓ V1.4.13 起卦首頁 UI 改版（Hero 單圖、五模式列、六爻／卦名／卦序／上下卦／數字卦對齊）

Current Task

資料補齊（可用 Data Editor 分批輸入）。

Next Task

Windows 安裝包（暫緩）；V1.5 AI（暫緩）。

---

# Tech Stack

Python 3.13

PySide6

Qt Designer

MVC Architecture

JSON Storage

Windows

---

# Project Structure

```
IChing/
├── main.py
├── ForAI/              # AI 交接文件（本目錄）
├── core/               # 核心邏輯（含 Controller、Presenter、Engine）
│   ├── hexagram.py
│   ├── hexagram_lookup.py
│   ├── controller.py
│   ├── presenter.py
│   ├── result.py
│   ├── history.py
│   ├── history_manager.py
│   ├── session.py
│   └── paths.py
├── ui/
│   ├── main_window.py
│   ├── main_window.ui
│   ├── ui_mainwindow.py
│   └── history_page.py
├── data/
│   ├── hexagrams.json
│   ├── hexagram_map.py
│   └── history.json
├── tools/
│   └── data_editor/    # 獨立 64 卦資料編輯器
├── packaging/          # Windows 安裝包草稿（暫緩）
├── tests/
└── docs/               # 另一套規格文件（V1.0 路線）
```

注意：`controller/`、`presenter/` 不在獨立目錄，而是放在 `core/` 內。

---

# Architecture

UI

↓

Controller

↓

HexagramEngine

↓

Presenter

↓

UI

Engine 不可操作 UI。

Presenter 不可運算。

Controller 不可存取 Widget。

View 不可包含商業邏輯。

---

# UI Tabs（目前）

- 起卦（tabDivination）
- 解卦（tab_interpretation）
- 歷史紀錄（tab_history）

設定頁尚未建立（規格中有，UI 尚無）。

---

# Development Rules

每次只完成一個功能。

不要跨版本。

不要自行增加功能。

不要重新設計 UI。

不要修改 ObjectName。

不要改 MVC。

不要重構既有程式。

不要修改已完成功能。

不要加入未規劃功能。

除非規格衝突，否則維持現有設計。

---

# Working Rules

修改程式前請閱讀：

PRODUCT_SPEC.md

完成後：

更新 DEVELOPMENT_LOG.md。

不要修改 PRODUCT_SPEC。

不要自行調整 Roadmap。

---

# V1 Scope

V1 包含：

- 起卦
- 排卦
- 解卦
- 研究心得
- 歷史紀錄
- AI（V1.5）

---

# Out of Scope

V1 不包含：

- 六親
- 六神
- 納甲
- 世應
- 用神
- 八字
- 紫微斗數
- 奇門遁甲
- 梅花易數
- 雲端同步
- SQLite
- Plugin
- Web
- Mobile

---

# Code Style

保持現有 Coding Style。

不要大規模格式化。

不要修改無關程式。

一次只修改必要檔案。

提供完整檔案。

不要提供程式片段。

---

# Priority

1. 修正 Bug
2. 完成目前功能
3. 更新 Development Log

不要自行執行第 4 步。
