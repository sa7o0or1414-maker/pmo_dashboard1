import streamlit as st

def apply_theme(theme: dict, logo: dict, layout: dict, lang: str):
    primary = theme.get("primary", "#3B82F6")
    bg = theme.get("bg", "#0B1220")
    card = theme.get("card_bg", "#111B2E")
    text = theme.get("text", "#E5E7EB")
    radius = int(theme.get("radius", 18))

    font_ar = theme.get("font_ar", "Montserrat Arabic")
    font_en = theme.get("font_en", "Montserrat")

    # اتجاه الصفحة
    direction = "rtl" if lang == "ar" else "ltr"
    font_family = "var(--font-ar)" if lang == "ar" else "var(--font-en)"

    # محاذاة عنوان الصفحة
    title_align = layout.get("title_align", "right")
    title_css_align = {"left": "left", "center": "center", "right": "right"}.get(title_align, "right")
    title_size = int(layout.get("title_size_px", 22))

    # 1 سم تقريبًا = 38px
    cards_gap_px = int(layout.get("cards_gap_px", 38))

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

      /* تقليل/تثبيت المسافات بين الأعمدة (يشمل الكروت) */
      div[data-testid="stHorizontalBlock"] {{
        gap: var(--cards-gap) !important;
      }}

      /* أزرار */
      .stButton > button {{
