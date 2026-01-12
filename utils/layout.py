import streamlit as st
from pathlib import Path

from utils.settings import load_settings
from utils.style import apply_theme

def t(texts: dict, lang: str, key_base: str, fallback: str = "") -> str:
    # key_base مثل: dashboard_title
    if lang == "ar":
        return texts.get(f"{key_base}_ar", fallback)
    return texts.get(f"{key_base}_en", fallback)

def render_header(title_key_base: str = "", page_title_fallback: str = ""):
    settings = load_settings()
    lang = settings.get("lang", "ar")
    theme = settings.get("theme", {})
    logo = settings.get("logo", {})
    texts = settings.get("texts", {})

    apply_theme(theme, logo, lang)

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

    # Place logo
    if logo.get("location", "header") == "sidebar":
        with st.sidebar:
            show_logo()
    else:
        show_logo()

    # Title
    title = page_title_fallback
    if title_key_base:
        title = t(texts, lang, title_key_base, page_title_fallback)

    if title:
        st.markdown(f"## {title}")
