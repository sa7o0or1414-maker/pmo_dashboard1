import streamlit as st

def apply_sidebar_style():
    st.markdown(
        """
        <style>
        /* hide Streamlit default navigation (App) everywhere */
        div[data-testid="stSidebarNav"] { display: none !important; }

        section[data-testid="stSidebar"] { padding-top: 10px; }

        .brand-title { text-align:center; font-size:20px; font-weight:800; margin:8px 0 4px 0; }
        .brand-sub   { text-align:center; font-size:14px; opacity:0.9; margin:0 0 12px 0; }
        .brand-hr    { border:0; border-top:1px solid rgba(255,255,255,0.18); margin:12px 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )

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

    def nav_button(label: str, target: str, is_active: bool):
        if st.sidebar.button(label, use_container_width=True, disabled=is_active):
            st.switch_page(target)

    nav_button("🏠 الصفحة الرئيسية", "pages/1_🏠_الصفحة_الرئيسية.py", active == "home")
    nav_button("📤 رفع البيانات", "pages/2_📤_رفع_البيانات.py", active == "upload")
    nav_button("🎨 الإعدادات", "pages/3_🎨_الإعدادات.py", active == "settings")
    nav_button("🔐 تسجيل الدخول", "pages/4_🔐_تسجيل_الدخول.py", active == "login")

    st.sidebar.markdown("<hr class='brand-hr'/>", unsafe_allow_html=True)

def render_page_title(title: str):
    st.markdown(f"## {title}")
