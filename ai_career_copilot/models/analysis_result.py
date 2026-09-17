"""AnalysisResult — the output produced by SkillMatcher and CareerAdvisor."""

from dataclasses import dataclass, field


@dataclass
class AnalysisResult:
    """Structured result returned after analysing a CareerProfile.

    Produced by :class:`~engine.skill_matcher.SkillMatcher` (for skill data)
    and enriched by :class:`~engine.career_advisor.CareerAdvisor` (for
    suggestions and summary).

    Attributes:
        matched_skills: Required skills the user already has.
        missing_skills: Required skills the user is still missing.
        readiness_score: Percentage of required skills matched (0.0–100.0).
        readiness_label: Human-readable level — Beginner, Developing, or Ready.
        suggestions: Actionable improvement advice strings.
        learning_areas: Recommended study topics from the role data.
        summary: A single narrative paragraph summarising the analysis.
    """

    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    readiness_score: float = 0.0
    readiness_label: str = ""
    suggestions: list[str] = field(default_factory=list)
    learning_areas: list[str] = field(default_factory=list)
    summary: str = ""
