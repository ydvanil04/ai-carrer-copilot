"""Data model for the output of a career analysis."""

from dataclasses import dataclass, field


@dataclass
class CareerAnalysisResult:
    """Represents the structured result produced by the career engine.

    Acts as the typed data contract returned from the engine and
    consumed by the Streamlit UI.
    """

    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    readiness_score: float = 0.0
    readiness_label: str = ""
    suggestions: list[str] = field(default_factory=list)
    learning_areas: list[str] = field(default_factory=list)
    summary: str = ""
