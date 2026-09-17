"""Pure validation functions for all user-submitted profile fields.

No Streamlit imports anywhere in this module.
Every function either returns a clean value or raises a named custom
exception from ``exceptions.errors``.
"""

import re

from exceptions.errors import InvalidExperienceError, InvalidProfileError, UnknownRoleError
from models.career_profile import CareerProfile


def validate_name(name: str) -> str:
    """Strip and validate the user's full name.

    Args:
        name: Raw string entered by the user.

    Returns:
        The stripped, validated name.

    Raises:
        InvalidProfileError: If the name is empty, longer than 60 characters,
            or contains characters other than letters, spaces, and hyphens.
    """
    name = name.strip()
    if not name:
        raise InvalidProfileError("Name must not be empty.")
    if len(name) > 60:
        raise InvalidProfileError("Name must not exceed 60 characters.")
    if not re.fullmatch(r"[A-Za-z\s\-]+", name):
        raise InvalidProfileError(
            "Name may only contain letters, spaces, and hyphens."
        )
    return name


def validate_current_role(role: str) -> str:
    """Strip and validate the user's current job role.

    Args:
        role: Raw string entered by the user.

    Returns:
        The stripped, validated role string.

    Raises:
        InvalidProfileError: If the role is empty or longer than 80 characters.
    """
    role = role.strip()
    if not role:
        raise InvalidProfileError("Current role must not be empty.")
    if len(role) > 80:
        raise InvalidProfileError("Current role must not exceed 80 characters.")
    return role


def validate_skills(raw_input: str) -> list[str]:
    """Parse a comma-separated skills string into a clean, deduplicated list.

    Each token is stripped and lowercased.  Empty tokens and duplicates
    are silently removed.

    Args:
        raw_input: Comma-separated string of skills entered by the user.

    Returns:
        A deduplicated list of lowercase skill strings.

    Raises:
        InvalidProfileError: If no valid skills remain after processing.
    """
    tokens = [token.strip().lower() for token in raw_input.split(",")]
    skills = list(dict.fromkeys(token for token in tokens if token))
    if not skills:
        raise InvalidProfileError("At least one skill must be provided.")
    return skills


def validate_education(education: str) -> str:
    """Strip and validate the user's education or qualification.

    Args:
        education: Raw string entered by the user.

    Returns:
        The stripped, validated education string.

    Raises:
        InvalidProfileError: If the field is empty or longer than 120 characters.
    """
    education = education.strip()
    if not education:
        raise InvalidProfileError("Education must not be empty.")
    if len(education) > 120:
        raise InvalidProfileError("Education must not exceed 120 characters.")
    return education


def validate_target_role(role: str, known_roles: list[str]) -> str:
    """Strip and validate the selected target role.

    Args:
        role: The role name selected or entered by the user.
        known_roles: List of valid role names loaded from job_roles.json.

    Returns:
        The stripped, validated role name.

    Raises:
        UnknownRoleError: If the stripped role is not present in *known_roles*.
    """
    role = role.strip()
    if role not in known_roles:
        raise UnknownRoleError(
            f"'{role}' is not a recognised role. Choose from the available options."
        )
    return role


def validate_years_of_experience(years: int) -> int:
    """Validate that years of experience is within the accepted range [0, 50].

    Args:
        years: Integer value from the UI number input.

    Returns:
        The validated integer.

    Raises:
        InvalidExperienceError: If years < 0 or years > 50.
    """
    if years < 0:
        raise InvalidExperienceError("Years of experience cannot be negative.")
    if years > 50:
        raise InvalidExperienceError("Years of experience cannot exceed 50.")
    return int(years)


def build_career_profile(raw_inputs: dict, known_roles: list[str]) -> CareerProfile:
    """Validate all raw inputs and construct a :class:`~models.CareerProfile`.

    Calls each individual validator in order.  Raises on the first
    validation failure so that the UI can display a precise error message.

    Args:
        raw_inputs: Dictionary with keys ``name``, ``current_role``,
            ``skills``, ``education``, ``target_role``,
            ``years_of_experience``.
        known_roles: Sorted list of valid role names.

    Returns:
        A fully validated :class:`~models.CareerProfile` instance.

    Raises:
        InvalidProfileError: On any profile field validation failure.
        UnknownRoleError: If ``target_role`` is not in *known_roles*.
        InvalidExperienceError: If ``years_of_experience`` is out of range.
    """
    name = validate_name(raw_inputs["name"])
    current_role = validate_current_role(raw_inputs["current_role"])
    skills = validate_skills(raw_inputs["skills"])
    education = validate_education(raw_inputs["education"])
    target_role = validate_target_role(raw_inputs["target_role"], known_roles)
    years_of_experience = validate_years_of_experience(raw_inputs["years_of_experience"])

    return CareerProfile(
        name=name,
        current_role=current_role,
        skills=skills,
        education=education,
        target_role=target_role,
        years_of_experience=years_of_experience,
    )


# Backwards-compatible alias so existing code using build_user_profile still works.
build_user_profile = build_career_profile
