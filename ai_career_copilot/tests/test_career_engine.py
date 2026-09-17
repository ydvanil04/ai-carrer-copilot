"""Tests for the full engine layer — CareerEngine, SkillMatcher, CareerAdvisor."""

import pytest

from engine.career_engine import CareerEngine
from engine.skill_matcher import SkillMatcher
from engine.career_advisor import CareerAdvisor
from exceptions.errors import UnknownRoleError
from models.career_profile import CareerProfile
from models.job_role import JobRole
from models.analysis_result import AnalysisResult

# ---------------------------------------------------------------------------
# Shared test fixtures and helpers
# ---------------------------------------------------------------------------

TEST_ROLE = JobRole(
    name="Test Role",
    description="A role used only in tests.",
    required_skills=["Python", "SQL", "Git", "Testing", "REST APIs"],
    recommended_experience_years=1,
    learning_areas=["Learn Python", "Practice SQL"],
)

TEST_ROLES_DICT = {TEST_ROLE.name: TEST_ROLE}


def _make_profile(
    skills: list[str],
    years: int = 2,
    name: str = "Alice",
    target_role: str = "Test Role",
) -> CareerProfile:
    return CareerProfile(
        name=name,
        current_role="Developer",
        skills=skills,
        education="BSc",
        target_role=target_role,
        years_of_experience=years,
    )


# ---------------------------------------------------------------------------
# SkillMatcher tests
# ---------------------------------------------------------------------------

@pytest.fixture
def matcher() -> SkillMatcher:
    return SkillMatcher()


def test_full_skill_match(matcher):
    profile = _make_profile(["python", "sql", "git", "testing", "rest apis"])
    result = matcher.match(profile, TEST_ROLE)
    assert result.readiness_score == 100.0


def test_no_skill_match(matcher):
    profile = _make_profile(["java", "scala"])
    result = matcher.match(profile, TEST_ROLE)
    assert result.readiness_score == 0.0


def test_partial_match(matcher):
    # 2 of 5 required skills → 40.0 %
    profile = _make_profile(["python", "sql"])
    result = matcher.match(profile, TEST_ROLE)
    assert result.readiness_score == 40.0


def test_missing_skills_correct(matcher):
    profile = _make_profile(["python", "sql"])
    result = matcher.match(profile, TEST_ROLE)
    assert set(result.missing_skills) == {"Git", "Testing", "REST APIs"}


def test_matched_skills_correct(matcher):
    profile = _make_profile(["python", "sql"])
    result = matcher.match(profile, TEST_ROLE)
    assert set(result.matched_skills) == {"Python", "SQL"}


def test_readiness_label_beginner(matcher):
    # 1 of 5 = 20 % → Beginner
    profile = _make_profile(["python"])
    result = matcher.match(profile, TEST_ROLE)
    assert result.readiness_label == "Beginner"


def test_readiness_label_developing(matcher):
    # 3 of 5 = 60 % → Developing
    profile = _make_profile(["python", "sql", "git"])
    result = matcher.match(profile, TEST_ROLE)
    assert result.readiness_label == "Developing"


def test_readiness_label_ready(matcher):
    # 4 of 5 = 80 % → Ready
    profile = _make_profile(["python", "sql", "git", "testing"])
    result = matcher.match(profile, TEST_ROLE)
    assert result.readiness_label == "Ready"


def test_case_insensitive_matching(matcher):
    profile = _make_profile(["PYTHON", "SQL", "GIT", "TESTING", "REST APIS"])
    result = matcher.match(profile, TEST_ROLE)
    assert result.readiness_score == 100.0


def test_duplicate_user_skills_handled(matcher):
    # Duplicated "python" must not inflate the matched count
    profile = _make_profile(["python", "python"])
    result = matcher.match(profile, TEST_ROLE)
    assert result.readiness_score == 20.0
    assert len(result.matched_skills) == 1


# ---------------------------------------------------------------------------
# CareerAdvisor tests
# ---------------------------------------------------------------------------

@pytest.fixture
def advisor() -> CareerAdvisor:
    return CareerAdvisor()


def test_zero_experience_suggestions(advisor):
    profile = _make_profile(["java"], years=0)
    partial = AnalysisResult(missing_skills=["Python", "SQL", "Git", "Testing", "REST APIs"])
    advisor.advise(profile, TEST_ROLE, partial)
    entry_level = [s for s in partial.suggestions if "entry-level" in s.lower()]
    assert entry_level, "Expected an entry-level phrase in suggestions"


def test_experienced_suggestions(advisor):
    profile = _make_profile(["java"], years=6)
    partial = AnalysisResult(missing_skills=["Git"])
    advisor.advise(profile, TEST_ROLE, partial)
    experienced = [s for s in partial.suggestions if "experienced" in s.lower()]
    assert experienced, "Expected an experienced professional phrase in suggestions"


def test_no_missing_skills_positive_message(advisor):
    profile = _make_profile(["python", "sql", "git", "testing", "rest apis"])
    partial = AnalysisResult(
        matched_skills=["Python", "SQL", "Git", "Testing", "REST APIs"],
        missing_skills=[],
    )
    advisor.advise(profile, TEST_ROLE, partial)
    assert any("already have all the required skills" in s for s in partial.suggestions)


def test_learning_areas_populated(advisor):
    profile = _make_profile(["python"])
    partial = AnalysisResult(missing_skills=["SQL"])
    advisor.advise(profile, TEST_ROLE, partial)
    assert partial.learning_areas == TEST_ROLE.learning_areas


def test_summary_contains_name(advisor):
    profile = _make_profile(["python"], name="Alice")
    partial = AnalysisResult(
        matched_skills=["Python"],
        missing_skills=["SQL", "Git", "Testing", "REST APIs"],
        readiness_score=20.0,
        readiness_label="Beginner",
    )
    advisor.advise(profile, TEST_ROLE, partial)
    assert "Alice" in partial.summary


# ---------------------------------------------------------------------------
# CareerEngine integration tests (uses real job_roles.json via data loader)
# ---------------------------------------------------------------------------

@pytest.fixture
def engine() -> CareerEngine:
    return CareerEngine()


def test_engine_analyse_returns_result(engine):
    profile = _make_profile(
        ["python", "sql"],
        target_role="Data Scientist",
    )
    result = engine.analyse(profile)
    assert isinstance(result, AnalysisResult)
    assert 0.0 <= result.readiness_score <= 100.0


def test_engine_unknown_role_raises(engine):
    profile = _make_profile(["python"], target_role="Nonexistent Role")
    with pytest.raises(UnknownRoleError):
        engine.analyse(profile)


def test_engine_full_pipeline_score(engine):
    """User with ALL Data Scientist skills should score 100 %."""
    from engine.data_loader import get_role
    role = get_role("Data Scientist")
    # Feed the exact required skills (lowercased) so all match
    user_skills = [s.lower() for s in role.required_skills]
    profile = _make_profile(user_skills, target_role="Data Scientist")
    result = engine.analyse(profile)
    assert result.readiness_score == 100.0
    assert result.missing_skills == []
