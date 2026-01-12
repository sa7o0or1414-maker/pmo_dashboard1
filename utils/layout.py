import streamlit as st
import os

def sidebar_menu(active: str):
    """
    active = dashboard | upload | settings | login
    """

    # إخفاء App الافتراضية
    st.markdown("""
    <style>
    div[data-testid="stSidebarNav"] { display: none !important; }
    .brand-title { text-align:center; font-size:20px; font-weight:800; margin:8px 0 4px 0; }
    .brand-sub { text-align:center; font-size:14px; opacity:0.85; margin-bottom:12px; }
    .brand-hr { border:0; border-top:1px solid rgba(255,255,255,0.25); margin:12px 0; }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div class="brand-title">🏠 الصفحة الرئيسية</div>
    <div class="brand-sub">📊 لوحة المعلومات</div>
    <hr class="brand-hr"/>
    """, unsafe_allow_html=True)

    def go(label, path, is_active):
        if st.sidebar.button(label, use_container_width=True, disabled=is_active):
            st.switch_page(path)

    go("📊 الداشبورد", "pages/1_🏠_الداشبورد.py", active == "dashboard")
    go("📤 رفع البيانات", "pages/2_📤_رفع_البيانات.py", active == "upload")
    go("🎨 الإعدادات", "pages/3_🎨_الإعدادات.py", active == "settings")
    go("🔐 تسجيل الدخول", "pages/4_🔐_تسجيل_الدخول.py", active == "login")

    st.sidebar.markdown("<hr class='brand-hr'/>", unsafe_allow_html=True)


def page_title(title: str):
    st.markdown(f"## {title}")
