# I Ching UI Visual Assets V2

## 品牌
中文：易經占卜
英文：I Ching
不要在 UI 顯示 Project IChing。

## 資產

- `hero_background.svg`
  - 深藍墨色 Hero 底圖
  - 不含文字、太極、按鈕
  - 建議滿版填滿 Hero

- `taiji_emblem.svg`
  - 透明背景太極徽章
  - 建議置於 Hero 中央偏左或中央
  - 不要與品牌文字重疊

- `bagua_ring.svg`
  - 透明背景八卦環
  - 建議低透明度放在 Hero 背景／太極周圍
  - 不要搶過品牌文字

- `ink_mountain.svg`
  - 透明背景水墨山景
  - 建議放 Hero 最底層或底部
  - 可與 hero_background 疊加

- `paper_texture.svg`
  - 淡宣紙紋理
  - 用於 Input Card、Question Card 或頁面背景
  - 不要用於深色 Hero

- `ornamental_divider.svg`
  - 金色裝飾分隔線
  - 用於品牌下方或 Section 間
  - 不要大量重複

## Hero Layer 順序

1. hero_background.svg
2. ink_mountain.svg
3. bagua_ring.svg（低透明度）
4. taiji_emblem.svg
5. 品牌文字：易經占卜 / I Ching
6. ornamental_divider.svg（可選）

文字不可烘焙進圖片。

## 建議色票

深藍：#0D1B2A
金色：#D4AF37
墨灰：#2B2E34
宣紙米白：#F7F4EC
紙底：#F1E8D6
水墨灰：#6B7280

## Qt 實作

優先使用 QSvgWidget / QSvgRenderer。
不要用 QSS background-image 載入主要 SVG。
SVG 僅作視覺資產，不包含功能。
不要新增動畫、粒子、3D 或即時模糊。
