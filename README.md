<p align="right"><a href="README.pt-BR.md">Português</a></p>

# EzTranslator

A lightweight background translator for Windows. Press a global hotkey from anywhere, and a small popup translates whatever's on your clipboard — no window to open, no browser tab to switch to.

## Features

- Lives in the system tray, starts instantly, stays out of the way
- Global hotkey (default **Shift+Alt+T**, rebindable) opens a popup near your cursor
- Reads the clipboard automatically and translates immediately
- Auto-detects the source language, or pick one manually from the dropdown
- Quick-swap button to flip source/target
- Auto-translates as you type (after a short pause) or on Enter — no extra clicks
- Copy button to grab the result
- Closes on `Esc` or by clicking outside the popup
- Settings window: default languages, hotkey capture (click the field, press the new combo), start-with-Windows toggle
- Fully ephemeral — nothing about your translations is logged, stored, or kept in any history

Translation is powered by Google Translate (via [deep-translator](https://github.com/nidhaloff/deep-translator)), free, no API key required.

## Install

Download `EzTranslator.exe` from the [latest release](https://github.com/LuizBrunca/EzTranslator/releases/latest) and run it. No installer, no setup — it's a single executable.

> **Note:** since the executable isn't code-signed, Windows Defender SmartScreen may warn on first launch ("Windows protected your PC"). Click **More info** → **Run anyway**.

To start EzTranslator automatically on login, enable **Start with Windows** in the tray menu's Settings.

## Development

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```powershell
git clone https://github.com/LuizBrunca/EzTranslator.git
cd EzTranslator
uv sync
uv run translator-app
```

### Project structure

```text
src/translator_app/
├── main.py              # Entry point — wires tray, popup, hotkey listener, settings
├── tray.py               # System tray icon and menu
├── hotkey_listener.py     # Global hotkey registration (pynput)
├── single_instance.py    # Prevents running more than one copy at once
├── startup.py             # Windows "start on boot" registry toggle
├── config.py              # Paths + config.json load/save
├── logger.py               # Rotating file logger
├── ui/
│   ├── popup.py            # The translation popup
│   └── settings.py         # Settings window
├── translator/
│   ├── engine.py            # GoogleTranslator wrapper
│   ├── worker.py             # Runs translation on a background QThread
│   └── languages.py          # Curated language list
└── assets/
    └── app.ico
```

### Building the executable

```powershell
uv run pyinstaller translator-app.spec --noconfirm
```

Produces `dist/EzTranslator.exe` (single-file, windowed, no console).

## License

MIT — see [LICENSE](LICENSE).
