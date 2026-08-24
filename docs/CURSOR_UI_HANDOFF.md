# I Ching UI — 現況說明

更新日期：2026-08-24

本文件描述**目前已上線的桌面 UI**，不是舊版分層 SVG Hero 規格。

## 品牌

- 中文：易經占卜
- 英文：I Ching
- 禁止在 UI 顯示 `Project IChing`

## 視覺

深藍黑、金色、米白宣紙、水墨山景與太極八卦皆已合成在 Hero PNG 內。主題 tokens：`ui/theme/tokens.py`。

## 頁面流程

啟動 → 起卦首頁 → 選五種起卦方式 → 輸入 → 占卜問題 →「開始解卦」→ 解卦頁。  
寬屏頂部導航；窄屏底部導航。起卦首頁不顯示底欄。

## 起卦首頁

五種模式（`ModeSelector` + `QStackedWidget` 固定高度）：

1. 六爻輸入  
2. 卦名  
3. 卦序  
4. 上下卦  
5. 數字卦（梅花三數）

Hero：`assets/ui/hero_banner_desktop.png`（Cover，見 `BrandHero`）。  
輸入卡標題兩側：`ornamental_divider.svg`。  
最下方主按鈕：「開始解卦」（不自動排卦）。

## 解卦頁

- 本卦／變卦卡片、動爻、占卜時間／方式
- 內容分頁含：卦辭、大帥解釋、象傳、文言、白話翻譯、爻辭（本卦與變卦對齊）
- AI 分析：UI 占位，未串接
- 心得、事後驗證、收藏、儲存問題（**首次寫入歷史**）

## 歷史

搜尋、排序、升降、單擊選取、雙擊開啟、多選刪除、收藏與驗證狀態。  
排卦當下不寫 `history.json`；解卦頁按「儲存問題」才新增紀錄。

## 修改原則

- 不要重寫 Core／Controller／Presenter／HistoryManager 的排卦規則
- 不要刪除 JSON 既有欄位
- 資產只放 `assets/ui/` 且須列入 `packaging/iching.spec` 才會進 exe
