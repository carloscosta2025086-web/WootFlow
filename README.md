# WootFlow

> Advanced RGB lighting control for Wooting keyboards — dynamic effects, screen ambience, audio reactivity, and per-key customization.

[![CI](https://github.com/carloscosta2025086-web/WootFlow/actions/workflows/ci.yml/badge.svg)](https://github.com/carloscosta2025086-web/WootFlow/actions/workflows/ci.yml)
[![Latest Release](https://img.shields.io/github/v/release/carloscosta2025086-web/WootFlow)](https://github.com/carloscosta2025086-web/WootFlow/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Changelog](https://img.shields.io/badge/Changelog-keep%20a%20changelog-blue)](CHANGELOG.md)

![WootFlow Screenshot](assets/screenshot.png)

## Features

- **Dynamic RGB effects** — Wave, ripple, reactive typing, fire, aurora, matrix rain, starfield, equalizer, and more
- **Screen Ambience** — Mirrors your display colors live onto your keyboard (SignalRGB-style per-key sampling)
- **Audio Reactive** — Keyboard reacts to music and system audio in real time
- **Per-key customization** — Full per-key color and effect control via a clean web UI
- **Profile system** — Save and switch between multiple lighting profiles instantly
- **System tray** — Runs quietly in the background; accessible from the tray icon
- **No cloud required** — Fully local, no account needed

## Download

**[⬇ Download the latest release from GitHub Releases](https://github.com/carloscosta2025086-web/WootFlow/releases/latest)**

Each release ships two files — pick the one that suits you:

| File | Description |
|------|-------------|
| `WootFlow-Setup-vX.Y.Z-win.exe` | **Recommended** — standard Windows installer |
| `WootFlow-vX.Y.Z-win-portable.zip` | No installation — extract anywhere and run `WootFlow.exe` |

No Python or Node.js required for end users. See [CHANGELOG.md](CHANGELOG.md) for what's new in each version.

## Requirements

- **OS:** Windows 10 / 11 (64-bit)
- **Keyboard:** Wooting 60HE (other Wooting models may work)
- **Wooting drivers** must be installed ([download here](https://wooting.io/wooting-double-speed-technology))

> For audio reactivity, a working audio output device is required.

## Usage

After installation, launch **WootFlow** from the Start Menu or desktop shortcut. The app opens in your system tray — right-click the tray icon to access settings and profiles. The control panel opens automatically in your browser at `http://localhost`.

### Effect switching

Open the control panel and select any effect from the sidebar. Changes apply instantly.

### Screen Ambience

Enable the **Screen Ambience** profile from the sidebar to mirror your screen colors onto your keyboard in real time.

### Audio Reactive

Enable the **Sound Reactive** profile to have your keyboard pulse to music or system audio.

## Building from Source

Requires **Python 3.13+** and **Node.js 22+**.

```powershell
# Clone and set up
git clone https://github.com/carloscosta2025086-web/WootFlow.git
cd WootFlow

# Install all dependencies and launch in dev mode
powershell -ExecutionPolicy Bypass -File .\run_app.ps1
```

To build the installer yourself:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_installer_prereqs.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\build_installer.ps1 -Version X.Y.Z
```

See [docs/dev.md](docs/dev.md) for the full developer guide.

## Project Structure

```
WootFlow/
├── core/          # Effects engine, screen ambience, profile logic
├── services/      # Profile loader and service layer
├── utils/         # Wooting RGB SDK wrapper, helpers
├── ui/            # React/TypeScript frontend (Vite + Tailwind)
├── profiles/      # Default lighting profiles (JSON)
├── assets/        # Icons and static assets
├── scripts/       # Build and installer automation
├── docs/          # Developer and release documentation
└── tests/         # Automated tests
```

## License

[MIT](LICENSE) © 2026 WootFlow contributors
