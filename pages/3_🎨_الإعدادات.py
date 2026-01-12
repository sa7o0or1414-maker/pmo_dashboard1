import streamlit as st
from utils.auth import require_admin
from utils.settings import load_settings, save_settings

st.set_page_config(page_title="الإعدادات", layout="wide")

require_admin()

st.title("🎨 إعدادات الواجهة (Admin)")

settings = load_settings()
theme = settings["theme"]
logo = settings["logo"]

left, right = st.columns([1, 1])

with left:
    st.subheader("ألوان الموقع")
    theme["primary"] = st.color_picker("اللون الأساسي", theme["primary"])
    theme["bg"] = st.color_picker("الخلفية", theme["bg"])
    theme["card_bg"] = st.color_picker("لون الكروت/الصناديق", theme["card_bg"])
    theme["text"] = st.color_picker("لون النص", theme["text"])
    theme["radius"] = st.slider("انحناء الزوايا", 8, 28, int(theme.get("radius", 18)))

    st.markdown("### 🧩 لوحة ألوان (Palette)")
    st.caption("أضيفي/احذفي ألوان براحتك—نستخدمها لاحقًا للرسوم والبادجات وحالة المشاريع.")
    palette = theme.get("palette", [])
    if "palette_work" not in st.session_state:
        st.session_state.palette_work = palette[:] if palette else []

    new_color = st.color_picker("أضيفي لون جديد للـ Palette", "#22C55E")
    cols = st.columns([1, 1, 2])
    with cols[0]:
        if st.button("➕ إضافة اللون"):
            st.session_state.palette_work.append(new_color)
    with cols[1]:
        if st.button("🧹 تفريغ"):
            st.session_state.palette_work = []
    with cols[2]:
        st.write("عدد الألوان:", len(st.session_state.palette_work))

    # عرض + حذف
    for i, c in enumerate(st.session_state.palette_work):
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.markdown(f"<div style='padding:10px;border-radius:12px;background:{c};'></div>", unsafe_allow_html=True)
        with c2:
            updated = st.color_picker(f"لون #{i+1}", c, key=f"pal_{i}")
            st.session_state.palette_work[i] = updated
        with c3:
            if st.button("حذف", key=f"del_{i}"):
                st.session_state.palette_work.pop(i)
                st.rerun()

    theme["palette"] = st.session_state.palette_work
from pathlib import Path

st.markdown("### 🖼️ رفع اللوقو (محفوظ)")

logo_upload = st.file_uploader("ارفع لوقو جديد (PNG/JPG)", type=["png", "jpg", "jpeg"])
if logo_upload is not None:
    # نحفظه كملف ثابت
    Path("data").mkdir(parents=True, exist_ok=True)
    save_path = Path(logo.get("file_path", "data/logo.png"))

    # لو الرفع jpg نخليه png؟ (اختياري) — هنا نحفظه كما هو:
    with open(save_path, "wb") as f:
        f.write(logo_upload.getbuffer())

    st.success("✅ تم حفظ اللوقو بنجاح!")
    st.image(str(save_path), width=200)

with right:
    st.subheader("إعدادات اللوقو")
    logo["enabled"] = st.toggle("إظهار اللوقو", value=bool(logo.get("enabled", True)))
    logo["location"] = st.selectbox("مكان اللوقو", ["header", "sidebar"], index=0 if logo.get("location")=="header" else 1)
    logo["align"] = st.selectbox("محاذاة اللوقو", ["left", "center", "right"], index=["left","center","right"].index(logo.get("align","left")))
    logo["width"] = st.slider("عرض اللوقو (px)", 60, 360, int(logo.get("width", 160)))
    logo["top_margin"] = st.slider("مسافة فوق اللوقو", 0, 40, int(logo.get("top_margin", 6)))
    logo["bottom_margin"] = st.slider("مسافة تحت اللوقو", 0, 40, int(logo.get("bottom_margin", 10)))

    st.markdown("---")
    if st.button("💾 حفظ الإعدادات"):
        settings["theme"] = theme
        settings["logo"] = logo
        save_settings(settings)
        st.success("تم حفظ الإعدادات ✅")
        st.info("إذا ما انعكس فورًا، سوي Refresh أو Rerun.")

    if st.button("↩️ استرجاع الافتراضي"):
        from utils.settings import DEFAULT_SETTINGS
        save_settings(DEFAULT_SETTINGS)
        st.session_state.pop("palette_work", None)
        st.success("تمت إعادة الإعدادات الافتراضية ✅")
        st.rerun()
