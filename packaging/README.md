# Project IChing — Windows 打包

一般 Windows 電腦**不必安裝 Python**。

| 方式 | 說明 |
|------|------|
| **免安裝資料夾 / zip**（建議） | 解壓後雙擊 `IChing.exe` 或 `IChingDataEditor.exe` |
| Inno Setup | 編譯 `iching.iss` |
| 開發 | `python main.py` / `python -m tools.data_editor` |

主程式與 Data Editor 在**同一資料夾**，共用一份 `_internal`（Editor 依賴是主程式的子集）。

歷史與可編輯卦辭：`%APPDATA%\IChing\data\`

## 建置

```powershell
.\packaging\build_exes.ps1
```

產出（`dist\` 只保留這些）：

- `dist\IChing\IChing.exe`
- `dist\IChing\IChingDataEditor.exe`
- `dist\IChing\_internal\`
- `dist\IChing-portable.zip`

## 依賴

- Python 3.10+（僅建置端）
- PySide6、PyInstaller
