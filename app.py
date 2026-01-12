import streamlit as st
from utils.style import apply_theme

st.set_page_config(page_title="PMO Portal", layout="wide")

# حفظ الإعدادات في الجلسة
if "theme" not in st.session_state:
    st.session_state.theme = {
        "primary": "#3B82F6",
        "bg": "#0B1220",
        "card_bg": "#111B2E",
        "text": "#E5E7EB",
        "logo_width": 160,
        "radius": 18,
    }

st.sidebar.title("🎨 تخصيص الواجهة")

st.session_state.theme["primary"] = st.sidebar.color_picker("لون أساسي", st.session_state.theme["primary"])
st.session_state.theme["bg"] = st.sidebar.color_picker("لون الخلفية", st.session_state.theme["bg"])
st.session_state.theme["card_bg"] = st.sidebar.color_picker("لون الكروت/الصناديق", st.session_state.theme["card_bg"])
st.session_state.theme["text"] = st.sidebar.color_picker("لون النص", st.session_state.theme["text"])

st.session_state.theme["logo_width"] = st.sidebar.slider("حجم اللوقو", 60, 320, st.session_state.theme["logo_width"])
st.session_state.theme["radius"] = st.sidebar.slider("انحناء الزوايا", 8, 28, st.session_state.theme["radius"])

uploaded_logo = st.sidebar.file_uploader("ارفع لوقو (اختياري)", type=["png", "jpg", "jpeg"])

# تطبيق الثيم
apply_theme(
    primary=st.session_state.theme["primary"],
    bg=st.session_state.theme["bg"],
    card_bg=st.session_state.theme["card_bg"],
    text=st.session_state.theme["text"],
    logo_width=st.session_state.theme["logo_width"],
    radius=st.session_state.theme["radius"],
)

# عرض اللوقو (من رفع المستخدم أو افتراضي)
if uploaded_logo:
    st.markdown('<div class="pmo-logo">', unsafe_allow_html=True)
    st.image(uploaded_logo)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # لو عندك ملف ثابت داخل الريبو
    # st.image("assets/logo.png", width=st.session_state.theme["logo_width"])
    st.markdown("")

st.markdown(
    """
    <h1 style="margin-bottom:0;">PMO Portal</h1>
    <p style="opacity:0.85;margin-top:6px;">تحديث أسبوعي عبر Excel + داشبورد تفاعلي + صلاحيات</p>
    """,
    unsafe_allow_html=True
)
st.info("من القائمة الجانبية: رفع البيانات → الداشبورد")
