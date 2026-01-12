import streamlit as st
from pathlib import Path

st.set_page_config(page_title="رفع البيانات", page_icon="📤", layout="wide")

st.title("📤 رفع البيانات")

if not st.session_state.get("logged_in", False):
    st.warning("هذه الصفحة للمسؤول فقط")
    pwd = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل الدخول"):
        if pwd == "admin123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة")
    st.stop()

uploaded = st.file_uploader("ارفع ملف Excel", type=["xlsx"])

if uploaded:
    Path("data").mkdir(exist_ok=True)
    with open("data/latest.xlsx", "wb") as f:
        f.write(uploaded.getbuffer())
    st.success("تم رفع الملف بنجاح")
