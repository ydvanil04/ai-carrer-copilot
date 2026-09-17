# AI Career Copilot — Implementation Plan

## Top-Level Overview

**Goal:** Build a beginner-friendly, rule-based AI Career Copilot web application using Python, OOP, and Streamlit.

**Scope:**
- A single-page Streamlit app where a user fills in their career profile
- A Python backend that matches the user's skills against predefined role requirements
- Rule-based logic to calculate a readiness score, identify missing skills, and generate suggestions
- No external API, no ML model, no database — all data lives in memory and a single JSON file
- Full pytest test coverage for the business logic layer

**Approach:**
- Strict separation of UI (Streamlit) from business logic (Python classes)
- Small, single-responsibility classes and functions
- Predefined job-role data stored in a static JSON file
- OOP design with clearly defined data models
- Input validated before it reaches the engine
- Custom exceptions for known failure conditions

**Non-Goals (V1):**
- User authentication or persistent user accounts
- External AI or ML APIs
- Dynamic role data management
- Email or PDF export of the report

---

## Project Architecture

```
ai_career_copilot/
│
├── app.py                        ← Streamlit UI entry point
│
├── models/
│   ├── __init__.py
│   ├── user_profile.py           ← UserProfile dataclass
│   └── career_result.py          ← CareerAnalysisResult dataclass
│
├── data/
│   ├── __init__.py
│   └── job_roles.json            ← Predefined role requirements (static)
│
├── engine/
│   ├── __init__.py
│   ├── career_engine.py          ← Core matching and analysis logic
│   └── data_loader.py            ← Loads and caches job_roles.json
│
├── utils/
│   ├── __init__.py
│   └── validators.py             ← Input validation and sanitisation
│
├── exceptions/
│   ├── __init__.py
│   └── errors.py                 ← Custom exception classes
│
├── tests/
│   ├── __init__.py
│   ├── test_validators.py
│   ├── test_career_engine.py
│   └── test_data_loader.py
│
├── requirements.txt
└── README.md
```

**Why this structure?**
Each folder has a single purpose. A beginner can open any file and immediately understand what it does without reading the whole project. The `engine/` folder contains zero Streamlit imports; `app.py` contains zero business logic.

---

## Sub-Task 1 — Project Scaffold and Dependencies

**Intent:** Create the folder structure, `requirements.txt`, and empty `__init__.py` files so the project is immediately runnable with no import errors.

**Expected Outcomes:**
- All folders and placeholder files exist
- `pip install -r requirements.txt` installs without errors
- Running `streamlit run app.py` shows a blank Streamlit page without crashing

**Todo List:**
1. Create all folders listed in the architecture above
2. Create an empty `__init__.py` in every package folder (models, data, engine, utils, exceptions, tests)
3. Create `requirements.txt` with the following dependencies:
   - `streamlit>=1.32.0`
   - `pytest>=8.0.0`
4. Create a minimal `app.py` that renders a Streamlit title only
5. Create an empty `README.md`

**Why only these two dependencies?**
Streamlit and pytest cover the entire project. No pandas, no numpy, no ML library. Every other tool used (dataclasses, json, pathlib) is part of the Python standard library.

**Relevant Context:** None — this is the starting scaffold.

**Status:** [x] done

---

## Sub-Task 2 — Predefined Job Role Data (job_roles.json)

**Intent:** Define a static JSON file that acts as the "knowledge base" for the rule-based engine. This replaces any ML model.

**Expected Outcomes:**
- `job_roles.json` contains at least 8 roles
- Each role entry is complete and consistently structured
- The file can be loaded with Python's built-in `json` module without any transformation

**Todo List:**
1. Create `data/job_roles.json` with the structure defined below
2. Include exactly these 8 roles:
   - Software Engineer
   - Data Scientist
   - Data Analyst
   - Frontend Developer
   - Backend Developer
   - UX Designer
   - DevOps Engineer
   - Machine Learning Engineer
3. Each role must have all four fields: `required_skills`, `recommended_experience_years`, `learning_areas`, `description`

