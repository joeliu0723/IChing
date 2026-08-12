# DEVELOPMENT_LOG.md

# Project IChing - Development Log

本文件記錄 Project IChing 的開發歷程。

目的：

- 紀錄每次完成的功能
- 紀錄修改內容
- 方便日後追蹤問題
- 讓其他 AI 快速了解專案演進

---

# Log Format

每筆紀錄包含：

- Version
- Date
- Feature
- Modified Files
- Description

---

# V0.1

Date

2026-06

Feature

專案建立

Modified Files

- Git Repository
- Python Environment

Description

- 建立 Git Repository
- 建立 Python 專案
- 建立 Virtual Environment
- 安裝 PySide6
- 安裝 Qt Designer

---

# V0.2

Feature

專案架構

Modified Files

- core/
- ui/

Description

- 建立 MVC 架構
- 建立專案目錄
- Controller、Presenter、Engine 皆置於 core/

---

# V0.3

Feature

UI

Description

完成 MainWindow。

建立：

- 起卦頁
- 解卦頁

---

# V0.3A-1

Feature

六爻輸入 UI

Description

建立六爻輸入介面。

六列。

由下而上排列。

---

# V0.3A-2

Feature

HexagramEngine

Description

完成：

- 六爻轉本卦
- 六爻轉變卦
- 動爻判定

---

# V0.3A-3

Feature

Controller / Presenter

Description

完成 MVC 完整流程。

Controller → Engine → Presenter → UI

完成排卦。

---

# V0.3A-4

Feature

解卦頁

Description

建立：

- 本卦資訊
- 變卦資訊

完成 UI 串接。

---

# V1.0

Date

2026-07

Feature

核心功能與歷史紀錄

Modified Files

- core/controller.py
- core/presenter.py
- core/history.py
- core/history_manager.py
- core/session.py
- ui/main_window.py
- ui/history_page.py

Description

完成：

- HexagramResult 資料模型
- 解卦頁顯示卦辭、彖傳、象傳、文言、白話翻譯
- HistoryRecord / HistoryManager
- 排卦後自動寫入 history.json
- HistoryPage 列表顯示
- Session 工作階段管理

---

# V1.1

Status

Completed

---

## Completed

### 六爻輸入

Status

Completed

Description

- 六爻輸入 UI（groupLinesInput）
- 動爻判定
- 本卦 / 變卦計算
- 排卦完成自動切換解卦頁

---

### 卦序輸入

Status

Completed

Description

- spinHexagramNumber + btnNumberCalculate
- HexagramLookup.number_to_lines()
- Controller.calculate_by_number()
- 排卦完成自動切換解卦頁

---

### 卦名輸入

Status

Completed

Description

- ComboBox 選擇 / 手動輸入
- hexagrams.json 正式卦名查詢
- 依卦名排卦並切換解卦頁

---

### 輸入模式切換

Status

Completed

Description

- 四種 RadioButton 切換
- 僅顯示目前輸入區塊

---

## V1.1.2

Date

2026-07-26

Feature

上下卦輸入 UI 串接、輸入模式切換完成

Modified Files

- ui/main_window.py

Description

- 建立上下卦 ComboBox 輸入區
- 串接 calculate_by_trigrams()
- 完成四種輸入模式 RadioButton 切換
- 抽出 show_result() 共用排卦後流程

---

## V1.1.1

Date

2026-07-26

Feature

卦名輸入 UI 串接

Modified Files

- core/hexagram_lookup.py
- ui/main_window.py

Description

- 從 hexagrams.json 載入正式卦名與簡稱查詢
- 建立卦名 ComboBox 輸入區
- 串接依卦名排卦
- 六爻 / 卦名 RadioButton 切換顯示對應輸入區
- 無效卦名顯示錯誤提示

---

## V1.2

Date

2026-07-26

Feature

起卦功能完善

Modified Files

- core/controller.py
- core/history_manager.py
- ui/main_window.py

Description

- Controller 新增六爻 / 卦序 / 卦名 / 上下卦輸入驗證
- 移除 Controller、HistoryManager debug print
- main_window 抽出 run_cast() 共用起卦流程
- 四種輸入方式統一錯誤提示與結果顯示

---

## V1.3

Date

2026-07-26

Feature

解卦頁完善

Modified Files

- core/result.py
- core/controller.py
- core/presenter.py
- ui/main_window.py
- ui/history_page.py

Description

- 顯示占卜問題
- 顯示變卦卦辭、彖傳、象傳、文言
- 顯示爻辭（含動爻標記）
- History 點選載入完整解卦內容
- Controller 新增 build_result()

---

## V1.3.1

Date

2026-08-05

Feature

解卦欄位折疊與「開始解卦」流程

Modified Files

- ui/main_window.py
- ui/widgets/collapsible_groupbox.py

