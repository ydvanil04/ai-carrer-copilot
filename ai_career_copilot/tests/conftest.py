"""pytest configuration — adds ai_career_copilot/ to sys.path so all test
files can use the same package-relative imports as the application code
(e.g. ``from engine.career_engine import CareerEngine``).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
