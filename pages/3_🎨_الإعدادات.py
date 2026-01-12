import streamlit as st
from pathlib import Path

from utils.auth import require_admin
from utils.layout import render_header
from utils.settings import load_settings, save_settings, DEFAULT_SETTINGS

st.set_page_config(page_title="الإعدادات", layout="wide")

render_header(title_key_base="settings_title", page_title_fallback="🎨 إعدادات الواجهة (Admin)")
require_admin()

settings = load_settings()
theme = settings.get("theme", {})
logo = settings.get("logo", {})
texts = settings.get("texts", {})
layout = settings.get("layout", {})
data_cfg = settings.get("data", {})
lang_default = settings.get("lang", "ar")

left, right = st.columns([1, 1])

with left:
    st.subheader("🌐 اللغة الافتراضية + الخط")
    lang_default = st.selectbox("اللغة الافتراضية للموقع (للجميع)", ["ar", "en"], index=0 if lang_default == "ar" else 1)

    theme["font_ar"] = st.text_input("خط عربي (CSS name)", value=theme.get("font_ar", "Montserrat Arabic"))
    theme["font_en"] = st.text_input("خط إنجليزي (CSS name)", value=theme.get("font_en", "Montserrat"))

    st.divider()

    st.subheader("📌 محاذاة العناوين")
    layout["title_align"] = st.selectbox("محاذاة عنوان الصفحة", ["right", "center", "left"],
                                         index=["right", "center", "left"].index(layout.get("title_align", "right")))
    layout["title_size_px"] = st.slider("حجم عنوان الصفحة (px)", 16, 34, int(layout.get("title_size_px", 22)))

    st.divider()

    st.subheader("🎨 ألوان الموقع")
    theme["primary"] = st.color_picker("اللون الأساسي", theme.get("primary", "#3B82F6"))
    theme["bg"] = st.color_picker("الخلفية", theme.get("bg", "#0B1220"))
    theme["card_bg"] = st.color_picker("لون الكروت/الصناديق", theme.get("card_bg", "#111B2E"))
    theme["text"] = st.color_picker("لون النص", theme.get("text", "#E5E7EB"))
    theme["radius"] = st.slider("انحناء الزوايا", 8, 28, int(theme.get("radius", 18)))

    st.markdown("### 🧩 ألوان الشارتات (Palette)")
    palette = theme.get("palette", [])
    if "palette_work" not in st.session_state:
        st.session_state.palette_work = palette[:] if palette else []

    new_color = st.color_picker("أضيفي لون", "#22C55E", key="new_palette_color")
    c_add, c_clear, c_count = st.columns([1, 1, 2])

    with c_add:
        if st.button("➕ إضافة"):
            st.session_state.palette_work.append(new_color)
    with c_clear:
        if st.button("🧹 تفريغ"):
            st.session_state.palette_work = []
    with c_count:
        st.write("عدد الألوان:", len(st.session_state.palette_work))

    for i, c in enumerate(st.session_state.palette_work):
        a, b, d = st.columns([2, 2, 1])
        with a:
            st.markdown(f"<div style='padding:10px;border-radius:12px;background:{c};'></div>", unsafe_allow_html=True)
        with b:
            st.session_state.palette_work[i] = st.color_picker(f"#{i+1}", c, key=f"pal_{i}")
        with d:
            if st.button("حذف", key=f"del_{i}"):
                st.session_state.palette_work.pop(i)
                st.rerun()

    theme["palette"] = st.session_state.palette_work

    st.divider()

    st.subheader("✍️ عناوين الصفحات")
    texts["dashboard_title_ar"] = st.text_input("عنوان الداشبورد (عربي)", texts.get("dashboard_title_ar", "📊 داشبورد المشاريع"))
    texts["dashboard_title_en"] = st.text_input("Dashboard title (EN)", texts.get("dashboard_title_en", "📊 Projects Dashboard"))
    texts["upload_title_ar"] = st.text_input("عنوان رفع البيانات (عربي)", texts.get("upload_title_ar", "📤 رفع البيانات الأسبوعي"))
    texts["upload_title_en"] = st.text_input("Upload title (EN)", texts.get("upload_title_en", "📤 Weekly Data Upload"))

with right:
    st.subheader("🖼️ اللوقو (رفع + إعدادات)")
    logo_upload = st.file_uploader("ارفع لوقو (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if logo_upload is not None:
        Path("data").mkdir(parents=True, exist_ok=True)
        save_path = Path(logo.get("file_path", "data/logo.png"))
        with open(save_path, "wb") as f:
            f.write(logo_upload.getbuffer())
        st.success("✅ تم حفظ اللوقو")
        st.image(str(save_path), width=220)

    current_path = Path(logo.get("file_path", "data/logo.png"))
    if current_path.exists():
        st.caption("اللوقو الحالي:")
        st.image(str(current_path), width=220)
        if st.button("🗑️ حذف اللوقو"):
            current_path.unlink()
            st.success("تم حذف اللوقو.")
            st.rerun()
    else:
        st.info("لا يوجد لوقو محفوظ.")

    st.divider()

    logo["enabled"] = st.toggle("إظهار اللوقو", value=bool(logo.get("enabled", True)))
    logo["location"] = st.selectbox("مكان اللوقو", ["header", "sidebar"], index=0 if logo.get("location", "header") == "header" else 1)
    logo["align"] = st.selectbox("محاذاة اللوقو", ["left", "center", "right"], index=["left","center","right"].index(logo.get("align", "left")))
    logo["width"] = st.slider("عرض اللوقو (px)", 60, 360, int(logo.get("width", 160)))
    logo["top_margin"] = st.slider("مسافة فوق اللوقو", 0, 40, int(logo.get("top_margin", 6)))
    logo["bottom_margin"] = st.slider("مسافة تحت اللوقو", 0, 40, int(logo.get("bottom_margin", 10)))

    st.divider()

    st.subheader("🗺️ إعدادات الخريطة (أسماء الأعمدة في Excel)")
    data_cfg["lat_col"] = st.text_input("اسم عمود Latitude", value=data_cfg.get("lat_col", "lat"))
    data_cfg["lon_col"] = st.text_input("اسم عمود Longitude", value=data_cfg.get("lon_col", "lon"))
    data_cfg["map_link_col"] = st.text_input("اسم عمود رابط الموقع (اختياري)", value=data_cfg.get("map_link_col", "رابط الموقع"))

    st.divider()

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("💾 حفظ الإعدادات"):
            settings["lang"] = lang_default
            settings["theme"] = theme
            settings["logo"] = logo
            settings["texts"] = texts
            settings["layout"] = layout
            settings["data"] = data_cfg
            save_settings(settings)
            st.success("تم حفظ الإعدادات ✅")
            st.rerun()

    with c2:
        if st.button("↩️ استرجاع الافتراضي"):
            save_settings(DEFAULT_SETTINGS)
            st.session_state.pop("palette_work", None)
            st.success("تمت إعادة الإعدادات الافتراضية ✅")
            st.rerun()
