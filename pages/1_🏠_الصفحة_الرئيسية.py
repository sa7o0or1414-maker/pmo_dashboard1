import os
import pandas as pd
import streamlit as st
import plotly.express as px
from utils.analytics import analyze

# --------------------------------------------------
# إعداد الصفحة
# --------------------------------------------------
st.set_page_config(
    page_title="الصفحة الرئيسية",
    page_icon="🏠",
    layout="wide"
)

st.title("📊 لوحة المعلومات")

# --------------------------------------------------
# التحقق من وجود ملف البيانات
# --------------------------------------------------
DATA_PATH = "data/latest.xlsx"

if not os.path.exists(DATA_PATH):
    st.warning("لا يوجد ملف Excel بعد. انتقلي إلى صفحة (📤 رفع البيانات) وارفعي الملف.")
    st.stop()

# --------------------------------------------------
# قراءة البيانات
# --------------------------------------------------
df = pd.read_excel(DATA_PATH)
df.columns = [str(c).strip() for c in df.columns]

# --------------------------------------------------
# الفلاتر
# --------------------------------------------------
st.sidebar.markdown("### 🔎 الفلاتر")

def safe_unique(col):
    return sorted(df[col].dropna().unique().tolist()) if col in df.columns else []

status = st.sidebar.selectbox("حالة المشروع", ["الكل"] + safe_unique("حالة المشروع"))
municipality = st.sidebar.selectbox("البلدية", ["الكل"] + safe_unique("البلدية"))
entity = st.sidebar.selectbox("الجهة", ["الكل"] + safe_unique("الجهة"))

# --------------------------------------------------
# التحليل
# --------------------------------------------------
result = analyze(df, status, municipality, entity)

filtered = result.filtered
overdue = result.overdue
forecast = result.forecast_late

# --------------------------------------------------
# كروت
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("عدد المشاريع", len(filtered))

if "قيمة العقد" in filtered.columns:
    c2.metric("إجمالي العقود", f"{filtered['قيمة العقد'].sum():,.0f}")
else:
    c2.metric("إجمالي العقود", "—")

if "نسبة الإنجاز" in filtered.columns:
    c3.metric("متوسط الإنجاز", f"{filtered['نسبة الإنجاز'].mean():.1f}%")
else:
    c3.metric("متوسط الإنجاز", "—")

c4.metric("التنبيهات", f"متأخرة: {len(overdue)} | متوقعة: {len(forecast)}")

st.divider()

# --------------------------------------------------
# تنبيهات (زر يفتح / يقفل)
# --------------------------------------------------
if "show_overdue" not in st.session_state:
    st.session_state.show_overdue = False
if "show_forecast" not in st.session_state:
    st.session_state.show_forecast = False

b1, b2 = st.columns(2)

with b1:
    if st.button(f"⛔ المشاريع المتأخرة ({len(overdue)})"):
        st.session_state.show_overdue = not st.session_state.show_overdue
    if st.session_state.show_overdue:
        st.dataframe(overdue, use_container_width=True)

with b2:
    if st.button(f"⚠️ المشاريع المتوقع تأخرها ({len(forecast)})"):
        st.session_state.show_forecast = not st.session_state.show_forecast
    if st.session_state.show_forecast:
        st.dataframe(forecast, use_container_width=True)

st.divider()

# --------------------------------------------------
# شارتات
# --------------------------------------------------
if "حالة المشروع" in filtered.columns:
    st.plotly_chart(
        px.histogram(filtered, x="حالة المشروع", title="توزيع المشاريع حسب الحالة"),
        use_container_width=True
    )

if "البلدية" in filtered.columns:
    st.plotly_chart(
        px.bar(filtered["البلدية"].value_counts().reset_index(),
               x="البلدية", y="count",
               title="عدد المشاريع لكل بلدية"),
        use_container_width=True
    )

st.divider()

st.subheader("📋 جدول البيانات")
st.dataframe(filtered, use_container_width=True)
