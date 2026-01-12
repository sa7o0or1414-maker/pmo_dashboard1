import streamlit as st

st.set_page_config(page_title="PMO Portal", layout="wide")

# لوقو
st.image("assets/logo.png", width=160)

st.markdown(
    """
    <h1 style="margin-bottom:0;">PMO Portal</h1>
    <p style="opacity:0.8;margin-top:4px;">موقع داخلي لتحديث ومتابعة مشاريع البلديات</p>
    """,
    unsafe_allow_html=True
)

st.info("استخدمي القائمة الجانبية للتنقل: رفع البيانات → الداشبورد → المستخدمين")
