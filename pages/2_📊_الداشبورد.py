import os
import re
from datetime import date

import pandas as pd
import streamlit as st
import plotly.express as px

from utils.layout import render_header
from utils.settings import load_settings

# ---------- Page config ----------
st.set_page_config(page_title="الداشبورد", layout="wide")
render_header(title_key_base="dashboard_title", page_title_fallback="📊 داشبورد المشاريع")

# ---------- Settings ----------
settings = load_settings()
theme = settings.get("theme", {})
palette = theme.get("palette", ["#3B82F6", "#22C55E", "#F59E0B", "#EF4444", "#A855F7"])
data_cfg = settings.get("data", {})
lat_col = data_cfg.get("lat_col", "lat")
lon_col = data_cfg.get("lon_col", "lon")
map_link_col = data_cfg.get("map_link_col", "رابط الموقع")

# ---------- Load data ----------
path = os.path.join("data", "latest.xlsx")
if not os.path.exists(path):
    st.warning("لا يوجد ملف بيانات بعد. اذهبي لصفحة (رفع البيانات) وارفعِ ملف Excel.")
    st.stop()

df = pd.read_excel(path, sheet_name=0)
df.columns = [str(c).strip() for c in df.columns]

# ---------- Helpers ----------
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

def show_projects_dropdown(table_df: pd.DataFrame, title: str, show_reason: bool = True):
    """منسدلة تلقائيًا تعرض: أسماء المشاريع + جدول مع أسباب (اختياري)."""
    if len(table_df) == 0:
        st.info("لا توجد نتائج.")
        return

    name_col = "إسم المشـــروع" if "إسم المشـــروع" in table_df.columns else None

    with st.expander(title, expanded=True):
        # أسماء المشاريع
        if name_col:
            st.markdown("**أسماء المشاريع:**")
            names = table_df[name_col].dropna().astype(str).unique().tolist()
            for n in names:
                st.write("•", n)
        else:
            st.info("عمود اسم المشروع غير موجود.")

        # جدول
        base_cols = [
            "رقم العقد",
            "إسم المشـــروع",
            "البلدية",
            "الجهة",
            "حالة المشروع",
            "نسبة الإنجاز",
            "تاريخ الانتهاء من المشروع",
            "forecast_end",
            "variance_days",
        ]
        if show_reason:
            base_cols.insert(8, "reason")  # سبب التأخر/التنبؤ

        cols_show = [c for c in base_cols if c in table_df.columns]

        # ترتيب: المتأخر أولًا
        sort_cols = [c for c in ["is_overdue", "is_forecast_late", "variance_days"] if c in table_df.columns]
        if sort_cols:
            asc = [False, False, False][: len(sort_cols)]
            table_df = table_df.sort_values(by=sort_cols, ascending=asc)

        st.dataframe(table_df[cols_show], use_container_width=True)

# ---------- Sidebar filters (بدون كلمة الفلاتر) ----------
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

# ---------- KPIs ----------
k1, k2, k3, k4 = st.columns(4)
k1.metric("عدد المشاريع", f"{len(filtered):,}")

if "قيمة العقد" in filtered.columns:
    k2.metric("إجمالي قيمة العقود", f"{filtered['قيمة العقد'].fillna(0).sum():,.0f}")
else:
    k2.metric("إجمالي قيمة العقود", "—")

if "قيمة المستخلصات المعتمده" in filtered.columns:
    k3.metric("إجمالي المستخلصات", f"{filtered['قيمة المستخلصات المعتمده'].fillna(0).sum():,.0f}")
else:
    k3.metric("إجمالي المستخلصات", "—")

if "نسبة الإنجاز" in filtered.columns:
    k4.metric("متوسط الإنجاز", f"{pd.to_numeric(filtered['نسبة الإنجاز'], errors='coerce').fillna(0).mean():.1f}%")
else:
    k4.metric("متوسط الإنجاز", "—")

st.divider()

# ---------- Alerts + Forecast ----------
alerts = filtered.copy()
today = pd.Timestamp(date.today())

# تجهيز تواريخ/أرقام
if "تاريخ الانتهاء من المشروع" in alerts.columns:
    alerts["تاريخ الانتهاء من المشروع"] = pd.to_datetime(alerts["تاريخ الانتهاء من المشروع"], errors="coerce")

if "تاريخ تسليم الموقع" in alerts.columns:
    alerts["تاريخ تسليم الموقع"] = pd.to_datetime(alerts["تاريخ تسليم الموقع"], errors="coerce")

if "المدة المنقضية بالايام" in alerts.columns:
    alerts["المدة المنقضية بالايام"] = pd.to_numeric(alerts["المدة المنقضية بالايام"], errors="coerce")

