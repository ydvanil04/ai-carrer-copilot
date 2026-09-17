"""CareerProfile — the user's career information."""

from dataclasses import dataclass, field


@dataclass
class CareerProfile:
    """Stores all career-related information entered by the user.

    This is the primary data object passed through the application.
    It is built by the validator layer and consumed by SkillMatcher
    and CareerAdvisor.

    Attributes:
        name: The user's full name.
        current_role: The user's current job title or career level.
        skills: Normalised (lowercased, deduplicated) list of skills.
        education: The user's highest qualification.
        target_role: The job role the user wants to move into.
        years_of_experience: Total professional years (0 = entry-level).
    """

    name: str
    current_role: str
    skills: list[str] = field(default_factory=list)
    education: str = ""
    target_role: str = ""
    years_of_experience: int = 0

    def to_dict(self) -> dict:
        """Serialise to a plain dictionary for JSON persistence."""
        return {
            "name": self.name,
            "current_role": self.current_role,
            "skills": self.skills,
            "education": self.education,
            "target_role": self.target_role,
            "years_of_experience": self.years_of_experience,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CareerProfile":
        """Deserialise from a plain dictionary loaded from JSON.

        Args:
            data: Dictionary with the same keys as :meth:`to_dict`.

        Returns:
            A :class:`CareerProfile` instance.
        """
        return cls(
            name=data.get("name", ""),
            current_role=data.get("current_role", ""),
            skills=data.get("skills", []),
            education=data.get("education", ""),
            target_role=data.get("target_role", ""),
            years_of_experience=int(data.get("years_of_experience", 0)),
        )
