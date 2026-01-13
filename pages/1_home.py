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

# فلاتر
st.sidebar.markdown("### 🔎 الفلاتر")

def uniq(col):
    return sorted(df[col].dropna().unique()) if col in df.columns else []

status = st.sidebar.selectbox("حالة المشروع", ["الكل"] + uniq("حالة المشروع"))
municipality = st.sidebar.selectbox("البلدية", ["الكل"] + uniq("البلدية"))
entity = st.sidebar.selectbox("الجهة", ["الكل"] + uniq("الجهة"))

res = analyze(df, status, municipality, entity)
filtered = res.filtered
overdue = res.overdue
forecast = res.forecast_late

# KPI Cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("عدد المشاريع", f"{len(filtered):,}")
c2.metric("متأخرة فعليًا", f"{len(overdue):,}")
c3.metric("متوقع تأخرها", f"{len(forecast):,}")

if "قيمة العقد" in filtered.columns:
    c4.metric("إجمالي قيمة العقود", f"{filtered['قيمة العقد'].fillna(0).sum():,.0f}")
else:
    c4.metric("إجمالي قيمة العقود", "—")

st.divider()

# Toggle tables on click
if "show_overdue" not in st.session_state:
    st.session_state.show_overdue = False
if "show_forecast" not in st.session_state:
    st.session_state.show_forecast = False

b1, b2 = st.columns(2)

with b1:
    if st.button(f"⛔ المشاريع المتأخرة فعليًا ({len(overdue):,})", use_container_width=True):
        st.session_state.show_overdue = not st.session_state.show_overdue

    if st.session_state.show_overdue:
        cols = [c for c in [
            "رقم العقد", "إسم المشـــروع", "البلدية", "الجهة", "حالة المشروع",
            "نسبة الإنجاز", "تاريخ الانتهاء من المشروع", "reason"
        ] if c in overdue.columns]
        st.dataframe(overdue[cols] if cols else overdue, use_container_width=True)

with b2:
    if st.button(f"⚠️ المشاريع المتوقع تأخرها ({len(forecast):,})", use_container_width=True):
        st.session_state.show_forecast = not st.session_state.show_forecast

    if st.session_state.show_forecast:
        cols = [c for c in [
            "رقم العقد", "إسم المشـــروع", "البلدية", "الجهة", "حالة المشروع",
            "نسبة الإنجاز", "تاريخ الانتهاء من المشروع", "forecast_end", "variance_days", "reason"
        ] if c in forecast.columns]
        st.dataframe(forecast[cols] if cols else forecast, use_container_width=True)

st.divider()

# Charts
row1_l, row1_r = st.columns(2)

if "حالة المشروع" in filtered.columns:
    row1_l.plotly_chart(
        px.histogram(filtered, x="حالة المشروع", title="توزيع المشاريع حسب الحالة"),
        use_container_width=True
    )
else:
    row1_l.info("عمود (حالة المشروع) غير موجود")

if "البلدية" in filtered.columns:
    vc = filtered["البلدية"].value_counts().reset_index()
    vc.columns = ["البلدية", "count"]
    row1_r.plotly_chart(
        px.bar(vc, x="البلدية", y="count", title="عدد المشاريع لكل بلدية"),
        use_container_width=True
    )
else:
    row1_r.info("عمود (البلدية) غير موجود")

row2_l, row2_r = st.columns(2)

if "نسبة الإنجاز" in filtered.columns:
    row2_l.plotly_chart(
        px.box(filtered, y="نسبة الإنجاز", title="توزيع نسبة الإنجاز"),
        use_container_width=True
    )
else:
    row2_l.info("عمود (نسبة الإنجاز) غير موجود")

if "نسبة الإنجاز" in filtered.columns and "نسبة الصرف" in filtered.columns:
    row2_r.plotly_chart(
        px.scatter(
            filtered, x="نسبة الإنجاز", y="نسبة الصرف",
            hover_name=("إسم المشـــروع" if "إسم المشـــروع" in filtered.columns else None),
            title="العلاقة بين الإنجاز والصرف"
        ),
        use_container_width=True
    )
else:
    row2_r.info("يلزم وجود (نسبة الإنجاز) و(نسبة الصرف)")

st.divider()

st.subheader("📋 جدول البيانات (حسب الفلاتر)")
st.dataframe(filtered, use_container_width=True)

