# 🔗 個人化鏈結與資源摘要 Vault (Link Summarizer Vault)

這是一個結合 **FastAPI**、**Gemini API** 與 **Streamlit** 的現代軟體工程專案。當你丟入文章、技術教學或網頁連結時，系統能自動抓取網頁核心內容，並透過 AI 產生重點摘要與技術標籤，最後統一收納管理。

---

## 🚀 專案特色

* **智慧內容擷取**：使用 `trafilatura` 自動抓取網頁內文，過濾廣告與雜訊。
* **AI 自動化摘要**：串接官方 `google-genai` SDK，自動萃取標題、產生 3 個重點摘要，並分類技術標籤。
* **前後端分離架構**：
  * **後端**：FastAPI 提供高效能 RESTful API 與 SQLite 資料庫持久化。
  * **前端**：Streamlit 提供簡潔、直覺的互動式卡片介面。

---

## 📁 專案資料夾結構

```text
link-summarizer-vault/
├── main.py              # FastAPI 後端主程式（含資料庫與 Gemini 串接）
├── app.py               # Streamlit 前端介面
├── requirements.txt     # Python 依賴套件清單
├── .gitignore           # Git 忽略清單（排除暫存檔與資料庫）
└── README.md            # 專案說明文件