**JSON Structure (per role):**
```json
{
  "Software Engineer": {
    "description": "Designs, builds and maintains software systems.",
    "required_skills": ["Python", "Git", "OOP", "Data Structures", "Algorithms", "SQL", "REST APIs", "Testing"],
    "recommended_experience_years": 2,
    "learning_areas": [
      "Complete a Python OOP course",
      "Practice LeetCode data structures",
      "Build a REST API project",
      "Learn Git branching and pull requests"
    ]
  }
}
```

**Why a JSON file and not a Python dict?**
A JSON file can be edited without touching any Python code, making it safe for a beginner to update or extend the data. It also reflects real-world patterns where configuration and data are kept separate from logic.

**Relevant Context:** None — pure data definition step.

**Status:** [x] done

---

## Sub-Task 3 — Custom Exceptions

**Intent:** Define all known failure conditions as named exceptions so that error messages are clear and catching is precise.

**Expected Outcomes:**
- `exceptions/errors.py` contains three custom exception classes
- Each exception has a clear docstring

**Todo List:**
1. Create `exceptions/errors.py`
2. Define `InvalidProfileError(Exception)` — raised when a required profile field is missing or blank
3. Define `UnknownRoleError(Exception)` — raised when the selected target role is not found in `job_roles.json`
4. Define `InvalidExperienceError(Exception)` — raised when years of experience is negative or non-numeric

**Why custom exceptions rather than generic `ValueError`?**
Named exceptions allow the UI layer (`app.py`) to catch only the errors it knows how to handle and display a user-friendly message, without accidentally swallowing unexpected bugs.

**Relevant Context:** Used in `validators.py` and `career_engine.py`.

**Status:** [x] done

---

## Sub-Task 4 — Data Models

**Intent:** Define `UserProfile` and `CareerAnalysisResult` as Python dataclasses. These act as the typed data contracts between the UI, the validator, and the engine.

**Expected Outcomes:**
- `models/user_profile.py` defines `UserProfile`
- `models/career_result.py` defines `CareerAnalysisResult`
- Both are importable and instantiable with no errors
- All fields have correct types and sensible defaults

**Todo List:**
1. Create `models/user_profile.py` — define `UserProfile` as a `@dataclass`
2. Create `models/career_result.py` — define `CareerAnalysisResult` as a `@dataclass`

**UserProfile Fields:**

| Field | Type | Description |
|---|---|---|
| `name` | `str` | User's full name |
| `current_role` | `str` | Current job title or "Student" |
| `skills` | `list[str]` | Normalised list of skills the user has |
| `education` | `str` | Highest qualification |
| `target_role` | `str` | Role the user wants to move into |
| `years_of_experience` | `int` | Total professional years (0 = student/entry-level) |

**CareerAnalysisResult Fields:**

| Field | Type | Description |
|---|---|---|
| `matched_skills` | `list[str]` | Skills user has that match the role |
| `missing_skills` | `list[str]` | Required skills the user lacks |
| `readiness_score` | `float` | Percentage of required skills matched (0.0–100.0) |
| `readiness_label` | `str` | "Beginner", "Developing", or "Ready" |
| `suggestions` | `list[str]` | Text-based improvement advice |
| `learning_areas` | `list[str]` | Recommended study topics from role data |
| `summary` | `str` | One-paragraph narrative summary |

**Why dataclasses?**
They are standard Python (no extra imports), self-documenting, and let you access fields by name (`result.readiness_score`) rather than by dictionary key, which reduces bugs for beginners.

**Relevant Context:** Used by `validators.py`, `career_engine.py`, and `app.py`.

**Status:** [x] done

---

## Sub-Task 5 — Input Validation

**Intent:** Create a pure-function validator module that cleans and validates all user inputs before they reach the engine.

**Expected Outcomes:**
- `utils/validators.py` implements all validation functions
- Each function either returns a clean value or raises a named exception
- No Streamlit imports anywhere in this file

