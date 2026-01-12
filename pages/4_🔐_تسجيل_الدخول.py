import streamlit as st
from utils.layout import sidebar_menu, page_title
from utils.auth import login_form, is_logged_in, logout_button

st.set_page_config(
    page_title="تسجيل الدخول",
    page_icon="🔐",
    layout="wide"
)

sidebar_menu(active="login")
page_title("🔐 تسجيل الدخول")

if is_logged_in():
    st.success("أنتِ مسجلة دخول بالفعل ✅")
    logout_button()
else:
    login_form()
