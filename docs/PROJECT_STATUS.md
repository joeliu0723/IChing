# PROJECT_STATUS.md

# Project IChing — 開發狀態儀表板

更新日期：2026-08-24

---

## Current Version

**V1.4.15**

Status：**Active Development**

定位：易經研究工作台（Local First／Python 3.13／PySide6／MVC／JSON）

---

## Current Milestone

資料補齊（以 Data Editor 分批填入 64 卦解卦欄位）

---

## Next Tasks

| 優先 | 項目 | 狀態 |
|------|------|------|
| 1 | 以 Data Editor 補齊 hexagrams.json 內容 | In Progress |
| 2 | Inno 安裝程式實機驗證 | Deferred |
| 3 | V1.5 AI 解卦／問答 | Deferred |
| 4 | 設定頁、備份／還原 ZIP | Todo |

---

## Completed（功能總覽）

### Core／架構

- [x] HexagramEngine（本卦／變卦／動爻）
- [x] HexagramController／Presenter／Result
- [x] HexagramLookup（卦序／卦名／上下卦）
- [x] 梅花三數起卦（`core/meihua.py`）
- [x] Session、HistoryRecord、HistoryManager
- [x] 共用資料路徑（`core/paths.py`；開發 `data/`，打包 `%APPDATA%\IChing\data\`）

### 起卦

- [x] 六爻／卦名／卦序／上下卦／數字卦
- [x] 「開始解卦」按鈕（不自動排卦）
- [x] V1.4.13–15 起卦與全站 UI

### 解卦

- [x] 本卦／變卦／動爻；卦辭、大帥解釋、象傳、文言、白話、爻辭
- [x] 問題／心得／驗證／收藏
- [ ] AI 分析（僅 UI 占位）

### 歷史

- [x] 「儲存問題」後寫入 history.json
- [x] 搜尋、排序、多選刪除、雙擊開啟

### 工具／發行

- [x] Data Editor（`python -m tools.data_editor`）
- [x] PyInstaller 可攜資料夾（主程式與 Data Editor 共用 `_internal`）
- [ ] Inno 正式發行驗證
- [ ] 設定頁、備份 ZIP、匯出 PDF／Word

---

## Architecture（簡圖）

```
UI (main_window / history_page / data_editor)
    ↓
Controller
    ↓
Engine / Lookup / Meihua / HistoryManager
    ↓
JSON (hexagrams.json / history.json)
    ↓
Presenter → UI
```

---

## Key Paths

| 路徑 | 說明 |
|------|------|
| `main.py` | 主程式入口 |
| `ui/main_window.py` | 主視窗 |
| `tools/data_editor/` | 64 卦資料編輯器 |
| `data/hexagrams.json` | 卦資料（開發） |
| `data/history.json` | 歷史（本機產物，勿隨意推送） |
| `docs/` | 規格與狀態 |
| `ForAI/` | 開發日誌與決策 |
| `packaging/` | exe／Inno |

---

## Git

- Branch：`main`
- 勿將個人 `history.json`／未定稿卦文內容隨意推送

---

## Long Term（未排程）

- 統計分析
- 更多起卦變體
- 雲端同步（若未來要做，不得破壞 Local First）
