import streamlit as st
from pathlib import Path

from utils.auth import require_admin
from utils.layout import render_header
from utils.settings import load_settings, save_settings

# لازم تكون أول شيء قبل أي مخرجات
st.set_page_config(page_title="الإعدادات", layout="wide")

# هيدر + حماية أدمن
render_header("🎨 إعدادات الواجهة (Admin)")
require_admin()

settings = load_settings()
theme = settings.get("theme", {})
logo = settings.get("logo", {})
texts = settings.get("texts", {})

left, right = st.columns([1, 1])

# =========================
# العمود الأيسر: الألوان + النصوص
# =========================
with left:
    st.subheader("ألوان الموقع")
    theme["primary"] = st.color_picker("اللون الأساسي", theme.get("primary", "#3B82F6"))
    theme["bg"] = st.color_picker("الخلفية", theme.get("bg", "#0B1220"))
    theme["card_bg"] = st.color_picker("لون الكروت/الصناديق", theme.get("card_bg", "#111B2E"))
    theme["text"] = st.color_picker("لون النص", theme.get("text", "#E5E7EB"))
    theme["radius"] = st.slider("انحناء الزوايا", 8, 28, int(theme.get("radius", 18)))

    st.markdown("### 🧩 لوحة ألوان (Palette)")
    st.caption("أضيفي/احذفي ألوان براحتك—نستخدمها لاحقًا للرسوم والبادجات وحالة المشاريع.")

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

    st.subheader("✍️ نصوص الصفحات")
    texts["dashboard_title"] = st.text_input(
        "عنوان صفحة الداشبورد",
        value=texts.get("dashboard_title", "📊 داشبورد المشاريع")
    )
    texts["upload_title"] = st.text_input(
        "عنوان صفحة رفع البيانات",
        value=texts.get("upload_title", "📤 رفع البيانات الأسبوعي")
    )

# =========================
# العمود الأيمن: اللوقو + إعداداته
# =========================
with right:
    st.subheader("🖼️ رفع اللوقو (محفوظ)")
    st.caption("ارفعي لوقو هنا وسيُحفظ في data/logo.png ويظهر في كل الصفحات.")

    logo_upload = st.file_uploader(
        "ارفع لوقو جديد (PNG / JPG)",
        type=["png", "jpg", "jpeg"]
    )

    if logo_upload is not None:
        Path("data").mkdir(parents=True, exist_ok=True)
        save_path = Path(logo.get("file_path", "data/logo.png"))
        with open(save_path, "wb") as f:
            f.write(logo_upload.getbuffer())
        st.success("✅ تم حفظ اللوقو بنجاح")
        st.image(str(save_path), width=200)

    # معاينة اللوقو الحالي إن وجد
    current_path = Path(logo.get("file_path", "data/logo.png"))
    if current_path.exists():
        st.markdown("**اللوقو الحالي:**")
        st.image(str(current_path), width=200)
        if st.button("🗑️ حذف اللوقو المحفوظ"):
            current_path.unlink()
            st.success("تم حذف اللوقو.")
            st.rerun()
    else:
        st.info("لا يوجد لوقو محفوظ حالياً.")

    st.divider()

    st.subheader("إعدادات اللوقو")
    logo["enabled"] = st.toggle("إظهار اللوقو", value=bool(logo.get("enabled", True)))
    logo["location"] = st.selectbox(
        "مكان اللوقو",
        ["header", "sidebar"],
        index=0 if logo.get("location", "header") == "header" else 1
    )
    logo["align"] = st.selectbox(
        "محاذاة اللوقو",
        ["left", "center", "right"],
        index=["left", "center", "right"].index(logo.get("align", "left"))
    )
    logo["width"] = st.slider("عرض اللوقو (px)", 60, 360, int(logo.get("width", 160)))
    logo["top_margin"] = st.slider("مسافة فوق اللوقو", 0, 40, int(logo.get("top_margin", 6)))
    logo["bottom_margin"] = st.slider("مسافة تحت اللوقو", 0, 40, int(logo.get("bottom_margin", 10)))

    st.divider()

    col_save, col_reset = st.columns([1, 1])

    with col_save:
        if st.button("💾 حفظ الإعدادات"):
            settings["theme"] = theme
            settings["logo"] = logo
            settings["texts"] = texts
            save_settings(settings)
            st.success("تم حفظ الإعدادات ✅")
            st.rerun()

    with col_reset:
        if st.button("↩️ استرجاع الافتراضي"):
            from utils.settings import DEFAULT_SETTINGS
            save_settings(DEFAULT_SETTINGS)
            st.session_state.pop("palette_work", None)
            st.success("تمت إعادة الإعدادات الافتراضية ✅")
            st.rerun()
