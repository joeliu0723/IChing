# DECISIONS.md

# Project IChing - Technical Decisions

Version: V1.0

---

# Purpose

本文件記錄 Project IChing 已確認的重要設計決策。

所有 AI 與開發者應遵循本文件。

除非使用者明確要求，否則不得推翻既有決策。

---

# Architecture

Decision

採用 MVC Architecture。

Status

Fixed

Reason

- 降低耦合
- 容易維護
- UI 與邏輯分離

---

Decision

Engine 不得操作 UI。

Status

Fixed

---

Decision

Presenter 不得包含商業邏輯。

Status

Fixed

---

Decision

View 不得包含易經運算。

Status

Fixed

---

Decision

Controller 負責流程控制。

Status

Fixed

---

# UI

Decision

使用 Qt Designer。

Status

Fixed

Reason

避免手寫 UI。

---

Decision

ObjectName 視為固定 API。

Status

Fixed

不得重新命名。

---

Decision

維持既有 UI Layout。

Status

Fixed

不得重新設計畫面。

---

# Data

Decision

資料保存於 JSON。

Status

Fixed

Reason

Local First。

方便備份。

容易閱讀。

---

Decision

V1 不使用 SQLite。

Status

Fixed

---

Decision

所有資料皆保存本機。

Status

Fixed

---

# Product

Decision

Project IChing 定位為：

易經研究工作台。

Status

Fixed

不是算命軟體。

---

Decision

V1 優先完成研究工具。

Status

Fixed

AI 功能延後。

---

Decision

AI 功能安排於 V1.5。

Status

Fixed

原因

核心功能優先。

---

# Scope

Decision

V1 不加入：

- 六親
- 六神
- 納甲
- 世應
- 用神
- 飛伏神

Status

Fixed

Reason

避免 Scope 擴張。

---

Decision

V1 不加入：

- 八字
- 紫微斗數
- 奇門遁甲
- 梅花易數

Status

Fixed

---

Decision

V1 不加入：

- Cloud
- Login
- Plugin
- Mobile
- Web

Status

Fixed

---

# Development

Decision

一次只完成一項功能。

Status

Fixed

---

Decision

不得跨版本開發。

Status

Fixed

---

Decision

不得自行新增功能。

Status

Fixed

---

Decision

不得自行重構。

Status

Fixed

---

Decision

不得修改 MVC。

Status

Fixed

---

Decision

不得修改已完成功能。

Status

Fixed

除非修正 Bug。

---

Decision

不得修改 ObjectName。

Status

Fixed

---

Decision

不得重新命名檔案。

Status

Fixed

除非使用者要求。

---

# Coding Style

Decision

維持既有 Coding Style。

Status

Fixed

---

Decision

不要大量格式化。

Status

Fixed

---

Decision

一次只修改必要檔案。

Status

Fixed

---

Decision

不要修改無關程式。

Status

Fixed

---

# Documentation

Decision

產品需求以 PRODUCT_SPEC.md 為唯一來源。

Status

Fixed

---

Decision

開發規則以 CLAUDE.md 為唯一來源。

Status

Fixed

---

Decision

完成一項功能後更新 DEVELOPMENT_LOG.md。

Status

Fixed

---

# Future Decisions

新增決策請依照以下格式：

---

Date

YYYY-MM-DD

Decision

......

Status

Fixed

Reason

......

---

不得修改既有決策。

僅可新增。

---

# End