import streamlit as st


def sidebar_menu(active: str):
    """
    active = home | upload | settings | login
    """

    # إخفاء App الافتراضي فقط (بدون كسر التنقل)
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

    # ✅ روابط رسمية وآمنة
    st.sidebar.page_link(
        "pages/1_🏠_الصفحة_الرئيسية.py",
        label="🏠 الصفحة الرئيسية",
        disabled=(active == "home"),
    )

    st.sidebar.page_link(
        "pages/2_📤_رفع_البيانات.py",
        label="📤 رفع البيانات",
        disabled=(active == "upload"),
    )

    st.sidebar.page_link(
        "pages/3_🎨_الإعدادات.py",
        label="🎨 الإعدادات",
        disabled=(active == "settings"),
    )

    st.sidebar.page_link(
        "pages/4_🔐_تسجيل_الدخول.py",
        label="🔐 تسجيل الدخول",
        disabled=(active == "login"),
    )

    st.sidebar.markdown("<hr class='brand-hr'/>", unsafe_allow_html=True)


def page_title(title: str):
    st.markdown(f"## {title}")