if "نسبة الإنجاز" in alerts.columns:
    alerts["نسبة الإنجاز"] = pd.to_numeric(alerts["نسبة الإنجاز"], errors="coerce")

# ---------- Forecast (محصّن) ----------
alerts["predicted_total_days"] = pd.Series([None] * len(alerts), dtype="float64")
alerts["forecast_end"] = pd.NaT

MAX_PREDICT_DAYS = 20000
MIN_PROGRESS = 0.5
MAX_PROGRESS = 100

can_forecast = (
    ("المدة المنقضية بالايام" in alerts.columns) and
    ("نسبة الإنجاز" in alerts.columns) and
    ("تاريخ تسليم الموقع" in alerts.columns)
)

if can_forecast:
    valid = (
        alerts["المدة المنقضية بالايام"].notna() &
        alerts["تاريخ تسليم الموقع"].notna() &
        alerts["نسبة الإنجاز"].notna() &
        (alerts["نسبة الإنجاز"] >= MIN_PROGRESS) &
        (alerts["نسبة الإنجاز"] <= MAX_PROGRESS) &
        (alerts["المدة المنقضية بالايام"] >= 0)
    )

    pred = alerts.loc[valid, "المدة المنقضية بالايام"] / (alerts.loc[valid, "نسبة الإنجاز"] / 100.0)
    pred = pred.where((pred >= 0) & (pred <= MAX_PREDICT_DAYS), other=pd.NA)
    alerts.loc[valid, "predicted_total_days"] = pred

    valid2 = alerts["predicted_total_days"].notna()
    alerts.loc[valid2, "forecast_end"] = (
        alerts.loc[valid2, "تاريخ تسليم الموقع"] +
        pd.to_timedelta(alerts.loc[valid2, "predicted_total_days"], unit="D", errors="coerce")
    )

# Flags
alerts["is_overdue"] = False
if "تاريخ الانتهاء من المشروع" in alerts.columns:
    prog = alerts["نسبة الإنجاز"] if "نسبة الإنجاز" in alerts.columns else pd.Series([0] * len(alerts))
    alerts["is_overdue"] = (
        alerts["تاريخ الانتهاء من المشروع"].notna() &
        (today > alerts["تاريخ الانتهاء من المشروع"]) &
        (prog.fillna(0) < 100)
    )

alerts["is_forecast_late"] = False
if "تاريخ الانتهاء من المشروع" in alerts.columns:
    alerts["is_forecast_late"] = (
        alerts["forecast_end"].notna() &
        alerts["تاريخ الانتهاء من المشروع"].notna() &
        (alerts["forecast_end"] > alerts["تاريخ الانتهاء من المشروع"])
    )

# ---------- Reasons (سبب التأخر/التنبؤ) ----------
alerts["variance_days"] = pd.NA  # الفرق بين forecast_end و planned_end
if "تاريخ الانتهاء من المشروع" in alerts.columns:
    # variance_days = forecast_end - planned_end
    alerts["variance_days"] = (alerts["forecast_end"] - alerts["تاريخ الانتهاء من المشروع"]).dt.days

def build_reason(row):
    # متأخر فعليًا
    if bool(row.get("is_overdue", False)):
        planned = row.get("تاريخ الانتهاء من المشروع", pd.NaT)
        if pd.isna(planned):
            return "متأخر فعليًا: تاريخ الانتهاء المخطط غير موجود."
        days = (today - planned).days
        return f"متأخر فعليًا: تجاوز تاريخ الانتهاء المخطط بـ {days} يوم."

    # متوقع يتأخر (Forecast)
    if bool(row.get("is_forecast_late", False)):
        progress = row.get("نسبة الإنجاز", pd.NA)
        elapsed = row.get("المدة المنقضية بالايام", pd.NA)
        predicted = row.get("predicted_total_days", pd.NA)
        forecast_end = row.get("forecast_end", pd.NaT)
        planned_end = row.get("تاريخ الانتهاء من المشروع", pd.NaT)
        variance = row.get("variance_days", pd.NA)

        # إذا بيانات ناقصة
        missing = []
        if pd.isna(progress): missing.append("نسبة الإنجاز")
        if pd.isna(elapsed): missing.append("المدة المنقضية")
        if pd.isna(predicted): missing.append("أيام متوقعة إجمالًا")
        if pd.isna(forecast_end): missing.append("تاريخ التنبؤ")
        if pd.isna(planned_end): missing.append("تاريخ الانتهاء المخطط")

        if missing:
            return "متوقع يتأخر: بيانات غير كافية (" + "، ".join(missing) + ")."

        # رسالة تفسير التنبؤ
        return (
            f"التنبؤ: المدة المنقضية {_fmt_days(elapsed)} مع إنجاز {_fmt_pct(progress)} "
            f"⇒ الأيام المتوقعة إجمالًا {_fmt_days(predicted)} "
            f"⇒ تاريخ التنبؤ {pd.to_datetime(forecast_end).date()} "
            f"أبعد من المخطط بـ {int(variance)} يوم."
        )

    # لا شيء
    return ""

