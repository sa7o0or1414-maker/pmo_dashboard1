import os
from pathlib import Path
import streamlit as st

from utils.layout import sidebar_menu, page_title
from utils.auth import require_login, logout_button

st.set_page_config(page_title="رفع البيانات", page_icon="📤", layout="wide")

sidebar_menu(active="upload")
page_title("📤 رفع البيانات")

# 🔒 حماية الصفحة: لو ما فيه دخول، يظهر نموذج الدخول داخل نفس الصفحة
require_login()

# ✅ بعد تسجيل الدخول يظهر رفع الإكسل مباشرة (مثل أول)
st.success("تم تسجيل الدخول ✅ يمكنك رفع ملف Excel الآن")
logout_button()

uploaded = st.file_uploader("ارفع ملف Excel (xlsx)", type=["xlsx"])

if uploaded:
    Path("data").mkdir(exist_ok=True)
    save_path = os.path.join("data", "latest.xlsx")
    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())

    st.success("✅ تم رفع الملف وتحديثه بنجاح")
    st.info("اذهبي إلى 🏠 الصفحة الرئيسية لمشاهدة الداشبورد بعد التحديث")
