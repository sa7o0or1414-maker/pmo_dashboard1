import os
import streamlit as st


def apply_sidebar_style():
    st.markdown(
        """
        <style>
        /* اخفاء Navigation الافتراضي اللي يظهر فيه App */
        div[data-testid="stSidebarNav"] { display: none !important; }

        section[data-testid="stSidebar"] { padding-top: 10px; }

        .brand-title { text-align:center; font-size:20px; font-weight:800; margin:8px 0 4px 0; }
        .brand-sub   { text-align:center; font-size:14px; opacity:0.9; margin:0 0 12px 0; }
        .brand-hr    { border:0; border-top:1px solid rgba(255,255,255,0.18); margin:12px 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _list_pages_files():
    pages_dir = "pages"
    if not os.path.isdir(pages_dir):
        return []
    return sorted([f for f in os.listdir(pages_dir) if f.endswith(".py") and not f.startswith("_")])


def _find_page_path(keywords_ar=None, keywords_en=None):
    """
    يرجّع مسار صفحة داخل pages/ بالبحث في اسم الملف.
    """
    keywords_ar = keywords_ar or []
    keywords_en = keywords_en or []
    files = _list_pages_files()

    # عربي
    if keywords_ar:
        for f in files:
            name = f.lower()
            if all(k.lower() in name for k in keywords_ar):
                return f"pages/{f}"

    # انجليزي
    if keywords_en:
        for f in files:
            name = f.lower()
            if all(k.lower() in name for k in keywords_en):
                return f"pages/{f}"

    return None


def render_sidebar_menu(active: str):
    """
    active: home | upload | settings | login
    """
    apply_sidebar_style()

    st.sidebar.markdown(
        """
        <div class="brand-title">🏠 الصفحة الرئيسية</div>
        <div class="brand-sub">📊 لوحة المعلومات</div>
        <hr class="brand-hr"/>
        """,
        unsafe_allow_html=True,
    )

    # اكتشاف الصفحات تلقائيًا (بدون مسارات ثابتة)
    upload_page = _find_page_path(keywords_ar=["رفع"], keywords_en=["upload"])
    settings_page = _find_page_path(keywords_ar=["الإعدادات"], keywords_en=["settings"]) or \
                    _find_page_path(keywords_ar=["اعدادات"], keywords_en=["settings"])
    login_page = _find_page_path(keywords_ar=["تسجيل"], keywords_en=["login"])

    # زر الصفحة الرئيسية: يرجّع للرابط الرئيسي (app.py) بدون switch_page
    # نستخدم query param بسيط ثم rerun، و app.py يرجّع يفتح الداشبورد
    if st.sidebar.button("🏠 الصفحة الرئيسية", use_container_width=True, disabled=(active == "home")):
        st.experimental_set_query_params(home="1")
        st.rerun()

    def go_button(label, target, is_active):
        if st.sidebar.button(label, use_container_width=True, disabled=is_active):
            if target:
                st.switch_page(target)
            else:
                st.sidebar.error("الصفحة غير موجودة داخل مجلد pages. تأكدي من اسم الملف.")

    go_button("📤 رفع البيانات", upload_page, active == "upload")
    go_button("🎨 الإعدادات", settings_page, active == "settings")
    go_button("🔐 تسجيل الدخول", login_page, active == "login")

    st.sidebar.markdown("<hr class='brand-hr'/>", unsafe_allow_html=True)


def render_page_title(title: str):
    st.markdown(f"## {title}")
