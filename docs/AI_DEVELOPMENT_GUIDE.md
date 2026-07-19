# AI_DEVELOPMENT_GUIDE.md

# Project IChing - AI Development Guide

Version: V1.0
Status: Frozen

---

# Purpose

本文件規範所有 AI 在 Project IChing 專案中的開發方式。

任何 AI 接手本專案時，必須遵守本文件。

本文件目的為：

- 保持程式架構一致
- 保持程式風格一致
- 避免重複開發
- 避免自行修改規格
- 方便多人或不同 AI 接手

---

# Before Coding

開始任何工作之前，必須依序閱讀：

1. README.md
2. AI_BOOTSTRAP.md
3. DATA_SPEC.md
4. PRODUCT_SPEC.md
5. 開發日誌.md
6. PROJECT_STATUS.md

未閱讀完成，不得開始修改程式。

---

# Development Principles

遵循以下原則：

- Specification First
- Simplicity First
- Readability First
- Maintainability First

不要過度設計。

不要為未來功能增加複雜度。

V1.0 只完成 V1.0。

---

# Coding Rules

一次只完成一個功能。

完成後：

- 可以執行
- 可以測試
- 沒有已知錯誤

不要一次修改大量程式。

---

# Architecture Rules

所有程式採模組化。

禁止將大量程式寫在 main.py。

main.py 僅負責：

- 啟動程式
- 建立 QApplication
- 建立 MainWindow

商業邏輯不得寫在 UI。

UI 不直接操作 JSON。

---

# Folder Rules

建議結構：

```
core/
ui/
database/
data/
assets/
backup/
logs/
docs/
```

不得任意新增大量資料夾。

若新增資料夾，需更新 README。

---

# UI Rules

所有畫面：

使用 Qt Designer。

Python 僅負責：

- Event
- Logic
- Data Binding

避免在 Python 內大量建立 UI。

---

# Naming Rules

Class

PascalCase

例如：

HexagramGenerator

MainWindow

---

Function

snake_case

例如：

load_json()

save_record()

generate_hexagram()

---

Variable

snake_case

例如：

moving_lines

hexagram_name

record_list

---

Constant

UPPER_CASE

例如：

MAX_HISTORY

DEFAULT_FONT_SIZE

---

# JSON Rules

所有 JSON：

UTF-8

Indent = 4

不得修改 DATA_SPEC.md 定義。

若需要新增欄位：

必須保持向下相容。

不得刪除舊欄位。

---

# Error Handling

不得因：

- JSON 損毀
- 找不到檔案
- 使用者輸入錯誤

導致程式崩潰。

所有錯誤應：

提示使用者。

記錄 Log。

繼續執行。

---

# Logging

重要錯誤：

寫入：

logs/

一般操作：

不需要 Log。

避免產生大量無用紀錄。

---

# Performance

V1.0 應支援：

至少

10000

筆占卜。

搜尋：

低於

1 秒。

避免不必要重複讀取 JSON。

---

# Refactoring

若程式需要重構：

不得改變：

- UI 行為
- JSON Schema
- 使用者操作流程

重構僅改善：

- 可讀性
- 維護性

不得修改功能。

---

# New Features

若想到新功能：

不要直接加入。

先確認：

是否屬於 V1.0。

若不是：

加入 Future List。

不得直接開發。

---

# Testing

每完成一項功能：

至少確認：

✓ 可以啟動

✓ 沒有 Exception

✓ 功能正常

✓ JSON 正常讀寫

✓ UI 正常顯示

完成後再進行下一項功能。

---

# Documentation

完成一個功能後：

更新：

開發日誌.md

PROJECT_STATUS.md

若規格變更：

同步更新：

PRODUCT_SPEC.md

DATA_SPEC.md

不得讓程式與文件不同步。

---

# Communication

若 AI 對需求有疑問：

優先詢問。

不要自行猜測。

不要自行增加功能。

不要自行修改流程。

---

# V1.0 Final Goal

完成：

✓ 起卦

✓ 排卦

✓ 解卦

✓ 儲存

✓ 查詢

✓ 收藏

✓ 備份

✓ 還原

除此之外，不做任何額外功能。

---

# End