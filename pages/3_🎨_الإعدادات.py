import streamlit as st
from pathlib import Path

from utils.auth import require_admin
from utils.layout import render_header
from utils.settings import load_settings, save_settings, DEFAULT_SETTINGS

st.set_page_config(page_title="الإعدادات", layout="wide")

render_header(title_key_base="settings_title", page_title_fallback="🎨 إعدادات الواجهة (Admin)")
require_admin()

settings = load_settings()
lang = settings.get("lang", "ar")
theme = settings.get("theme", {})
logo = settings.get("logo", {})
texts = settings.get("texts", {})

left, right = st.columns([1, 1])

with left:
    st.subheader("🌐 اللغة والخط")

    lang = st.selectbox("لغة الموقع", ["ar", "en"], index=0 if lang == "ar" else 1)

    # الخطوط (موجودة افتراضيًا لكن نخليها قابلة للتغيير لو تبين)
    theme["font_ar"] = st.text_input("خط عربي (CSS font name)", value=theme.get("font_ar", "Montserrat Arabic"))
    theme["font_en"] = st.text_input("خط إنجليزي (CSS font name)", value=theme.get("font_en", "Montserrat"))

    st.divider()

    st.subheader("🎨 ألوان الموقع")
    theme["primary"] = st.color_picker("اللون الأساسي", theme.get("primary", "#3B82F6"))
    theme["bg"] = st.color_picker("الخلفية", theme.get("bg", "#0B1220"))
    theme["card_bg"] = st.color_picker("لون الكروت/الصناديق", theme.get("card_bg", "#111B2E"))
    theme["text"] = st.color_picker("لون النص", theme.get("text", "#E5E7EB"))
    theme["radius"] = st.slider("انحناء الزوايا", 8, 28, int(theme.get("radius", 18)))

    st.markdown("### 🧩 لوحة ألوان (Palette)")
    palette = theme.get("palette", [])
    if "palette_work" not in st.session_state:
        st.session_state.palette_work = palette[:] if palette else []

    new_color = st.color_picker("أضيفي لون جديد للـ Palette", "#22C55E", key="new_palette_color")
    c_add, c_clear, c_count = st.columns([1, 1, 2])

    with c_add:
        if st.button("➕ إضافة اللون"):
            st.session_state.palette_work.append(new_color)

    with c_clear:
        if st.button("🧹 تفريغ"):
            st.session_state.palette_work = []

    with c_count:
        st.write("عدد الألوان:", len(st.session_state.palette_work))

    for i, c in enumerate(st.session_state.palette_work):
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.markdown(
                f"<div style='padding:10px;border-radius:12px;background:{c};'></div>",
                unsafe_allow_html=True
            )
        with c2:
            updated = st.color_picker(f"لون #{i+1}", c, key=f"pal_{i}")
            st.session_state.palette_work[i] = updated
        with c3:
            if st.button("حذف", key=f"del_{i}"):
                st.session_state.palette_work.pop(i)
                st.rerun()

    theme["palette"] = st.session_state.palette_work

    st.divider()

    st.subheader("✍️ عناوين الصفحات (قابلة للتعديل)")
    texts["dashboard_title_ar"] = st.text_input("عنوان الداشبورد (عربي)", value=texts.get("dashboard_title_ar", "📊 داشبورد المشاريع"))
    texts["dashboard_title_en"] = st.text_input("Dashboard title (English)", value=texts.get("dashboard_title_en", "📊 Projects Dashboard"))
    texts["upload_title_ar"] = st.text_input("عنوان رفع البيانات (عربي)", value=texts.get("upload_title_ar", "📤 رفع البيانات الأسبوعي"))
    texts["upload_title_en"] = st.text_input("Upload title (English)", value=texts.get("upload_title_en", "📤 Weekly Data Upload"))

with right:
    st.subheader("🖼️ اللوقو (حفظ + إعدادات)")

    logo_upload = st.file_uploader("ارفع لوقو جديد (PNG / JPG)", type=["png", "jpg", "jpeg"])
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
        if st.button("🗑️ حذف اللوقو المحفوظ"):
            current_path.unlink()
            st.success("تم حذف اللوقو.")
            st.rerun()
    else:
        st.info("لا يوجد لوقو محفوظ حالياً.")

    st.divider()

    st.subheader("إعدادات اللوقو")
    logo["enabled"] = st.toggle("إظهار اللوقو", value=bool(logo.get("enabled", True)))
    logo["location"] = st.selectbox("مكان اللوقو", ["header", "sidebar"], index=0 if logo.get("location", "header") == "header" else 1)
    logo["align"] = st.selectbox("محاذاة اللوقو", ["left", "center", "right"], index=["left","center","right"].index(logo.get("align", "left")))
    logo["width"] = st.slider("عرض اللوقو (px)", 60, 360, int(logo.get("width", 160)))
    logo["top_margin"] = st.slider("مسافة فوق اللوقو", 0, 40, int(logo.get("top_margin", 6)))
    logo["bottom_margin"] = st.slider("مسافة تحت اللوقو", 0, 40, int(logo.get("bottom_margin", 10)))

    st.divider()

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("💾 حفظ الإعدادات"):
            settings["lang"] = lang
            settings["theme"] = theme
            settings["logo"] = logo
            settings["texts"] = texts
            save_settings(settings)
            st.success("تم حفظ الإعدادات ✅")
            st.rerun()

    with c2:
        if st.button("↩️ استرجاع الافتراضي"):
            save_settings(DEFAULT_SETTINGS)
            st.session_state.pop("palette_work", None)
            st.success("تمت إعادة الإعدادات الافتراضية ✅")
            st.rerun()
