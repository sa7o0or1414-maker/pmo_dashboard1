import streamlit as st
from pathlib import Path

from utils.settings import load_settings
from utils.style import apply_theme


def _t(texts, lang, key_base, fallback):
    if lang == "ar":
        return texts.get(f"{key_base}_ar", fallback)
    return texts.get(f"{key_base}_en", fallback)


def _get_lang(default_lang):
    # per-user view language
    if "lang_view" not in st.session_state:
        st.session_state.lang_view = default_lang
    return st.session_state.lang_view


def render_header(title_key_base="", page_title_fallback=""):
    settings = load_settings()

    theme = settings.get("theme", {})
    logo = settings.get("logo", {})
    layout = settings.get("layout", {})
    texts = settings.get("texts", {})
    default_lang = settings.get("lang", "ar")

    lang = _get_lang(default_lang)

    # Apply global theme + fonts + spacing
    apply_theme(theme, logo, layout, lang)

    # Title
    title = page_title_fallback
    if title_key_base:
        title = _t(texts, lang, title_key_base, page_title_fallback)

    # Logo paths
    saved_logo = Path(logo.get("file_path", "data/logo.png"))
    repo_logo = Path("assets") / "logo.png"
    logo_width = int(logo.get("width", 160))

    # 1) Logo on top
    if logo.get("enabled", True):
        st.markdown("<div class='pmo-logo-top'>", unsafe_allow_html=True)
        if saved_logo.exists():
            st.image(str(saved_logo), width=logo_width)
        elif repo_logo.exists():
            st.image(str(repo_logo), width=logo_width)
        st.markdown("</div>", unsafe_allow_html=True)

    # 2) Row: title on one side, 🌍 on the opposite side
    if lang == "ar":
        # Arabic: title RIGHT, globe LEFT
        col_globe, col_title = st.columns([1, 7])
        with col_globe:
            with st.popover("🌍", use_container_width=False):
                choice = st.radio("Language / اللغة", ["ar", "en"], index=0, horizontal=True)
                if choice != st.session_state.lang_view:
                    st.session_state.lang_view = choice
                    st.rerun()
        with col_title:
            st.markdown(f"<div class='pmo-page-title'>{title}</div>", unsafe_allow_html=True)
    else:
        # English: title LEFT, globe RIGHT
        col_title, col_globe = st.columns([7, 1])
        with col_title:
            st.markdown(f"<div class='pmo-page-title'>{title}</div>", unsafe_allow_html=True)
        with col_globe:
            with st.popover("🌍", use_container_width=False):
                choice = st.radio("Language / اللغة", ["en", "ar"], index=0, horizontal=True)
                if choice != st.session_state.lang_view:
                    st.session_state.lang_view = choice
                    st.rerun()
