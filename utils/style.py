import streamlit as st

def apply_theme(theme: dict, logo: dict):
    primary = theme["primary"]
    bg = theme["bg"]
    card = theme["card_bg"]
    text = theme["text"]
    radius = int(theme.get("radius", 18))

    # نحول الباليت لأكواد CSS (مفيدة للرسوم/بادجات لاحقًا)
    palette = theme.get("palette", [])
    palette_css = ",".join(palette) if palette else primary

    align = logo.get("align", "left")
    justify = {"left": "flex-start", "center": "center", "right": "flex-end"}.get(align, "flex-start")

    top_margin = int(logo.get("top_margin", 6))
    bottom_margin = int(logo.get("bottom_margin", 10))

    css = f"""
    <style>
      :root {{
        --primary: {primary};
        --bg: {bg};
        --card: {card};
        --text: {text};
        --radius: {radius}px;
        --palette: {palette_css};
      }}

      .stApp {{
        background: var(--bg);
        color: var(--text);
      }}

      /* زر */
      .stButton > button {{
        background: var(--primary) !important;
        border: 1px solid var(--primary) !important;
        color: #fff !important;
        border-radius: var(--radius) !important;
        padding: 0.6rem 1rem !important;
      }}

      /* بطاقات/حاويات */
      div[data-testid="stMetric"] {{
        background: var(--card) !important;
        border-radius: var(--radius) !important;
        padding: 14px !important;
      }}

      /* صندوق اللوقو */
      .pmo-logo-wrap {{
        display: flex;
        justify-content: {justify};
        margin-top: {top_margin}px;
        margin-bottom: {bottom_margin}px;
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
