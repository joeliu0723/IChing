# I Ching UI 改版 — Cursor 接手規格

## 品牌
UI 顯示名稱固定為：
- 中文：易經占卜
- 英文：I Ching

禁止在 UI 顯示 `Project IChing`。

## 視覺
保留目前已確認風格：
- 太極
- 八卦
- 水墨山景
- 米白宣紙
- 深藍黑
- 金色點綴
- 現代桌面工具感

建議色彩：
- 深藍黑：#0F1B26
- 金色：#D4AF37
- 米白：#F6F1E9
- 淡灰：#EFE6D5
- 文字深色：#2B2B28
- 輔助灰：#8A8A8A
- 警示紅：#B23A3A

## 頁面流程
啟動 → 起卦首頁 → 選五種起卦方式 → 輸入 → 占卜問題 → 開始解卦 → 解卦頁。
首頁不要同時顯示解卦與 History。

## 首頁
五種模式：
1. 六爻輸入
2. 卦名
3. 卦序
4. 上下卦
5. 數字卦（梅花三數）

模式用按鈕列切換；輸入區使用 QStackedWidget 並保持固定高度。
占卜問題在輸入區下方。
最下方大型主按鈕「開始解卦」。
保留現有五種起卦邏輯與 start_interpretation()。

上方使用 `taiji_hero.svg` 作為主要視覺背景，可搭配 `bagua_ring.svg`。
不要把文字烘焙到背景圖。

## 解卦頁
上方顯示占卜問題、時間／方式（若現有資料可用）。
中央兩張大型卡片：
[本卦] → [變卦]
顯示大型卦圖、第X卦、卦名、動爻。

點本卦：
[卦辭] [大帥解釋] [白話翻譯] [爻辭（有動爻才顯示）]

點變卦：
[變卦卦辭] [變卦大帥解釋] [變卦白話翻譯]

內容區共用一個 ContentViewer，不建立兩套重複 Panel。
長文字由 ContentViewer 自己垂直捲動，可有顯示更多／收合。

不在新版 UI 顯示：
- 象傳
- 文言
- 變卦象傳
- 變卦文言
- AI 分析
但不要刪除 JSON/Core 既有欄位。

我的心得與事後驗證放在解說區下方，各自保留「儲存」按鈕。
保留收藏。
不要放目前不存在的匯出／分享按鈕。

## History
保留目前：
搜尋、清除搜尋、排序、升降、單擊選取、雙擊開啟、多選、刪除、收藏、驗證狀態。
不要新增匯出／分享。

## Cursor 修改原則
先閱讀目前 main 分支的 UI/Core/History 程式。
不要重寫 Core、Controller、Presenter、HistoryManager。
不要改五種起卦規則。
不要刪除 JSON 欄位。
優先新增可重用 Widget、QStackedWidget、ContentViewer。
不要把所有 UI 寫死在 main_window.py。
每完成一頁先測試再 commit。

## 實作順序
1. 建立 UI redesign branch
2. 首頁
3. 解卦頁
4. History
5. 統一 stylesheet / spacing / buttons / cards / scroll area
6. 回歸測試
7. commit

## 圖片資產
assets/ui/：
- taiji_hero.svg：首頁主視覺
- taiji.svg：太極圖
- bagua_ring.svg：八卦環
- paper_texture.svg：宣紙背景
- ornamental_divider.svg：裝飾分隔線

優先使用 SVG，因為 Qt 可縮放且不需依賴大量 PNG。
