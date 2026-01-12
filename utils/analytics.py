from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import pandas as pd
import numpy as np


@dataclass
class AnalysisResult:
    df: pd.DataFrame
    filtered: pd.DataFrame
    overdue: pd.DataFrame
    forecast_late: pd.DataFrame


def _to_dt(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce")


def _to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    # أعمدة متوقعة (لو موجودة)
    if "تاريخ تسليم الموقع" in df.columns:
        df["تاريخ تسليم الموقع"] = _to_dt(df["تاريخ تسليم الموقع"])
    if "تاريخ الانتهاء من المشروع" in df.columns:
        df["تاريخ الانتهاء من المشروع"] = _to_dt(df["تاريخ الانتهاء من المشروع"])

    if "المدة المنقضية بالايام" in df.columns:
        df["المدة المنقضية بالايام"] = _to_num(df["المدة المنقضية بالايام"])
    if "نسبة الإنجاز" in df.columns:
        df["نسبة الإنجاز"] = _to_num(df["نسبة الإنجاز"])

    return df


def compute_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """
    يحسب:
    - is_overdue: متأخر فعليًا
    - is_forecast_late: متوقع يتأخر
    - forecast_end: تاريخ انتهاء متوقع
    - reason: سبب/منطق التنبؤ
    """
    out = df.copy()
    today = pd.Timestamp(date.today())

    out["predicted_total_days"] = pd.Series([np.nan] * len(out), dtype="float64")
    out["forecast_end"] = pd.NaT
    out["is_overdue"] = False
    out["is_forecast_late"] = False
    out["variance_days"] = np.nan
    out["reason"] = ""

    # Overdue فعلي
    if "تاريخ الانتهاء من المشروع" in out.columns:
        prog = out["نسبة الإنجاز"] if "نسبة الإنجاز" in out.columns else pd.Series([0] * len(out))
        out["is_overdue"] = (
            out["تاريخ الانتهاء من المشروع"].notna()
            & (today > out["تاريخ الانتهاء من المشروع"])
            & (prog.fillna(0) < 100)
        )

    # Forecast
    can_forecast = all(c in out.columns for c in ["تاريخ تسليم الموقع", "المدة المنقضية بالايام", "نسبة الإنجاز"])
    if can_forecast:
        # قواعد أمان
        MIN_PROGRESS = 0.5
        MAX_PRED_DAYS = 20000

        valid = (
            out["تاريخ تسليم الموقع"].notna()
            & out["المدة المنقضية بالايام"].notna()
            & out["نسبة الإنجاز"].notna()
            & (out["نسبة الإنجاز"] >= MIN_PROGRESS)
            & (out["نسبة الإنجاز"] <= 100)
            & (out["المدة المنقضية بالايام"] >= 0)
        )

        pred = out.loc[valid, "المدة المنقضية بالايام"] / (out.loc[valid, "نسبة الإنجاز"] / 100.0)
        pred = pred.where((pred >= 0) & (pred <= MAX_PRED_DAYS), np.nan)
        out.loc[valid, "predicted_total_days"] = pred

        valid2 = out["predicted_total_days"].notna()
        out.loc[valid2, "forecast_end"] = (
            out.loc[valid2, "تاريخ تسليم الموقع"]
            + pd.to_timedelta(out.loc[valid2, "predicted_total_days"], unit="D", errors="coerce")
        )

        if "تاريخ الانتهاء من المشروع" in out.columns:
            out["is_forecast_late"] = (
                out["forecast_end"].notna()
                & out["تاريخ الانتهاء من المشروع"].notna()
                & (out["forecast_end"] > out["تاريخ الانتهاء من المشروع"])
            )
            out["variance_days"] = (out["forecast_end"] - out["تاريخ الانتهاء من المشروع"]).dt.days

    # سبب التنبؤ
    def _fmt_days(x):
        try:
            return f"{int(round(float(x))):,} يوم"
        except Exception:
            return "—"

    def _fmt_pct(x):
        try:
            return f"{float(x):.1f}%"
        except Exception:
            return "—"

    for i, row in out.iterrows():
        if bool(row.get("is_overdue", False)):
            planned = row.get("تاريخ الانتهاء من المشروع", pd.NaT)
            if pd.isna(planned):
                out.at[i, "reason"] = "متأخر فعليًا: تاريخ الانتهاء المخطط غير موجود."
            else:
                out.at[i, "reason"] = f"متأخر فعليًا: تجاوز المخطط بـ {(today - planned).days} يوم."
            continue

        if bool(row.get("is_forecast_late", False)):
            # تفسير شفاف
            progress = row.get("نسبة الإنجاز", np.nan)
            elapsed = row.get("المدة المنقضية بالايام", np.nan)
            predicted = row.get("predicted_total_days", np.nan)
            variance = row.get("variance_days", np.nan)
            fe = row.get("forecast_end", pd.NaT)
            pe = row.get("تاريخ الانتهاء من المشروع", pd.NaT)

            if pd.isna(progress) or pd.isna(elapsed) or pd.isna(predicted) or pd.isna(fe) or pd.isna(pe):
                out.at[i, "reason"] = "متوقع يتأخر: بيانات غير كافية لحساب التنبؤ."
            else:
                out.at[i, "reason"] = (
                    f"التنبؤ مبني على: مدة منقضية {_fmt_days(elapsed)} + إنجاز {_fmt_pct(progress)} "
                    f"⇒ إجمالي متوقع {_fmt_days(predicted)} ⇒ تاريخ متوقع {pd.to_datetime(fe).date()} "
                    f"(تأخير متوقع ~ {int(variance)} يوم عن المخطط)."
                )

    return out


def apply_filters(df: pd.DataFrame, status: str, municipality: str, entity: str) -> pd.DataFrame:
    out = df.copy()

    if status != "الكل" and "حالة المشروع" in out.columns:
        out = out[out["حالة المشروع"] == status]
    if municipality != "الكل" and "البلدية" in out.columns:
        out = out[out["البلدية"] == municipality]
    if entity != "الكل" and "الجهة" in out.columns:
        out = out[out["الجهة"] == entity]

    return out


def analyze(df: pd.DataFrame, status: str, municipality: str, entity: str) -> AnalysisResult:
    df = prepare_dataframe(df)
    df_alerts = compute_alerts(df)
    filtered = apply_filters(df_alerts, status, municipality, entity)

    overdue = filtered[filtered["is_overdue"] == True].copy()  # noqa
    forecast_late = filtered[filtered["is_forecast_late"] == True].copy()  # noqa

    return AnalysisResult(df=df_alerts, filtered=filtered, overdue=overdue, forecast_late=forecast_late)
