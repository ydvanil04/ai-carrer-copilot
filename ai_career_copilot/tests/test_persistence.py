"""Tests for engine/persistence.py."""

import json
from pathlib import Path

import pytest

from engine.persistence import delete_profile, load_profile, save_profile
from models.career_profile import CareerProfile


@pytest.fixture
def tmp_path_profile(tmp_path) -> Path:
    """Return a temporary file path for test persistence."""
    return tmp_path / "test_profile.json"


@pytest.fixture
def sample_profile() -> CareerProfile:
    return CareerProfile(
        name="Alice",
        current_role="Student",
        skills=["python", "sql"],
        education="BSc Computer Science",
        target_role="Data Scientist",
        years_of_experience=1,
    )


# ---------------------------------------------------------------------------
# save_profile
# ---------------------------------------------------------------------------

def test_save_creates_file(tmp_path_profile, sample_profile):
    save_profile(sample_profile, path=tmp_path_profile)
    assert tmp_path_profile.exists()


def test_save_writes_valid_json(tmp_path_profile, sample_profile):
    save_profile(sample_profile, path=tmp_path_profile)
    with tmp_path_profile.open() as fh:
        data = json.load(fh)
    assert data["name"] == "Alice"
    assert data["target_role"] == "Data Scientist"


def test_save_returns_path(tmp_path_profile, sample_profile):
    returned = save_profile(sample_profile, path=tmp_path_profile)
    assert returned == tmp_path_profile


# ---------------------------------------------------------------------------
# load_profile
# ---------------------------------------------------------------------------

def test_load_returns_career_profile(tmp_path_profile, sample_profile):
    save_profile(sample_profile, path=tmp_path_profile)
    loaded = load_profile(path=tmp_path_profile)
    assert isinstance(loaded, CareerProfile)
    assert loaded.name == "Alice"
    assert loaded.skills == ["python", "sql"]
    assert loaded.years_of_experience == 1


def test_load_returns_none_when_file_missing(tmp_path):
    missing = tmp_path / "no_such_file.json"
    result = load_profile(path=missing)
    assert result is None


def test_load_raises_on_corrupt_json(tmp_path_profile):
    tmp_path_profile.write_text("{this is not valid json", encoding="utf-8")
    with pytest.raises(ValueError):
        load_profile(path=tmp_path_profile)


def test_save_and_load_roundtrip(tmp_path_profile, sample_profile):
    save_profile(sample_profile, path=tmp_path_profile)
    loaded = load_profile(path=tmp_path_profile)
    assert loaded.name == sample_profile.name
    assert loaded.skills == sample_profile.skills
    assert loaded.target_role == sample_profile.target_role
    assert loaded.years_of_experience == sample_profile.years_of_experience


# ---------------------------------------------------------------------------
# delete_profile
# ---------------------------------------------------------------------------

def test_delete_existing_file(tmp_path_profile, sample_profile):
    save_profile(sample_profile, path=tmp_path_profile)
    assert tmp_path_profile.exists()
    result = delete_profile(path=tmp_path_profile)
    assert result is True
    assert not tmp_path_profile.exists()


def test_delete_nonexistent_file(tmp_path):
    missing = tmp_path / "ghost.json"
    result = delete_profile(path=missing)
    assert result is False
