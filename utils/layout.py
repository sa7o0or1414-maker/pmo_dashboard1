import os
import streamlit as st

def _list_pages_files():
    pages_dir = "pages"
    if not os.path.isdir(pages_dir):
        return []
    files = []
    for f in os.listdir(pages_dir):
        if f.endswith(".py") and not f.startswith("_"):
            files.append(f)
    return sorted(files)

def _find_page_path(keywords_ar=None, keywords_en=None):
    """
    يبحث عن صفحة داخل pages/ باستخدام كلمات مفتاحية.
    يدعم اختلاف الأرقام/الإيموجي/الأسماء.
    """
    keywords_ar = keywords_ar or []
    keywords_en = keywords_en or []

    pages = _list_pages_files()

    # 1) جرّب كلمات عربية
    if keywords_ar:
        for f in pages:
            name = f.lower()
            ok = all(k.lower() in name for k in keywords_ar)
            if ok:
                return f"pages/{f}"

    # 2) جرّب كلمات انجليزية
    if keywords_en:
        for f in pages:
            name = f.lower()
            ok = all(k.lower() in name for k in keywords_en)
            if ok:
                return f"pages/{f}"

    return None

def apply_sidebar_style():
    """
    يخفي Sidebar Navigation الافتراضي اللي يظهر فيه (App)
    """
    st.markdown(
        """
        <style>
        /* Hide Streamlit default pages navigation (removes App header everywhere) */
        div[data-testid="stSidebarNav"] { display: none !important; }

        /* Slight sidebar padding */
        section[data-testid="stSidebar"] { padding-top: 10px; }

        /* Center our custom brand blocks */
        .pmo-brand-title { text-align:center; font-size:20px; font-weight:800; margin:8px 0 4px 0; }
        .pmo-brand-sub { text-align:center; font-size:14px; opacity:0.9; margin:0 0 12px 0; }

        /* Divider */
        .pmo-hr { border:0; border-top:1px solid rgba(255,255,255,0.18); margin:12px 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar_menu(active: str = "home"):
    """
    يرسم البار اليمين بنفس الشكل في كل الصفحات
    active: home | upload | settings | login
    """
    apply_sidebar_style()

    st.sidebar.markdown(
        """
        <div class="pmo-brand-title">🏠 الصفحة الرئيسية</div>
        <div class="pmo-brand-sub">📊 لوحة المعلومات</div>
        <hr class="pmo-hr"/>
        """,
        unsafe_allow_html=True,
    )

    # اكتشاف صفحات المشروع تلقائياً
    upload_page = _find_page_path(keywords_ar=["رفع"], keywords_en=["upload"])
    settings_page = _find_page_path(keywords_ar=["الإعدادات"], keywords_en=["settings"])
    if settings_page is None:
        settings_page = _find_page_path(keywords_ar=["اعدادات"], keywords_en=["settings"])
    login_page = _find_page_path(keywords_ar=["تسجيل"], keywords_en=["login"])

    # أزرار تنقل
    def _go(path):
        if path:
            st.switch_page(path)
        else:
            st.sidebar.error("لم أجد الصفحة داخل مجلد pages.")

    # زر الصفحة الرئيسية (يرجع للـ app.py)
    # لا يوجد switch_page لـ app.py، لذلك نستخدم rerun مع توضيح:
    if st.sidebar.button("🏠 الصفحة الرئيسية", use_container_width=True, disabled=(active == "home")):
        # الرجوع للصفحة الرئيسية (app.py)
        st.experimental_set_query_params()  # تنظيف
        st.rerun()

    if st.sidebar.button("📤 رفع البيانات", use_container_width=True, disabled=(active == "upload")):
        _go(upload_page)

    if st.sidebar.button("🎨 الإعدادات", use_container_width=True, disabled=(active == "settings")):
        _go(settings_page)

    if st.sidebar.button("🔐 تسجيل الدخول", use_container_width=True, disabled=(active == "login")):
        _go(login_page)

    st.sidebar.markdown("<hr class='pmo-hr'/>", unsafe_allow_html=True)

def render_header(page_title_fallback: str = "📊 لوحة المعلومات"):
    """
    هيدر بسيط أعلى الصفحة. (إذا عندك لوقو/لغة في ملف ثاني، خليهم هناك)
    """
    st.markdown(f"## {page_title_fallback}")
