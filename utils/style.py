import streamlit as st

def apply_theme(theme: dict, logo: dict, layout: dict, lang: str):
    primary = theme.get("primary", "#3B82F6")
    bg = theme.get("bg", "#0B1220")
    card = theme.get("card_bg", "#111B2E")
    text = theme.get("text", "#E5E7EB")
    radius = int(theme.get("radius", 18))

    font_ar = theme.get("font_ar", "Montserrat Arabic")
    font_en = theme.get("font_en", "Montserrat")

    align = logo.get("align", "left")
    justify_logo = {"left": "flex-start", "center": "center", "right": "flex-end"}.get(align, "flex-start")

    top_margin = int(logo.get("top_margin", 6))
    bottom_margin = int(logo.get("bottom_margin", 10))

    direction = "rtl" if lang == "ar" else "ltr"
    font_family = "var(--font-ar)" if lang == "ar" else "var(--font-en)"

    title_align = layout.get("title_align", "right") if lang == "ar" else layout.get("title_align", "left")
    # للإنجليزي لو تبين نفس تحكمك ما يتغير، خليها نفس القيمة. إذا تبين افتراضي EN يسار، خليه كما هو فوق.
    title_css_align = {"left": "left", "center": "center", "right": "right"}.get(title_align, "right")
    title_size = int(layout.get("title_size_px", 22))

    css = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
      @import url('https://fonts.googleapis.com/css2?family=Montserrat+Arabic:wght@300;400;500;600;700&display=swap');

      :root {{
        --primary: {primary};
        --bg: {bg};
        --card: {card};
        --text: {text};
        --radius: {radius}px;
        --font-ar: "{font_ar}", sans-serif;
        --font-en: "{font_en}", sans-serif;
      }}

      html, body, .stApp {{
        background: var(--bg) !important;
        color: var(--text) !important;
        direction: {direction};
        font-family: {font_family} !important;
      }}

      /* Buttons */
      .stButton > button {{
        background: var(--primary) !important;
        border: 1px solid var(--primary) !important;
        color: #fff !important;
        border-radius: var(--radius) !important;
        padding: 0.55rem 0.95rem !important;
      }}

      /* Metric card */
      div[data-testid="stMetric"] {{
        background: var(--card) !important;
        border-radius: var(--radius) !important;
        padding: 14px !important;
      }}

      /* Sidebar bg */
      section[data-testid="stSidebar"] > div {{
        background: var(--card) !important;
      }}

      /* Logo wrap */
      .pmo-logo-wrap {{
        display: flex;
        justify-content: {justify_logo};
        margin-top: {top_margin}px;
        margin-bottom: {bottom_margin}px;
      }}

      /* Page Title */
      .pmo-page-title {{
        text-align: {title_css_align};
        font-size: {title_size}px;
        font-weight: 700;
        margin: 0.25rem 0 0.75rem 0;
      }}

      /* Top toolbar */
      .pmo-topbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.2rem;
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
