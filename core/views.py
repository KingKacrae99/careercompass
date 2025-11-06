from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .form import CustomUserForm, AssessmentForm,LoginForm
#from .career import careers
# Create your views here.

def home_View(request):
    """
    existing_names = set(Career.objects.values_list('name', flat=True))

    new_careers = [
        Career(name=c.name, description=c.description, subject_group=c.subject_group,
            strength=c.strength, interest=c.interest, discipline=c.discipline)
        for c in careers if c.name not in existing_names
    ]

    Career.objects.bulk_create(new_careers)
    """
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

