"""persistence — save and load a CareerProfile as JSON.

Uses Python's built-in ``json`` module and ``pathlib``.
No external libraries required.

The default save location is ``data/saved_profile.json`` inside the
``ai_career_copilot/`` package directory.  The Streamlit UI passes the
path explicitly so it is always predictable regardless of where the
user runs the app from.
"""

import json
from pathlib import Path

from models.career_profile import CareerProfile

# Default path for the saved profile — relative to this file's parent directory.
_DEFAULT_SAVE_PATH = Path(__file__).parent / "data" / "saved_profile.json"


def save_profile(profile: CareerProfile, path: Path | None = None) -> Path:
    """Serialise *profile* to a JSON file and return the path written.

    Args:
        profile: The :class:`~models.CareerProfile` to persist.
        path: Where to write the file.  Defaults to
            ``data/saved_profile.json`` inside the package directory.

    Returns:
        The :class:`~pathlib.Path` of the file that was written.

    Raises:
        OSError: If the file cannot be written (e.g. permission denied).
    """
    save_path = path or _DEFAULT_SAVE_PATH
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with save_path.open("w", encoding="utf-8") as fh:
        json.dump(profile.to_dict(), fh, indent=2)
    return save_path


def load_profile(path: Path | None = None) -> CareerProfile | None:
    """Deserialise a :class:`~models.CareerProfile` from a JSON file.

    Args:
        path: Path to the saved profile JSON.  Defaults to the same
            location used by :func:`save_profile`.

    Returns:
        A :class:`~models.CareerProfile` instance if the file exists and
        is valid, or ``None`` if the file does not exist.

    Raises:
        ValueError: If the file exists but contains malformed JSON or
            cannot be deserialised into a CareerProfile.
    """
    load_path = path or _DEFAULT_SAVE_PATH
    if not load_path.exists():
        return None
    try:
        with load_path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        return CareerProfile.from_dict(data)
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError(
            f"Could not load career profile from '{load_path}': {exc}"
        ) from exc


def delete_profile(path: Path | None = None) -> bool:
    """Remove a saved profile file if it exists.

    Args:
        path: Path to the file to delete.  Defaults to the same
            location used by :func:`save_profile`.

    Returns:
        ``True`` if a file was deleted, ``False`` if no file existed.
    """
    delete_path = path or _DEFAULT_SAVE_PATH
    if delete_path.exists():
        delete_path.unlink()
        return True
    return False
