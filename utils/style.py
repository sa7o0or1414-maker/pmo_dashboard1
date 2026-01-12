import streamlit as st

def apply_theme(theme: dict, logo: dict, lang: str):
    primary = theme.get("primary", "#3B82F6")
    bg = theme.get("bg", "#0B1220")
    card = theme.get("card_bg", "#111B2E")
    text = theme.get("text", "#E5E7EB")
    radius = int(theme.get("radius", 18))

    font_ar = theme.get("font_ar", "Montserrat Arabic")
    font_en = theme.get("font_en", "Montserrat")

    align = logo.get("align", "left")
    justify = {"left": "flex-start", "center": "center", "right": "flex-end"}.get(align, "flex-start")
    top_margin = int(logo.get("top_margin", 6))
    bottom_margin = int(logo.get("bottom_margin", 10))

    # اتجاه الصفحة حسب اللغة
    direction = "rtl" if lang == "ar" else "ltr"

    css = f"""
    <style>
      /* Fonts */
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

      html, body, [class*="css"], .stApp {{
        background: var(--bg) !important;
        color: var(--text) !important;
        direction: {direction};
        font-family: {"var(--font-ar)" if lang=="ar" else "var(--font-en)"} !important;
      }}

      /* Buttons */
      .stButton > button {{
        background: var(--primary) !important;
        border: 1px solid var(--primary) !important;
        color: #fff !important;
        border-radius: var(--radius) !important;
        padding: 0.6rem 1rem !important;
      }}

      /* Metrics */
      div[data-testid="stMetric"] {{
        background: var(--card) !important;
        border-radius: var(--radius) !important;
        padding: 14px !important;
      }}

      /* Sidebar */
      section[data-testid="stSidebar"] > div {{
        background: var(--card) !important;
      }}

      /* Logo wrapper */
      .pmo-logo-wrap {{
        display: flex;
        justify-content: {justify};
        margin-top: {top_margin}px;
        margin-bottom: {bottom_margin}px;
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
