import os
import pandas as pd
import streamlit as st
from utils.layout import render_header
render_header("📤 رفع البيانات الأسبوعي")
from utils.schema import REQUIRED_COLUMNS

st.set_page_config(page_title="رفع البيانات", layout="wide")

st.title("📤 رفع ملف البيانات الأسبوعي")
st.caption("ارفعي ملف Excel وسيتم تحديث الداشبورد مباشرة بعد التحقق من الأعمدة.")

uploaded = st.file_uploader("ارفع ملف Excel", type=["xlsx"])

def normalize_cols(cols):
    # توحيد بسيط لتقليل مشاكل المسافات
    return [str(c).strip() for c in cols]

if uploaded:
    try:
        df = pd.read_excel(uploaded, sheet_name=0)
        df.columns = normalize_cols(df.columns)

        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            st.error("❌ أعمدة ناقصة في الملف:")
            st.write(missing)
            st.stop()

        os.makedirs("data", exist_ok=True)
        save_path = os.path.join("data", "latest.xlsx")
        with open(save_path, "wb") as f:
            f.write(uploaded.getbuffer())

        st.success("✅ تم حفظ الملف وتحديث البيانات بنجاح!")
        st.info("الآن افتحي صفحة الداشبورد لمشاهدة التحديث.")

        st.subheader("معاينة سريعة")
        st.dataframe(df.head(20), use_container_width=True)

    except Exception as e:
        st.exception(e)
