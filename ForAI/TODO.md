# TODO.md

# Project IChing - TODO

Version: V1.4.15

Status: Development

---

# Purpose

本文件記錄目前尚未完成的工作。

僅記錄「待完成」事項。

已完成功能請移至 DEVELOPMENT_LOG.md。

---

# Current Version

V1.4.15

---

# Current Sprint

## Current Task

資料補齊（Data Editor）。

Priority

★★★★☆

Status

In Progress

---

# High Priority

## V1.3.1 解卦 UX 與起卦流程

Status

Completed

---

# Medium Priority

## V1.4 研究功能

Status

Completed

Tasks

- ✓ 我的心得（txtNotes 編輯與儲存）
- ✓ 刪除（UI + 確認；單擊選取／雙擊開啟／多選批次刪除）
- ✓ 搜尋（問題、卦名、卦序、收藏、驗證）
- ✓ 收藏（favorite Checkbox）
- ✓ 驗證內容／驗證結果
- ✓ 編輯（問題／心得／驗證／收藏）
- ✓ 排序（日期、本卦、收藏、驗證結果；可切換升降）

已有

- ✓ HistoryManager（add / load / save / get / update / delete / delete_many / search / sort_records）
- ✓ HistoryPage 列表顯示
- ✓ 排卦後自動寫入 history.json
- ✓ 點選 History 顯示完整解卦內容（V1.3；現為雙擊開啟）
- ✓ 心得儲存（save_notes / updated_at）
- ✓ 歷史刪除（delete_records + 多選確認）
- ✓ 歷史搜尋
- ✓ 收藏（chkFavorite / set_favorite）
- ✓ 驗證（save_verification；列表顯示驗證結果）
- ✓ 問題編輯（save_question）
- ✓ 歷史排序（combo_sort + 升降切換）
- ✓ 變卦白話翻譯（txtChangedTranslation）
- ✓ 輸入模式 QStackedWidget（位置固定）
- ✓ 數字卦／梅花三數（rbMeihuaNumbers；使用者指定）

---

## Data Editor

Status

Completed

啟動

```
python -m tools.data_editor
```

備註

- 右側可捲動；語音輸入用 Win+H（中文台灣）
- 「依欄位匯入」暫時隱藏

---

## Windows 安裝包

Status

Deferred

Tasks

- PyInstaller 產 IChing.exe / IChingDataEditor.exe（packaging/ 草稿已有）
- Inno Setup 安裝程式
- 實機安裝驗證

---

## V1.5 AI 功能

Status

Deferred

Tasks

- AI 解卦（txtAIAnalysis 已有 UI 占位，尚未串接）
- AI 問答
- AI 研究助手

---

# Bug List

目前：

None

---

# Technical Debt

目前：

None

---

# Blocked

目前：

None

---

# Completed

請勿在此紀錄完成項目。

完成後請移至：

DEVELOPMENT_LOG.md

---

# Priority Rules

Priority

★★★★★

目前工作

★★★★☆

下一版本

★★★☆☆

未來版本

★★☆☆☆

---

# Development Rules

一次只完成：

一項功能。

不得跨版本。

不得自行新增功能。

不得修改已完成功能。

完成後更新：

DEVELOPMENT_LOG.md

---

# End
