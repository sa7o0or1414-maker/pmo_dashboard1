import os
import re
from datetime import datetime, date

import pandas as pd
import streamlit as st
import plotly.express as px

from utils.layout import render_header
from utils.settings import load_settings

st.set_page_config(page_title="الداشبورد", layout="wide")
render_header(title_key_base="dashboard_title", page_title_fallback="📊 داشبورد المشاريع")

settings = load_settings()
theme = settings.get("theme", {})
palette = theme.get("palette", ["#3B82F6", "#22C55E", "#F59E0B", "#EF4444", "#A855F7"])
data_cfg = settings.get("data", {})
lat_col = data_cfg.get("lat_col", "lat")
lon_col = data_cfg.get("lon_col", "lon")
map_link_col = data_cfg.get("map_link_col", "رابط الموقع")

path = os.path.join("data", "latest.xlsx")
if not os.path.exists(path):
    st.warning("لا يوجد ملف بيانات بعد. اذهبي لصفحة (رفع البيانات) وارفعِ ملف Excel.")
    st.stop()

df = pd.read_excel(path, sheet_name=0)
df.columns = [str(c).strip() for c in df.columns]

# ---------- Helpers ----------
def safe_unique(col):
    if col not in df.columns:
        return []
    return sorted([x for x in df[col].dropna().unique().tolist()])

def to_num(s):
    try:
        return float(s)
    except Exception:
        return None

def parse_latlon_from_link(link: str):
    """
    يدعم روابط Google Maps مثل:
    - .../@24.7136,46.6753,15z
    - ...?q=24.7136,46.6753
    """
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
        out[lat_col] = lats
        out[lon_col] = lons
        return out

    # no coords
    out[lat_col] = None
    out[lon_col] = None
    return out

# ---------- Sidebar filters ----------
st.sidebar.header("🎛️ الفلاتر")

status_opt = ["الكل"] + safe_unique("حالة المشروع")
mun_opt = ["الكل"] + safe_unique("البلدية")
entity_opt = ["الكل"] + safe_unique("الجهة")

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
c1, c2, c3, c4 = st.columns(4)

c1.metric("عدد المشاريع", f"{len(filtered):,}")

if "قيمة العقد" in filtered.columns:
    c2.metric("إجمالي قيمة العقود", f"{filtered['قيمة العقد'].fillna(0).sum():,.0f}")

if "قيمة المستخلصات المعتمده" in filtered.columns:
    c3.metric("إجمالي المستخلصات", f"{filtered['قيمة المستخلصات المعتمده'].fillna(0).sum():,.0f}")

if "نسبة الإنجاز" in filtered.columns:
    c4.metric("متوسط الإنجاز", f"{filtered['نسبة الإنجاز'].fillna(0).mean():.1f}%")

st.divider()

# ---------- Alerts + Forecast ----------
# Overdue rule:
# - planned_end = "تاريخ الانتهاء من المشروع"
# - overdue if today > planned_end AND progress < 100 AND status not "منتهي/مكتمل" (إن وجد)
today = pd.Timestamp(date.today())

alerts = filtered.copy()

if "تاريخ الانتهاء من المشروع" in alerts.columns:
    alerts["تاريخ الانتهاء من المشروع"] = pd.to_datetime(alerts["تاريخ الانتهاء من المشروع"], errors="coerce")

if "تاريخ تسليم الموقع" in alerts.columns:
    alerts["تاريخ تسليم الموقع"] = pd.to_datetime(alerts["تاريخ تسليم الموقع"], errors="coerce")

if "المدة المنقضية بالايام" in alerts.columns:
    alerts["المدة المنقضية بالايام"] = pd.to_numeric(alerts["المدة المنقضية بالايام"], errors="coerce")

if "نسبة الإنجاز" in alerts.columns:
    alerts["نسبة الإنجاز"] = pd.to_numeric(alerts["نسبة الإنجاز"], errors="coerce")

# Forecasted end date based on: predicted_total_days = elapsed_days / (progress/100)
# forecast_end = site_handover + predicted_total_days
alerts["predicted_total_days"] = None
alerts["forecast_end"] = pd.NaT

mask = (
    alerts.get("المدة المنقضية بالايام").notna()
    & alerts.get("نسبة الإنجاز").notna()
    & (alerts["نسبة الإنجاز"] > 0)
    & alerts.get("تاريخ تسليم الموقع").notna()
)

if mask is not None and mask.any():
    alerts.loc[mask, "predicted_total_days"] = alerts.loc[mask, "المدة المنقضية بالايام"] / (alerts.loc[mask, "نسبة الإنجاز"] / 100.0)
    alerts.loc[mask, "forecast_end"] = alerts.loc[mask, "تاريخ تسليم الموقع"] + pd.to_timedelta(alerts.loc[mask, "predicted_total_days"], unit="D")

