import streamlit as st

def apply_theme(
    primary: str,
    bg: str,
    card_bg: str,
    text: str,
    logo_width: int = 160,
    radius: int = 16,
):
    # CSS عام
    css = f"""
    <style>
      :root {{
        --primary: {primary};
        --bg: {bg};
        --card: {card_bg};
        --text: {text};
        --radius: {radius}px;
      }}

      /* خلفية التطبيق */
      .stApp {{
        background: var(--bg);
        color: var(--text);
      }}

      /* كروت/حاويات */
      div[data-testid="stMetric"], 
      div[data-testid="stDataFrame"],
      section[data-testid="stSidebar"] > div {{
        border-radius: var(--radius) !important;
      }}

      /* لون الأزرار */
      .stButton > button {{
        background: var(--primary) !important;
        border: 1px solid var(--primary) !important;
        color: white !important;
        border-radius: var(--radius) !important;
        padding: 0.6rem 1rem !important;
      }}

      /* مدخلات و سلايدرز */
      input, textarea, .stSelectbox, .stMultiSelect {{
        border-radius: var(--radius) !important;
      }}

      /* عنوان السايدبار */
      section[data-testid="stSidebar"] h2, 
      section[data-testid="stSidebar"] h3 {{
        color: var(--text) !important;
      }}

      /* ستايل بسيط للّوقو */
      .pmo-logo img {{
        width: {logo_width}px !important;
        height: auto !important;
        border-radius: 12px;
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
