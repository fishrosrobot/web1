"""
运行方式: streamlit run app.py

草场碳排放监测系统
- 上传 JPG/PNG 草场照片
- 缩略图预览与点击查看大图
- 模拟碳排放趋势折线图
"""

import streamlit as st
import pandas as pd
import random
from PIL import Image

# ---------------------------------------------------------------------------
# 页面配置
# ---------------------------------------------------------------------------
st.set_page_config(page_title="草场碳排放监测系统", layout="wide")

# ---------------------------------------------------------------------------
# 自定义主题 CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
    .stApp {
        background-color: #f0faf0;
    }
    section[data-testid="stSidebar"] {
        background-color: #e8f5e9;
    }
    h1, h2, h3 {
        color: #2e7d32 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 会话状态初始化
# ---------------------------------------------------------------------------
if "images" not in st.session_state:
    st.session_state.images = {}
if "selected_key" not in st.session_state:
    st.session_state.selected_key = None

# ---------------------------------------------------------------------------
# 侧边栏：图片上传
# ---------------------------------------------------------------------------
st.sidebar.title("🌿 草场碳排放监测")

uploaded_files = st.sidebar.file_uploader(
    "上传草场照片（JPG / PNG）",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

# 将新上传的图片存入 session_state
if uploaded_files:
    for f in uploaded_files:
        uid = f"{f.name}_{f.size}"
        if uid not in st.session_state.images:
            img = Image.open(f).convert("RGB")
            st.session_state.images[uid] = (f.name, img)

# ---------------------------------------------------------------------------
# 主区域
# ---------------------------------------------------------------------------
st.title("🌿 草场碳排放监测系统")

if not st.session_state.images:
    st.info("请上传草场照片以开始分析")
    st.stop()

# ---- 1) 缩略图行 ----
st.subheader("已上传照片")
items = list(st.session_state.images.items())
cols = st.columns(len(items))

for col, (uid, (fname, img)) in zip(cols, items):
    with col:
        thumb = img.copy()
        thumb.thumbnail((150, 150))
        st.image(thumb, width=150)

        if st.button(f"🔍 {fname}", key=f"btn_{uid}", use_container_width=True):
            st.session_state.selected_key = uid

# ---- 2) 大图显示 ----
if st.session_state.selected_key is not None:
    selected = st.session_state.images.get(st.session_state.selected_key)
    if selected:
        fname, img = selected
        st.subheader(f"原图：{fname}")
        st.image(img, use_container_width=True)

# ---- 3) 碳排趋势图 ----
st.subheader("碳排放趋势轴线图")
st.caption("# TODO: 替换为真实算法")

n = len(st.session_state.images)
values = [100.0]
for _ in range(1, n):
    values.append(round(values[-1] + random.uniform(-5, 20), 1))

df = pd.DataFrame({
    "图片序号": list(range(1, n + 1)),
    "碳排放量 (kg CO₂/ha)": values,
})

st.line_chart(df, x="图片序号", y="碳排放量 (kg CO₂/ha)")
