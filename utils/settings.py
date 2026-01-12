import json
from pathlib import Path

SETTINGS_PATH = Path("data") / "ui_settings.json"

DEFAULT_SETTINGS = {
    "lang": "ar",  # default language (admin sets default)
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
 "layout": {
  "title_align": "right",
  "title_size_px": 22,
  "cards_gap_px": 38
},
    "data": {
        # أسماء الأعمدة المتوقعة للخريطة
        "lat_col": "lat",
        "lon_col": "lon",
        "map_link_col": "رابط الموقع"  # لو ما عندك lat/lon واستخدمتي رابط
    },
    "texts": {
        "dashboard_title_ar": "📊 داشبورد المشاريع",
        "dashboard_title_en": "📊 Projects Dashboard",
        "upload_title_ar": "📤 رفع البيانات الأسبوعي",
        "upload_title_en": "📤 Weekly Data Upload",
        "settings_title_ar": "🎨 إعدادات الواجهة (Admin)",
        "settings_title_en": "🎨 UI Settings (Admin)",
    }
}

def _deep_merge(defaults: dict, incoming: dict) -> dict:
    out = defaults.copy()
    for k, v in incoming.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out

def load_settings() -> dict:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if SETTINGS_PATH.exists():
        try:
            data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
            return _deep_merge(DEFAULT_SETTINGS, data)
        except Exception:
            return DEFAULT_SETTINGS
    return DEFAULT_SETTINGS

def save_settings(settings: dict) -> None:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