Description

- 解卦頁各經文區塊改為 CollapsibleGroupBox，預設折疊
- 輸入模式列新增「開始解卦」按鈕
- 六爻選滿不再自動排卦；卦序／卦名／上下卦改由「開始解卦」統一觸發

---

---

## V1.4.1

Date

2026-08-05

Feature

心得編輯與儲存

Modified Files

- core/history.py
- core/controller.py
- ui/main_window.py

Description

- HistoryRecord 新增 updated_at
- Controller.save_notes() 寫回 history.json
- 解卦頁「我的心得」新增「儲存心得」按鈕
- 從歷史載入時同步 Session，方可儲存心得

---

---

## V1.4.2

Date

2026-08-05

Feature

歷史紀錄刪除

Modified Files

- core/controller.py
- ui/history_page.py
- ui/main_window.py

Description

- 歷史頁新增「刪除選取紀錄」按鈕
- 刪除前 QMessageBox 確認
- Controller.delete_record()；若刪除目前 Session 紀錄則清空 Session

---

## V1.4.3

Date

2026-08-05

Feature

歷史多選刪除與開啟分離

Modified Files

- ui/history_page.py
- ui/main_window.py
- core/controller.py
- core/history_manager.py

Description

- 單擊僅選取，雙擊才開啟解卦
- ExtendedSelection 支援 Ctrl／Shift 多選
- delete_records / delete_many 批次刪除，一次確認

---

## V1.4.4

Date

2026-08-05

Feature

歷史紀錄搜尋

Modified Files

- core/history_manager.py
- ui/history_page.py

Description

- HistoryManager.search()：問題、卦名、卦序
- 歷史頁搜尋列即時過濾 + 清除按鈕
- 姓名／收藏／驗證搜尋待欄位完成後擴充

---

## V1.4.5

Date

2026-08-05

Feature

收藏

Modified Files

- core/history.py
- core/history_manager.py
- core/controller.py
- ui/main_window.py
- ui/history_page.py

Description

- HistoryRecord.favorite 寫入 JSON
- 解卦頁「收藏」Checkbox，切換即儲存
- 歷史列表收藏顯示 ★
- 搜尋關鍵字「收藏」可篩選已收藏紀錄

---

## V1.4.6

Date

2026-08-05

Feature

驗證內容與驗證結果

Modified Files

- core/history.py
- core/history_manager.py
- core/controller.py
- ui/main_window.py
- ui/history_page.py

Description

- HistoryRecord 新增 verification_content / verification_result（固定四值）
- 解卦頁「事後驗證」折疊區塊：下拉結果 + 內容 + 儲存驗證
- Controller.save_verification 寫入 JSON 並更新 updated_at
- 歷史列表顯示非「未驗證」的驗證結果；搜尋可篩選驗證結果／內容

---

## V1.4.7

Date

2026-08-05

Feature

編輯（占卜問題）

Modified Files

- core/controller.py
- core/presenter.py
- ui/main_window.py

Description

- 解卦頁問題改為可編輯 QLineEdit +「儲存問題」
- Controller.save_question() 寫回 history.json，並同步 session.result
- 規格可改欄位已齊：問題、心得、驗證內容／結果、收藏（id／created_at 不可改）

---

## V1.4.8

Date

2026-08-05

Feature

歷史紀錄排序

Modified Files

- core/history_manager.py
- ui/history_page.py

Description

- HistoryManager.sort_records()：日期（新→舊）、本卦、收藏、驗證結果
- 歷史頁新增排序下拉，與搜尋條件併用
- V1.4 研究功能完成

---

## V1.4.9

Date

2026-08-06

Feature

UX 修正：排序升降、標題更名、變卦白話、輸入模式版面

Modified Files

- core/history_manager.py
- core/presenter.py
- ui/history_page.py
- ui/main_window.py

Description

- 排序各欄位可切換小→大／大→小
- 解卦「彖傳」顯示改為「大帥解釋」；「變卦彖傳」改為「變卦大帥解釋」（ObjectName／資料欄位不變）
- 新增「變卦白話翻譯」，來源同本卦 translation（result.changed.translation）
- 起卦四種輸入改 QStackedWidget 固定高度，切換時「輸入模式」位置不再跳動

---

## V1.4.10

Date

2026-08-06

Feature

獨立 Data Editor（64 卦資料編輯與欄位匯入）

Modified Files

- core/paths.py（新增）
- core/hexagram.py
- core/hexagram_lookup.py
- core/history_manager.py
- tools/data_editor/（新增）
- tools/__init__.py
- data/__init__.py
- requirements.txt

Description

