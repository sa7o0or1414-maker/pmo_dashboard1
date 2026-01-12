from pathlib import Path

import streamlit as st
from utils.layout import render_sidebar_menu, render_page_title
from utils.auth import require_admin
from utils.settings import load_settings, save_settings, DEFAULT_SETTINGS

st.set_page_config(page_title="الإعدادات", page_icon="🎨", layout="wide")
render_sidebar_menu(active="settings")
render_page_title("🎨 الإعدادات")

require_admin()

settings = load_settings()
theme = settings.setdefault("theme", {})
texts = settings.setdefault("texts", {})
data_cfg = settings.setdefault("data", {})
logo = settings.setdefault("logo", {})

# Defaults
theme.setdefault("primary", "#3B82F6")
theme.setdefault("bg", "#0B1220")
theme.setdefault("card_bg", "#111827")
theme.setdefault("text", "#E5E7EB")
theme.setdefault("radius", 18)
theme.setdefault("palette", ["#3B82F6", "#22C55E", "#F59E0B", "#EF4444", "#A855F7"])

texts.setdefault("dashboard_title", "📊 لوحة المعلومات")

data_cfg.setdefault("show_map", True)
data_cfg.setdefault("map_link_col", "رابط الموقع")
data_cfg.setdefault("lat_col", "lat")
data_cfg.setdefault("lon_col", "lon")

logo.setdefault("file_path", "data/logo.png")

left, right = st.columns([1, 1])

with left:
    st.subheader("🎨 ألوان الموقع")
    theme["primary"] = st.color_picker("اللون الأساسي", theme["primary"])
    theme["bg"] = st.color_picker("الخلفية", theme["bg"])
    theme["card_bg"] = st.color_picker("لون الكروت/الصناديق", theme["card_bg"])
    theme["text"] = st.color_picker("لون النص", theme["text"])
    theme["radius"] = st.slider("انحناء الزوايا", 8, 28, int(theme.get("radius", 18)))

    st.markdown("### 🧩 لوحة ألوان (Palette)")
    st.caption("أضيفي/عدّلي ألوان الرسوم والبادجات.")
    palette = theme.get("palette", [])
    if "palette_work" not in st.session_state:
        st.session_state.palette_work = palette[:] if palette else []

    new_color = st.color_picker("أضيفي لون جديد", "#22C55E")
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("➕ إضافة اللون"):
            st.session_state.palette_work.append(new_color)
    with c2:
        if st.button("🧹 تفريغ"):
            st.session_state.palette_work = []
    with c3:
        st.write("عدد الألوان:", len(st.session_state.palette_work))

    for i, c in enumerate(st.session_state.palette_work):
        a, b, d = st.columns([2, 2, 1])
        with a:
            st.markdown(
                f"<div style='height:34px;border-radius:12px;background:{c};'></div>",
                unsafe_allow_html=True
            )
        with b:
            st.session_state.palette_work[i] = st.color_picker(f"لون #{i+1}", c, key=f"pal_{i}")
        with d:
            if st.button("حذف", key=f"del_{i}"):
                st.session_state.palette_work.pop(i)
                st.rerun()

    theme["palette"] = st.session_state.palette_work

with right:
    st.subheader("🧩 إعدادات الداشبورد")
    texts["dashboard_title"] = st.text_input("عنوان الداشبورد", value=texts.get("dashboard_title", "📊 لوحة المعلومات"))

    st.markdown("---")
    st.subheader("🗺️ الخريطة")
    data_cfg["show_map"] = st.toggle("إظهار الخريطة في الداشبورد", value=bool(data_cfg.get("show_map", True)))
    data_cfg["map_link_col"] = st.text_input("اسم عمود رابط الموقع (Google Maps)", value=data_cfg.get("map_link_col", "رابط الموقع"))
    data_cfg["lat_col"] = st.text_input("اسم عمود LAT (اختياري)", value=data_cfg.get("lat_col", "lat"))
    data_cfg["lon_col"] = st.text_input("اسم عمود LON (اختياري)", value=data_cfg.get("lon_col", "lon"))

    st.markdown("---")
    st.subheader("🖼️ رفع اللوقو")
    st.caption("يرفع ويحفظ في data/logo.png")
    logo_upload = st.file_uploader("ارفع لوقو جديد (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if logo_upload is not None:
        Path("data").mkdir(parents=True, exist_ok=True)
        save_path = Path(logo.get("file_path", "data/logo.png"))
        with open(save_path, "wb") as f:
            f.write(logo_upload.getbuffer())
        st.success("✅ تم حفظ اللوقو")
        st.image(str(save_path), width=220)

    if Path(logo.get("file_path", "data/logo.png")).exists():
        st.caption("اللوقو الحالي:")
        st.image(logo.get("file_path", "data/logo.png"), width=220)

st.markdown("---")

c1, c2 = st.columns([1, 1])
with c1:
    if st.button("💾 حفظ الإعدادات", use_container_width=True):
        settings["theme"] = theme
        settings["texts"] = texts
        settings["data"] = data_cfg
        settings["logo"] = logo
        save_settings(settings)
        st.success("تم حفظ الإعدادات ✅")
        st.rerun()

with c2:
    if st.button("↩️ استرجاع الافتراضي", use_container_width=True):
        save_settings(DEFAULT_SETTINGS)
        st.session_state.pop("palette_work", None)
        st.success("تم الاسترجاع ✅")
        st.rerun()