**Todo List:**
1. Create `utils/validators.py`
2. Implement `validate_name(name: str) -> str`
3. Implement `validate_current_role(role: str) -> str`
4. Implement `validate_skills(raw_input: str) -> list[str]`
5. Implement `validate_education(education: str) -> str`
6. Implement `validate_target_role(role: str, known_roles: list[str]) -> str`
7. Implement `validate_years_of_experience(years: int) -> int`
8. Implement `build_user_profile(raw_inputs: dict, known_roles: list[str]) -> UserProfile` — calls all validators above and returns a clean `UserProfile`, or raises the appropriate custom exception on the first failure

**Validation Rules Per Field:**

| Field | Rules |
|---|---|
| `name` | Non-empty after strip; letters, spaces, hyphens only; max 60 chars |
| `current_role` | Non-empty after strip; max 80 chars |
| `skills` | Split on comma; strip each entry; deduplicate; lowercase; at least 1 skill remaining |
| `education` | Non-empty after strip; max 120 chars |
| `target_role` | Must exist in `known_roles` list |
| `years_of_experience` | Integer; min 0; max 50 |

**Why pure functions with no Streamlit dependency?**
These functions can be called and tested in complete isolation from the UI. This is the most important separation-of-concerns principle in the project.

**Relevant Context:** `exceptions/errors.py`, `models/user_profile.py`

**Status:** [x] done

---

## Sub-Task 6 — Data Loader

**Intent:** Create a single module responsible for reading `job_roles.json` and providing it to the rest of the application.

**Expected Outcomes:**
- `engine/data_loader.py` can load and return the full role dictionary
- Loading is safe — raises a clear error if the file is missing or malformed
- Returns a plain Python dict with no transformation needed

**Todo List:**
1. Create `engine/data_loader.py`
2. Implement `load_job_roles() -> dict` — uses `pathlib.Path` to locate `data/job_roles.json` relative to the project root and returns the parsed dictionary
3. Implement `get_role_names() -> list[str]` — returns a sorted list of role names from the loaded dictionary (used to populate the Streamlit selectbox)
4. Cache the result using a module-level variable so the file is only read once per session

**Why pathlib instead of a hardcoded string path?**
`pathlib.Path(__file__).parent` resolves the correct path regardless of which directory the user runs the app from, avoiding the most common beginner file-not-found issue.

**Relevant Context:** `data/job_roles.json`

**Status:** [x] done

---

## Sub-Task 7 — Career Engine (Core Logic)

**Intent:** Implement the `CareerEngine` class, which is the heart of the application. It takes a `UserProfile` and produces a `CareerAnalysisResult` using pure rule-based logic.

**Expected Outcomes:**
- `engine/career_engine.py` implements `CareerEngine`
- All methods are pure (no side effects, no UI calls, no file I/O)
- All methods are independently testable
- The engine raises `UnknownRoleError` if the profile's target role is not in the data

**Todo List:**
1. Create `engine/career_engine.py`
2. Implement `CareerEngine` class with `__init__(self, job_roles: dict)` — accepts the pre-loaded role dictionary
3. Implement `analyze(self, profile: UserProfile) -> CareerAnalysisResult` — the public entry point that orchestrates all steps below
4. Implement `_get_required_skills(self, target_role: str) -> list[str]` — retrieves required skills for the role; raises `UnknownRoleError` if role not found
5. Implement `_match_skills(self, user_skills: list[str], required_skills: list[str]) -> tuple[list[str], list[str]]` — returns `(matched, missing)` using set intersection/difference on lowercased skill names
6. Implement `_calculate_readiness_score(self, matched: list[str], required: list[str]) -> float` — returns `(len(matched) / len(required)) * 100`, or `0.0` if required is empty
7. Implement `_get_readiness_label(self, score: float) -> str` — returns "Beginner" for score < 40, "Developing" for 40–69, "Ready" for 70+
8. Implement `_generate_suggestions(self, missing_skills: list[str], years_exp: int) -> list[str]` — generates one suggestion string per missing skill, with phrasing adjusted for experience level
9. Implement `_get_learning_areas(self, target_role: str) -> list[str]` — returns the `learning_areas` list from role data
10. Implement `_generate_summary(self, profile: UserProfile, result: CareerAnalysisResult) -> str` — builds a single narrative paragraph combining name, target role, score, and top suggestions

