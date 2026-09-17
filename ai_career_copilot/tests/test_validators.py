"""Tests for utils/validators.py — all 12 cases."""

import pytest

from exceptions.errors import InvalidExperienceError, InvalidProfileError, UnknownRoleError
from utils.validators import (
    validate_name,
    validate_skills,
    validate_target_role,
    validate_years_of_experience,
    build_career_profile,
)

KNOWN_ROLES = ["Data Scientist", "Software Engineer", "Frontend Developer"]


# ---------------------------------------------------------------------------
# validate_name
# ---------------------------------------------------------------------------

def test_valid_name():
    assert validate_name("Alice") == "Alice"


def test_name_with_spaces():
    assert validate_name("Mary Jane") == "Mary Jane"


def test_empty_name_raises():
    with pytest.raises(InvalidProfileError):
        validate_name("")


def test_name_too_long_raises():
    with pytest.raises(InvalidProfileError):
        validate_name("A" * 61)


# ---------------------------------------------------------------------------
# validate_skills
# ---------------------------------------------------------------------------

def test_valid_skills():
    assert validate_skills("Python, SQL, Git") == ["python", "sql", "git"]


def test_skills_deduplication():
    assert validate_skills("Python, python, PYTHON") == ["python"]


def test_empty_skills_raises():
    with pytest.raises(InvalidProfileError):
        validate_skills("")


# ---------------------------------------------------------------------------
# validate_years_of_experience
# ---------------------------------------------------------------------------

def test_valid_years():
    assert validate_years_of_experience(3) == 3


def test_negative_years_raises():
    with pytest.raises(InvalidExperienceError):
        validate_years_of_experience(-1)


def test_years_over_limit_raises():
    with pytest.raises(InvalidExperienceError):
        validate_years_of_experience(51)


# ---------------------------------------------------------------------------
# validate_target_role
# ---------------------------------------------------------------------------

def test_valid_target_role():
    assert validate_target_role("Data Scientist", KNOWN_ROLES) == "Data Scientist"


def test_unknown_role_raises():
    with pytest.raises(UnknownRoleError):
        validate_target_role("Wizard", KNOWN_ROLES)


# ---------------------------------------------------------------------------
# build_career_profile — integration test
# ---------------------------------------------------------------------------

def test_build_career_profile_returns_profile():
    from models.career_profile import CareerProfile

    raw = {
        "name": "Alice",
        "current_role": "Student",
        "skills": "Python, SQL",
        "education": "BSc Computer Science",
        "target_role": "Data Scientist",
        "years_of_experience": 1,
    }
    profile = build_career_profile(raw, KNOWN_ROLES)
    assert isinstance(profile, CareerProfile)
    assert profile.name == "Alice"
    assert "python" in profile.skills
    assert "sql" in profile.skills
