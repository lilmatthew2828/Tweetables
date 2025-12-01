# app_state.py
# Application state management
# (shared, mutable state)
class _State:
    CURRENT_USER: str | None = None

state = _State()