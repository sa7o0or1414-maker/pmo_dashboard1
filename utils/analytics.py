import pandas as pd
from types import SimpleNamespace


def analyze(df: pd.DataFrame, status="الكل", municipality="الكل", entity="الكل"):
    data = df.copy()

    # تنظيف أسماء الأعمدة
    data.columns = [str(c).strip() for c in data.columns]

    # تطبيق الفلاتر لو الأعمدة موجودة
    if status != "الكل" and "حالة المشروع" in data.columns:
        data = data[data["حالة المشروع"] == status]

    if municipality != "الكل" and "البلدية" in data.columns:
        data = data[data["البلدية"] == municipality]

    if entity != "الكل" and "الجهة" in data.columns:
        data = data[data["الجهة"] == entity]

    today = pd.Timestamp.today().normalize()

    # -----------------------------
    # المتأخرة فعليًا
    # -----------------------------
    overdue = pd.DataFrame()
    if "تاريخ الانتهاء من المشروع" in data.columns:
        end_plan = pd.to_datetime(data["تاريخ الانتهاء من المشروع"], errors="coerce")

        # لو نسبة الإنجاز موجودة نخلي المتأخر فعليًا: اليوم > تاريخ الانتهاء و الإنجاز < 100
        if "نسبة الإنجاز" in data.columns:
            prog = pd.to_numeric(data["نسبة الإنجاز"], errors="coerce")
            overdue_mask = (end_plan.notna()) & (end_plan < today) & (prog.fillna(0) < 100)
        else:
            overdue_mask = (end_plan.notna()) & (end_plan < today)

        overdue = data.loc[overdue_mask].copy()
        overdue["reason"] = "تجاوز تاريخ الانتهاء المخطط"

    # -----------------------------
    # المتوقع تأخرها (تنبؤ بسيط واضح)
    # predicted_total_days = elapsed_days / (progress%)
    # forecast_end = site_handover + predicted_total_days
    # إذا forecast_end > planned_end => متوقع تأخر
    # -----------------------------
    forecast = pd.DataFrame()

    need_cols = {"تاريخ تسليم الموقع", "المدة المنقضية بالايام", "نسبة الإنجاز", "تاريخ الانتهاء من المشروع"}
    if need_cols.issubset(set(data.columns)):
        start = pd.to_datetime(data["تاريخ تسليم الموقع"], errors="coerce")
        elapsed = pd.to_numeric(data["المدة المنقضية بالايام"], errors="coerce")
        prog = pd.to_numeric(data["نسبة الإنجاز"], errors="coerce")
        end_plan = pd.to_datetime(data["تاريخ الانتهاء من المشروع"], errors="coerce")

        prog_ratio = (prog / 100.0).replace([0, float("inf"), -float("inf")], pd.NA)

        # تجنب القيم الشاذة
        valid = (
            start.notna()
            & end_plan.notna()
            & elapsed.notna()
            & prog_ratio.notna()
            & (elapsed >= 0)
            & (prog_ratio > 0)
            & (prog_ratio <= 1.0)
        )

        predicted_total_days = pd.Series(pd.NA, index=data.index, dtype="float64")
        predicted_total_days.loc[valid] = (elapsed.loc[valid] / prog_ratio.loc[valid]).clip(lower=0, upper=50000)

        forecast_end = pd.Series(pd.NaT, index=data.index, dtype="datetime64[ns]")
        # تحويل الأيام لتايم دلتا مع حماية OutOfBounds
        safe_days = predicted_total_days.fillna(0).astype("float64").clip(0, 50000)
        forecast_end.loc[valid] = start.loc[valid] + pd.to_timedelta(safe_days.loc[valid], unit="D")

        variance_days = (forecast_end - end_plan).dt.days

        late_mask = valid & forecast_end.notna() & (forecast_end > end_plan)

        forecast = data.loc[late_mask].copy()
        forecast["predicted_total_days"] = predicted_total_days.loc[late_mask].round(0)
        forecast["forecast_end"] = forecast_end.loc[late_mask]
        forecast["variance_days"] = variance_days.loc[late_mask]

        # سبب التنبؤ نصيًا
        forecast["reason"] = (
            "التنبؤ مبني على: المدة المنقضية ÷ نسبة الإنجاز. "
            "نسبة الإنجاز الحالية منخفضة مقارنة بالمدة المنقضية مما يشير لتأخر محتمل."
        )

    return SimpleNamespace(
        filtered=data,
        overdue=overdue,
        forecast_late=forecast
    )
