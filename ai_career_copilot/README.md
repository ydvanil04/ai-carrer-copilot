# AI Career Copilot

A beginner-friendly, rule-based career guidance web application built with
**Python**, **OOP**, and **Streamlit**.

No machine-learning model or external API is required.  
All "AI" logic is transparent rule-based matching using Python sets.

---

## Features

- Enter your career profile (name, role, skills, education, experience)
- Select a target job role from 8 predefined options
- See your **career readiness score** (0–100 %)
- View **matched skills** and **missing skills**
- Receive **personalised improvement suggestions**
- See **recommended learning areas**
- Read a **career summary** paragraph
- Profile is **saved automatically** as JSON and reloaded on your next visit

---

## Prerequisites

- Python **3.10** or higher

---

## Installation

```bash
# 1. Clone the repository (or download the project folder)
git clone <your-repo-url>

# 2. Move into the project folder
cd ai_career_copilot

# 3. Install the two required packages
pip install -r requirements.txt
```

---

## Running the Application

```bash
# Run from inside the ai_career_copilot/ directory
cd ai_career_copilot
streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`.

---

## Running the Tests

```bash
# Run from inside the ai_career_copilot/ directory
cd ai_career_copilot
pytest tests/ -v
```

Expected output: **49 tests passed**.

---

## Project Structure

```
ai_career_copilot/
│
├── app.py                        ← Streamlit UI (no business logic here)
├── requirements.txt              ← Only two dependencies: streamlit + pytest
├── README.md
│
├── models/                       ← Data classes — pure Python, no framework
│   ├── career_profile.py         ← CareerProfile dataclass (user input)
│   ├── job_role.py               ← JobRole dataclass (role requirements)
│   └── analysis_result.py        ← AnalysisResult dataclass (engine output)
│
├── data/
│   └── job_roles.json            ← 8 predefined roles (edit to add more)
│
├── engine/                       ← Business logic layer
│   ├── skill_matcher.py          ← SkillMatcher class
│   ├── career_advisor.py         ← CareerAdvisor class
│   ├── career_engine.py          ← CareerEngine — orchestrates the above two
│   ├── data_loader.py            ← Loads job_roles.json into JobRole objects
│   └── persistence.py            ← save_profile / load_profile / delete_profile
│
├── utils/
│   └── validators.py             ← Pure input validation functions
│
├── exceptions/
│   └── errors.py                 ← InvalidProfileError, UnknownRoleError,
│                                    InvalidExperienceError
│
└── tests/
    ├── conftest.py               ← sys.path fix so pytest finds packages
    ├── test_career_engine.py     ← 18 engine tests
    ├── test_data_loader.py       ← 9 data loader tests
    ├── test_persistence.py       ← 9 persistence tests
    └── test_validators.py        ← 13 validator tests
```

---

## Adding a New Job Role

Open `data/job_roles.json` and add a new entry.  
No Python code changes are needed.

```json
"Cloud Architect": {
    "description": "Designs scalable cloud infrastructure solutions.",
    "required_skills": ["AWS", "Azure", "Terraform", "Networking", "Docker"],
    "recommended_experience_years": 4,
    "learning_areas": [
        "Complete the AWS Solutions Architect certification",
        "Practice Terraform Infrastructure as Code",
        "Study cloud security fundamentals"
    ]
}
```

---

## How Skill Matching Works

1. The user's skills are **lowercased and deduplicated** by the validator.
2. The required skills for the target role are loaded from `job_roles.json`.
3. Both lists are converted to **Python sets** and compared:
   - `matched = user_skills_set ∩ required_skills_set`
   - `missing  = required_skills_set − user_skills_set`
4. **Readiness score** = `(len(matched) / len(required)) × 100`, rounded to 1 decimal.
5. Labels: **Beginner** < 40 % · **Developing** 40–69 % · **Ready** ≥ 70 %
6. **Suggestions** are generated for each missing skill, with an
   experience-level prefix for entry-level (0 years) and senior (≥ 5 years) users.

---

## Dependencies

```
streamlit>=1.32.0
pytest>=8.0.0
```

All other tools used — `json`, `pathlib`, `dataclasses`, `re` — are part of
the Python standard library.
