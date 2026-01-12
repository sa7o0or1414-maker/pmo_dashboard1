import os
from pathlib import Path
import streamlit as st

from utils.layout import sidebar_menu, page_title

st.set_page_config(page_title="رفع البيانات", page_icon="📤", layout="wide")

sidebar_menu(active="upload")
page_title("📤 رفع البيانات")

# --------------------------------------------------
# Auth (مُدمج داخل الصفحة) — حل مضمون بدون utils.auth
# --------------------------------------------------
def _get_admin_password() -> str:
    # لو عندك Secrets في Streamlit Cloud
    if "ADMIN_PASSWORD" in st.secrets:
        return str(st.secrets["ADMIN_PASSWORD"])
    # مؤقتًا: غيّريها
    return "admin123"

def _is_logged_in() -> bool:
    return bool(st.session_state.get("logged_in", False))

def _login_form():
    st.subheader("🔐 تسجيل الدخول للمسؤول")
    pwd = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل الدخول", use_container_width=True):
        if pwd == _get_admin_password():
            st.session_state["logged_in"] = True
            st.success("✅ تم تسجيل الدخول")
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")

def _logout_button():
    if st.button("تسجيل الخروج", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()

# حماية الصفحة
if not _is_logged_in():
    st.warning("هذه الصفحة للمسؤول فقط. سجّلي الدخول للمتابعة.")
    _login_form()
    st.stop()

# --------------------------------------------------
# بعد تسجيل الدخول: رفع الإكسل مثل أول
# --------------------------------------------------
st.success("✅ مسجل دخول — يمكنك رفع ملف Excel الآن")
_logout_button()

uploaded = st.file_uploader("ارفع ملف Excel (xlsx)", type=["xlsx"])

if uploaded:
    Path("data").mkdir(exist_ok=True)
    save_path = os.path.join("data", "latest.xlsx")

    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())

    st.success("✅ تم رفع الملف وتحديثه بنجاح")
    st.info("اذهبي إلى 🏠 الصفحة الرئيسية لمشاهدة الداشبورد بعد التحديث")
