import streamlit as st

def apply_sidebar_css():
    st.markdown(
        """
        <style>
        /* اخفاء القائمة الافتراضية اللي يظهر فيها App */
        div[data-testid="stSidebarNav"] { display: none !important; }

        .brand-title{ text-align:center; font-size:20px; font-weight:800; margin:8px 0 4px 0; }
        .brand-sub{ text-align:center; font-size:14px; opacity:0.9; margin:0 0 12px 0; }
        .brand-hr{ border:0; border-top:1px solid rgba(255,255,255,0.18); margin:12px 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def sidebar_menu(active: str):
    """
    active: home | upload
    """
    apply_sidebar_css()

    st.sidebar.markdown(
        """
        <div class="brand-title">🏠 الصفحة الرئيسية</div>
        <div class="brand-sub">📊 لوحة المعلومات</div>
        <hr class="brand-hr"/>
        """,
        unsafe_allow_html=True,
    )

    def nav_btn(label, target, is_active):
        if st.sidebar.button(label, use_container_width=True, disabled=is_active):
            st.switch_page(target)

    nav_btn("🏠 الصفحة الرئيسية", "pages/1_🏠_الصفحة_الرئيسية.py", active == "home")
    nav_btn("📤 رفع البيانات", "pages/2_📤_رفع_البيانات.py", active == "upload")

    st.sidebar.markdown("<hr class='brand-hr'/>", unsafe_allow_html=True)

def page_title(title: str):
    st.markdown(f"## {title}")
