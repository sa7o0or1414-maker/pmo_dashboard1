import os
import re
from datetime import date

import pandas as pd
import streamlit as st
import plotly.express as px

from utils.layout import render_header
from utils.settings import load_settings

# --------------------------------------------------
# إعدادات الصفحة
# --------------------------------------------------
st.set_page_config(page_title="الصفحة الرئيسية", page_icon="🏠", layout="wide")
import streamlit as st

st.set_page_config(
    page_title="الصفحة الرئيسية",
    page_icon="🏠",
    layout="wide"
)

# ==================================================
# 🎨 تخصيص السايدبار (إزالة App + توسيط العناوين)
# ==================================================
st.markdown("""
<style>
/* 1️⃣ حذف كلمة App (عنوان مجموعة الصفحات) */
div[data-testid="stSidebarNav"] > div:first-child {
    display: none !important;
}

/* 2️⃣ توسيط عنوان السايدبار المخصص */
section[data-testid="stSidebar"] h2 {
    text-align: center !important;
    width: 100%;
}

/* 3️⃣ تحسين المسافات */
section[data-testid="stSidebar"] {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 🏠 العناوين اللي تبغينها فعليًا
# ==================================================
st.sidebar.markdown(
    "<h2>🏠 الصفحة الرئيسية</h2>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<h3 style='text-align:center; margin-top:0.5rem;'>📊 لوحة المعلومات</h3>",
    unsafe_allow_html=True
)

# ✅ إخفاء كلمة App (عنوان التنقل الافتراضي في السايدبار)
st.markdown(
    """
    <style>
    /* Hide the default "App" label in sidebar navigation */
    div[data-testid="stSidebarNav"] > div:first-child {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ✅ العنوان اللي تبينه بدل App
st.sidebar.title("🏠 الصفحة الرئيسية")
st.sidebar.caption("📊 لوحة المعلومات")

# هيدر الموقع (اللوقو + العنوان + اللغة)
render_header(title_key_base="dashboard_title", page_title_fallback="📊 لوحة المعلومات")

# --------------------------------------------------
# الإعدادات
# --------------------------------------------------
settings = load_settings()
theme = settings.get("theme", {})
palette = theme.get("palette", ["#3B82F6", "#22C55E", "#F59E0B", "#EF4444", "#A855F7"])

data_cfg = settings.get("data", {})
lat_col = data_cfg.get("lat_col", "lat")
lon_col = data_cfg.get("lon_col", "lon")
map_link_col = data_cfg.get("map_link_col", "رابط الموقع")
show_map = bool(data_cfg.get("show_map", True))

# --------------------------------------------------
# تحميل البيانات
# --------------------------------------------------
path = os.path.join("data", "latest.xlsx")
if not os.path.exists(path):
    st.warning("لا يوجد ملف بيانات بعد. اذهبي لصفحة (رفع البيانات) وارفعِ ملف Excel.")
    st.stop()

df = pd.read_excel(path, sheet_name=0)
df.columns = [str(c).strip() for c in df.columns]

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def safe_unique(frame: pd.DataFrame, col: str):
    if col not in frame.columns:
        return []
    return sorted([x for x in frame[col].dropna().unique().tolist()])

def parse_latlon_from_link(link: str):
    """يدعم روابط Google Maps مثل .../@lat,lon أو ?q=lat,lon"""
    if not isinstance(link, str) or not link:
        return None, None

    m = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", link)
    if m:
        return float(m.group(1)), float(m.group(2))

    m = re.search(r"[?&]q=(-?\d+\.\d+),(-?\d+\.\d+)", link)
    if m:
        return float(m.group(1)), float(m.group(2))

    return None, None

def ensure_latlon(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()

    if lat_col in out.columns and lon_col in out.columns:
        out[lat_col] = pd.to_numeric(out[lat_col], errors="coerce")
        out[lon_col] = pd.to_numeric(out[lon_col], errors="coerce")
        return out

    if map_link_col in out.columns:
        lats, lons = [], []
        for x in out[map_link_col].fillna("").astype(str).tolist():
            la, lo = parse_latlon_from_link(x)
            lats.append(la)
            lons.append(lo)
        out[lat_col] = pd.to_numeric(pd.Series(lats), errors="coerce")
        out[lon_col] = pd.to_numeric(pd.Series(lons), errors="coerce")
        return out

    out[lat_col] = pd.NA
    out[lon_col] = pd.NA
    return out

def _fmt_days(x):
    try:
        if pd.isna(x):
            return "—"
        return f"{int(round(float(x))):,} يوم"
    except Exception:
        return "—"

def _fmt_pct(x):
    try:
        if pd.isna(x):
            return "—"
        return f"{float(x):.1f}%"
    except Exception:
        return "—"

def show_dropdown(table_df: pd.DataFrame, title: str):
    if len(table_df) == 0:
        st.info("لا توجد نتائج.")
        return

    name_col = "إسم المشـــروع" if "إسم المشـــروع" in table_df.columns else None

    with st.expander(title, expanded=True):
        if name_col:
            st.markdown("**أسماء المشاريع:**")
            for n in table_df[name_col].dropna().astype(str).unique().tolist():
                st.write("•", n)
        else:
            st.info("عمود اسم المشروع غير موجود.")

        cols_show = [c for c in [
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
        ] if c in table_df.columns]

        sort_cols = [c for c in ["is_overdue", "is_forecast_late", "variance_days"] if c in table_df.columns]
        if sort_cols:
            table_df = table_df.sort_values(by=sort_cols, ascending=[False] * len(sort_cols))

        st.dataframe(table_df[cols_show], use_container_width=True)

# --------------------------------------------------
# Sidebar filters (بدون عنوان "الفلاتر")
# --------------------------------------------------
status_opt = ["الكل"] + safe_unique(df, "حالة المشروع")
mun_opt = ["الكل"] + safe_unique(df, "البلدية")
entity_opt = ["الكل"] + safe_unique(df, "الجهة")

status = st.sidebar.selectbox("حالة المشروع", status_opt)
mun = st.sidebar.selectbox("البلدية", mun_opt)
entity = st.sidebar.selectbox("الجهة", entity_opt)

filtered = df.copy()
if status != "الكل" and "حالة المشروع" in filtered.columns:
    filtered = filtered[filtered["حالة المشروع"] == status]
if mun != "الكل" and "البلدية" in filtered.columns:
    filtered = filtered[filtered["البلدية"] == mun]
if entity != "الكل" and "الجهة" in filtered.columns:
    filtered = filtered[filtered["الجهة"] == entity]

# --------------------------------------------------
# KPIs
# --------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("عدد المشاريع", f"{len(filtered):,}")
k2.metric("إجمالي قيمة العقود", f"{filtered['قيمة العقد'].fillna(0).sum():,.0f}" if "قيمة العقد" in filtered.columns else "—")
k3.metric("إجمالي المستخلصات", f"{filtered['قيمة المستخلصات المعتمده'].fillna(0).sum():,.0f}" if "قيمة المستخلصات المعتمده" in filtered.columns else "—")
k4.metric("متوسط الإنجاز", f"{pd.to_numeric(filtered['نسبة الإنجاز'], errors='coerce').fillna(0).mean():.1f}%" if "نسبة الإنجاز" in filtered.columns else "—")

st.divider()

# --------------------------------------------------
# Alerts + Forecast
# --------------------------------------------------
alerts = filtered.copy()
today = pd.Timestamp(date.today())

if "تاريخ الانتهاء من المشروع" in alerts.columns:
    alerts["تاريخ الانتهاء من المشروع"] = pd.to_datetime(alerts["تاريخ الانتهاء من المشروع"], errors="coerce")
if "تاريخ تسليم الموقع" in alerts.columns:
    alerts["تاريخ تسليم الموقع"] = pd.to_datetime(alerts["تاريخ تسليم الموقع"], errors="coerce")
if "المدة المنقضية بالايام" in alerts.columns:
    alerts["المدة المنقضية بالايام"] = pd.to_numeric(alerts["المدة المنقضية بالايام"], errors="coerce")
if "نسبة الإنجاز" in alerts.columns:
    alerts["نسبة الإنجاز"] = pd.to_numeric(alerts["نسبة الإنجاز"], errors="coerce")

alerts["predicted_total_days"] = pd.Series([None] * len(alerts), dtype="float64")
alerts["forecast_end"] = pd.NaT

MAX_PREDICT_DAYS = 20000
MIN_PROGRESS = 0.5
MAX_PROGRESS = 100

can_forecast = (
    ("المدة المنقضية بالايام" in alerts.columns)
    and ("نسبة الإنجاز" in alerts.columns)
    and ("تاريخ تسليم الموقع" in alerts.columns)
)

if can_forecast:
    valid = (
        alerts["المدة المنقضية بالايام"].notna()
        & alerts["تاريخ تسليم الموقع"].notna()
        & alerts["نسبة الإنجاز"].notna()
        & (alerts["نسبة الإنجاز"] >= MIN_PROGRESS)
        & (alerts["نسبة الإنجاز"] <= MAX_PROGRESS)
        & (alerts["المدة المنقضية بالايام"] >= 0)
    )

    pred = alerts.loc[valid, "المدة المنقضية بالايام"] / (alerts.loc[valid, "نسبة الإنجاز"] / 100.0)
    pred = pred.where((pred >= 0) & (pred <= MAX_PREDICT_DAYS), other=pd.NA)
    alerts.loc[valid, "predicted_total_days"] = pred

    valid2 = alerts["predicted_total_days"].notna()
    alerts.loc[valid2, "forecast_end"] = (
        alerts.loc[valid2, "تاريخ تسليم الموقع"]
        + pd.to_timedelta(alerts.loc[valid2, "predicted_total_days"], unit="D", errors="coerce")
    )

alerts["is_overdue"] = False
if "تاريخ الانتهاء من المشروع" in alerts.columns:
    prog = alerts["نسبة الإنجاز"] if "نسبة الإنجاز" in alerts.columns else pd.Series([0] * len(alerts))
    alerts["is_overdue"] = (
        alerts["تاريخ الانتهاء من المشروع"].notna()
        & (today > alerts["تاريخ الانتهاء من المشروع"])
        & (prog.fillna(0) < 100)
    )

alerts["is_forecast_late"] = False
if "تاريخ الانتهاء من المشروع" in alerts.columns:
    alerts["is_forecast_late"] = (
        alerts["forecast_end"].notna()
        & alerts["تاريخ الانتهاء من المشروع"].notna()
        & (alerts["forecast_end"] > alerts["تاريخ الانتهاء من المشروع"])
    )

alerts["variance_days"] = pd.NA
if "تاريخ الانتهاء من المشروع" in alerts.columns:
    alerts["variance_days"] = (alerts["forecast_end"] - alerts["تاريخ الانتهاء من المشروع"]).dt.days

def build_reason(row):
    if bool(row.get("is_overdue", False)):
        planned = row.get("تاريخ الانتهاء من المشروع", pd.NaT)
        if pd.isna(planned):
            return "متأخر فعليًا: تاريخ الانتهاء المخطط غير موجود."
        return f"متأخر فعليًا: تجاوز المخطط بـ {(today - planned).days} يوم."

    if bool(row.get("is_forecast_late", False)):
        progress = row.get("نسبة الإنجاز", pd.NA)
        elapsed = row.get("المدة المنقضية بالايام", pd.NA)
        predicted = row.get("predicted_total_days", pd.NA)
        forecast_end = row.get("forecast_end", pd.NaT)
        planned_end = row.get("تاريخ الانتهاء من المشروع", pd.NaT)
        variance = row.get("variance_days", pd.NA)

        missing = []
        if pd.isna(progress): missing.append("نسبة الإنجاز")
        if pd.isna(elapsed): missing.append("المدة المنقضية")
        if pd.isna(predicted): missing.append("أيام متوقعة إجمالًا")
        if pd.isna(forecast_end): missing.append("تاريخ التنبؤ")
        if pd.isna(planned_end): missing.append("تاريخ الانتهاء المخطط")
        if missing:
            return "متوقع يتأخر: بيانات غير كافية (" + "، ".join(missing) + ")."

        return (
            f"التنبؤ: مدة {_fmt_days(elapsed)} مع إنجاز {_fmt_pct(progress)} "
            f"⇒ إجمالي متوقع {_fmt_days(predicted)} "
            f"⇒ تاريخ التنبؤ {pd.to_datetime(forecast_end).date()} "
            f"أبعد من المخطط بـ {int(variance)} يوم."
        )

    return ""

alerts["reason"] = alerts.apply(build_reason, axis=1)

# --------------------------------------------------
# Toggle buttons (ضغطة تظهر/ضغطة تختفي)
# --------------------------------------------------
if "alerts_toggle" not in st.session_state:
    st.session_state.alerts_toggle = None  # None | overdue | forecast

overdue_count = int(alerts["is_overdue"].sum())
forecast_count = int(alerts["is_forecast_late"].sum())

col_over, col_fore = st.columns(2)

with col_over:
    if st.button(f"⛔ متأخر فعليًا • {overdue_count:,}", use_container_width=True, key="btn_overdue"):
        st.session_state.alerts_toggle = None if st.session_state.alerts_toggle == "overdue" else "overdue"
    if st.session_state.alerts_toggle == "overdue":
        show_dropdown(alerts[alerts["is_overdue"]].copy(), "📌 تفاصيل المتأخرة فعليًا")

with col_fore:
    if st.button(f"⚠️ متوقع يتأخر (Forecast) • {forecast_count:,}", use_container_width=True, key="btn_forecast"):
        st.session_state.alerts_toggle = None if st.session_state.alerts_toggle == "forecast" else "forecast"
    if st.session_state.alerts_toggle == "forecast":
        show_dropdown(alerts[alerts["is_forecast_late"]].copy(), "📌 تفاصيل المتوقع تأخرها + سبب التنبؤ")

st.divider()

# --------------------------------------------------
# Charts
# --------------------------------------------------
l, r = st.columns(2)

alerts_summary = pd.DataFrame(
    {
        "الحالة": ["Overdue", "Forecast Late", "On Track"],
        "العدد": [
            int(alerts["is_overdue"].sum()),
            int(alerts["is_forecast_late"].sum()),
            int(max(len(alerts) - alerts["is_overdue"].sum(), 0)),
        ],
    }
)

fig_alerts = px.bar(
    alerts_summary,
    x="الحالة",
    y="العدد",
    title="تنبيهات التأخير",
    color="الحالة",
    color_discrete_sequence=palette,
)
l.plotly_chart(fig_alerts, use_container_width=True)

if "تاريخ الانتهاء من المشروع" in alerts.columns:
    tmp = alerts.copy()
    tmp = tmp[tmp["تاريخ الانتهاء من المشروع"].notna() | tmp["forecast_end"].notna()].copy()
    if len(tmp) > 0:
        tmp["project_label"] = tmp["إسم المشـــروع"] if "إسم المشـــروع" in tmp.columns else tmp.index.astype(str)
        fig_fc = px.scatter(
            tmp,
            x="تاريخ الانتهاء من المشروع",
            y="forecast_end",
            hover_name="project_label",
            title="مقارنة المخطط vs التنبؤ (Forecast)",
        )
        r.plotly_chart(fig_fc, use_container_width=True)
    else:
        r.info("لا توجد بيانات كافية لعرض التنبؤ.")
else:
    r.info("عمود 'تاريخ الانتهاء من المشروع' غير موجود لعرض التنبؤ.")

st.divider()

# --------------------------------------------------
# Map (اختياري من الإعدادات)
# --------------------------------------------------
if show_map:
    st.subheader("🗺️ الخريطة (تتغير حسب الفلاتر)")

    geo = ensure_latlon(filtered)
    geo = geo.dropna(subset=[lat_col, lon_col]).copy()

    if len(geo) == 0:
        st.info("لا توجد إحداثيات. أضيفي في Excel أعمدة lat/lon أو رابط Google Maps في عمود رابط الموقع.")
    else:
        map_df = pd.DataFrame(
            {
                "lat": geo[lat_col].astype(float),
                "lon": geo[lon_col].astype(float),
            }
        )
        st.map(map_df, zoom=10)

    st.divider()

# --------------------------------------------------
# Regular charts
# --------------------------------------------------
g1, g2 = st.columns(2)

if "حالة المشروع" in filtered.columns:
    fig1 = px.histogram(
        filtered,
        x="حالة المشروع",
        title="توزيع المشاريع حسب الحالة",
        color_discrete_sequence=palette,
    )
    g1.plotly_chart(fig1, use_container_width=True)
else:
    g1.info("لا يوجد عمود 'حالة المشروع'.")

if "البلدية" in filtered.columns:
    fig2 = px.histogram(
        filtered,
        x="البلدية",
        title="توزيع المشاريع حسب البلدية",
        color_discrete_sequence=palette,
    )
    g2.plotly_chart(fig2, use_container_width=True)
else:
    g2.info("لا يوجد عمود 'البلدية'.")

st.subheader("📋 جدول المشاريع (بعد الفلترة)")
st.dataframe(filtered, use_container_width=True)
