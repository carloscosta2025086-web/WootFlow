# Contributing to WootFlow

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

**Prerequisites:** Python 3.13+, Node.js 22+, a Wooting keyboard (or the SDK for simulation).

```powershell
git clone https://github.com/carloscosta2025086-web/WootFlow.git
cd WootFlow
powershell -ExecutionPolicy Bypass -File .\run_app.ps1
```

This installs all dependencies and launches the app in development mode. See [docs/dev.md](docs/dev.md) for a detailed guide.

## How to Contribute

### Bug Reports

Open an issue using the **Bug Report** template. Include:
- Your OS and keyboard model
- WootFlow version
- Steps to reproduce
- What you expected vs. what happened

### Feature Requests

Open an issue using the **Feature Request** template. Describe the problem it solves and any implementation ideas you have.

### Pull Requests

1. Fork the repository and create a branch from `main`.
2. Make your changes with clear, focused commits.
3. Run the test suite: `python -m pytest tests -q`
4. Run the linter: `python -m ruff check core services utils tests`
5. Open a pull request describing what you changed and why.

## Code Style

- Python: follow [Ruff](https://docs.astral.sh/ruff/) defaults (enforced by CI).
- TypeScript/React: follow the existing patterns in `ui/src/`.
- Keep changes focused — one concern per PR.

## Commit Messages

Use short, imperative messages: `Add fire effect`, `Fix tray icon on Windows 11`, `Update screen ambience zone mapping`.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
