"""AI Career Copilot — Streamlit UI entry point.

Run from inside the ai_career_copilot/ directory:

    streamlit run app.py

The UI is intentionally thin: it collects inputs, delegates all
business logic to the engine layer, and renders the results.
"""

import streamlit as st

from engine.career_engine import CareerEngine
from engine.data_loader import get_role_names
from engine.persistence import delete_profile, load_profile, save_profile
from exceptions.errors import (
    InvalidExperienceError,
    InvalidProfileError,
    UnknownRoleError,
)
from utils.validators import build_career_profile

# ── Page config — must be the very first Streamlit call ──────────────────────
st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🤖",
    layout="wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🤖 AI Career Copilot")
    st.write(
        "AI Career Copilot analyses your skills and experience against "
        "your chosen target role, produces a readiness score, highlights "
        "skill gaps, and gives you personalised suggestions to accelerate "
        "your career."
    )
    st.divider()
    st.markdown("**How to use**")
    st.write("1. Fill in your profile in the left column.")
    st.write("2. Click **🔍 Analyse My Career**.")
    st.write("3. Review your readiness dashboard on the right.")
    st.info("💡 Enter skills as a comma-separated list, e.g. Python, SQL, Git")
    st.divider()
    st.caption("Data is saved locally as JSON — no external service is used.")

# ── Load any previously saved profile ────────────────────────────────────────
_saved = load_profile()

# ── Helper: pre-fill a widget default from the saved profile ──────────────────
def _default(field: str, fallback: str = "") -> str:
    """Return the saved-profile value for *field*, or *fallback*."""
    if _saved is None:
        return fallback
    return str(getattr(_saved, field, fallback))


def _default_int(field: str, fallback: int = 0) -> int:
    if _saved is None:
        return fallback
    return int(getattr(_saved, field, fallback))


# ── Main two-column layout ────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1])

# ── Left column — Profile Input Form ─────────────────────────────────────────
with left_col:
    st.subheader("📋 Your Career Profile")

    if _saved:
        st.success("✅ Previous profile loaded — you can edit it below.")

    name = st.text_input("Full Name", value=_default("name"))
    current_role = st.text_input(
        "Current Job Role or Career Level",
        value=_default("current_role"),
    )
    skills_input = st.text_area(
        "Your Skills (comma-separated)",
        value=", ".join(_saved.skills) if _saved else "",
        height=100,
        help="Example: Python, SQL, Git, Data Visualization",
    )
    education = st.text_input(
        "Education / Qualification",
        value=_default("education"),
    )
    role_names = get_role_names()
    saved_target = _default("target_role")
    target_index = role_names.index(saved_target) if saved_target in role_names else 0
    target_role = st.selectbox(
        "Target Role",
        options=role_names,
        index=target_index,
    )
    years_of_experience = st.number_input(
        "Years of Experience",
        min_value=0,
        max_value=50,
        step=1,
        value=_default_int("years_of_experience"),
    )

    col_btn, col_clear = st.columns([2, 1])
    with col_btn:
        submitted = st.button("🔍 Analyse My Career", type="primary", use_container_width=True)
    with col_clear:
        clear_btn = st.button("🗑️ Clear Saved", use_container_width=True)

    if clear_btn:
        delete_profile()
        st.success("Saved profile cleared.")
        st.rerun()

# ── Process the form submission ───────────────────────────────────────────────
if submitted:
    raw_inputs = {
        "name": name,
        "current_role": current_role,
        "skills": skills_input,
        "education": education,
        "target_role": target_role,
        "years_of_experience": int(years_of_experience),
    }

    try:
        profile = build_career_profile(raw_inputs, role_names)
    except InvalidProfileError as exc:
        st.error(f"❌ Profile Error: {exc}")
        st.stop()
    except InvalidExperienceError as exc:
        st.error(f"❌ Experience Error: {exc}")
        st.stop()
    except UnknownRoleError as exc:
        st.error(f"❌ Role Error: {exc}")
        st.stop()

    # Persist the validated profile
    save_profile(profile)

    try:
        engine = CareerEngine()
        result = engine.analyse(profile)
    except UnknownRoleError as exc:
        st.error(f"❌ Analysis Error: {exc}")
        st.stop()

    # ── Right column — Career Readiness Dashboard ─────────────────────────────
    with right_col:
        st.subheader("📊 Career Readiness Dashboard")

        # ── Section 1: Career Profile Card ───────────────────────────────────
        st.info(
            f"**👤 Name:** {profile.name}  \n"
            f"**💼 Current Role:** {profile.current_role}  \n"
            f"**🎓 Education:** {profile.education}  \n"
            f"**🎯 Target Role:** {profile.target_role}  \n"
            f"**📅 Experience:** {profile.years_of_experience} year(s)"
        )

        # ── Section 2: Readiness Score ────────────────────────────────────────
        st.metric(
            label="Career Readiness Score",
            value=f"{result.readiness_score}%",
            delta=result.readiness_label,
        )
        if result.readiness_label == "Ready":
            st.success(f"🟢 {result.readiness_label} — Great position to apply!")
        elif result.readiness_label == "Developing":
            st.warning(f"🟡 {result.readiness_label} — Keep building your skills.")
        else:
            st.error(f"🔴 {result.readiness_label} — Focus on the fundamentals first.")

        st.divider()

        # ── Section 3: Matched Skills ─────────────────────────────────────────
        st.subheader("✅ Matched Skills")
        if result.matched_skills:
            st.success(", ".join(result.matched_skills))
        else:
            st.warning("No skills matched the requirements for this role yet.")

        st.divider()

        # ── Section 4: Missing Skills ─────────────────────────────────────────
        st.subheader("❌ Missing Skills")
        if result.missing_skills:
            st.error(", ".join(result.missing_skills))
        else:
            st.success("🎉 You have all the required skills for this role!")

        st.divider()

        # ── Section 5: Career Improvement Suggestions ─────────────────────────
        st.subheader("💡 Career Improvement Suggestions")
        for suggestion in result.suggestions:
            st.write(f"• {suggestion}")

        st.divider()

        # ── Section 6: Recommended Learning Areas ────────────────────────────
        st.subheader("📚 Recommended Learning Areas")
        for area in result.learning_areas:
            st.write(f"• {area}")

        st.divider()

        # ── Section 7: Career Summary ─────────────────────────────────────────
        st.subheader("📝 Career Summary")
        st.info(result.summary)

        # ── Section 8: Raw Profile (Expander) ────────────────────────────────
        with st.expander("🔍 View Raw Profile Data"):
            st.json(profile.to_dict())

else:
    # Placeholder shown before the button is first clicked
    with right_col:
        st.info(
            "👈 Fill in your career profile on the left and click "
            "**🔍 Analyse My Career** to see your personalised readiness "
            "dashboard here."
        )
