import pandas as pd
from types import SimpleNamespace

def analyze(df, status="الكل", municipality="الكل", entity="الكل"):
    data = df.copy()

    if status != "الكل" and "حالة المشروع" in data.columns:
        data = data[data["حالة المشروع"] == status]

    if municipality != "الكل" and "البلدية" in data.columns:
        data = data[data["البلدية"] == municipality]

    if entity != "الكل" and "الجهة" in data.columns:
        data = data[data["الجهة"] == entity]

    today = pd.Timestamp.today()

    overdue = pd.DataFrame()
    forecast = pd.DataFrame()

    # مشاريع متأخرة فعليًا
    if "تاريخ الانتهاء من المشروع" in data.columns:
        end = pd.to_datetime(data["تاريخ الانتهاء من المشروع"], errors="coerce")
        overdue = data[end < today].copy()
        overdue["reason"] = "تجاوز تاريخ الانتهاء المخطط"

    # تنبؤ بالتأخير
    if "نسبة الإنجاز" in data.columns and "المدة المنقضية بالايام" in data.columns:
        eng = pd.to_numeric(data["نسبة الإنجاز"], errors="coerce")
        days = pd.to_numeric(data["المدة المنقضية بالايام"], errors="coerce")

        mask = (eng < 80) & (days > 0)
        forecast = data[mask].copy()
        forecast["variance_days"] = (100 - eng[mask]) * 0.5
        forecast["reason"] = "انخفاض نسبة الإنجاز مقارنة بالمدة المنقضية"

    return SimpleNamespace(
        filtered=data,
        overdue=overdue,
        forecast_late=forecast
    )
