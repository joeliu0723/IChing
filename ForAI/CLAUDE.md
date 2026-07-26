# CLAUDE.md

# Project IChing

## Project

Project IChing 是一套使用 Python + PySide6 開發的本機易經研究工作台。

目的不是算命，而是建立一套可以長期累積易經研究資料的桌面工具。

所有資料皆保存於本機 JSON。

---

# Development Stage

Current Version

V1.1

Current Progress

- ✓ 六爻輸入
- ✓ 卦序輸入
- □ 卦名輸入
- □ 上下卦輸入
- □ 輸入模式切換

Current Task

完成「卦名輸入」。

Next Task

完成「上下卦輸入」。

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

core/
controller/
presenter/
ui/
data/
tests/
docs/

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