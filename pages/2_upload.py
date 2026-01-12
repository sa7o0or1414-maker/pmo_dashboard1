from pathlib import Path
import streamlit as st

st.set_page_config(page_title="رفع البيانات", page_icon="📤", layout="wide")
st.title("📤 رفع البيانات")

# حماية
if not st.session_state.get("logged_in", False):
    st.warning("هذه الصفحة للمسؤول فقط")
    pwd = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل الدخول", use_container_width=True):
        if pwd == "admin123":
            st.session_state.logged_in = True
            st.success("✅ تم تسجيل الدخول")
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")
    st.stop()

st.success("✅ مسجل دخول — ارفع ملف Excel")
if st.button("تسجيل الخروج", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

uploaded = st.file_uploader("ارفع ملف Excel (xlsx)", type=["xlsx"])

if uploaded:
    Path("data").mkdir(exist_ok=True)
    with open("data/latest.xlsx", "wb") as f:
        f.write(uploaded.getbuffer())
    st.success("✅ تم رفع الملف وتحديثه")
    st.info("اذهبي إلى (الصفحة الرئيسية) لمشاهدة الداشبورد بعد التحديث")
