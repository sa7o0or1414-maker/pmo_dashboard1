import os
from pathlib import Path

import streamlit as st

from utils.layout import render_sidebar_menu, render_page_title
from utils.auth import require_admin

st.set_page_config(page_title="رفع البيانات", page_icon="📤", layout="wide")

render_sidebar_menu(active="upload")
render_page_title("📤 رفع البيانات")

# ✅ لا تفتح إلا للمسجلين (أدمن)
require_admin()

st.write("ارفعي ملف Excel وسيتم حفظه كـ **data/latest.xlsx** وتحديث الداشبورد مباشرة.")

uploaded = st.file_uploader("رفع ملف Excel", type=["xlsx"])

if uploaded is not None:
    Path("data").mkdir(parents=True, exist_ok=True)
    save_path = os.path.join("data", "latest.xlsx")

    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())

    st.success("✅ تم رفع الملف بنجاح. ارجعي للصفحة الرئيسية لعرض التحديث.")
