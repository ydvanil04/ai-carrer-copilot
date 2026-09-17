"""models package — exports all data model classes."""

from models.career_profile import CareerProfile
from models.job_role import JobRole
from models.analysis_result import AnalysisResult

# Keep the old names as aliases so existing test imports don't break
CareerAnalysisResult = AnalysisResult
UserProfile = CareerProfile

__all__ = [
    "CareerProfile",
    "JobRole",
    "AnalysisResult",
    "CareerAnalysisResult",  # backwards-compat alias
    "UserProfile",           # backwards-compat alias
]
