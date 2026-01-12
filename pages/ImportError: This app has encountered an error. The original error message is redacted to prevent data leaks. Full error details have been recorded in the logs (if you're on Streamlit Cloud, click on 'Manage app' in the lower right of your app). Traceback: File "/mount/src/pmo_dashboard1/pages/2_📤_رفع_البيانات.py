import streamlit as st
from pathlib import Path
import os

from utils.layout import sidebar_menu, page_title

st.set_page_config(page_title="رفع البيانات", page_icon="📤", layout="wide")

sidebar_menu(active="upload")
page_title("📤 رفع البيانات")

uploaded = st.file_uploader("رفع ملف Excel", type=["xlsx"])

if uploaded:
    Path("data").mkdir(exist_ok=True)
    with open("data/latest.xlsx", "wb") as f:
        f.write(uploaded.getbuffer())
    st.success("تم رفع الملف بنجاح ✅ انتقلي للداشبورد لمشاهدة التحليل")
