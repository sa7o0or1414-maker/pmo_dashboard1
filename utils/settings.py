import json
from pathlib import Path

SETTINGS_PATH = Path("data") / "ui_settings.json"

DEFAULT_SETTINGS = {
    "lang": "ar",  # ar | en
    "theme": {
        "primary": "#3B82F6",
        "bg": "#0B1220",
        "card_bg": "#111B2E",
        "text": "#E5E7EB",
        "radius": 18,
        "palette": ["#3B82F6", "#22C55E", "#F59E0B", "#EF4444", "#A855F7"],
        "font_ar": "Montserrat Arabic",
        "font_en": "Montserrat",
    },
    "logo": {
        "enabled": True,
        "location": "header",  # header | sidebar
        "align": "left",       # left | center | right
        "width": 160,
        "top_margin": 6,
        "bottom_margin": 10,
        "file_path": "data/logo.png"
    },
    "texts": {
        # عناوين قابلة للتعديل باللغتين
        "dashboard_title_ar": "📊 داشبورد المشاريع",
        "dashboard_title_en": "📊 Projects Dashboard",
        "upload_title_ar": "📤 رفع البيانات الأسبوعي",
        "upload_title_en": "📤 Weekly Data Upload",
        "settings_title_ar": "🎨 إعدادات الواجهة (Admin)",
        "settings_title_en": "🎨 UI Settings (Admin)",
    }
}

def load_settings() -> dict:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if SETTINGS_PATH.exists():
        try:
            data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
            # دمج مع الافتراضي لضمان مفاتيح جديدة
            merged = DEFAULT_SETTINGS.copy()
            merged.update(data)

            merged["theme"] = {**DEFAULT_SETTINGS["theme"], **data.get("theme", {})}
            merged["logo"] = {**DEFAULT_SETTINGS["logo"], **data.get("logo", {})}
            merged["texts"] = {**DEFAULT_SETTINGS["texts"], **data.get("texts", {})}
            return merged
        except Exception:
            return DEFAULT_SETTINGS
    return DEFAULT_SETTINGS

def save_settings(settings: dict) -> None:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
