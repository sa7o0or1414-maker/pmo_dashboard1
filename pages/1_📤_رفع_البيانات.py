import os
from pathlib import Path
import streamlit as st

from utils.layout import sidebar_menu, page_title

st.set_page_config(page_title="رفع البيانات", page_icon="📤", layout="wide")
sidebar_menu(active="upload")
page_title("📤 رفع البيانات")

st.write("ارفعي ملف Excel وسيتم حفظه كـ **data/latest.xlsx** وتحديث لوحة المعلومات مباشرة.")

uploaded = st.file_uploader("رفع ملف Excel", type=["xlsx"])

if uploaded is not None:
    Path("data").mkdir(parents=True, exist_ok=True)
    save_path = os.path.join("data", "latest.xlsx")

    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())

    st.success("✅ تم رفع الملف بنجاح. انتقلي إلى (🏠 الصفحة الرئيسية) لرؤية الداشبورد.")
