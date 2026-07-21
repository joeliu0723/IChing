# PROJECT_STATUS.md

# Project IChing（易經研究工作台）

## Current Version

V0.8.2

---

# 專案狀態

目前核心 MVC 已完成並驗證。

目前程式流程：

```
MainWindow
    ↓
HexagramController
    ↓
HexagramEngine
    ↓
HexagramResult
    ↓
HexagramPresenter
    ↓
UI
```

此流程已確認可正常運作。

---

# 已完成

## Git

* Git Repository
* GitHub Repository
* GitHub Desktop

---

## Environment

* Python
* PySide6
* Qt Designer

---

## UI

完成：

* 六爻輸入
* 解卦頁
* 本卦顯示
* 變卦顯示
* 動爻顯示

---

## Core

完成：

* HexagramEngine
* HexagramController
* HexagramPresenter
* HexagramResult

---

## Data

目前使用：

hexagrams.json

保持目前資料格式，不進行擴充。

---

## 已完成功能

* 六爻輸入
* 排卦
* 本卦
* 變卦
* 動爻
* 解卦頁顯示
* MVC 完整串接

---

# 尚未開始

## History

每次占卜自動建立紀錄。

內容包含：

* 日期
* 時間
* 問題
* 六爻
* 本卦
* 變卦
* 動爻

---

## Notes

每筆紀錄可編輯心得。

---

## AI Analysis

根據：

* 本卦
* 變卦
* 動爻
* 問題

產生 AI 解卦內容。

---

## Search

搜尋歷史紀錄。

---

## Favorite

收藏重要占卜。

---

# 下一次開始

直接開始：

## V0.9.0

第一個功能：

History（占卜紀錄）

完成後依序開發：

History → Notes → AI Analysis → Search → Favorite

除非發現重大架構問題，否則不再修改 MVC 核心架構。
