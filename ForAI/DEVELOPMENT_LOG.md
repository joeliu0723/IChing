# DEVELOPMENT_LOG.md

# Project IChing - Development Log

本文件記錄 Project IChing 的開發歷程。

目的：

- 紀錄每次完成的功能
- 紀錄修改內容
- 方便日後追蹤問題
- 讓其他 AI 快速了解專案演進

---

# Log Format

每筆紀錄包含：

- Version
- Date
- Feature
- Modified Files
- Description

---

# V0.1

Date

2026-06

Feature

專案建立

Modified Files

- Git Repository
- Python Environment

Description

- 建立 Git Repository
- 建立 Python 專案
- 建立 Virtual Environment
- 安裝 PySide6
- 安裝 Qt Designer

---

# V0.2

Feature

專案架構

Modified Files

core/

controller/

presenter/

ui/

Description

- 建立 MVC 架構
- 建立專案目錄
- 建立主要模組

---

# V0.3

Feature

UI

Description

完成 MainWindow。

建立：

- 起卦頁
- 解卦頁

---

# V0.3A-1

Feature

六爻輸入 UI

Description

建立六爻輸入介面。

六列。

由下而上排列。

---

# V0.3A-2

Feature

HexagramEngine

Description

完成：

- 六爻轉本卦
- 六爻轉變卦
- 動爻判定

---

# V0.3A-3

Feature

Controller

Description

完成：

Controller

↓

Engine

↓

Presenter

↓

UI

完整流程。

完成排卦。

---

# V0.3A-4

Feature

解卦頁

Description

建立：

- 本卦資訊
- 變卦資訊

完成 UI 串接。

---

# V1.1

Status

Development

---

## Completed

### 六爻輸入

Status

Completed

Description

完成：

- 六爻輸入
- 動爻判定
- 本卦
- 變卦

---

### 卦序輸入

Status

Completed

Description

完成：

- 1~64 卦序輸入
- 自動取得本卦

---

## In Progress

### 卦名輸入

Status

Working

Description

目前正在開發。

尚未完成。

---

## Todo

- 上下卦輸入
- 輸入模式切換

---

# Future

## V1.2

- 起卦流程完善

## V1.3

- 解卦頁

## V1.4

- 研究功能

## V1.5

- AI 功能

---

# Change Log Rules

每完成一項功能：

新增一筆紀錄。

不得覆蓋舊紀錄。

保持時間順序排列。

---

# Version Rules

Patch

修正 Bug。

Minor

新增功能。

Major

重大版本。

---

# Example

## V1.1.1

Date

YYYY-MM-DD

Feature

卦名輸入

Modified Files

- hexagram_engine.py
- controller.py
- main_window.py

Description

完成卦名輸入。

可依卦名建立本卦資訊。

---

# End