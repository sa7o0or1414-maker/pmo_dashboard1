import os
import streamlit as st

# --------------------------------------------------
# CSS – إخفاء App وتنظيم السايدبار
# --------------------------------------------------
def _sidebar_css():
    st.markdown(
        """
        <style>
        div[data-testid="stSidebarNav"] { display: none !important; }
        section[data-testid="stSidebar"] { padding-top: 10px; }

        .brand-title {
            text-align: center;
            font-size: 20px;
            font-weight: 800;
            margin: 8px 0 4px 0;
        }
        .brand-sub {
            text-align: center;
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 12px;
        }
        .brand-hr {
            border: 0;
            border-top: 1px solid rgba(255,255,255,0.2);
            margin: 12px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# أدوات مساعدة
# --------------------------------------------------
def _page_exists(filename: str) -> bool:
    return os.path.exists(os.path.join("pages", filename))

def _safe_switch(filename: str):
    path = f"pages/{filename}"
    if _page_exists(filename):
        st.switch_page(path)
    else:
        st.warning(f"الصفحة غير موجودة: {filename}")

# --------------------------------------------------
# Sidebar Menu
# --------------------------------------------------
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

    # 🔹 الصفحة الرئيسية (بدون switch_page)
    if st.sidebar.button(
        "🏠 الصفحة الرئيسية",
        use_container_width=True,
        disabled=(active == "home"),
    ):
        # نعيد تشغيل الصفحة الحالية
        # والداشبورد أصلاً هو الصفحة الرئيسية
        st.experimental_set_query_params()
        st.rerun()

    # 🔹 رفع البيانات
    if st.sidebar.button(
        "📤 رفع البيانات",
        use_container_width=True,
        disabled=(active == "upload"),
    ):
        _safe_switch("2_📤_رفع_البيانات.py")

    # 🔹 الإعدادات
    if st.sidebar.button(
        "🎨 الإعدادات",
        use_container_width=True,
        disabled=(active == "settings"),
    ):
        _safe_switch("3_🎨_الإعدادات.py")

    # 🔹 تسجيل الدخول
    if st.sidebar.button(
        "🔐 تسجيل الدخول",
        use_container_width=True,
        disabled=(active == "login"),
    ):
        _safe_switch("4_🔐_تسجيل_الدخول.py")

    st.sidebar.markdown("<hr class='brand-hr'/>", unsafe_allow_html=True)

# --------------------------------------------------
# عنوان الصفحة
# --------------------------------------------------
def page_title(title: str):
    st.markdown(f"## {title}")
