# DATA_SPEC.md

# Project IChing - Data Specification

Version: V1.0
Status: Frozen

---

# Purpose

本文件定義 Project IChing V1.0 的所有資料結構。

所有程式、JSON、儲存格式皆必須依照本文件實作。

本文件為唯一資料規格（Single Source of Truth）。

---

# Storage

Storage Type

- JSON

Architecture

- Local First
- One Divination = One JSON File

Database

- None

Encoding

- UTF-8

JSON Format

- Pretty Print
- Indent = 4

---

# Folder Structure

```
database/
├── divinations/
├── favorites/
└── index/

data/
├── classics/
├── reference/
└── settings/

backup/
```

---

# Divination Record

每一次占卜建立一個 JSON。

檔名：

```
YYYYMMDD_HHMMSS.json
```

例如：

```
20260718_203501.json
```

檔名只作為儲存用途。

真正識別資料請使用 UUID。

---

# JSON Schema

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",

    "created_at": "2026-07-18T20:35:01",
    "updated_at": "2026-07-18T20:35:01",

    "question": "",

    "user": {
        "name": "",
        "gender": "",
        "age": 0
    },

    "hexagram": {
        "number": 0,
        "name": ""
    },

    "changed_hexagram": null,

    "moving_lines": [],

    "interpretation": "",

    "validation": "",

    "validation_result": "未驗證",

    "favorite": false
}
```

---

# Field Specification

## id

UUID v4。

建立後不得修改。

---

## created_at

建立時間。

ISO 8601。

例如：

```
2026-07-18T20:35:01
```

建立後不得修改。

---

## updated_at

最後修改時間。

每次存檔更新。

---

## question

占卜問題。

String。

---

## user

```json
{
    "name": "",
    "gender": "",
    "age": 0
}
```

---

## hexagram

本卦。

```json
{
    "number": 1,
    "name": "乾"
}
```

---

## changed_hexagram

有動爻：

```json
{
    "number": 44,
    "name": "姤"
}
```

沒有動爻：

```json
null
```

---

## moving_lines

由下而上。

例如：

```json
[2,5]
```

表示：

二爻、五爻。

沒有動爻：

```json
[]
```

---

## interpretation

我的解卦。

Multi-line String。

---

## validation

事後驗證。

Multi-line String。

---

## validation_result

固定值：

- 未驗證
- 符合
- 部分符合
- 不符合

不得使用其他文字。

---

## favorite

Boolean。

```
true
false
```

---

# Favorite

不建立 Favorites Database。

直接使用：

```json
"favorite": true
```

---

# Search Fields

搜尋來源：

```
database/divinations/
```

支援：

- question
- user.name
- hexagram.number
- hexagram.name
- changed_hexagram.number
- changed_hexagram.name
- validation_result
- favorite
- created_at

---

# Settings

位置：

```
data/settings/settings.json
```

格式：

```json
{
    "default_name": "",
    "default_gender": "",
    "default_age": 0,

    "font_size": 10,

    "dark_mode": false,

    "window_width": 1600,
    "window_height": 900
}
```

---

# Reference Data

位置：

```
data/classics/
```

保存：

- 易經原文
- 十翼
- 卦辭
- 爻辭

唯讀。

---

位置：

```
data/reference/
```

保存：

- 老師筆記
- 書籍資料
- 匯入資料

唯讀。

---

# Backup

Backup

將

```
database/
```

壓縮為 ZIP。

Restore

直接覆蓋：

```
database/
```

---

# Development Rules

所有 JSON：

- UTF-8
- Pretty Print
- Indent = 4

不得：

- SQLite
- MySQL
- PostgreSQL
- ORM
- Binary Format

V1.0 僅使用 JSON。

---

# AI Development Rules

新增欄位：

不得修改既有 Schema。

若 V2 新增欄位：

只能向下擴充。

不得刪除或重新命名既有欄位。

---

# End