alerts["reason"] = alerts.apply(build_reason, axis=1)

# ---------- Click-to-expand cards (منسدلة تحتها) ----------
if "alerts_view" not in st.session_state:
    st.session_state.alerts_view = None  # None | overdue | forecast | all

overdue_count = int(alerts["is_overdue"].sum())
forecast_count = int(alerts["is_forecast_late"].sum())

col_over, col_fore, col_all = st.columns([3, 3, 2])

with col_over:
    if st.button(f"⛔ متأخر فعليًا • {overdue_count:,}", use_container_width=True, key="btn_overdue"):
        st.session_state.alerts_view = "overdue"

    if st.session_state.alerts_view == "overdue":
        df_over = alerts[alerts["is_overdue"]].copy()
        # للمتأخر فعليًا: نعرض السبب (عدد الأيام)
        show_projects_dropdown(df_over, "📌 تفاصيل المشاريع المتأخرة فعليًا", show_reason=True)

with col_fore:
    if st.button(f"⚠️ متوقع يتأخر (Forecast) • {forecast_count:,}", use_container_width=True, key="btn_forecast"):
        st.session_state.alerts_view = "forecast"

    if st.session_state.alerts_view == "forecast":
        df_fc = alerts[alerts["is_forecast_late"]].copy()
        # للي متوقع يتأخر: نعرض سبب التنبؤ بالتفصيل
        show_projects_dropdown(df_fc, "📌 تفاصيل المشاريع المتوقع تأخرها (Forecast) + سبب التنبؤ", show_reason=True)

with col_all:
    if st.button("🔎 عرض الكل", use_container_width=True, key="btn_all"):
        st.session_state.alerts_view = "all"

    if st.session_state.alerts_view == "all":
        df_all = alerts[(alerts["is_overdue"]) | (alerts["is_forecast_late"])].copy()
        show_projects_dropdown(df_all, "📌 كل المشاريع (متأخرة + متوقع تأخرها) + الأسباب", show_reason=True)

st.divider()

# ---------- Alerts charts ----------
l, r = st.columns(2)

alerts_summary = pd.DataFrame({
    "الحالة": ["Overdue", "Forecast Late", "On Track"],
    "العدد": [
        int(alerts["is_overdue"].sum()),
        int(alerts["is_forecast_late"].sum()),
        int(max(len(alerts) - alerts["is_overdue"].sum(), 0))
    ]
})

fig_alerts = px.bar(
    alerts_summary,
    x="الحالة",
    y="العدد",
    title="تنبيهات التأخير",
    color="الحالة",
    color_discrete_sequence=palette
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

# ---------- Map (changes with filters) ----------
st.subheader("🗺️ الخريطة (تتغير حسب الفلاتر)")

geo = ensure_latlon(filtered)
geo = geo.dropna(subset=[lat_col, lon_col]).copy()

if len(geo) == 0:
    st.info("لا توجد إحداثيات. أضيفي في Excel أعمدة lat/lon أو رابط Google Maps في عمود رابط الموقع.")
else:
    map_df = pd.DataFrame({
        "lat": geo[lat_col].astype(float),
        "lon": geo[lon_col].astype(float),
    })
    st.map(map_df, zoom=10)

st.divider()

# ---------- Regular charts ----------
g1, g2 = st.columns(2)

if "حالة المشروع" in filtered.columns:
    fig1 = px.histogram(
        filtered,
        x="حالة المشروع",
        title="توزيع المشاريع حسب الحالة",
        color_discrete_sequence=palette
    )
    g1.plotly_chart(fig1, use_container_width=True)
else:
    g1.info("لا يوجد عمود 'حالة المشروع'.")

if "البلدية" in filtered.columns:
    fig2 = px.histogram(
        filtered,
        x="البلدية",
        title="توزيع المشاريع حسب البلدية",
        color_discrete_sequence=palette
    )
    g2.plotly_chart(fig2, use_container_width=True)
else:
    g2.info("لا يوجد عمود 'البلدية'.")

st.subheader("📋 جدول المشاريع (بعد الفلترة)")
st.dataframe(filtered, use_container_width=True)
