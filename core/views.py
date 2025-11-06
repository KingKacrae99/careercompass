from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .form import CustomUserForm, AssessmentForm,LoginForm
# Create your views here.

def home_View(request):
    return render(request, 'core/index.html')

def login_view(request):
    previous_url = request.META.get('HTTP_REFERER', '/')
    print(f"Previous URL: {previous_url}")

    if request.user.is_authenticated:
        print("User already authenticated")
        if 'login' not in previous_url.lower():
            return redirect(previous_url)
        return redirect('home')

    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Login attempt with email: {email}")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user.first_name} {user.last_name}')
            return redirect(previous_url if 'login' not in previous_url.lower() else 'home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out.")
    return redirect('Login')  


def sigup_view(request):
    form = CustomUserForm(request.POST or None)
    print(form)
    if form.is_valid():
        user=form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(request, 'Account has been created successfully')
        return redirect('Login')
    else:
        messages.error(request, 'Invalid information')
    
    context ={
        'form': form,
    }
    return render(request, 'core/signup.html', context)

@login_required(login_url='Login')
def assessment_view(request):
    form = AssessmentForm(request.POST or None)
    if request.method == 'POST' and  request.headers.get('Content-Type') == 'application/json':
       try:
           data = json.loads(request.body)
       except json.JSONDecodeError:
           return JsonResponse({'error': 'Invalid JSON.'}, status=400)

       form = AssessmentForm({
            'favorite_subject': data.get('favorite'),
            'classified': data.get('classfied'),
            'strength': data.get('strength'),
            'interest' : data.get('interest')
        })
       if form.is_valid():
           assessment = form.save(commit=False)
           assessment.user = request.user
           assessment.save()

           discipline = assessment.classified
           careers = Career.objects.filter(
                strength=assessment.strength, 
                interest= assessment.interest,
                discipline=discipline
                )

           assessment.career.set(careers)

           career_list = list(careers.values(
                'name', 'description', 'subject_group', 'strength','interest', 'discipline'
            ))
            
           return JsonResponse({
                'message': f'{careers.count()} career(s) matched.',
                'careers': career_list
            })
       else:
           return JsonResponse({'errors': form.errors}, status=400)
        

    context ={
        'form': form,
    }
    return render(request, 'core/assessment.html', context)

@login_required(login_url='Login')
def UserDashboardView(request):
    assessment = Assessment.objects.filter(user=request.user).order_by('-id').first()
    career = assessment.career.all() #.first() if assessment and assessment.career.exists() else None

    context = {
        'career': career,
        'assessment': assessment
    }
    return render(request, 'core/user_dashboard.html', context)

# Get or create disciplines
science = Discipline.objects.get_or_create(branch='science')[0]
arts = Discipline.objects.get_or_create(branch='arts')[0]
social = Discipline.objects.get_or_create(branch='social science')[0]
mgt = Discipline.objects.get_or_create(branch='mgt science')[0]

careers = [
    Career(name='Software Engineer', description='Designs and builds software applications to solve real-world problems.', subject_group='Maths, Computer Science, Physics', strength='problem_solving', interest='programming', discipline=science),
    Career(name='Graphic Designer', description='Creates digital and print designs for branding and marketing.', subject_group='Fine Arts, ICT, English', strength='creativity', interest='design', discipline=arts),
    Career(name='Psychologist', description='Studies human behavior to help individuals improve mental health.', subject_group='Biology, Social Studies, Psychology', strength='empathy', interest='psychology', discipline=social),
    Career(name='Civil Engineer', description='Plans and oversees construction of roads, buildings, and other structures.', subject_group='Maths, Physics, Technical Drawing', strength='analytical', interest='engineering', discipline=science),
    Career(name='Digital Marketer', description='Promotes brands using digital strategies and platforms.', subject_group='Marketing, ICT, English', strength='communication', interest='marketing', discipline=mgt),
    Career(name='Teacher', description='Educates students and fosters learning and development.', subject_group='English, Education, Subject area', strength='teaching', interest='education', discipline=social),
    Career(name='Financial Analyst', description='Analyzes financial data to guide business decisions.', subject_group='Maths, Economics, Accounting', strength='numerical', interest='finance', discipline=mgt),
    Career(name='Environmental Scientist', description='Researches environmental problems and proposes solutions.', subject_group='Biology, Chemistry, Geography', strength='research', interest='nature', discipline=science),
    Career(name='Actor', description='Performs roles in plays, films, and television.', subject_group='Literature, Drama, Music', strength='performance', interest='acting', discipline=arts),
    Career(name='Entrepreneur', description='Builds and manages new businesses or startups.', subject_group='Business Studies, Economics, ICT', strength='leadership', interest='entrepreneurship', discipline=mgt),
    Career(name='UI/UX Designer', description='Designs user interfaces and experiences for apps/websites.', subject_group='ICT, Visual Arts', strength='visual', interest='design', discipline=arts),
    Career(name='Nurse', description='Provides healthcare support and treatment to patients.', subject_group='Biology, Chemistry, Health Science', strength='empathy', interest='healthcare', discipline=science),
    Career(name='Lawyer', description='Represents clients in legal matters and court proceedings.', subject_group='Government, Literature, CRS/IRS', strength='persuasive', interest='politics', discipline=social),
    Career(name='Data Analyst', description='Interprets data to solve business and scientific problems.', subject_group='Maths, Computer Science, Statistics', strength='logical', interest='technology', discipline=science),
    Career(name='Biochemist', description='Studies the chemical processes in living organisms.', subject_group='Biology, Chemistry, Physics', strength='experimental', interest='laboratory', discipline=science),
    Career(name='Musician', description='Performs or composes music professionally.', subject_group='Music, Literature, Performing Arts', strength='emotional', interest='music', discipline=arts),
    Career(name='Economist', description='Studies production, distribution, and consumption of goods.', subject_group='Economics, Maths, Government', strength='decision_making', interest='finance', discipline=social),
    Career(name='Fashion Designer', description='Designs and creates clothing and accessories.', subject_group='Fine Arts, Business Studies, Home Economics', strength='imaginative', interest='fashion', discipline=arts),
    Career(name='Historian', description='Researches and analyzes historical events and trends.', subject_group='History, Literature, Government', strength='research', interest='history', discipline=social),
    Career(name='Web Developer', description='Builds and maintains websites and web applications.', subject_group='Computer Science, ICT, Maths', strength='problem_solving', interest='programming', discipline=science),
    Career(name='Project Manager', description='Leads teams to complete projects efficiently and on time.', subject_group='Business Studies, Economics, ICT', strength='organization', interest='business', discipline=mgt),
    Career(name='Real Estate Agent', description='Helps clients buy, sell, or rent properties.', subject_group='Economics, Business Studies, Geography', strength='salesmanship', interest='real_estate', discipline=mgt),
    Career(name='Sociologist', description='Studies society, social behavior, and culture.', subject_group='Social Studies, Literature, Government', strength='observational', interest='culture', discipline=social),
    Career(name='Public Relations Officer', description='Manages communication between organizations and the public.', subject_group='English, Literature, Marketing', strength='communication', interest='marketing', discipline=social),
    Career(name='Chemist', description='Researches substances and chemical reactions.', subject_group='Chemistry, Physics, Biology', strength='precision', interest='laboratory', discipline=science),
    Career(name='Content Creator', description='Produces online content like videos, blogs, or posts.', subject_group='English, ICT, Arts', strength='storytelling', interest='film', discipline=arts),
    Career(name='Architect', description='Designs buildings and oversees construction.', subject_group='Technical Drawing, Physics, Mathematics', strength='visual', interest='engineering', discipline=science),
    Career(name='Counselor', description='Guides individuals through academic, career, or personal decisions.', subject_group='Psychology, Education, Social Studies', strength='empathy', interest='psychology', discipline=social),
    Career(name='Business Analyst', description='Evaluates business needs and recommends solutions.', subject_group='Business Studies, Economics, ICT', strength='planning', interest='business', discipline=mgt),
    Career(name='eCommerce Specialist', description='Manages online buying and selling platforms.', subject_group='Business Studies, ICT, Marketing', strength='organization', interest='ecommerce', discipline=mgt),
    # SCIENCE
    Career(
        name="Mechanical Engineer",
        description="Designs and develops machines, tools, and mechanical systems.",
        subject_group="Physics, Mathematics, Technical Drawing",
        strength="Problem-Solving",
        interest="Technology",
        discipline=science
    ),
    Career(
        name="Doctor",
        description="Diagnoses and treats illnesses and injuries in patients.",
        subject_group="Biology, Chemistry, Physics",
        strength="Compassion",
        interest="Health",
        discipline=science
    ),
    Career(
        name="Veterinarian",
        description="Provides medical care for animals.",
        subject_group="Biology, Chemistry, Agricultural Science",
        strength="Compassion",
        interest="Animals",
        discipline=science
    ),
    Career(
        name="Pharmacist",
        description="Dispenses medications and advises patients on their use.",
        subject_group="Chemistry, Biology, Mathematics",
        strength="Attention to Detail",
        interest="Health",
        discipline=science
    ),
    Career(
        name="Data Scientist",
        description="Analyzes and interprets complex data to help organizations make decisions.",
        subject_group="Mathematics, Computer Science, Statistics",
        strength="Analytical Thinking",
        interest="Technology",
        discipline=science
    ),

    # ART
    Career(
        name="Graphic Designer",
        description="Creates visual content for branding, advertising, and media.",
        subject_group="Fine Arts, ICT, English",
        strength="Creativity",
        interest="Design",
        discipline=arts
    ),
    Career(
        name="Fashion Designer",
        description="Designs clothing and accessories, keeping in mind trends and functionality.",
        subject_group="Home Economics, Fine Arts, English",
        strength="Creativity",
        interest="Fashion",
        discipline=arts
    ),
    Career(
        name="Journalist",
        description="Researches and writes news articles, reports, and interviews.",
        subject_group="English, Literature, Government",
        strength="Communication",
        interest="Media",
        discipline=arts
    ),
    Career(
        name="Animator",
        description="Creates animated visuals using 2D/3D tools for films, games, or ads.",
        subject_group="Fine Arts, ICT, Mathematics",
        strength="Creativity",
        interest="Multimedia",
        discipline=arts
    ),
    Career(
        name="Lawyer",
        description="Provides legal advice and represents clients in legal matters.",
        subject_group="Government, Literature, CRS/IRS",
        strength="Critical Thinking",
        interest="Debate",
        discipline=arts
    ),

    # COMMERCIAL
    Career(
        name="Accountant",
        description="Manages financial records and ensures compliance with regulations.",
        subject_group="Accounting, Economics, Commerce",
        strength="Detail-Oriented",
        interest="Finance",
        discipline=mgt
    ),
    Career(
        name="Banker",
        description="Handles financial transactions and offers financial services to clients.",
        subject_group="Economics, Commerce, Mathematics",
        strength="Trustworthiness",
        interest="Finance",
        discipline=mgt
    ),
    Career(
        name="Economist",
        description="Analyzes economic data and trends to influence policy or strategy.",
        subject_group="Economics, Mathematics, Government",
        strength="Analytical Thinking",
        interest="Policy",
        discipline=social
    ),
    Career(
        name="Business Analyst",
        description="Evaluates business processes and proposes improvements using data.",
        subject_group="Commerce, Mathematics, ICT",
        strength="Problem-Solving",
        interest="Business",
        discipline=mgt
    ),
    Career(
        name="Entrepreneur",
        description="Creates and runs businesses, taking on financial risks in the hope of profit.",
        subject_group="Commerce, Accounting, Economics",
        strength="Leadership",
        interest="Innovation",
        discipline=social
    ),


]

if not Career.objects.exists():
    Career.objects.bulk_create(careers)
