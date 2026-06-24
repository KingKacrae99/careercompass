# C:\Users\HP\Desktop\careercompass\careercompass\core\management\commands\seed_careers.py
from django.core.management.base import BaseCommand
from core.models import Discipline, Career

class Command(BaseCommand):
    help = "Seeds initial disciplines and careers into the database using bulk operations"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # 1. Get or create disciplines safely
        science, _ = Discipline.objects.get_or_create(branch='science')
        arts, _ = Discipline.objects.get_or_create(branch='arts')
        social, _ = Discipline.objects.get_or_create(branch='social science')
        mgt, _ = Discipline.objects.get_or_create(branch='mgt science')

        # 2. Complete career dataset list
        careers_data = [
            {'name': 'Software Engineer', 'description': 'Designs and builds software applications.', 'subject_group': 'Maths, Computer Science, Physics', 'strength': 'problem_solving', 'interest': 'programming', 'discipline': science},
            {'name': 'Graphic Designer', 'description': 'Creates digital and print designs.', 'subject_group': 'Fine Arts, ICT, English', 'strength': 'creativity', 'interest': 'design', 'discipline': arts},
            {'name': 'Psychologist', 'description': 'Studies human behavior.', 'subject_group': 'Biology, Social Studies', 'strength': 'empathy', 'interest': 'psychology', 'discipline': social},
            {'name': 'Civil Engineer', 'description': 'Plans construction structures.', 'subject_group': 'Maths, Physics', 'strength': 'analytical', 'interest': 'engineering', 'discipline': science},
            {'name': 'Digital Marketer', 'description': 'Promotes brands online.', 'subject_group': 'Marketing, ICT', 'strength': 'communication', 'interest': 'marketing', 'discipline': mgt},
            {'name': 'Teacher', 'description': 'Educates students.', 'subject_group': 'English, Education', 'strength': 'teaching', 'interest': 'education', 'discipline': social},
            {'name': 'Financial Analyst', 'description': 'Analyzes financial data.', 'subject_group': 'Maths, Economics', 'strength': 'numerical', 'interest': 'finance', 'discipline': mgt},
            {'name': 'Environmental Scientist', 'description': 'Researches environmental problems.', 'subject_group': 'Biology, Chemistry', 'strength': 'research', 'interest': 'nature', 'discipline': science},
            {'name': 'Actor', 'description': 'Performs roles.', 'subject_group': 'Literature, Drama', 'strength': 'performance', 'interest': 'acting', 'discipline': arts},
            {'name': 'Entrepreneur', 'description': 'Builds businesses.', 'subject_group': 'Business Studies', 'strength': 'leadership', 'interest': 'entrepreneurship', 'discipline': mgt},
            {'name': 'UI/UX Designer', 'description': 'Designs app interfaces.', 'subject_group': 'ICT, Visual Arts', 'strength': 'visual', 'interest': 'design', 'discipline': arts},
            {'name': 'Nurse', 'description': 'Provides healthcare.', 'subject_group': 'Biology, Chemistry', 'strength': 'empathy', 'interest': 'healthcare', 'discipline': science},
            {'name': 'Lawyer', 'description': 'Represents clients in legal matters.', 'subject_group': 'Government, Literature', 'strength': 'persuasive', 'interest': 'politics', 'discipline': social},
            {'name': 'Data Analyst', 'description': 'Interprets business data.', 'subject_group': 'Maths, Computer Science', 'strength': 'logical', 'interest': 'technology', 'discipline': science},
            {'name': 'Biochemist', 'description': 'Studies chemical processes.', 'subject_group': 'Biology, Chemistry', 'strength': 'experimental', 'interest': 'laboratory', 'discipline': science},
            {'name': 'Musician', 'description': 'Performs music.', 'subject_group': 'Music, Literature', 'strength': 'emotional', 'interest': 'music', 'discipline': arts},
            {'name': 'Economist', 'description': 'Studies production and consumption.', 'subject_group': 'Economics, Maths', 'strength': 'decision_making', 'interest': 'finance', 'discipline': social},
            {'name': 'Fashion Designer', 'description': 'Designs clothing.', 'subject_group': 'Fine Arts, Home Economics', 'strength': 'imaginative', 'interest': 'fashion', 'discipline': arts},
            {'name': 'Historian', 'description': 'Researches historical events.', 'subject_group': 'History, Literature', 'strength': 'research', 'interest': 'history', 'discipline': social},
            {'name': 'Web Developer', 'description': 'Builds websites.', 'subject_group': 'Computer Science, ICT', 'strength': 'problem_solving', 'interest': 'programming', 'discipline': science},
            {'name': 'Project Manager', 'description': 'Leads project teams.', 'subject_group': 'Business Studies', 'strength': 'organization', 'interest': 'business', 'discipline': mgt},
            {'name': 'Real Estate Agent', 'description': 'Sells properties.', 'subject_group': 'Economics, Business', 'strength': 'salesmanship', 'interest': 'real_estate', 'discipline': mgt},
            {'name': 'Sociologist', 'description': 'Studies society and culture.', 'subject_group': 'Social Studies, Literature', 'strength': 'observational', 'interest': 'culture', 'discipline': social},
            {'name': 'Public Relations Officer', 'description': 'Manages communication.', 'subject_group': 'English, Literature', 'strength': 'communication', 'interest': 'marketing', 'discipline': social},
            {'name': 'Chemist', 'description': 'Researches chemical reactions.', 'subject_group': 'Chemistry, Physics', 'strength': 'precision', 'interest': 'laboratory', 'discipline': science},
            {'name': 'Content Creator', 'description': 'Produces online media content.', 'subject_group': 'English, ICT', 'strength': 'storytelling', 'interest': 'film', 'discipline': arts},
            {'name': 'Architect', 'description': 'Designs buildings.', 'subject_group': 'Technical Drawing, Physics', 'strength': 'visual', 'interest': 'engineering', 'discipline': science},
            {'name': 'Counselor', 'description': 'Guides personal decisions.', 'subject_group': 'Psychology, Education', 'strength': 'empathy', 'interest': 'psychology', 'discipline': social},
            {'name': 'Business Analyst', 'description': 'Evaluates corporate needs.', 'subject_group': 'Business Studies, Economics', 'strength': 'planning', 'interest': 'business', 'discipline': mgt},
            {'name': 'eCommerce Specialist', 'description': 'Manages online store platforms.', 'subject_group': 'Business Studies, ICT', 'strength': 'organization', 'interest': 'ecommerce', 'discipline': mgt},
            {'name': "Mechanical Engineer", 'description': "Designs machines.", 'subject_group': "Physics, Mathematics", 'strength': "Problem-Solving", 'interest': "Technology", 'discipline': science},
            {'name': "Doctor", 'description': "Diagnoses illnesses.", 'subject_group': "Biology, Chemistry", 'strength': "Compassion", 'interest': "Health", 'discipline': science},
            {'name': "Veterinarian", 'description': "Provides medical care for animals.", 'subject_group': "Biology, Agricultural Science", 'strength': "Compassion", 'interest': "Animals", 'discipline': science},
            {'name': "Pharmacist", 'description': "Dispenses medications.", 'subject_group': "Chemistry, Biology", 'strength': "Attention to Detail", 'interest': "Health", 'discipline': science},
            {'name': "Data Scientist", 'description': "Analyzes complex data.", 'subject_group': "Mathematics, Statistics", 'strength': "Analytical Thinking", 'interest': "Technology", 'discipline': science}
        ]

        # 3. Optimize: Find what already exists to avoid duplication crashes
        existing_names = set(Career.objects.values_list('name', flat=True))

        # 4. Prepare objects in local memory only
        new_careers = []
        for item in careers_data:
            if item['name'] not in existing_names:
                new_careers.append(
                    Career(
                        name=item['name'],
                        description=item['description'],
                        subject_group=item['subject_group'],
                        strength=item['strength'],
                        interest=item['interest'],
                        discipline=item['discipline']
                    )
                )

        # 5. Execute exactly one single database transaction
        if new_careers:
            Career.objects.bulk_create(new_careers)
            self.stdout.write(self.style.SUCCESS(f"Successfully batch-inserted {len(new_careers)} new careers!"))
        else:
            self.stdout.write(self.style.WARNING("All careers already exist in the database."))
