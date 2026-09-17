"""Data model for a user's career profile."""

from dataclasses import dataclass, field


@dataclass
class UserProfile:
    """Represents the career profile submitted by the user.

    Acts as the typed data contract passed from the UI and validator
    into the career engine.
    """

    name: str
    current_role: str
    skills: list[str] = field(default_factory=list)
    education: str = ""
    target_role: str = ""
    years_of_experience: int = 0
