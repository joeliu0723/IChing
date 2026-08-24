IChing Research Workbench（易經研究工作台）

Version：V1.4.15（Development）  
最後同步：2026-08-24

---

一、專案定位

易經研究工作台：起卦、解卦、紀錄、本機知識整理。不是算命平台。

---

二、V1 已達成

可輸入五種卦象（含梅花三數）、排卦、顯示本卦／變卦／動爻、閱讀經文、儲存心得與驗證、歷史查詢、Data Editor 編輯 64 卦、Windows 可攜 exe。

AI 功能仍暫緩。

---

三、不納入 V1

六親、六神、納甲、世應、用神、飛伏、八字、紫微、奇門、雲端帳號、Web／Mobile。

梅花**三數起卦**已實作；傳統梅花體例不做。

---

四、技術架構

UI → Controller → HexagramEngine → Presenter → UI

- `core/` — Engine、Controller、Presenter、History、Session、paths、meihua
- `ui/` — 主視窗、解卦頁、歷史、widgets
- `data/` — hexagrams.json、history.json（開發）；打包後見 `%APPDATA%\IChing\data\`

---

五、資料與發行注意

- 歷史在「儲存問題」後才寫入
- 給他人的空卦辭發行版：須清 `_internal/data/hexagrams.json`（或重建），不能只清本機 APPDATA
- 產品規格：`docs/PRODUCT_SPEC.md`
- 詳細日誌：`ForAI/DEVELOPMENT_LOG.md`
- 待辦儀表板：`docs/PROJECT_STATUS.md`

---

六、下一個工作

資料補齊（Data Editor）。安裝包 Inno 與 V1.5 AI 暫緩。
