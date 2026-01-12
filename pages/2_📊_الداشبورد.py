import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="الداشبورد", layout="wide")

st.title("📊 داشبورد المشاريع")

path = os.path.join("data", "latest.xlsx")
if not os.path.exists(path):
    st.warning("لا يوجد ملف بيانات بعد. اذهبي لصفحة (رفع البيانات) وارفعِ ملف Excel.")
    st.stop()

df = pd.read_excel(path, sheet_name=0)
df.columns = [str(c).strip() for c in df.columns]

# ---- فلاتر جانبية
st.sidebar.header("🎛️ الفلاتر")

def safe_unique(col):
    return sorted([x for x in df[col].dropna().unique().tolist()])

status_opt = ["الكل"] + safe_unique("حالة المشروع")
mun_opt    = ["الكل"] + safe_unique("البلدية")
entity_opt = ["الكل"] + safe_unique("الجهة")

status = st.sidebar.selectbox("حالة المشروع", status_opt)
mun    = st.sidebar.selectbox("البلدية", mun_opt)
entity = st.sidebar.selectbox("الجهة", entity_opt)

filtered = df.copy()
if status != "الكل":
    filtered = filtered[filtered["حالة المشروع"] == status]
if mun != "الكل":
    filtered = filtered[filtered["البلدية"] == mun]
if entity != "الكل":
    filtered = filtered[filtered["الجهة"] == entity]

# ---- مؤشرات
col1, col2, col3, col4 = st.columns(4)
col1.metric("عدد المشاريع", f"{len(filtered):,}")
if "قيمة العقد" in filtered.columns:
    col2.metric("إجمالي قيمة العقود", f"{filtered['قيمة العقد'].fillna(0).sum():,.0f}")
if "قيمة المستخلصات المعتمده" in filtered.columns:
    col3.metric("إجمالي المستخلصات", f"{filtered['قيمة المستخلصات المعتمده'].fillna(0).sum():,.0f}")
if "نسبة الإنجاز" in filtered.columns:
    col4.metric("متوسط الإنجاز", f"{filtered['نسبة الإنجاز'].fillna(0).mean():.1f}%")

st.divider()

# ---- رسوم بسيطة
left, right = st.columns(2)

if "حالة المشروع" in filtered.columns:
    fig1 = px.histogram(filtered, x="حالة المشروع", title="توزيع المشاريع حسب الحالة")
    left.plotly_chart(fig1, use_container_width=True)

if "البلدية" in filtered.columns:
    fig2 = px.histogram(filtered, x="البلدية", title="توزيع المشاريع حسب البلدية")
    right.plotly_chart(fig2, use_container_width=True)

st.subheader("📋 جدول المشاريع (بعد الفلترة)")
st.dataframe(filtered, use_container_width=True)
