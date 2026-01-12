import os
from pathlib import Path
import streamlit as st

from utils.layout import sidebar_menu, page_title
from utils.auth import require_login, logout_button

st.set_page_config(
    page_title="رفع البيانات",
    page_icon="📤",
    layout="wide"
)

sidebar_menu(active="upload")
page_title("📤 رفع البيانات")

# 🔒 حماية الصفحة
require_login()

st.success("أنتِ مسجلة دخول ويمكنك رفع البيانات ✅")
logout_button()

st.write("ارفعي ملف Excel وسيتم تحديث الداشبورد تلقائيًا.")

uploaded = st.file_uploader("رفع ملف Excel", type=["xlsx"])

if uploaded:
    Path("data").mkdir(exist_ok=True)
    with open("data/latest.xlsx", "wb") as f:
        f.write(uploaded.getbuffer())

    st.success("✅ تم رفع الملف بنجاح")
    st.info("انتقلي إلى 🏠 الصفحة الرئيسية لمشاهدة الداشبورد المحدّث")
