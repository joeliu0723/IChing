IChing Research Workbench（易經研究工作台）

Version：V1.4（Development）

最後同步：2026-07-26（依程式碼現況更新）

---

一、專案定位

本專案不是一般的算命程式。

定位為：

易經研究工作台（I Ching Research Workbench）

主要目的為建立一套方便研究、閱讀、分析、整理易經資料的平台。

希望未來能整合：

易經全文
六爻排卦
解卦
AI 研究
個人研究資料
搜尋
收藏
長期知識管理

而不是傳統命理軟體。

---

二、V1 開發目標

V1 的目標只有一個：

完成一套可正常使用的易經研究工具。

必須做到：

可輸入卦象
可排卦
可顯示本卦
可顯示變卦
可閱讀經文
可保存研究心得

AI 功能放在最後完成。

---

三、不納入 V1 的功能

以下功能全部延後。

V1 不開發：

六親
六神
納甲
世應
用神
飛伏神
神煞
梅花易數
八字
紫微
奇門

原因：

避免專案快速失控。

先完成核心功能。

---

四、目前技術架構

採用 MVC。

資料流程：

UI → Controller → HexagramEngine → Presenter → UI

各層職責：

UI — 顯示、接收輸入，不得放商業邏輯

Controller — 接收 UI 操作、呼叫 Engine / Presenter，不得直接操作 UI 控制項

Engine — 排卦、卦象計算、動爻、變卦，不得碰 UI

Presenter — 將 Engine 回傳資料轉換成 UI 可顯示格式，不得做演算法

實際目錄：

- `core/` — Engine、Controller、Presenter、History、Session
- `ui/` — MainWindow、HistoryPage、Qt Designer 檔案
- `data/` — hexagrams.json、history.json

---

五、目前已完成

✅ Git 專案建立
✅ Python 環境（PySide6、Qt Designer）
✅ MVC 架構
✅ MainWindow（起卦 / 解卦 / 歷史紀錄 三個分頁）
✅ HexagramEngine（本卦、變卦、動爻）
✅ HexagramController / HexagramPresenter
✅ 六爻輸入（UI 已串接）
✅ 卦序輸入（UI 已串接）
✅ 排卦完成自動切換解卦頁
✅ 解卦頁顯示本卦卦辭、彖傳、象傳、文言、白話翻譯
✅ HistoryManager + history.json 自動儲存
✅ HistoryPage 列表顯示
✅ HexagramLookup 查詢模組
✅ 上下卦輸入（UI 已串接）
✅ 輸入模式切換（四種方式）

---

六、目前開發順序（唯一版本）

後續開發依照以下順序，不得跳號。

V1.1 輸入方式完善 — 已完成

V1.2 起卦功能完善 — 已完成

- 共用起卦流程 run_cast()
- Controller 輸入驗證
- 錯誤提示
- 移除 debug print

V1.3 解卦頁 — 已完成

V1.3.1 解卦 UX 與起卦流程 — 已完成

- 解卦欄位可折疊（預設收合）
- 「開始解卦」按鈕（按下後才進解卦）

V1.4 研究功能

- 我的心得編輯與儲存
- 搜尋、收藏、編輯、刪除

V1.5 AI 功能

- AI 解卦
- AI 問答
- AI 研究輔助

---

七、AI 開發原則

所有 AI 必須遵守：

一次只完成一個功能。
不得跳版本開發。
不得自行增加功能。
不得自行修改 MVC 架構。
不得自行更改 UI ObjectName。
每次修改提供完整檔案，不提供程式片段。
若規格沒有衝突，不要反覆要求使用者確認流程。
以既有專案結構為準，不重新設計架構。

---

八、下一個工作

目前下一個工作為：

V1.4：搜尋紀錄。

已完成：心得編輯與儲存、歷史刪除（含多選）。