# Overdue & risk flags
alerts["is_overdue"] = False
if "تاريخ الانتهاء من المشروع" in alerts.columns:
    prog = alerts["نسبة الإنجاز"] if "نسبة الإنجاز" in alerts.columns else pd.Series([None]*len(alerts))
    alerts["is_overdue"] = (alerts["تاريخ الانتهاء من المشروع"].notna()) & (today > alerts["تاريخ الانتهاء من المشروع"]) & (prog.fillna(0) < 100)

alerts["is_forecast_late"] = False
if "تاريخ الانتهاء من المشروع" in alerts.columns:
    alerts["is_forecast_late"] = (alerts["forecast_end"].notna()) & (alerts["تاريخ الانتهاء من المشروع"].notna()) & (alerts["forecast_end"] > alerts["تاريخ الانتهاء من المشروع"])

# Cards row
a1, a2, a3, a4 = st.columns(4)
a1.metric("متأخر فعليًا", f"{int(alerts['is_overdue'].sum()):,}")
a2.metric("متوقع يتأخر (Forecast)", f"{int(alerts['is_forecast_late'].sum()):,}")
if "TROUBLED3 PRO" in alerts.columns:
    a3.metric("TROUBLED3 PRO", f"{alerts['TROUBLED3 PRO'].fillna(0).sum():,.0f}")
else:
    a3.metric("تنبيهات", "—")
if "حالة المشروع" in alerts.columns:
    a4.metric("عدد حالات", f"{alerts['حالة المشروع'].nunique():,}")
else:
    a4.metric("عدد حالات", "—")

# Charts row
l, r = st.columns(2)

# Alerts chart
alerts_summary = pd.DataFrame({
    "الحالة": ["Overdue", "Forecast Late", "On Track"],
    "العدد": [
        int(alerts["is_overdue"].sum()),
        int(alerts["is_forecast_late"].sum()),
        int(len(alerts) - alerts["is_overdue"].sum())
    ]
})
fig_alerts = px.bar(alerts_summary, x="الحالة", y="العدد", title="تنبيهات التأخير", color="الحالة",
                    color_discrete_sequence=palette)
l.plotly_chart(fig_alerts, use_container_width=True)

# Forecast vs Planned (scatter if dates exist)
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

st.subheader("📌 قائمة المشاريع المتأخرة / المتوقع تأخرها")
cols_show = []
for c in ["رقم العقد","إسم المشـــروع","البلدية","الجهة","حالة المشروع","نسبة الإنجاز","تاريخ الانتهاء من المشروع","forecast_end"]:
    if c in alerts.columns:
        cols_show.append(c)
late_table = alerts[(alerts["is_overdue"]) | (alerts["is_forecast_late"])].copy()
if len(late_table) == 0:
    st.info("لا توجد مشاريع متأخرة أو متوقع تأخرها حسب القواعد الحالية.")
else:
    st.dataframe(late_table[cols_show], use_container_width=True)

st.divider()

# ---------- Map card ----------
st.subheader("🗺️ الخريطة (تتغير حسب الفلاتر)")
geo = ensure_latlon(filtered)
geo = geo.dropna(subset=[lat_col, lon_col]).copy()

if len(geo) == 0:
    st.info("لا توجد إحداثيات. أضيفي في Excel أعمدة lat/lon أو رابط Google Maps في عمود رابط الموقع.")
else:
    # مركز الخريطة يتغير حسب الفلترة (median)
    center_lat = float(geo[lat_col].median())
    center_lon = float(geo[lon_col].median())

    map_df = pd.DataFrame({
        "lat": geo[lat_col],
        "lon": geo[lon_col],
    })

    st.map(map_df, zoom=10)

st.divider()

# ---------- Regular charts ----------
g1, g2 = st.columns(2)

if "حالة المشروع" in filtered.columns:
    fig1 = px.histogram(filtered, x="حالة المشروع", title="توزيع المشاريع حسب الحالة",
                        color_discrete_sequence=palette)
    g1.plotly_chart(fig1, use_container_width=True)

if "البلدية" in filtered.columns:
    fig2 = px.histogram(filtered, x="البلدية", title="توزيع المشاريع حسب البلدية",
                        color_discrete_sequence=palette)
    g2.plotly_chart(fig2, use_container_width=True)

st.subheader("📋 جدول المشاريع (بعد الفلترة)")
st.dataframe(filtered, use_container_width=True)
