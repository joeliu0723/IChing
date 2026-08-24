# AI_DEVELOPMENT_GUIDE.md

Version: V1.4.15  
更新日期：2026-08-24

任何 AI 改本專案時遵守本文件。細節以程式為準。

## 開工前閱讀

1. `docs/README.md`
2. `docs/AI_BOOTSTRAP.md`
3. `docs/DATA_SPEC.md`
4. `docs/PRODUCT_SPEC.md`
5. `docs/PROJECT_STATUS.md`
6. `ForAI/DEVELOPMENT_LOG.md`（需要歷史脈絡時）

## 原則

規格優先、一次一項功能、可執行再開下一項。不要為未來功能加複雜度。

## 架構

- `main.py` 只啟動應用
- 商業邏輯在 `core/`
- UI 不直接讀寫 JSON（經 Controller／Store／paths）

起卦頁大量 Python 組裝（Designer 骨架 + 執行時重組）是現況，不要為了「純 Designer」重寫整頁。

## 目錄

```
core/  ui/  data/  assets/ui/  tools/data_editor/  packaging/  tests/  docs/  ForAI/
```

不要恢復已刪的 `database/`、`backup/`、一次性爬蟲腳本。

## JSON

UTF-8。結構見 `DATA_SPEC.md`。新增欄位保持向下相容；不要刪既有欄位。

開發與打包路徑見 `core/paths.py`。

## UI

品牌名：易經占卜 / I Ching。Hero 只用 `hero_banner_desktop.png`。打包須更新 `packaging/iching.spec` 的 `datas`。

## 錯誤

輸入錯誤與 JSON 損毀：提示、不崩潰。不要依賴不存在的 `logs/` 目錄。

## 功能完成後

更新 `ForAI/DEVELOPMENT_LOG.md` 與 `docs/PROJECT_STATUS.md`。規格變了再改 `PRODUCT_SPEC.md`／`DATA_SPEC.md`。

## 不做（V1）

六親／納甲／世應等專業六爻體例、八字紫微奇門、雲端帳號、Web／Mobile。  
梅花**三數起卦**已在產品內；傳統梅花體例仍不做。
