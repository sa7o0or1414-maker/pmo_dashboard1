import streamlit as st
from pathlib import Path

from utils.settings import load_settings, save_settings
from utils.style import apply_theme

def t(texts: dict, lang: str, key_base: str, fallback: str = "") -> str:
    if lang == "ar":
        return texts.get(f"{key_base}_ar", fallback)
    return texts.get(f"{key_base}_en", fallback)

def get_effective_lang(settings_lang: str) -> str:
    # لكل مستخدم: تبديل لغة "عرض فقط" عبر session_state
    if "lang_view" not in st.session_state:
        st.session_state.lang_view = settings_lang
    return st.session_state.lang_view

def render_header(title_key_base: str = "", page_title_fallback: str = ""):
    settings = load_settings()
    theme = settings.get("theme", {})
    logo = settings.get("logo", {})
    layout = settings.get("layout", {})
    texts = settings.get("texts", {})
    default_lang = settings.get("lang", "ar")

    lang = get_effective_lang(default_lang)

    # CSS + RTL/LTR + font
    apply_theme(theme, logo, layout, lang)

    # Top bar (Title + globe switch)
    st.markdown("<div class='pmo-topbar'>", unsafe_allow_html=True)

    # Title text
    title = page_title_fallback
    if title_key_base:
        title = t(texts, lang, title_key_base, page_title_fallback)

    if title:
        st.markdown(f"<div class='pmo-page-title'>{title}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div></div>", unsafe_allow_html=True)

    # Globe language control (view only)
    with st.popover("🌍", use_container_width=False):
        choice = st.radio(
            "Language / اللغة",
            ["ar", "en"],
            index=0 if lang == "ar" else 1,
            horizontal=True
        )
        if choice != st.session_state.lang_view:
            st.session_state.lang_view = choice
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Logo
    saved_logo = Path(logo.get("file_path", "data/logo.png"))
    repo_logo = Path("assets") / "logo.png"

    def show_logo():
        if not logo.get("enabled", True):
            return
        st.markdown("<div class='pmo-logo-wrap'>", unsafe_allow_html=True)
        width = int(logo.get("width", 160))
        if saved_logo.exists():
            st.image(str(saved_logo), width=width)
        elif repo_logo.exists():
            st.image(str(repo_logo), width=width)
        st.markdown("</div>", unsafe_allow_html=True)

    if logo.get("location", "header") == "sidebar":
        with st.sidebar:
            show_logo()
    else:
        show_logo()
