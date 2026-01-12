import streamlit as st
from utils.layout import render_sidebar_menu, render_header
from utils.auth import require_admin
from utils.settings import load_settings, save_settings, DEFAULT_SETTINGS

st.set_page_config(page_title="الإعدادات", page_icon="🎨", layout="wide")

render_sidebar_menu(active="settings")
render_header(page_title_fallback="🎨 الإعدادات")

require_admin()

settings = load_settings()

st.subheader("إعدادات سريعة")
st.write("هنا تضيفين إعداداتك (ألوان/لوقو/خريطة...)")

c1, c2 = st.columns(2)
with c1:
    if st.button("💾 حفظ (تجريبي)"):
        save_settings(settings)
        st.success("تم الحفظ ✅")

with c2:
    if st.button("↩️ استرجاع الافتراضي"):
        save_settings(DEFAULT_SETTINGS)
        st.success("تم الاسترجاع ✅")
        st.rerun()
