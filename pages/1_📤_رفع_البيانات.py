import os
from pathlib import Path

import streamlit as st

from utils.layout import render_sidebar_menu, render_header
from utils.auth import require_admin

st.set_page_config(page_title="رفع البيانات", page_icon="📤", layout="wide")

render_sidebar_menu(active="upload")
render_header(page_title_fallback="📤 رفع البيانات")

require_admin()

st.subheader("رفع ملف Excel لتحديث الداشبورد")
uploaded = st.file_uploader("ارفع ملف Excel", type=["xlsx"])

if uploaded is not None:
    Path("data").mkdir(parents=True, exist_ok=True)
    save_path = os.path.join("data", "latest.xlsx")
    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())
    st.success("✅ تم رفع الملف وتحديثه. ارجعي للصفحة الرئيسية لعرض النتائج.")