**Skill Matching Algorithm:**
```
user_skills_set   = {skill.strip().lower() for skill in profile.skills}
required_set      = {skill.strip().lower() for skill in required_skills}
matched_set       = user_skills_set & required_set
missing_set       = required_set - user_skills_set
```
All comparisons are lowercase. The returned `matched_skills` and `missing_skills` lists preserve the original casing from the role data (not the user's input) for display consistency.

**Suggestion Logic:**
- For each missing skill, generate one sentence: `"Learn {skill} — it is required for this role."`
- If `years_of_experience == 0`: prefix suggestions with `"As an entry-level candidate, focus first on: "`
- If `years_of_experience >= 5`: prefix with `"As an experienced professional, accelerate your path by adding: "`
- If no missing skills: return `["You already have all required skills for this role. Consider applying now!"]`

**Why a class instead of standalone functions?**
The class holds `job_roles` as state injected at construction time (`__init__`), so it does not need to reload the JSON file on every call. It also groups related methods logically and is a natural introduction to OOP dependency injection for beginners.

**Relevant Context:** `models/user_profile.py`, `models/career_result.py`, `exceptions/errors.py`, `engine/data_loader.py`

**Status:** [x] done

---

## Sub-Task 8 — Streamlit UI

**Intent:** Build the `app.py` Streamlit interface. The UI only collects inputs, calls the validator and engine, and renders the results. It contains no business logic.

**Expected Outcomes:**
- `app.py` renders a complete, working single-page Streamlit application
- All user inputs are collected and passed to `build_user_profile()`
- The `CareerEngine.analyze()` result is displayed clearly
- Validation and engine errors are caught and shown as `st.error()` messages without crashing
- The app runs with `streamlit run app.py`

**Todo List:**
1. Create `app.py`
2. Add page config: title "AI Career Copilot", wide layout, robot emoji favicon
3. Render a sidebar with a brief app description and instructions
4. Render the **Profile Input Section** (left or top area):
   - Text input: Full Name
   - Text input: Current Job Role
   - Text area: Your Skills (comma-separated)
   - Text input: Education / Qualification
   - Selectbox: Target Role (populated from `get_role_names()`)
   - Number input: Years of Experience (min 0, max 50, default 0)
   - Primary button: "Analyse My Career"
5. On button click:
   - Call `build_user_profile(raw_inputs, known_roles)` inside a `try/except`
   - If `InvalidProfileError` or `InvalidExperienceError`: show `st.error()` and stop
   - If valid: call `CareerEngine(job_roles).analyze(profile)`
   - If `UnknownRoleError`: show `st.error()` and stop
6. Render the **Career Readiness Dashboard** (shown only after successful analysis):
   - Section: Career Profile card — name, current role, education, experience
   - Section: Readiness Score — large `st.metric()` showing score %, label with colour indicator
   - Section: Matched Skills — green badges or a bulleted list
   - Section: Missing Skills — red/orange badges or a bulleted list
   - Section: Suggestions — numbered list of suggestion strings
   - Section: Recommended Learning Areas — bulleted list
   - Section: Career Summary — `st.info()` box with the narrative paragraph

**UI Layout Strategy:**
- Use `st.columns([1, 1])` to place input form on the left and results on the right on desktop
- Fall back gracefully to a stacked layout on mobile (Streamlit handles this automatically)
- Use `st.divider()` between major sections for visual clarity
- Use `st.expander()` for the raw profile data so the page is not overwhelming

**Why no session state for V1?**
Streamlit reruns the whole script on every interaction. For this project that is a feature, not a bug — the user simply re-clicks the button to re-analyse. Session state would add complexity without user-visible benefit.

**Relevant Context:** `utils/validators.py`, `engine/career_engine.py`, `engine/data_loader.py`, all models and exceptions

**Status:** [x] done

---

## Sub-Task 9 — pytest Tests

**Intent:** Write a comprehensive but focused test suite for all business logic. The UI is not tested (Streamlit UI testing requires additional tooling beyond this project's scope).

**Expected Outcomes:**
- All test files in `tests/` pass with `pytest tests/` from the project root
- No test imports `streamlit`
- Every public method in `CareerEngine` and `validators.py` is covered
- Edge cases from the requirements are explicitly tested

**Todo List:**
1. Create `tests/test_validators.py` — test all validation functions
2. Create `tests/test_career_engine.py` — test all `CareerEngine` methods
3. Create `tests/test_data_loader.py` — test that `load_job_roles()` returns a non-empty dict with the expected keys

**Tests for `test_validators.py`:**

| Test | Input | Expected |
|---|---|---|
| `test_valid_name` | `"Alice"` | Returns `"Alice"` |
| `test_name_with_spaces` | `"Mary Jane"` | Returns `"Mary Jane"` |
| `test_empty_name_raises` | `""` | Raises `InvalidProfileError` |
| `test_name_too_long_raises` | 61-char string | Raises `InvalidProfileError` |
| `test_valid_skills` | `"Python, SQL, Git"` | Returns `["python", "sql", "git"]` |
| `test_skills_deduplication` | `"Python, python, PYTHON"` | Returns `["python"]` |
| `test_empty_skills_raises` | `""` | Raises `InvalidProfileError` |
| `test_valid_years` | `3` | Returns `3` |
| `test_negative_years_raises` | `-1` | Raises `InvalidExperienceError` |
| `test_years_over_limit_raises` | `51` | Raises `InvalidExperienceError` |
| `test_valid_target_role` | `"Data Scientist"`, known list | Returns `"Data Scientist"` |
| `test_unknown_role_raises` | `"Wizard"`, known list | Raises `UnknownRoleError` |

**Tests for `test_career_engine.py`:**

| Test | Scenario | Expected |
|---|---|---|
| `test_full_skill_match` | User has all required skills | `readiness_score == 100.0` |
| `test_no_skill_match` | User has zero matching skills | `readiness_score == 0.0` |
| `test_partial_match` | User has half the skills | `readiness_score == 50.0` |
| `test_missing_skills_correct` | Known partial match | `missing_skills` list is correct |
| `test_matched_skills_correct` | Known partial match | `matched_skills` list is correct |
| `test_readiness_label_beginner` | Score = 30 | Label is "Beginner" |
| `test_readiness_label_developing` | Score = 55 | Label is "Developing" |
| `test_readiness_label_ready` | Score = 80 | Label is "Ready" |
| `test_case_insensitive_matching` | User skill `"PYTHON"`, required `"python"` | Matched correctly |
| `test_unknown_role_raises` | Target role not in data | Raises `UnknownRoleError` |
| `test_zero_experience_suggestions` | `years_of_experience = 0` | Entry-level phrasing in suggestions |
| `test_no_missing_skills_positive_message` | 100% match | Positive suggestion returned |
| `test_summary_contains_name` | Profile with name `"Alice"` | Summary string contains `"Alice"` |
| `test_duplicate_user_skills_handled` | `["python", "python"]` | Not double-counted in match |

**Tests for `test_data_loader.py`:**

| Test | Expected |
|---|---|
| `test_load_returns_dict` | Returns a `dict` |
| `test_load_contains_expected_roles` | All 8 roles present |
| `test_get_role_names_sorted` | Returns sorted list |
| `test_role_has_required_keys` | Each role has `required_skills`, `learning_areas`, `recommended_experience_years` |

**Status:** [x] done

---

## Sub-Task 10 — README and Final Polish

**Intent:** Write a `README.md` that explains what the project is, how to install it, how to run it, and how to run tests.

**Expected Outcomes:**
- `README.md` is clear enough that a beginner can clone the repo and run the app in under 5 minutes
- All badge-worthy things (install, run, test) are shown as code blocks

**Todo List:**
1. Write `README.md` with the following sections:
   - Project title and one-line description
   - Screenshot placeholder (can be updated later)
   - Prerequisites (Python 3.10+)
   - Installation: `pip install -r requirements.txt`
   - Running the app: `streamlit run app.py`
   - Running tests: `pytest tests/`
   - Project structure overview
   - How to add a new job role (edit `job_roles.json`)
   - How the skill matching works (plain English)

**Status:** [x] done

---

## Data Flow Summary

```
User fills Streamlit form
        |
        v
app.py collects raw_inputs dict
        |
        v
validators.build_user_profile(raw_inputs, known_roles)
    - validate_name()
    - validate_current_role()
    - validate_skills()       <-- normalises to lowercase list
    - validate_education()
    - validate_target_role()  <-- checks against known_roles
    - validate_years()
        |
   raises InvalidProfileError / UnknownRoleError / InvalidExperienceError
        |
        v
UserProfile object (clean, typed data)
        |
        v
CareerEngine(job_roles).analyze(profile)
    - _get_required_skills()
    - _match_skills()          <-- set intersection/difference
    - _calculate_readiness_score()
    - _get_readiness_label()
    - _generate_suggestions()
    - _get_learning_areas()
    - _generate_summary()
        |
   raises UnknownRoleError if role missing
        |
        v
CareerAnalysisResult object
        |
        v
app.py renders Career Readiness Dashboard
```

---

## Persistence Approach

**V1 decision: No persistence needed.**

Streamlit's execution model reruns the full script on every user interaction. All state is ephemeral and lives in Python variables during that run. This is the simplest possible approach and entirely appropriate for V1.

The only "persistence" in the project is `data/job_roles.json` — a static data file that defines the role knowledge base. It is read-only from the app's perspective.

**If persistence is added later (V2):**
- Save the `CareerAnalysisResult` to a CSV file using Python's built-in `csv` module
- Add a `st.download_button()` so the user can download their report as CSV
- No database, no ORM, no external service needed

---

## Edge Cases to Handle

| Edge Case | Handling |
|---|---|
| User has all required skills | Score = 100%, positive suggestion message, no missing skills section |
| User has zero skills after parsing | `InvalidProfileError` raised by validator |
| User enters only spaces in name | Strip + empty check catches it |
| User enters duplicate skills | Deduplicated in `validate_skills()` before reaching the engine |
| Target role not in JSON | `UnknownRoleError` raised; shown as `st.error()` |
| Years of experience = 0 | Entry-level suggestions generated |
| Skills entered in ALL CAPS or mixed case | Lowercased in validator; comparison is case-insensitive |
| `job_roles.json` has a role with empty `required_skills` | `_calculate_readiness_score()` returns `0.0` safely |
| User enters commas with spaces between skills | `strip()` on each token handles this |
| Number entered as name | Regex check in `validate_name()` catches it |

---

## Dependencies

```
# requirements.txt
streamlit>=1.32.0
pytest>=8.0.0
```

No other dependencies. All other tools used (`json`, `pathlib`, `dataclasses`, `re`, `math`) are Python standard library.

**Why so few dependencies?**
Every dependency is a maintenance burden. For a beginner project, the fewer the better. The entire skill-matching engine is achievable with Python sets, which are built in.

---

## Implementation Order

The sub-tasks should be implemented in this exact order. Each one builds cleanly on the previous.

| Order | Sub-Task | Why This Order |
|---|---|---|
| 1 | Project Scaffold | Nothing else can exist without the folder structure |
| 2 | job_roles.json | The data must exist before the loader or engine can be written |
| 3 | Custom Exceptions | Models and validators import exceptions; must exist first |
| 4 | Data Models | Validators and engine import models; must exist before them |
| 5 | Input Validators | Engine expects a clean UserProfile; validators must be ready |
| 6 | Data Loader | Engine needs the loader; must exist before the engine |
| 7 | Career Engine | Core logic; depends on everything above |
| 8 | Streamlit UI | UI wires everything together; written last |
| 9 | Tests | Written after all modules exist so they can import them |
| 10 | README | Written last when the project is complete and accurate |
