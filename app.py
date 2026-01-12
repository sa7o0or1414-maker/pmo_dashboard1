import streamlit as st
from pathlib import Path

from utils.settings import load_settings
from utils.style import apply_theme

st.set_page_config(page_title="PMO Portal", layout="wide")

settings = load_settings()
theme = settings["theme"]
logo = settings["logo"]

apply_theme(theme, logo)

uploaded_logo = st.sidebar.file_uploader("رفع لوقو (للعرض المؤقت)", type=["png","jpg","jpeg"])

def render_logo():
    if not logo.get("enabled", True):
        return

    st.markdown("<div class='pmo-logo-wrap'>", unsafe_allow_html=True)

    if uploaded_logo:
        st.image(uploaded_logo, width=int(logo.get("width", 160)))
    else:
        # لوقو ثابت من الريبو (اختياري)
        path = Path("assets") / "logo.png"
        if path.exists():
            st.image(str(path), width=int(logo.get("width", 160)))

    st.markdown("</div>", unsafe_allow_html=True)

# مكان اللوقو
if logo.get("location", "header") == "sidebar":
    with st.sidebar:
        render_logo()
else:
    render_logo()

st.markdown(
    """
    <h1 style="margin-bottom:0;">PMO Portal</h1>
    <p style="opacity:0.85;margin-top:6px;">تحديث أسبوعي عبر Excel + داشبورد تفاعلي + صلاحيات</p>
    """,
    unsafe_allow_html=True
)

st.info("من القائمة الجانبية: رفع البيانات → الداشبورد → الإعدادات (للأدمن فقط)")
