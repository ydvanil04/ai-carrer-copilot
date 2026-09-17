"""Data loader — reads job_roles.json and vends JobRole objects.

The JSON file is read once per interpreter session and cached so that
repeated calls pay no I/O cost.
"""

import json
from pathlib import Path

from models.job_role import JobRole

# Module-level cache populated on the first call to load_job_roles().
_raw_cache: dict | None = None
_roles_cache: dict[str, JobRole] | None = None

# Absolute path resolved relative to this file so the app works
# regardless of the working directory it is launched from.
_DATA_FILE = Path(__file__).parent.parent / "data" / "job_roles.json"


def _load_raw() -> dict:
    """Return the raw parsed JSON dictionary, loading from disk if needed."""
    global _raw_cache
    if _raw_cache is None:
        with _DATA_FILE.open(encoding="utf-8") as fh:
            _raw_cache = json.load(fh)
    return _raw_cache


def load_job_roles() -> dict[str, JobRole]:
    """Return a mapping of role name → :class:`~models.JobRole` instance.

    The JSON file is read only once; subsequent calls return the cached
    dictionary.

    Returns:
        dict mapping each role name string to a :class:`~models.JobRole`.

    Raises:
        FileNotFoundError: If ``data/job_roles.json`` cannot be found.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    global _roles_cache
    if _roles_cache is None:
        raw = _load_raw()
        _roles_cache = {
            name: JobRole.from_dict(name, data)
            for name, data in raw.items()
        }
    return _roles_cache


def get_role_names() -> list[str]:
    """Return an alphabetically sorted list of all available role names.

    Returns:
        Sorted list of role name strings.
    """
    return sorted(load_job_roles().keys())


def get_role(name: str) -> JobRole:
    """Return the :class:`~models.JobRole` for a given role name.

    Args:
        name: The exact role name as it appears in job_roles.json.

    Returns:
        The matching :class:`~models.JobRole` instance.

    Raises:
        KeyError: If *name* is not found in the loaded roles.
    """
    return load_job_roles()[name]
