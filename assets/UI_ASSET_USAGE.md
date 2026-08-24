# UI 視覺資產（現況）

更新日期：2026-08-24

## 品牌

- 中文：易經占卜
- 英文：I Ching
- UI 不顯示 Project IChing

## 執行時實際載入

程式只讀 `assets/ui/`（打包後為 `_MEIPASS/assets/ui/`）：

| 檔案 | 用途 |
|------|------|
| `hero_banner_desktop.png` | 起卦頁 Hero 單一完成稿（山景／太極／八卦／品牌字已烘焙在圖內） |
| `ornamental_divider.svg` | 起卦輸入區標題兩側金色飾線 |

替換 `hero_banner_desktop.png` 後，下次顯示會依檔案 mtime 自動重載。

## Hero 顯示（`ui/widgets/brand_hero.py`）

- Cover 滿版；較窄或較寬時等比放大後裁切，錨點對準太極與「易經占卜」
- 寬屏加高並加頂部深藍漸層，避免硬邊
- **不再**疊加 SVG 或 Qt 文字

宣紙區使用色票實心米白（`#F7F4EC`），不載入紙紋 SVG（Qt Svg 對 `feTurbulence` 會渲成灰塊）。

## 色票

深藍：`#0D1B2A`  
金色：`#D4AF37`  
宣紙米白：`#F7F4EC`
