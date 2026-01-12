import streamlit as st
from utils.layout import render_sidebar_menu, render_page_title
from utils.auth import login_form, is_admin, logout

st.set_page_config(page_title="تسجيل الدخول", page_icon="🔐", layout="wide")
render_sidebar_menu(active="login")
render_page_title("🔐 تسجيل الدخول")

if is_admin():
    st.success("أنتِ مسجلة دخول كأدمن ✅")
    if st.button("تسجيل خروج"):
        logout()
        st.rerun()

login_form()
