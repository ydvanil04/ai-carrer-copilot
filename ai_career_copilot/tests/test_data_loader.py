"""Tests for engine/data_loader.py."""

import pytest

from engine.data_loader import get_role, get_role_names, load_job_roles
from models.job_role import JobRole

EXPECTED_ROLES = {
    "Software Engineer",
    "Data Scientist",
    "Data Analyst",
    "Frontend Developer",
    "Backend Developer",
    "UX Designer",
    "DevOps Engineer",
    "Machine Learning Engineer",
}

REQUIRED_KEYS = {"required_skills", "learning_areas", "recommended_experience_years"}


def test_load_returns_dict():
    result = load_job_roles()
    assert isinstance(result, dict)


def test_load_returns_job_role_objects():
    roles = load_job_roles()
    for role in roles.values():
        assert isinstance(role, JobRole)


def test_load_contains_expected_roles():
    result = load_job_roles()
    assert EXPECTED_ROLES.issubset(result.keys())


def test_get_role_names_sorted():
    names = get_role_names()
    assert names == sorted(names)


def test_role_has_required_skills():
    roles = load_job_roles()
    for name, role in roles.items():
        assert role.required_skills, f"Role '{name}' has no required_skills"


def test_role_has_learning_areas():
    roles = load_job_roles()
    for name, role in roles.items():
        assert role.learning_areas, f"Role '{name}' has no learning_areas"


def test_role_recommended_experience_is_non_negative():
    roles = load_job_roles()
    for name, role in roles.items():
        assert role.recommended_experience_years >= 0, (
            f"Role '{name}' has negative recommended_experience_years"
        )


def test_get_role_returns_correct_role():
    role = get_role("Data Scientist")
    assert isinstance(role, JobRole)
    assert role.name == "Data Scientist"
    assert "Python" in role.required_skills


def test_get_role_missing_raises_key_error():
    with pytest.raises(KeyError):
        get_role("Wizard")