- 共用路徑：開發用專案 data/；打包後用 %APPDATA%\\IChing\\data\\（首次從內建預設複製）
- 獨立工具 `python -m tools.data_editor`：編輯卦辭／大帥解釋／象傳／文言／白話翻譯／爻辭
- 依欄位一鍵匯入（JSON 現有鍵／文字檔／資料夾），預設不覆蓋非空，可強制覆蓋
- 可儲存、重新載入、匯出備份
- Windows 安裝包（PyInstaller／Inno）已草稿於 packaging/，**建置與驗證暫緩**

---

## V1.4.11

Date

2026-08-06

Feature

Data Editor UX：捲動、語音輸入、隱藏匯入

Modified Files

- tools/data_editor/main_window.py

Description

- 右側編輯區包 QScrollArea，可垂直捲動到底部
- 「語音輸入」按鈕：聚焦欄位並送出 Win+H（需系統中文台灣語音）
- 「依欄位匯入」暫時隱藏（邏輯保留）

---

## V1.4.12

Date

2026-08-06

Feature

梅花易數「數字卦」輸入模式（使用者指定；SPEC 列為 Out of Scope，未改 PRODUCT_SPEC）

Modified Files

- core/meihua.py（新增）
- core/controller.py
- ui/main_window.py

Description

- 輸入模式新增「數字卦」Radio + 三數 SpinBox
- 經典三數法：上卦／下卦 ÷8 餘、動爻 ÷6 餘（餘0作8／6）；先天序1乾…8坤
- Controller.calculate_by_meihua → 既有 calculate(lines) 流程

---

## V1.4.13

Date

2026-08-12

Feature

起卦首頁 UI 視覺改版（Desktop 1200×800）

Modified Files

- ui/main_window.py
- ui/widgets/brand_hero.py（新增）
- ui/widgets/mode_selector.py（新增）
- assets/ui/（Hero 完成稿與視覺資產）
- docs/CURSOR_UI_HANDOFF.md

Description

- Hero 改為單一完成稿 `assets/ui/hero_banner_desktop.png`（等比例縮放，不裁切、無 SVG／文字疊加；檔案更新後依 mtime 自動重載）
- 五模式選擇列：等寬按鈕、深藍＋金邊 Active 態
- 六爻輸入改為宣紙色選項卡片＋ radio 指示器；選取態深藍＋金邊
- 卦名／卦序／上下卦／數字卦輸入頁對齊同一張 Input Card 與置中表單
- 卦名可輸入簡稱（如「坤」）正確查詢；ComboBox 禁止插入無效項目、補全改為包含比對
- 未改 Core／Controller／Presenter／Engine 排卦規則

---

## V1.4.14

Date

2026-08-12

Feature

起卦 CTA 精修

Modified Files

- ui/main_window.py（`_PrimaryCtaButton`）

Description

- 「開始解卦」改為深藍底＋內縮金色邊框主按鈕
- 保留 hover／focus 回饋，不影響排卦流程

---

## V1.4.15

Date

2026-08-12

Feature

全站 UI 對齊 Layout（起卦／解卦／歷史）

Modified Files

- ui/theme/tokens.py、ui/theme/app_stylesheet.py（新增）
- ui/pages/interpretation_page.py（新增）
- ui/widgets/app_nav_bar.py、nav_icons.py、hexagram_glyph.py、hexagram_card.py、history_record_row.py、content_viewer.py、segmented_tabs.py（新增）
- ui/widgets/brand_hero.py、mode_selector.py、collapsible_groupbox.py
- ui/main_window.py、ui/history_page.py
- core/controller.py、core/history.py、core/result.py（`cast_method`／占卜時間寫入）

Description

- 抽出共享 theme tokens／stylesheet；寬屏頂 Tab＋窄屏底部導航（圖示與分隔線）
- Hero：Cover 滿版、寬屏加高與頂部深藍→透明漸層；起卦首頁不顯示底欄
- 解卦頁：本卦／變卦卡、內容分頁、心得／驗證預設摺疊；顯示占卜時間／占卜方式（寬屏橫排）
- 歷史頁：解卦時間、本卦／變卦、問題、收藏、驗證；每頁 5–8 筆依可視高度均分行高
- 選取色：歷史列與本卦／變卦卡＝淺紙／暖紙＋金邊；六爻選項與模式列＝深藍底白字；卦名等輸入控件 focus＝暖紙＋金邊
- 起卦紀錄寫入 `cast_method`；移除暫用 Layout 參考圖與預覽截圖

---

# Future

## Packaging（暫緩）

- PyInstaller 產 exe
- Inno Setup 安裝程式

## V1.5

- AI 功能（暫緩）

---

# Change Log Rules

每完成一項功能：

新增一筆紀錄。

不得覆蓋舊紀錄。

保持時間順序排列。

---

# Version Rules

Patch

修正 Bug。

Minor

新增功能。

Major

重大版本。

---

# End
