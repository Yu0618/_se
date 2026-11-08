# NQU 響應式學生入口網 (Demo Project)

現代軟體工程 / Modern Software Engineering

李蕙妤 111210519 資工四



## 🔗 線上示範 (GitHub Pages)

* **Demo 網址：** [https://julianalidya.github.io/_se/HW2/](https://github.com/Yu0618/_se/tree/main/HW2)

## 🚀 執行方式

在瀏覽器中直接開啟 `index.html`，或使用 VS Code 的 **Live Server** 擴充套件開啟。

* **免安裝與建置：** 本專案無需安裝任何套件 (No npm/node modules dependency) 或執行任何建置/打包步驟。
* **示範登入帳密：**
  * **帳號：** `111210519`
  * **密碼：** `123456`
  * *註：請勿使用真實的大學系統密碼。*

## ✨ 功能特色 (Features)

* **儀表板 (Dashboard)：** 顯示已選總學分與今日課程安排。
* **學生個人檔案 (Student Profile)：** 檢視個人基本資訊。
* **課程搜尋與篩選 (Course Search & Filters)：** 支援關鍵字搜尋以及依星期、開課狀態進行篩選。
* **加退選功能 (Add/Drop Courses)：**
  * 內建**衝堂偵測** (Timetable conflict detection) 機制。
  * 設有 **25 學分**的示範選課上限。
* **選課資料持久化 (Persistent Enrollment)：** 使用瀏覽器 `localStorage` 保存選課紀錄，重新整理或關閉分頁後資料不遺失。
* **每週課表與列印支援 (Weekly Timetable & Print Layout)：** 提供視覺化每週課表，並針對列印樣式進行優化。
* **成績檢視：** 當學期成績皆標示為「尚未公布」。
* **響應式設計 (Responsive Design)：** 支援桌面端 (Desktop) 與行動裝置 (Mobile) 瀏覽。

### 📌 課程資料與規則說明

* 最初的 4 門課程採用學生提供的真實代碼、名稱、學分與節次（合計 11 學分）。
* 教師與教室資訊未經實體核實，故予以省略或標示為待確認。
* 其他標示為 `DEMO` 的課程僅供功能展示與示意。
* 25 學分上限為專案示範規則，並非國立金門大學之官方政策聲明。
* 本系統未編造任何成績或 GPA 資料。

## 📁 專案結構 (Project Structure)

```text
.
├── index.html        # 應用程式主要入口點
├── css/
│   └── style.css     # 版面配置、響應式樣式 (RWD) 與列印樣式
└── js/
    ├── data.js       # 個人檔案與預設課程資料
    └── app.js        # 頁面導覽、示範登入、篩選、加退選邏輯與課表繪製
