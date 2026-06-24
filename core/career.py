# C:\Users\HP\Desktop\careercompass\careercompass\core\career.py
from .models import Career, Discipline

def get_careers():
    """Safely retrieves careers from the database instead of creating them globally."""
    return Career.objects.all()
