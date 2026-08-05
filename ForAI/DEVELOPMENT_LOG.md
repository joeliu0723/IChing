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

# Future

## V1.4

- 心得編輯與儲存
- 搜尋、收藏、編輯、刪除

## V1.5

- AI 功能

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
