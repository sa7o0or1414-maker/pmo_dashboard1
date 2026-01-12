import streamlit as st
from utils.layout import render_header

st.set_page_config(page_title="تسجيل الدخول", layout="wide")
render_header(page_title_fallback="🔐 تسجيل الدخول")

from utils.auth import login_form, is_admin

st.set_page_config(page_title="تسجيل الدخول", layout="wide")
render_header(page_title_fallback="🔐 تسجيل دخول الأدمن")

if is_admin():
    st.success("أنتِ مسجلة دخول كأدمن ✅")
    st.info("تقدرين الآن تروحين لصفحات (رفع البيانات) و(الإعدادات).")

login_form()
