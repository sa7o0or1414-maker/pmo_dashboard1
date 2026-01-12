import streamlit as st
from pathlib import Path

from utils.settings import load_settings
from utils.style import apply_theme

def t(texts: dict, lang: str, key_base: str, fallback: str = "") -> str:
    if lang == "ar":
        return texts.get(f"{key_base}_ar", fallback)
    return texts.get(f"{key_base}_en", fallback)

def get_effective_lang(default_lang: str) -> str:
    # تبديل لغة عرض لكل مستخدم (بدون ما يغير إعدادات الكل)
    if "lang_view" not in st.session_state:
        st.session_state.lang_view = default_lang
    return st.session_state.lang_view

def render_header(title_key_base: str = "", page_title_fallback: str = ""):
    settings = load_settings()
    theme = settings.get("theme", {})
    logo = settings.get("logo", {})
    layout = settings.get("layout", {})
    texts = settings.get("texts", {})
    default_lang = settings.get("lang", "ar")

    lang = get_effective_lang(default_lang)

    # CSS + Montserrat + RTL/LTR + gaps
    apply_theme(theme, logo, layout, lang)

    # 1) اللوقو فوق
    saved_logo = Path(logo.get("file_path", "data/logo.png"))
    repo_logo = Path("assets") / "logo.png"
    logo_width = int(logo.get("width", 160))

    if logo.get("enabled", True):
        st.markdown("<div class='pmo-logo-top'>", unsafe_allow_html=True)
        if saved_logo.exists():
            st.image(str(saved_logo), width=logo_width)
        elif repo_logo.exists():
            st.image(str(repo_logo), width=logo_width)
        st.markdown("</div>", unsafe_allow_html=True)

    # عنوان الصفحة
    title = page_title_fallback
    if title_key_base:
        title = t(texts, lang, title_key_base, page_title_fallback)

    # 2) سطر (العنوان + 🌍) متعاكس
    # عربي: العنوان يمين + 🌍 يسار
    # إنجليزي: العنوان يسار + 🌍 يمين
    if lang == "ar":
        left_col, right_col = st.columns([1, 6])
        with left_col:
            with st.popover("🌍", use_container_width=False):
                choice = st.radio("Language / اللغة", ["ar", "en"], index=0, horizontal=True)
                if choice != st.session_state.lang_view:
                    st.session_state.lang_view = choice
                    st.rerun()
        with right_col:
            st.markdown(f"<div class='pmo-page-title'>{title}</div>", unsafe_allow_html=True)
    else:
        left_col, right_col = st.columns([6, 1])
        with left_col:
            st.markdown(f"<div class='pmo-page-title'>{title}</div>", unsafe_allow_html=True)
        with right_col:
            with st.popover("🌍", use_container_width=False):
                choice = st.radio("Language / اللغة", ["en", "ar"], index=0, horizontal=True)
                if choice != st.session_state.lang_view:
                    st.session_state.lang_view = choice
                    st.rerun()
