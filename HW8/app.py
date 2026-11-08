import requests
import streamlit as st

# FastAPI 後端網址
FASTAPI_URL = "http://127.0.0.1:8000/api/resources"

st.set_page_config(
    page_title="Personal Link Summarizer", page_icon="🔗", layout="centered"
)

st.title("🔗 個人化鏈結與資源摘要 Vault")
st.write("輸入技術文章、GitHub 或教學網址，讓 AI 自動為你抓取並產生重點摘要！")

# --- 輸入表單區塊 ---
with st.form("submit_form", clear_on_submit=True):
  url_input = st.text_input("輸入網址 (URL)", placeholder="https://...")
  submitted = st.form_submit_button("送出並生成 AI 摘要")

  if submitted:
    if url_input:
      with st.spinner("正在抓取網頁並呼叫 Gemini 產生摘要中，請稍候..."):
        try:
          response = requests.post(FASTAPI_URL, json={"url": url_input})
          if response.status_code == 200:
            st.success("成功新增並完成摘要！")
            st.rerun()
          else:
            err_detail = response.json().get("detail", "未知錯誤")
            st.error(f"新增失敗：{err_detail}")
        except requests.exceptions.ConnectionError:
          st.error("無法連線至 FastAPI 後端，請確認後端是否正在運行！")
    else:
      st.warning("請輸入有效的網址。")

st.divider()

# --- 列表展示區塊 ---
st.subheader("📚 歷史收藏與摘要")

try:
  res = requests.get(FASTAPI_URL)
  if res.status_code == 200:
    resources = res.json()
    if not resources:
      st.info("目前還沒有任何收藏，快在上方輸入第一個網址吧！")
    else:
      for item in resources:
        with st.container(border=True):
          st.markdown(f"### [{item['title']}]({item['url']})")
          st.caption(f"📅 建立時間：{item['created_at'][:19]}")

          # 顯示標籤
          if item["tags"]:
            tags = item["tags"].split(",")
            tag_badges = " ".join([f"`#{tag.strip()}`" for tag in tags])
            st.markdown(tag_badges)

          st.markdown("**核心摘要：**")
          st.text(item["summary"])
  else:
    st.error("無法取得資源列表。")
except requests.exceptions.ConnectionError:
  st.warning("⚠️ 目前無法連線至後端伺服器 (http://127.0.0.1:8000)。")
