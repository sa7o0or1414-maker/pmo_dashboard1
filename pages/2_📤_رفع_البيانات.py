import os
from pathlib import Path
import streamlit as st

from utils.layout import sidebar_menu, page_title
import utils.auth as auth  # ✅ بدل from-import

st.set_page_config(page_title="رفع البيانات", page_icon="📤", layout="wide")

sidebar_menu(active="upload")
page_title("📤 رفع البيانات")

# 🔒 حماية الصفحة
auth.require_login()

st.success("✅ مسجل دخول — يمكنك رفع ملف Excel الآن")
auth.logout_button()

uploaded = st.file_uploader("ارفع ملف Excel (xlsx)", type=["xlsx"])

if uploaded:
    Path("data").mkdir(exist_ok=True)
    save_path = os.path.join("data", "latest.xlsx")

    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())

    st.success("✅ تم رفع الملف وتحديثه بنجاح")
    st.info("اذهبي إلى 🏠 الصفحة الرئيسية لمشاهدة الداشبورد بعد التحديث")
