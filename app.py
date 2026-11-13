
import streamlit as st
from fitness_generator import generate_fitness_plan
from groq import Groq
import os

# Page configuration
st.set_page_config(
    page_title="AI Fitness Planner",
    page_icon="💪",
    layout="centered"
)

# Custom styling
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stButton > button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        height: 45px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Website heading
st.title("💪 AI Fitness Planner")
st.write(
    "Tell us about your fitness goals and preferences "
    "to create a personalized workout plan."
)

st.divider()

# Structured input form
with st.form("fitness_form"):

    st.subheader("1. Fitness Goal")

    fitness_goal = st.selectbox(
        "What is your primary fitness goal?",
        [
            "Build muscle",
            "Lose fat",
            "General fitness",
            "Improve endurance"
        ]
    )

    st.subheader("2. Experience Level")

    experience_level = st.selectbox(
        "How experienced are you with exercising?",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.subheader("3. Training Availability")

    days_per_week = st.slider(
        "How many days can you exercise per week?",
        min_value=1,
        max_value=7,
        value=3
    )

    st.write(f"**Selected: {days_per_week} days per week**")

    st.subheader("4. Equipment Access")

    equipment_access = st.selectbox(
        "What equipment do you have access to?",
        [
            "No equipment",
            "Home dumbbells",
            "Full gym"
        ]
    )

    st.subheader("5. Injuries or Physical Limitations")

    limitations = st.text_area(
        "Do you have any injuries or exercise limitations?",
        placeholder="e.g. Bad knees, no overhead pressing...",
        help="This field is optional."
    )

    st.divider()

    submitted = st.form_submit_button(
        "Generate My Fitness Plan"
    )
print(os.getenv("GROQ_MODEL", "gpt-oss-20b"))

# Process submitted inputs
if submitted:

    with st.spinner("Generating your personalized fitness plan..."):

        fitness_plan = generate_fitness_plan(
            fitness_goal=fitness_goal,
            experience_level=experience_level,
            days_per_week=days_per_week,
            equipment_access=equipment_access,
            injuries_limitations=limitations,
            api_key=os.getenv("GROQ_API_KEY")
        )

    if fitness_plan.startswith("Unable to generate"):
        st.error(fitness_plan)

    else:
        st.success("Your fitness plan is ready!")

        st.subheader("Your Personalized Workout Plan")

        st.markdown(fitness_plan)
