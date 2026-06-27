import os
import request
from django.conf import settings

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_TOKEN}"}

def get_career_advice(subject,strength,interest,discipline):
    prompt = f"""
            You are a professional career advisor.

            user Information:
            Discipline: {discipline}
            Favourite Subject: {subject}
            Strength: {strength}
            Interest: {interest}

            Provide:
            1. Three suitable careers.
            2. Why each career matches the user.
            3. Subjects the user should focus on.
            4. One piece of advice for preparing for these careers.

            Keep the response simple.
            """

    response = request.post(API_URL,headers=headers, json={'input':prompt})

    data = response.json()

    if isinstance(data, list):
       return data[0]["generated text"]

    return "Unable to generate recommendation right now"

