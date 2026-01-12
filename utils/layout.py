import os
import streamlit as st


def _sidebar_css():
    st.markdown(
        """
        <style>
        div[data-testid="stSidebarNav"] { display: none !important; }
        .brand-title { text-align:center; font-size:20px; font-weight:800; margin:8px 0 4px 0; }
        .brand-sub { text-align:center; font-size:14px; opacity:0.85; margin-bottom:12px; }
        .brand-hr { border:0; border-top:1px solid rgba(255,255,255,0.25); margin:12px 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _list_pages():
    if not os.path.isdir("pages"):
        return []
    return sorted([f for f in os.listdir("pages") if f.endswith(".py")])


def _find_page(keyword: str):
    """
    يرجّع مسار صفحة من pages/ بمجرد وجود كلمة في اسم الملف (مثل: رفع، الإعدادات، تسجيل، الصفحة_الرئيسية)
    """
    for f in _list_pages():
        if keyword in f:
            return f"pages/{f}"
    return None


def _safe_switch(path: str):
    if not path:
        st.sidebar.error("الصفحة غير موجودة داخل مجلد pages.")
        return
    if not os.path.exists(path):
        st.sidebar.error(f"الصفحة غير موجودة: {path}")
        return
    st.switch_page(path)


def sidebar_menu(active: str):
    """
    active = home | upload | settings | login
    """
    _sidebar_css()

    st.sidebar.markdown(
        """
        <div class="brand-title">🏠 الصفحة الرئيسية</div>
        <div class="brand-sub">📊 لوحة المعلومات</div>
        <hr class="brand-hr"/>
        """,
        unsafe_allow_html=True,
    )

    home_page = _find_page("الصفحة_الرئيسية") or _find_page("الصفحة الرئيسية") or _find_page("🏠")
    upload_page = _find_page("رفع_البيانات") or _find_page("رفع البيانات") or _find_page("📤")
    settings_page = _find_page("الإعدادات") or _find_page("اعدادات") or _find_page("🎨")
    login_page = _find_page("تسجيل_الدخول") or _find_page("تسجيل الدخول") or _find_page("🔐")

    def btn(label, target, is_active):
        if st.sidebar.button(label, use_container_width=True, disabled=is_active):
            _safe_switch(target)

    btn("🏠 الصفحة الرئيسية", home_page, active == "home")
    btn("📤 رفع البيانات", upload_page, active == "upload")
    btn("🎨 الإعدادات", settings_page, active == "settings")
    btn("🔐 تسجيل الدخول", login_page, active == "login")

    st.sidebar.markdown("<hr class='brand-hr'/>", unsafe_allow_html=True)


def page_title(title: str):
    st.markdown(f"## {title}")
