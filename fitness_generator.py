
import os
from groq import Groq


def generate_fitness_plan(
    fitness_goal: str,
    experience_level: str,
    days_per_week: int,
    equipment_access: str,
    injuries_limitations: str = "",
    api_key: str | None = None
) -> str:
    """
    Generate a personalized fitness plan using the Groq API.

    Args:
        fitness_goal: User's primary fitness goal.
        experience_level: Beginner, Intermediate, or Advanced.
        days_per_week: Number of available training days (1-7).
        equipment_access: Available workout equipment.
        injuries_limitations: Optional injuries or limitations.
        api_key: Optional Groq API key.

    Returns:
        AI-generated fitness plan as a string.
    """

    try:
        # Validate inputs
        valid_goals = [
            "Build muscle",
            "Lose fat",
            "General fitness",
            "Improve endurance"
        ]

        valid_levels = [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]

        valid_equipment = [
            "No equipment",
            "Home dumbbells",
            "Full gym"
        ]

        if fitness_goal not in valid_goals:
            raise ValueError("Invalid fitness goal.")

        if experience_level not in valid_levels:
            raise ValueError("Invalid experience level.")

        if not 1 <= days_per_week <= 7:
            raise ValueError("Training days must be between 1 and 7.")

        if equipment_access not in valid_equipment:
            raise ValueError("Invalid equipment selection.")

        # Initialize Groq client
        client = Groq(
            api_key=api_key or os.getenv("GROQ_API_KEY")
        )

        # Construct the AI prompt
        system_prompt = """
        You are an expert fitness coach and personal trainer.

        Your task is to create safe, practical, and personalized
        workout plans based on the user's fitness information.

        Follow these instructions:
        1. Create a weekly workout schedule.
        2. Recommend suitable exercises.
        3. Specify sets, repetitions, and rest periods.
        4. Match exercise difficulty to the user's experience.
        5. Only recommend exercises compatible with available equipment.
        6. Include warm-up and cool-down recommendations.
        7. Explain how the user can progressively improve.
        8. Make the plan realistic for the available training days.
        9. Avoid exercises that conflict with reported injuries
           or physical limitations.
        10. Never diagnose injuries or claim that an exercise
            is medically safe. Recommend professional assessment
            when limitations require individual guidance.

        Format your response using clear headings and bullet points.
        """

        user_prompt = f"""
        Create a personalized weekly fitness plan using these inputs:

        FITNESS GOAL:
        {fitness_goal}

        EXPERIENCE LEVEL:
        {experience_level}

        AVAILABLE TRAINING DAYS:
        {days_per_week} days per week

        EQUIPMENT ACCESS:
        {equipment_access}

        INJURIES OR PHYSICAL LIMITATIONS:
        {injuries_limitations if injuries_limitations.strip() else "None specified"}

        Please provide:

        1. Overview of the fitness plan.
        2. Weekly workout schedule.
        3. Exercises for each training day.
        4. Sets, repetitions, and rest periods.
        5. Warm-up and cool-down guidance.
        6. Progression recommendations.
        7. Recovery and rest-day guidance.

        Ensure the workout plan matches all the user's inputs.
        """

        # Send request to Groq API
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.5,
            max_tokens=3000
        )

        # Extract generated response
        fitness_plan = response.choices[0].message.content

        if not fitness_plan:
            raise ValueError("The AI returned an empty response.")

        return fitness_plan

    except Exception as e:
        print(f"Error generating fitness plan: {e}")
        return f"Unable to generate your fitness plan: {e}"
