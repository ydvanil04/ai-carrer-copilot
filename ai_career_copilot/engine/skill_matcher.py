"""SkillMatcher — compares a user's skills with a JobRole's requirements."""

from models.career_profile import CareerProfile
from models.job_role import JobRole
from models.analysis_result import AnalysisResult


class SkillMatcher:
    """Compares the skills in a :class:`~models.CareerProfile` against the
    requirements of a :class:`~models.JobRole` and produces the skill-gap
    portion of an :class:`~models.AnalysisResult`.

    The comparison is always case-insensitive so that "Python", "python",
    and "PYTHON" are all treated as the same skill.

    Example::

        role = JobRole(name="Data Scientist", required_skills=["Python", "SQL"])
        profile = CareerProfile(name="Alice", current_role="Student",
                                skills=["python"], target_role="Data Scientist")
        matcher = SkillMatcher()
        result = matcher.match(profile, role)
        # result.matched_skills == ["Python"]
        # result.missing_skills == ["SQL"]
        # result.readiness_score == 50.0
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def match(self, profile: CareerProfile, role: JobRole) -> AnalysisResult:
        """Run skill matching and return a partially populated AnalysisResult.

        The ``suggestions``, ``learning_areas``, and ``summary`` fields are
        left at their defaults — they are filled in by :class:`CareerAdvisor`.

        Args:
            profile: The validated career profile submitted by the user.
            role: The target job role loaded from the data file.

        Returns:
            An :class:`AnalysisResult` with ``matched_skills``,
            ``missing_skills``, ``readiness_score``, and ``readiness_label``
            populated.
        """
        matched, missing = self._split_skills(profile.skills, role.required_skills)
        score = self._calculate_score(matched, role.required_skills)
        label = self._readiness_label(score)

        return AnalysisResult(
            matched_skills=matched,
            missing_skills=missing,
            readiness_score=score,
            readiness_label=label,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _split_skills(
        self,
        user_skills: list[str],
        required_skills: list[str],
    ) -> tuple[list[str], list[str]]:
        """Return (matched, missing) preserving the original casing from
        ``required_skills`` while comparing case-insensitively.

        Args:
            user_skills: Normalised (lowercased) skills from the profile.
            required_skills: Title-cased skills from the role data.

        Returns:
            A tuple of (matched_list, missing_list).
        """
        user_set = {s.strip().lower() for s in user_skills}

        matched: list[str] = []
        missing: list[str] = []

        for skill in required_skills:
            if skill.strip().lower() in user_set:
                matched.append(skill)
            else:
                missing.append(skill)

        return matched, missing

    def _calculate_score(
        self,
        matched: list[str],
        required: list[str],
    ) -> float:
        """Return the percentage of required skills that are matched.

        Args:
            matched: Skills from required_skills that the user has.
            required: The full list of required skills for the role.

        Returns:
            A float in the range 0.0–100.0 rounded to one decimal place.
            Returns 0.0 when the required list is empty.
        """
        if not required:
            return 0.0
        return round((len(matched) / len(required)) * 100, 1)

    def _readiness_label(self, score: float) -> str:
        """Map a numeric score to a readiness label.

        Args:
            score: Career readiness percentage (0.0–100.0).

        Returns:
            ``"Beginner"`` for score < 40,
            ``"Developing"`` for 40 ≤ score < 70,
            ``"Ready"`` for score ≥ 70.
        """
        if score < 40:
            return "Beginner"
        if score < 70:
            return "Developing"
        return "Ready"
