import os
import pandas as pd
import streamlit as st
import plotly.express as px
from utils.analytics import analyze

st.set_page_config(page_title="الصفحة الرئيسية", page_icon="🏠", layout="wide")
st.title("📊 لوحة المعلومات")

DATA_PATH = "data/latest.xlsx"
if not os.path.exists(DATA_PATH):
    st.warning("لا يوجد ملف Excel بعد. اذهبي إلى صفحة (رفع البيانات) وارفعي الملف.")
    st.stop()

df = pd.read_excel(DATA_PATH)
df.columns = [str(c).strip() for c in df.columns]

st.sidebar.markdown("### 🔎 الفلاتر")

def uniq(col):
    return sorted(df[col].dropna().unique()) if col in df.columns else []

status = st.sidebar.selectbox("حالة المشروع", ["الكل"] + uniq("حالة المشروع"))
municipality = st.sidebar.selectbox("البلدية", ["الكل"] + uniq("البلدية"))
entity = st.sidebar.selectbox("الجهة", ["الكل"] + uniq("الجهة"))

result = analyze(df, status, municipality, entity)
filtered = result.filtered
overdue = result.overdue
forecast = result.forecast_late

c1, c2, c3, c4 = st.columns(4)
c1.metric("عدد المشاريع", len(filtered))
c2.metric("المتأخرة فعليًا", len(overdue))
c3.metric("المتوقع تأخرها", len(forecast))
c4.metric("إجمالي السجلات", len(df))

st.divider()

if st.button(f"⛔ المشاريع المتأخرة ({len(overdue)})"):
    st.dataframe(overdue, use_container_width=True)

if st.button(f"⚠️ المشاريع المتوقع تأخرها ({len(forecast)})"):
    st.dataframe(forecast, use_container_width=True)

st.divider()

if "حالة المشروع" in filtered.columns:
    st.plotly_chart(px.histogram(filtered, x="حالة المشروع", title="توزيع المشاريع حسب الحالة"), use_container_width=True)

if "البلدية" in filtered.columns:
    st.plotly_chart(
        px.bar(filtered["البلدية"].value_counts().reset_index(), x="البلدية", y="count", title="عدد المشاريع لكل بلدية"),
        use_container_width=True
    )

st.divider()
st.subheader("📋 جدول البيانات")
st.dataframe(filtered, use_container_width=True)
