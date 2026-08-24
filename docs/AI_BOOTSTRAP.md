# AI_BOOTSTRAP.md

Project IChing — AI 接手最小資訊  
Version: V1.4.15  
更新日期：2026-08-24

## 專案

Windows 桌面易經研究工作台。Python 3.13、PySide6、JSON、Local First。  
入口：`python main.py`。資料編輯：`python -m tools.data_editor`。

## 先讀

1. `docs/PROJECT_STATUS.md`
2. `docs/PRODUCT_SPEC.md`
3. `docs/DATA_SPEC.md`
4. 需要改 UI 時：`docs/CURSOR_UI_HANDOFF.md`、`assets/UI_ASSET_USAGE.md`
5. 決策衝突：`ForAI/DECISIONS.md`
6. 變更紀錄：`ForAI/DEVELOPMENT_LOG.md`

## 架構

UI → Controller → HexagramEngine / Lookup / Meihua / HistoryManager → Presenter → UI

- Engine 不碰 UI
- Presenter 不做排卦運算
- Controller 不直接操作 Widget

## 資料（現況）

- `hexagrams.json`：64 卦解卦內容（陣列）
- `history.json`：占卜紀錄陣列（**不是**一卦一個檔）
- 開發：專案 `data/`
- 打包後：`%APPDATA%\IChing\data\`；內建預設在 `_internal/data/`

歷史：排卦只進 session；解卦頁「儲存問題」才寫入 `history.json`。

## 已完成（摘要）

五種起卦（含梅花三數）、解卦經文與折疊、歷史搜尋排序刪除、Data Editor、可攜 exe（`packaging/`）。

## 未做

設定頁、備份／還原 ZIP、AI 串接、正式 Inno 發行驗證。

## 工作原則

一次改一件事；保持可執行；不要為未排程功能加架構。  
產品規格在 `docs/PRODUCT_SPEC.md`（`ForAI/` 不再另存一份 SPEC）。
