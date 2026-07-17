# Background Desktop Translator — Project Spec

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
3. Global hotkey (e.g. `Ctrl+Alt+T`) triggers a small popup window near the cursor or a fixed position.
4. Popup shows source text (auto-filled from clipboard, editable) + translated text.
5. User can copy result, switch languages, or dismiss (`Esc` or click-away).

## 4. Tech Stack

| Concern | Recommended library | Notes |
|---|---|---|
| GUI | `PyQt6` / `PySide6` | More native look, async-friendly. `Tkinter` works too if you want zero extra deps. |
| System tray icon | `pystray` | Lightweight, cross-platform tray icon + menu. |
| Global hotkey listener | `pynput` or `keyboard` | `keyboard` is simpler but needs admin rights on Windows in some setups; `pynput` is a safer default. |
| Clipboard access | `pyperclip` | Read/write clipboard content. |
| Translation engine | `deep-translator` (wraps Google/DeepL/MyMemory) or official DeepL API | `deep-translator` is free and quick to start; DeepL API gives better quality with an API key. |
| Packaging | `PyInstaller` | Bundle into a single `.exe`/binary for distribution. |
| Config/settings | `.json` or `.env` file | Store default languages, hotkey combo, API keys. |

## 5. Architecture

```
translator_app/
├── main.py              # Entry point, starts tray icon + hotkey listener
├── tray.py              # System tray icon, menu (Open, Settings, Quit)
├── hotkey_listener.py   # Global shortcut registration and callback
├── ui/
│   ├── popup.py         # Translation popup window
│   └── settings.py      # Settings window (languages, hotkey, API key)
├── translator/
│   └── engine.py        # Wraps the translation API, handles errors/retries
├── config.py            # Load/save user settings
└── assets/
    └── icon.png
```

**Threading note:** the hotkey listener and GUI event loop both need to run concurrently. Typical approach: run the GUI main loop on the main thread, and the hotkey listener on a background thread that emits a signal/event the GUI thread picks up (avoid touching GUI widgets directly from the listener thread).

## 6. Key Features (MVP)
- [ ] Runs in system tray, starts on boot (optional toggle)
- [ ] Global hotkey configurable by user
- [ ] Auto-detect source language
- [ ] Manual language pair selection with a quick-swap button
- [ ] Reads clipboard on trigger, auto-translates
- [ ] Copy-to-clipboard button on result
- [ ] Settings window: hotkey rebind, default languages, API key entry

## 7. Nice-to-Have (post-MVP)
- Offline mode via a local model (e.g. `argos-translate`)
- Text-to-speech playback of translated text
- Dark/light theme toggle
- Multi-monitor aware popup positioning

## 8. Non-Functional Requirements
- Startup time: tray icon ready in <2s.
- Memory footprint: target <150MB idle.
- Hotkey conflict handling: warn user if chosen combo is already bound elsewhere.
- Graceful handling of no internet / API rate limits (show inline error, don't crash).

## 9. Open Questions — Resolved
- **Platform**: Windows-only. No cross-platform requirement.
- **Translation engine**: Google Translate (via `deep-translator`'s `GoogleTranslator`). No DeepL/paid engine for now.
- **Privacy**: Translations are fully ephemeral — nothing is logged or stored. No history feature, no local/remote persistence of source or translated text.

## 10. Development Process
- The `/grill-me` skill must be used as part of this project's workflow.

## 11. Suggested Milestones
1. **Skeleton**: tray icon + quit menu working, app stays alive in background.
2. **Hotkey**: global shortcut opens a blank popup window.
3. **Translation core**: wire up `deep-translator`, hardcode language pair.
4. **UI polish**: language selectors, copy button, auto-fill from clipboard.
5. **Settings**: persist hotkey + language prefs to a config file.
6. **Packaging**: PyInstaller build + startup-on-boot option.
