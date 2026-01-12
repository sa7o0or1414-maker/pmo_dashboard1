import streamlit as st
from pathlib import Path

from utils.settings import load_settings
from utils.style import apply_theme


def render_header(page_title: str = "", title_key=None):
    settings = load_settings()
    theme = settings.get("theme", {})
    logo = settings.get("logo", {})
    texts = settings.get("texts", {})

    apply_theme(theme, logo)

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

    # Logo placement
    if logo.get("location", "header") == "sidebar":
        with st.sidebar:
            show_logo()
    else:
        show_logo()

    # Title from settings (optional)
    final_title = page_title
    if title_key is not None:
        final_title = texts.get(title_key, page_title)

    if final_title:
        st.markdown(f"## {final_title}")
