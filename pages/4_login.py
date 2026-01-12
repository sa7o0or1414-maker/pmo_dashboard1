import streamlit as st

st.set_page_config(page_title="تسجيل الدخول", page_icon="🔐", layout="wide")
st.title("🔐 تسجيل الدخول")

pwd = st.text_input("كلمة المرور", type="password")
if st.button("تسجيل الدخول", use_container_width=True):
    if pwd == "admin123":
        st.session_state.logged_in = True
        st.success("✅ تم تسجيل الدخول")
    else:
        st.error("❌ كلمة المرور غير صحيحة")

if st.session_state.get("logged_in", False):
    if st.button("تسجيل الخروج", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
