import os
import pandas as pd
import streamlit as st
import plotly.express as px
from utils.layout import sidebar_menu, page_title

sidebar_menu(active="home")
page_title("📊 لوحة المعلومات")
from utils.analytics import analyze

# --------------------------------------------------
# إعداد الصفحة
# --------------------------------------------------
st.set_page_config(
    page_title="الصفحة الرئيسية",
    page_icon="🏠",
    layout="wide"
)

sidebar_menu(active="dashboard")
page_title("📊 لوحة المعلومات")

# --------------------------------------------------
# التحقق من وجود ملف البيانات
# --------------------------------------------------
DATA_PATH = "data/latest.xlsx"

if not os.path.exists(DATA_PATH):
    st.warning("لا يوجد ملف Excel بعد. اذهبي إلى (📤 رفع البيانات) وارفعي الملف.")
    st.stop()

# --------------------------------------------------
# قراءة البيانات (كل الأعمدة مثل Power BI)
# --------------------------------------------------
df = pd.read_excel(DATA_PATH, sheet_name=0)
df.columns = [str(c).strip() for c in df.columns]

# --------------------------------------------------
# فلاتر (Power BI style)
# --------------------------------------------------
st.sidebar.markdown("### 🔎 الفلاتر")

def safe_unique(col):
    return sorted(df[col].dropna().unique().tolist()) if col in df.columns else []

status = st.sidebar.selectbox("حالة المشروع", ["الكل"] + safe_unique("حالة المشروع"))
municipality = st.sidebar.selectbox("البلدية", ["الكل"] + safe_unique("البلدية"))
entity = st.sidebar.selectbox("الجهة", ["الكل"] + safe_unique("الجهة"))

# --------------------------------------------------
# التحليل الذكي (تأخير + تنبؤ)
# --------------------------------------------------
result = analyze(
    df,
    status=status,
    municipality=municipality,
    entity=entity
)

filtered = result.filtered
overdue = result.overdue
forecast = result.forecast_late

# --------------------------------------------------
# كروت KPI
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("عدد المشاريع", f"{len(filtered):,}")

if "قيمة العقد" in filtered.columns:
    c2.metric("إجمالي قيمة العقود", f"{filtered['قيمة العقد'].fillna(0).sum():,.0f}")
else:
    c2.metric("إجمالي قيمة العقود", "—")

if "نسبة الإنجاز" in filtered.columns:
    c3.metric(
        "متوسط الإنجاز",
        f"{pd.to_numeric(filtered['نسبة الإنجاز'], errors='coerce').fillna(0).mean():.1f}%"
    )
else:
    c3.metric("متوسط الإنجاز", "—")

c4.metric(
    "التنبيهات",
    f"متأخرة: {len(overdue):,} | متوقعة: {len(forecast):,}"
)

st.divider()

# --------------------------------------------------
# مربعات التنبيهات (تفتح/تغلق بالضغط)
# --------------------------------------------------
if "show_overdue" not in st.session_state:
    st.session_state.show_overdue = False
if "show_forecast" not in st.session_state:
    st.session_state.show_forecast = False

b1, b2 = st.columns(2)

with b1:
    if st.button(f"⛔ المشاريع المتأخرة فعليًا ({len(overdue):,})", use_container_width=True):
        st.session_state.show_overdue = not st.session_state.show_overdue

    if st.session_state.show_overdue:
        cols = [
            c for c in [
                "رقم العقد",
                "إسم المشـــروع",
                "البلدية",
                "الجهة",
                "حالة المشروع",
                "نسبة الإنجاز",
                "تاريخ الانتهاء من المشروع",
                "reason",
            ] if c in overdue.columns
        ]
        st.dataframe(overdue[cols], use_container_width=True)

with b2:
    if st.button(f"⚠️ المشاريع المتوقع تأخرها ({len(forecast):,})", use_container_width=True):
        st.session_state.show_forecast = not st.session_state.show_forecast

    if st.session_state.show_forecast:
        cols = [
            c for c in [
                "رقم العقد",
                "إسم المشـــروع",
                "البلدية",
                "الجهة",
                "حالة المشروع",
                "نسبة الإنجاز",
                "تاريخ الانتهاء من المشروع",
                "forecast_end",
                "variance_days",
                "reason",
            ] if c in forecast.columns
        ]
        st.dataframe(forecast[cols], use_container_width=True)

st.divider()

# --------------------------------------------------
# شارتات ديناميكية (تُبنى من الأعمدة)
# --------------------------------------------------
row1_l, row1_r = st.columns(2)

if "حالة المشروع" in filtered.columns:
    fig = px.histogram(
        filtered,
        x="حالة المشروع",
        title="توزيع المشاريع حسب الحالة"
    )
    row1_l.plotly_chart(fig, use_container_width=True)
else:
    row1_l.info("عمود (حالة المشروع) غير موجود")

if "البلدية" in filtered.columns:
    fig = px.bar(
        filtered["البلدية"].value_counts().reset_index(),
        x="البلدية",
        y="count",
        title="عدد المشاريع لكل بلدية"
    )
    row1_r.plotly_chart(fig, use_container_width=True)
else:
    row1_r.info("عمود (البلدية) غير موجود")

row2_l, row2_r = st.columns(2)

if "نسبة الإنجاز" in filtered.columns:
    fig = px.box(
        filtered,
        y="نسبة الإنجاز",
        title="توزيع نسبة الإنجاز"
    )
    row2_l.plotly_chart(fig, use_container_width=True)
else:
    row2_l.info("عمود (نسبة الإنجاز) غير موجود")

if "قيمة العقد" in filtered.columns and "المقاول" in filtered.columns:
    top = (
        filtered
        .groupby("المقاول")["قيمة العقد"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig = px.bar(
        top,
        x="المقاول",
        y="قيمة العقد",
        title="أعلى 10 مقاولين حسب قيمة العقود"
    )
    row2_r.plotly_chart(fig, use_container_width=True)
else:
    row2_r.info("يلزم وجود (قيمة العقد) و(المقاول)")

row3_l, row3_r = st.columns(2)

if "نسبة الصرف" in filtered.columns:
    fig = px.histogram(
        filtered,
        x="نسبة الصرف",
        nbins=20,
        title="توزيع نسبة الصرف"
    )
    row3_l.plotly_chart(fig, use_container_width=True)
else:
    row3_l.info("عمود (نسبة الصرف) غير موجود")

if "نسبة الإنجاز" in filtered.columns and "نسبة الصرف" in filtered.columns:
    fig = px.scatter(
        filtered,
        x="نسبة الإنجاز",
        y="نسبة الصرف",
        hover_name=("إسم المشـــروع" if "إسم المشـــروع" in filtered.columns else None),
        title="العلاقة بين الإنجاز والصرف"
    )
    row3_r.plotly_chart(fig, use_container_width=True)
else:
    row3_r.info("يلزم وجود (نسبة الإنجاز) و(نسبة الصرف)")

st.divider()

# --------------------------------------------------
# جدول كامل (كل الأعمدة مثل Power BI)
# --------------------------------------------------
st.subheader("📋 جدول البيانات (حسب الفلاتر)")
st.dataframe(filtered, use_container_width=True)
