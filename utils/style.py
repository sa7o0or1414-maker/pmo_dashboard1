import streamlit as st

def apply_theme(theme, logo, layout, lang):
    primary = theme.get("primary", "#3B82F6")
    bg = theme.get("bg", "#0B1220")
    card = theme.get("card_bg", "#111B2E")
    text = theme.get("text", "#E5E7EB")
    radius = int(theme.get("radius", 18))

    font_ar = theme.get("font_ar", "Montserrat Arabic")
    font_en = theme.get("font_en", "Montserrat")

    # RTL/LTR + font per language
    direction = "rtl" if lang == "ar" else "ltr"
    font_family = 'var(--font-ar)' if lang == "ar" else 'var(--font-en)'

    # title align setting
    title_align = layout.get("title_align", "right")  # left|center|right
    title_css_align = {"left": "left", "center": "center", "right": "right"}.get(title_align, "right")
    title_size = int(layout.get("title_size_px", 22))

    # cards gap ~ 1cm
    cards_gap_px = int(layout.get("cards_gap_px", 38))

    # logo align in top area
    logo_align = logo.get("align", "center")
    justify_logo = {"left": "flex-start", "center": "center", "right": "flex-end"}.get(logo_align, "center")

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
        --cards-gap: {cards_gap_px}px;
      }}

      html, body, .stApp {{
        background: var(--bg) !important;
        color: var(--text) !important;
        direction: {direction};
        font-family: {font_family} !important;
      }}

      /* gap between columns (cards spacing) */
      div[data-testid="stHorizontalBlock"] {{
        gap: var(--cards-gap) !important;
      }}

      /* Sidebar bg */
      section[data-testid="stSidebar"] > div {{
        background: var(--card) !important;
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

      /* Logo (top) */
      .pmo-logo-top {{
        display: flex;
        justify-content: {justify_logo};
        margin-top: 6px;
        margin-bottom: 10px;
      }}

      /* Title */
      .pmo-page-title {{
        text-align: {title_css_align};
        font-size: {title_size}px;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
