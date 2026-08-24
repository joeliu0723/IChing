# DATA_SPEC.md

Project IChing — 資料規格（與程式對齊）  
Version: V1.4.15  
更新日期：2026-08-24

本文件描述**目前實作**。不再使用「一占一檔」或 `database/` 目錄。

## 儲存

- 格式：JSON、UTF-8
- 無 SQL
- 開發：專案根目錄 `data/`
- 打包後可寫目錄：`%APPDATA%\IChing\data\`（`core/paths.py`）
  - `hexagrams.json`：若使用者檔不存在，從安裝包 `_internal/data/` 複製
  - `history.json`：不強制從內建複製

## 檔案

| 路徑 | 用途 |
|------|------|
| `data/hexagrams.json` | 64 卦解卦內容（JSON 陣列） |
| `data/hexagram_map.py` | 上下卦 → 卦序 |
| `data/history.json` | 占卜歷史（JSON 陣列） |

## hexagrams.json

根節點為陣列，每卦一筆，建議欄位：

```json
{
  "number": 1,
  "name": "乾",
  "upper": "乾",
  "lower": "乾",
  "gua_text": "",
  "tuan": "",
  "xiang": "",
  "wenyan": "",
  "translation": "",
  "lines": ["", "", "", "", "", ""],
  "description": "",
  "fortune": "",
  "love": "",
  "career": "",
  "wealth": ""
}
```

| 欄位 | 說明 |
|------|------|
| number, name, upper, lower | 結構識別；Data Editor「清除全部資訊」會保留 |
| gua_text | 卦辭 |
| tuan | 大帥解釋（原彖傳欄） |
| xiang | 象傳 |
| wenyan | 文言 |
| translation | 白話翻譯 |
| lines | 六爻爻辭，由下而上，長度 6 |
| description, fortune, love, career, wealth | 舊欄位，仍可存在；解卦 UI 以經文欄為主 |

Data Editor 可編輯：卦辭、大帥解釋、象傳、文言、白話、爻辭。

## history.json

根節點為 `HistoryRecord` 陣列。單筆：

```json
{
  "id": "uuid",
  "created_at": "2026-08-24T14:00:00",
  "updated_at": "2026-08-24T14:00:00",
  "question": "",
  "cast_method": "六爻輸入",
  "lines": ["young_yang", "young_yin", "old_yang", "young_yin", "young_yang", "young_yin"],
  "main_number": 1,
  "main_name": "乾",
  "changed_number": 1,
  "changed_name": "乾",
  "moving_lines": [],
  "notes": "",
  "favorite": false,
  "verification_content": "",
  "verification_result": "未驗證"
}
```

| 欄位 | 規則 |
|------|------|
| id | UUID；建立後不改 |
| created_at | 建立時間，ISO 8601；不改 |
| updated_at | 每次存檔更新 |
| lines | 六爻字串，由下而上 |
| moving_lines | 動爻序號（1–6），無則 `[]` |
| verification_result | 僅：未驗證／符合／部分符合／不符合 |
| favorite | boolean |

寫入時機：解卦頁「儲存問題」才新增；心得／驗證／收藏需該筆已在歷史中。

規格中的姓名／性別／年齡、`data/settings/`、`data/classics/` **尚未實作**。

## 備份

規格曾規劃 ZIP 備份整個資料目錄；**尚未實作**。Data Editor 可另存備份檔到使用者資料目錄。
