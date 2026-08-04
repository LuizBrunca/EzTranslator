# Background Desktop Translator — Project Spec

> **Status: MVP shipped and released (see [releases](https://github.com/LuizBrunca/EzTranslator/releases)).**
> This doc still reflects the original plan; sections below are updated to match what was actually
> built, plus what shipped beyond the original MVP scope. Day-to-day history lives in `git log`.

## 1. Overview
A Python desktop application that runs continuously in the background, provides a graphical interface for translations, and can be invoked instantly via a global keyboard shortcut (works even when the app isn't in focus, similar to tools like PowerToys Run or Alfred).

## 2. Goals
- Translate selected/typed text without breaking workflow.
- Zero-friction access: press a hotkey from anywhere on the OS.
- Lightweight footprint — sits in the system tray, not a heavy always-open window.
- Cross-platform is a stretch goal; primary target is Windows (adjust if you're on Linux/Mac).

## 3. Core User Flow
1. App launches at startup and minimizes to the system tray.
2. User selects/copies text anywhere, or just presses the hotkey.
3. Global hotkey (default `Shift+Alt+T`, rebindable) triggers a small popup window near the cursor.
4. Popup shows source text (auto-filled from clipboard, editable) + translated text, auto-translating as you type.
5. User can copy result, swap languages, clear the input, or dismiss (`Esc` or click-away) — each with a hardcoded keyboard shortcut while the popup is open: `Ctrl+C` copy, `Ctrl+S` swap, `Ctrl+D` clear.

## 4. Tech Stack

| Concern | Library used | Notes |
|---|---|---|
| GUI | `PySide6` | Also provides the system tray icon (`QSystemTrayIcon`) and clipboard access (`QGuiApplication.clipboard()`) — no separate tray/clipboard libraries needed. |
| Global hotkey listener | `pynput` | Runs on a daemon thread; `hotkey_listener.py` emits a Qt `Signal` the GUI thread picks up. |
| Translation engine | `deep-translator` (`GoogleTranslator`) | Free, no API key. |
| Packaging | `PyInstaller` (`--onefile`) + `Inno Setup` | Built straight from a CLI command (no versioned `.spec` file); Inno Setup produces a proper per-user installer alongside the portable `.exe`. |
| Config/settings | `.json` file in `%LOCALAPPDATA%\EzTranslator\` | Stores default languages and hotkey; merge-forward defaults for compatibility. |
| Logging | Rotating file handler | Console + `%LOCALAPPDATA%\EzTranslator\logs\`, no remote/DB persistence. |

## 5. Architecture

```
src/translator_app/
├── main.py              # Entry point — wires tray, popup, hotkey listener, settings
├── tray.py              # System tray icon and menu (Open, Settings, Quit)
├── hotkey_listener.py   # Global hotkey registration (pynput) + Qt event capture for rebinding
├── single_instance.py   # Prevents running more than one copy at once
├── startup.py           # Windows "start on boot" registry toggle
├── config.py            # Paths + config.json load/save
├── logger.py            # Rotating file logger
├── ui/
│   ├── popup.py         # Translation popup window
│   └── settings.py      # Settings window
├── translator/
│   ├── engine.py         # GoogleTranslator wrapper
│   ├── worker.py          # Runs translation on a background QThread
│   └── languages.py       # Curated language list
└── assets/
    └── app.ico
```

`run.py` at the repo root is the PyInstaller entry point (absolute imports, required since PyInstaller can't target a script that uses relative imports).

**Threading note:** the hotkey listener runs on a background thread and emits a Qt `Signal`; translation requests run on a `QThread` worker. Neither touches GUI widgets directly — both hand off to the main/GUI thread via signals.

## 6. Key Features (MVP)

- [x] Runs in system tray, starts on boot (optional toggle, packaged build only)
- [x] Global hotkey configurable by user
- [x] Auto-detect source language
- [x] Manual language pair selection with a quick-swap button (also `Ctrl+S`)
- [x] Reads clipboard on trigger, auto-translates
- [x] Copy-to-clipboard button on result (also `Ctrl+C`)
- [x] Settings window: hotkey rebind, default languages
  - No API key entry — not needed, `deep-translator`'s Google Translate backend is free.

## 7. Shipped beyond MVP

- Auto-translate while typing (debounced), not just on trigger
- Retranslate automatically when either language is changed
- Inline clear (`×` button / `Ctrl+D`) for the input field
- Dark-themed, rounded, draggable popup with a scrollable result field for long translations
- Left-click on the tray icon opens the popup (not just the Open menu item)
- Windows installer (Inno Setup) alongside the portable `.exe`, both attached to every release
- Bilingual README (English/Portuguese)

## 8. Nice-to-Have (still open)

- Offline mode via a local model (e.g. `argos-translate`)
- Text-to-speech playback of translated text
- Light theme toggle (currently dark-only)
- Multi-monitor aware popup positioning beyond basic screen-edge clamping

## 9. Non-Functional Requirements

- Startup time: tray icon ready in <2s.
- Memory footprint: target <150MB idle.
- Hotkey conflict handling: warn user if chosen combo is already bound elsewhere.
- Graceful handling of no internet / API rate limits (show inline error, don't crash).

## 10. Open Questions — Resolved

- **Platform**: Windows-only. No cross-platform requirement.
- **Translation engine**: Google Translate (via `deep-translator`'s `GoogleTranslator`). No DeepL/paid engine for now.
- **Privacy**: Translations are fully ephemeral — nothing is logged or stored. No history feature, no local/remote persistence of source or translated text.

## 11. Development Process

- The `/grill-me` skill must be used as part of this project's workflow.

## 12. Milestones (all shipped)

1. **Skeleton**: tray icon + quit menu working, app stays alive in background.
2. **Hotkey**: global shortcut opens a blank popup window.
3. **Translation core**: wire up `deep-translator`, hardcode language pair.
4. **UI polish**: language selectors, copy button, auto-fill from clipboard.
5. **Settings**: persist hotkey + language prefs to a config file.
6. **Packaging**: PyInstaller build + startup-on-boot option.
