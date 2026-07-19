# Project IChing（易經研究工作台）

Version: V1.0

---

# 專案簡介

Project IChing 是一套以 Python + PySide6 開發的 Windows 桌面程式。

目的是建立一套可長期使用的易經研究工具，提供：

- 起卦
- 解卦
- 占卜紀錄
- 研究資料管理
- 驗證與心得整理

本專案採用 Local First 設計，不依賴網路服務，所有資料皆儲存在本機。

---

# V1.0 開發目標

完成一套可實際使用的桌面程式。

V1.0 不追求大量功能，而是完成核心流程：

1. 建立卦象
2. 顯示本卦與變卦
3. 解卦與紀錄
4. 儲存 JSON
5. 查詢歷史紀錄

---

# 技術

Language

- Python 3.13

GUI

- PySide6
- Qt Designer

Storage

- JSON

Architecture

- Local First

Platform

- Windows

---

# 專案結構

```
IChing/

core/
ui/
database/
data/
docs/
assets/
backup/
logs/

main.py
```

---

# 文件

本專案所有規格均位於 docs。

閱讀順序：

1. AI_BOOTSTRAP.md
2. PRODUCT_SPEC.md
3. DATA_SPEC.md

---

# 開發原則

- 規格優先
- 功能完成優先
- 文件保持精簡
- Local First
- JSON 儲存
- 一次完成一個功能

---

# Version

Current Version

V1.0