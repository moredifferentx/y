# Architecture
## Cloud AI Strategy

This project intentionally supports a limited set of
cloud AI providers:

- OpenAI
- Google Gemini

A generic multi-provider abstraction was explored but
explicitly abandoned to reduce complexity, improve
debuggability, and ensure long-term stability.

Deprecated cloud modules are retained in the repository
for historical reference and backward compatibility,
but are not used by the system.

All active cloud inference flows through:
- OpenAIEngine
- GeminiEngine

## Utils Module

The `backend/app/utils` directory contains **reserved infrastructure utilities**.

These modules are intentionally present but not yet wired:

- `async_tools.py` – async helpers & retry logic
- `hot_reload.py` – centralized hot-reload coordination
- `language.py` – language & i18n foundation

They exist to:
- Prevent future architectural drift
- Avoid scattering helpers across the codebase
- Enable clean expansion without breaking changes

These files MUST NOT be deleted.
