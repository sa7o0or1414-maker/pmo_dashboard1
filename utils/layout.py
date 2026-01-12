import streamlit as st
from utils.settings import load_settings

def apply_global_sidebar_branding():
    """
    يخفي الـ Navigation الافتراضي (اللي فيه App) ويضع عنوان ثابت
    'الصفحة الرئيسية' في كل الصفحات.
    """
    st.markdown(
        """
        <style>
        /* اخفاء قائمة الصفحات الافتراضية بالكامل (وتختفي معها كلمة App) */
        div[data-testid="stSidebarNav"] { display: none !important; }

        /* توسيط أي عناوين مخصصة داخل السايدبار */
        section[data-testid="stSidebar"] .brand-title { 
            text-align: center; 
            font-size: 20px; 
            font-weight: 800; 
            margin-top: 8px; 
            margin-bottom: 6px;
        }
        section[data-testid="stSidebar"] .brand-subtitle { 
            text-align: center; 
            font-size: 14px; 
            opacity: 0.9; 
            margin-bottom: 12px;
        }
        section[data-testid="stSidebar"] hr { opacity: 0.25; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        """
        <div class="brand-title">🏠 الصفحة الرئيسية</div>
        <div class="brand-subtitle">لوحة المعلومات</div>
        <hr/>
        """,
        unsafe_allow_html=True,
    )


def render_header(title_key_base: str = None, page_title_fallback: str = ""):
    """
    هيدر أعلى الصفحة (أنتِ عندك سابقاً لوقو/لغة… نتركه كما هو قدر الإمكان)
    + نطبق العلامة التجارية للسايدبار في كل صفحة
    """
    apply_global_sidebar_branding()

    # لو عندك هيدر أقدم (لوقو + عنوان + لغة) استمري عليه
    # هنا نخلي عنوان الصفحة يظهر كـ fallback
    if page_title_fallback:
        st.markdown(f"## {page_title_fallback}")
