import streamlit as st

uploaded_logo = st.sidebar.file_uploader("ارفع لوقو", type=["png", "jpg", "jpeg"])
if uploaded_logo:
    st.image(uploaded_logo, width=160)
else:
    st.title("PMO Portal")
