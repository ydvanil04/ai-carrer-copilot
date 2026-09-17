"""JobRole — represents a target career and its required skills."""

from dataclasses import dataclass, field


@dataclass
class JobRole:
    """Represents a predefined career role and the skills it requires.

    Instances are constructed by the data loader from job_roles.json.

    Attributes:
        name: The display name of the role (e.g. "Data Scientist").
        description: A one-sentence summary of what the role does.
        required_skills: List of skills required to be considered for the role.
        recommended_experience_years: Minimum suggested years of experience.
        learning_areas: Recommended topics or courses to fill skill gaps.
    """

    name: str
    description: str = ""
    required_skills: list[str] = field(default_factory=list)
    recommended_experience_years: int = 0
    learning_areas: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "JobRole":
        """Construct a JobRole from a name and its dictionary entry.

        Args:
            name: The top-level key from job_roles.json.
            data: The value dict containing description, required_skills, etc.

        Returns:
            A :class:`JobRole` instance.
        """
        return cls(
            name=name,
            description=data.get("description", ""),
            required_skills=data.get("required_skills", []),
            recommended_experience_years=data.get("recommended_experience_years", 0),
            learning_areas=data.get("learning_areas", []),
        )
