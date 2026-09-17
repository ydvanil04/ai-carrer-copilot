"""CareerAdvisor — generates recommendations and the career summary."""

from models.career_profile import CareerProfile
from models.job_role import JobRole
from models.analysis_result import AnalysisResult


class CareerAdvisor:
    """Enriches a partial :class:`~models.AnalysisResult` (produced by
    :class:`~engine.SkillMatcher`) with personalised improvement suggestions,
    recommended learning areas, and a narrative career summary.

    All logic is purely rule-based — no external API or ML model is used.

    Example::

        advisor = CareerAdvisor()
        advisor.advise(profile, role, result)
        # result.suggestions, result.learning_areas, result.summary are now set
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def advise(
        self,
        profile: CareerProfile,
        role: JobRole,
        result: AnalysisResult,
    ) -> None:
        """Populate ``suggestions``, ``learning_areas``, and ``summary`` on
        *result* in-place.

        Args:
            profile: The user's validated career profile.
            role: The target job role.
            result: A partial AnalysisResult from SkillMatcher — mutated here.
        """
        result.suggestions = self._build_suggestions(
            result.missing_skills,
            profile.years_of_experience,
        )
        result.learning_areas = role.learning_areas[:]
        result.summary = self._build_summary(profile, result)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_suggestions(
        self,
        missing_skills: list[str],
        years_exp: int,
    ) -> list[str]:
        """Build a list of actionable suggestion strings.

        Args:
            missing_skills: Skills the user is still missing.
            years_exp: The user's years of professional experience.

        Returns:
            A list of suggestion strings, with an experience-level opener
            prepended when relevant.
        """
        if not missing_skills:
            return [
                "You already have all the required skills for this role."
                " Consider applying now!"
            ]

        suggestions = [
            f"Learn {skill} - it is required for this role."
            for skill in missing_skills
        ]

        if years_exp == 0:
            suggestions.insert(
                0,
                "As an entry-level candidate, start with the fundamentals.",
            )
        elif years_exp >= 5:
            suggestions.insert(
                0,
                "As an experienced professional, add these skills to advance"
                " your career.",
            )

        return suggestions

    def _build_summary(
        self,
        profile: CareerProfile,
        result: AnalysisResult,
    ) -> str:
        """Return a single narrative paragraph summarising the analysis.

        Args:
            profile: The user's career profile.
            result: The partially or fully populated AnalysisResult.

        Returns:
            A human-readable summary string.
        """
        total = len(result.matched_skills) + len(result.missing_skills)
        improvement_count = len(result.missing_skills)

        return (
            f"{profile.name} is targeting the {profile.target_role} role. "
            f"Based on your current skills, your career readiness score is "
            f"{result.readiness_score}% ({result.readiness_label}). "
            f"You have matched {len(result.matched_skills)} of "
            f"{total} required skills. "
            f"{improvement_count} area(s) have been identified for improvement. "
            f"Focus on the recommended learning areas to strengthen your profile."
        )
