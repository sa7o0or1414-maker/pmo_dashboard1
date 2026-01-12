import json
from pathlib import Path

SETTINGS_PATH = Path("data") / "ui_settings.json"

DEFAULT_SETTINGS = {
    "theme": {
        "primary": "#3B82F6",
        "bg": "#0B1220",
        "card_bg": "#111B2E",
        "text": "#E5E7EB",
        "radius": 18,
        "palette": ["#3B82F6", "#22C55E", "#F59E0B", "#EF4444", "#A855F7"]
    },
  "logo": {
    "enabled": True,
    "location": "header",
    "align": "left",
    "width": 160,
    "top_margin": 6,
    "bottom_margin": 10,
    "file_path": "data/logo.png"
}
}

def load_settings() -> dict:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if SETTINGS_PATH.exists():
        try:
            return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_SETTINGS
    return DEFAULT_SETTINGS

def save_settings(settings: dict) -> None:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
