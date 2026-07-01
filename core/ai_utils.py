from google import genai
from django.conf import settings

client = genai.Client(
    api_key=settings.API_KEY
)


def get_career_advice(subject, strength, interest, discipline):
    prompt = f"""
    You are a professional career advisor.

    User Information:
    Discipline: {discipline}
    Favourite Subject: {subject}
    Strength: {strength}
    Interest: {interest}

    Provide:
    1. Three suitable careers.
    2. Why each career matches the user.
    3. Subjects the user should focus on.
    4. One piece of advice for preparing for these careers.

    Keep the response simple for a senior secondary school student.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )
        print(response.text)
        return response.text

    except Exception as e:
        return f"AI Error: {e}"