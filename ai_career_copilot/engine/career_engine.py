"""CareerEngine — orchestrates SkillMatcher and CareerAdvisor.

This is the single public entry point for the business logic layer.
The Streamlit UI creates one instance and calls ``analyse()``.
"""

from engine.career_advisor import CareerAdvisor
from engine.data_loader import get_role
from engine.skill_matcher import SkillMatcher
from exceptions.errors import UnknownRoleError
from models.analysis_result import AnalysisResult
from models.career_profile import CareerProfile


class CareerEngine:
    """Coordinates :class:`~engine.SkillMatcher` and
    :class:`~engine.CareerAdvisor` to produce a complete
    :class:`~models.AnalysisResult` for a given :class:`~models.CareerProfile`.

    The engine is stateless beyond holding references to the two
    collaborators, making it easy to test each collaborator independently.

    Example::

        engine = CareerEngine()
        result = engine.analyse(profile)
    """

    def __init__(self) -> None:
        self._matcher = SkillMatcher()
        self._advisor = CareerAdvisor()

    def analyse(self, profile: CareerProfile) -> AnalysisResult:
        """Run the full career analysis pipeline.

        1. Look up the :class:`~models.JobRole` for ``profile.target_role``.
        2. Use :class:`SkillMatcher` to compute matched/missing skills.
        3. Use :class:`CareerAdvisor` to generate suggestions and a summary.

        Args:
            profile: The validated career profile submitted by the user.

        Returns:
            A fully populated :class:`~models.AnalysisResult`.

        Raises:
            UnknownRoleError: If ``profile.target_role`` is not in the data.
        """
        try:
            role = get_role(profile.target_role)
        except KeyError:
            raise UnknownRoleError(
                f"Role '{profile.target_role}' was not found in the job roles data."
            )

        result = self._matcher.match(profile, role)
        self._advisor.advise(profile, role, result)
        return result
