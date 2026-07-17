import os
from pathlib import Path

APP_NAME = "EzTranslator"

APPDATA_DIR = Path(os.getenv("LOCALAPPDATA", Path.home())) / APP_NAME
LOGS_DIR = APPDATA_DIR / "logs"
LOCK_FILE = APPDATA_DIR / "eztranslator.lock"

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
ICON_PATH = ASSETS_DIR / "app.ico"

APPDATA_DIR.mkdir(parents=True, exist_ok=True)
