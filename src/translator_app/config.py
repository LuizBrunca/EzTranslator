import json
import os
from pathlib import Path

APP_NAME = "EzTranslator"

APPDATA_DIR = Path(os.getenv("LOCALAPPDATA", Path.home())) / APP_NAME
LOGS_DIR = APPDATA_DIR / "logs"
LOCK_FILE = APPDATA_DIR / "eztranslator.lock"
CONFIG_FILE = APPDATA_DIR / "config.json"

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
ICON_PATH = ASSETS_DIR / "app.ico"

APPDATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CONFIG = {
    "source_lang": "auto",
    "target_lang": "pt",
    "hotkey": "<ctrl>+<alt>+t",
}


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return dict(DEFAULT_CONFIG)

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONFIG)

    return {**DEFAULT_CONFIG, **data}


def save_config(data: dict) -> None:
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
