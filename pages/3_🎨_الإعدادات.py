import streamlit as st
from pathlib import Path

from utils.layout import sidebar_menu, page_title
from utils.settings import load_settings, save_settings

st.set_page_config(
    page_title="الإعدادات",
    page_icon="🎨",
    layout="wide"
)

# السايدبار الموحد
sidebar_menu(active="settings")
page_title("🎨 الإعدادات")

# --------------------------------------------------
# تحميل الإعدادات
# --------------------------------------------------
settings = load_settings()

theme = settings.setdefault("theme", {})
texts = settings.setdefault("texts", {})
charts = settings.setdefault("charts", {})
logo = settings.setdefault("logo", {})

# قيم افتراضية
theme.setdefault("primary", "#2563EB")
theme.setdefault("background", "#0F172A")
theme.setdefault("card", "#111827")
theme.setdefault("text", "#E5E7EB")

charts.setdefault("palette", ["#2563EB", "#22C55E", "#F59E0B", "#EF4444"])
charts.setdefault("style", "modern")

logo.setdefault("enabled", True)
logo.setdefault("width", 160)
logo.setdefault("path", "data/logo.png")

texts.setdefault("dashboard_title", "📊 لوحة المعلومات")

# --------------------------------------------------
# الواجهة
# --------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("🎨 ألوان الموقع")

    theme["primary"] = st.color_picker("اللون الأساسي", theme["primary"])
    theme["background"] = st.color_picker("الخلفية", theme["background"])
    theme["card"] = st.color_picker("لون الكروت", theme["card"])
    theme["text"] = st.color_picker("لون النص", theme["text"])

    st.markdown("### 📊 ألوان الشارتات")
    palette = charts.get("palette", [])
    if "palette_work" not in st.session_state:
        st.session_state.palette_work = palette.copy()

    new_color = st.color_picker("إضافة لون جديد", "#22C55E")
    if st.button("➕ إضافة لون"):
        st.session_state.palette_work.append(new_color)

    for i, c in enumerate(st.session_state.palette_work):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(
                f"<div style='height:24px;border-radius:6px;background:{c}'></div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.session_state.palette_work[i] = st.color_picker(
                f"لون {i+1}", c, key=f"pal_{i}"
            )

    charts["palette"] = st.session_state.palette_work

with right:
    st.subheader("🧩 إعدادات عامة")

    texts["dashboard_title"] = st.text_input(
        "عنوان لوحة المعلومات",
        value=texts["dashboard_title"]
    )

    st.markdown("---")
    st.subheader("🖼️ اللوقو")

    logo["enabled"] = st.toggle("إظهار اللوقو", value=logo["enabled"])
    logo["width"] = st.slider("عرض اللوقو (px)", 80, 300, logo["width"])

    uploaded_logo = st.file_uploader(
        "رفع لوقو (PNG / JPG)",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_logo is not None:
        Path("data").mkdir(exist_ok=True)
        logo_path = Path(logo["path"])
        with open(logo_path, "wb") as f:
            f.write(uploaded_logo.getbuffer())
        st.success("تم حفظ اللوقو بنجاح ✅")

    if Path(logo["path"]).exists():
        st.image(logo["path"], width=logo["width"])

# --------------------------------------------------
# حفظ الإعدادات
# --------------------------------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("💾 حفظ الإعدادات", use_container_width=True):
        settings["theme"] = theme
        settings["texts"] = texts
        settings["charts"] = charts
        settings["logo"] = logo
        save_settings(settings)
        st.success("تم حفظ الإعدادات بنجاح ✅")
        st.rerun()

with col2:
    if st.button("↩️ استرجاع الافتراضي", use_container_width=True):
        from utils.settings import DEFAULT_SETTINGS
        save_settings(DEFAULT_SETTINGS)
        st.success("تم استرجاع الإعدادات الافتراضية")
        st.rerun()
