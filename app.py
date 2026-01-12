import streamlit as st
from pathlib import Path

st.set_page_config(page_title="PMO Portal", layout="wide")

logo_path = Path("assets") / "logo.png"

try:
    if logo_path.exists():
        st.image(str(logo_path), width=160)
    else:
        st.warning("لم يتم العثور على اللوقو: assets/logo.png")
except Exception as e:
    st.warning("تعذر عرض اللوقو، لكن الموقع سيكمل العمل.")
    st.caption(str(e))

st.markdown(
    """
    <h1 style="margin-bottom:0;">PMO Portal</h1>
    <p style="opacity:0.8;margin-top:4px;">موقع داخلي لتحديث ومتابعة مشاريع البلديات</p>
    """,
    unsafe_allow_html=True
)
