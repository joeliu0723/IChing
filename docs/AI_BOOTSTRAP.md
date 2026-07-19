# AI_BOOTSTRAP.md

# Project IChing - AI Bootstrap

Version: V1.0

---

# Purpose

本文件提供任何 AI 接手 Project IChing 時所需的最小資訊。

目標：

- 快速理解專案
- 了解已確認的設計決策
- 依照既有架構繼續開發
- 避免重複設計與修改已確認規格

本文件優先於聊天紀錄。

---

# Project Summary

Project Name

Project IChing（易經研究工作台）

Type

Windows Desktop Application

Language

Python 3.13

GUI

PySide6 + Qt Designer

Storage

JSON

Architecture

Local First

Current Version

V1.0

Current Stage

Development

---

# Project Goal

建立一套可長期使用的易經研究工具。

V1.0 必須完成：

- 起卦
- 解卦
- 占卜紀錄
- 查詢紀錄
- JSON 儲存
- 備份與還原

不追求大量功能。

優先完成完整工作流程。

---

# Development Philosophy

遵循以下原則：

1.
Specification First

先確認功能，再撰寫程式。

2.
Feature Driven

一次完成一個功能。

不要同時修改多個模組。

3.
Keep It Simple

優先簡單且容易維護。

不要過度設計。

4.
Local First

所有資料皆儲存在本機。

不依賴雲端。

---

# Confirmed Decisions

以下內容已確認。

除非使用者要求，不可修改。

Storage

JSON

Database

不使用 SQL

GUI

Qt Designer

Framework

PySide6

Platform

Windows

Programming Language

Python 3.13

Architecture

Local First

One Divination

One JSON File

Record

可修改

Favorite

Boolean

Delete

永久刪除

Reference Data

唯讀

Settings

JSON

Backup

ZIP

---

# Development Priority

依照以下順序完成：

1.

Main Window

↓

2.

起卦

↓

3.

排卦核心

↓

4.

解卦

↓

5.

JSON 儲存

↓

6.

資料管理

↓

7.

設定

不要跳步。

---

# Working Rules

開始任何工作前：

1.

閱讀

PRODUCT_SPEC.md

2.

閱讀

DATA_SPEC.md

3.

完成目前功能。

4.

保持程式可執行。

不要一次修改大量程式。

---

# Scope

V1.0

僅完成：

已確認功能。

若想到新功能：

不要直接加入。

完成目前功能即可。

---

# Success Definition

V1.0 完成代表：

✓ 可以起卦

✓ 可以顯示本卦

✓ 可以顯示變卦

✓ 可以輸入解卦

✓ 可以儲存 JSON

✓ 可以重新開啟紀錄

✓ 可以搜尋紀錄

其它功能皆可留待 V2。

---

# Document Priority

若資訊衝突：

DATA_SPEC.md

↓

PRODUCT_SPEC.md

↓

README.md

聊天紀錄僅供參考。

正式文件優先。

---

# Final Rule

若有兩種以上實作方式：

優先選擇：

- 最簡單
- 最容易閱讀
- 最容易維護
- 最少程式碼

不要為了擴充性增加 V1.0 的複雜度。

完成比完美更重要。