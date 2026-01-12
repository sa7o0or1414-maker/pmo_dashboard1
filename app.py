import streamlit as st
from pathlib import Path

from utils.settings import load_settings
from utils.style import apply_theme

st.set_page_config(page_title="PMO Portal", layout="wide")

# 1) تحميل الإعدادات وتعريف المتغيرات
settings = load_settings()
theme = settings.get("theme", {})
logo = settings.get("logo", {})
texts = settings.get("texts", {})

# 2) تطبيق الثيم على الصفحة
apply_theme(theme, logo)

# (اختياري) رفع لوقو مؤقت للتجربة (لا يُحفظ)
uploaded_logo = st.sidebar.file_uploader("رفع لوقو (مؤقت للتجربة)", type=["png", "jpg", "jpeg"])

def render_logo():
    if not logo.get("enabled", True):
        return

    st.markdown("<div class='pmo-logo-wrap'>", unsafe_allow_html=True)

    w = int(logo.get("width", 160))
    saved_logo = Path(logo.get("file_path", "data/logo.png"))
    repo_logo = Path("assets") / "logo.png"

    if uploaded_logo:
        st.image(uploaded_logo, width=w)
    elif saved_logo.exists():
        st.image(str(saved_logo), width=w)
    elif repo_logo.exists():
        st.image(str(repo_logo), width=w)

    st.markdown("</div>", unsafe_allow_html=True)

# 3) مكان اللوقو (Header أو Sidebar)
if logo.get("location", "header") == "sidebar":
    with st.sidebar:
        render_logo()
else:
    render_logo()

# 4) عنوان الصفحة الرئيسية
st.markdown(
    """
    <h1 style="margin-bottom:0;">PMO Portal</h1>
    <p style="opacity:0.85;margin-top:6px;">تحديث أسبوعي عبر Excel + داشبورد تفاعلي + صلاحيات</p>
    """,
    unsafe_allow_html=True
)

st.info("من القائمة الجانبية: رفع البيانات → الداشبورد → الإعدادات (Admin)")
