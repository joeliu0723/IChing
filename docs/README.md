# Project IChing（易經研究工作台）

Version: V1.4.15  
更新日期：2026-08-24

Windows 桌面程式（Python 3.13 + PySide6）。Local First：資料存在本機 JSON，不依賴網路。

功能：起卦、解卦、占卜紀錄、64 卦資料編輯（Data Editor）。

## 啟動（開發）

```
python main.py
python -m tools.data_editor
```

需要已安裝 PySide6（見 `requirements.txt`）。虛擬環境：`.venv`。

免安裝執行包見 `packaging/README.md`（`dist/IChing/` 或 zip）。

## 技術

| 項目 | 內容 |
|------|------|
| Language | Python 3.13 |
| GUI | PySide6（Designer `.ui` + Python widgets） |
| Storage | JSON |
| Architecture | MVC（邏輯在 `core/`） |
| Platform | Windows |

## 專案結構

```
IChing/
  main.py
  core/           排卦、歷史、路徑
  ui/             主視窗與頁面
  data/           hexagrams.json、hexagram_map.py（開發時讀寫）
  tools/data_editor/
  assets/ui/      Hero PNG、飾線 SVG
  packaging/      PyInstaller / Inno
  tests/
  docs/           產品／資料規格與狀態
  ForAI/          開發日誌與決策紀錄
```

開發時資料在專案 `data/`。打包後：`%APPDATA%\IChing\data\`（首次從安裝包內建檔複製 `hexagrams.json`）。

## 文件

| 檔案 | 用途 |
|------|------|
| `docs/PROJECT_STATUS.md` | 現況與待辦 |
| `docs/PRODUCT_SPEC.md` | 產品功能 |
| `docs/DATA_SPEC.md` | JSON 結構（與程式對齊） |
| `docs/AI_BOOTSTRAP.md` | AI 接手最小資訊 |
| `docs/AI_DEVELOPMENT_GUIDE.md` | 開發約束 |
| `docs/CURSOR_UI_HANDOFF.md` | UI 現況 |
| `ForAI/DEVELOPMENT_LOG.md` | 詳細變更紀錄 |
| `ForAI/DECISIONS.md` | 已確認決策 |
| `packaging/README.md` | Windows 打包 |
| `assets/UI_ASSET_USAGE.md` | 實際載入的圖檔 |

衝突時以程式與 `DATA_SPEC.md`／`PRODUCT_SPEC.md` 為準。
