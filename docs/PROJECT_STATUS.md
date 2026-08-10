# PROJECT_STATUS.md

# Project IChing — 開發狀態儀表板

更新日期：2026-08-10

---

## Current Version

**V1.4.12**

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
| 2 | Windows 安裝包（PyInstaller + Inno） | Deferred |
| 3 | V1.5 AI 解卦／問答 | Deferred |
| 4 | 設定頁、備份／還原 | Todo |

---

## Completed（功能總覽）

### Core／架構

- [x] HexagramEngine（本卦／變卦／動爻）
- [x] HexagramController／Presenter／Result
- [x] HexagramLookup（卦序／卦名／上下卦）
- [x] 梅花三數起卦（`core/meihua.py`）
- [x] Session、HistoryRecord、HistoryManager
- [x] 共用資料路徑（`core/paths.py`；開發用 `data/`）

### 起卦

- [x] 六爻輸入
- [x] 卦名輸入
- [x] 卦序輸入
- [x] 上下卦輸入
- [x] 數字卦（梅花易數三數）
- [x] 輸入模式切換（固定高度 Stack，不跳動）
- [x] 「開始解卦」按鈕（不自動排卦）
- [x] 占卜問題輸入
- [x] 輸入驗證與錯誤提示

### 解卦

- [x] 本卦／變卦／動爻顯示
- [x] 本卦：卦辭、大帥解釋、象傳、文言、白話翻譯
- [x] 變卦：卦辭、大帥解釋、象傳、文言、白話翻譯
- [x] 爻辭（動爻標記）
- [x] 解卦區塊可折疊
- [x] 問題編輯與儲存
- [x] 我的心得編輯與儲存
- [x] 事後驗證（結果＋內容）
- [x] 收藏 Checkbox
- [ ] AI 分析（僅 UI 占位）

### 歷史

- [x] 排卦後自動寫入 history.json
- [x] 列表顯示（日期／卦名／問題／★／驗證）
- [x] 單擊選取、雙擊開啟
- [x] 多選刪除＋確認
- [x] 搜尋
- [x] 排序＋升降切換
- [x] 從歷史還原完整解卦內容

### 工具

- [x] Data Editor（`python -m tools.data_editor`）
- [x] Editor 捲動、Win+H 語音、隱藏批次匯入 UI
- [x] packaging/ 安裝包草稿（未驗證建置）

### 尚未完成

- [ ] 設定頁
- [ ] 備份／還原 ZIP
- [ ] 匯出 PDF／Word
- [ ] Windows Installer 正式發行
- [ ] AI 串接

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
| `data/hexagrams.json` | 卦資料 |
| `data/history.json` | 歷史（本機執行產物，通常不進版控） |
| `ForAI/` | AI 交接與詳細開發日誌 |
| `docs/` | 本目錄：規格／狀態／開發日誌（對外整理） |
| `packaging/` | 安裝包草稿（暫緩） |

---

## Git（參考）

- Branch：`main`
- 近期功能已分段 commit（含 Data Editor、梅花數字卦等）
- 勿將個人 `history.json`／未定稿卦文內容隨意推送

---

## Long Term（未排程）

- 統計分析
- 更多起卦變體（時間起卦等）
- 雲端同步（若未來要做，不得破壞 Local First 相容）
