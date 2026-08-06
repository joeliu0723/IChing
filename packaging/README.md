# Project IChing — Windows 打包說明

> **狀態：暫緩。** 腳本與 spec 已草稿，尚未完成建置驗證。目前請用開發方式執行主程式與 Data Editor。

## 資料目錄（重要）

| 環境 | 路徑 |
|------|------|
| 開發 | 專案內 `data/` |
| 安裝後（規劃） | `%APPDATA%\IChing\data\` |

- `hexagrams.json`：卦象／解卦內容（Data Editor 編輯此檔）
- `history.json`：占卜歷史（主程式寫入）

**不必在打包前填完 64 卦。** 可隨時用 Data Editor 分批補齊。

開發時啟動 Data Editor：

```powershell
python -m tools.data_editor
```

---

## 建置步驟（暫緩，供日後使用）

### 1. PyInstaller

```powershell
.\packaging\build_exes.ps1
```

或：

```powershell
pyinstaller --noconfirm packaging\iching.spec
pyinstaller --noconfirm packaging\iching_data_editor.spec
```

### 2. Inno Setup

1. 安裝 Inno Setup
2. 編譯 `packaging\iching.iss`
3. 產出於 `dist\installer\`

---

## 依賴

- Python 3.13
- PySide6
- PyInstaller（僅建置時）
- Inno Setup（僅建置安裝包時）
