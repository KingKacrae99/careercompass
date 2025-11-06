"""
URL configuration for careercompass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import home_View, login_view, logout_view, sigup_view, assessment_view, UserDashboardView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_View, name="home"),
    path('careercompass/login', login_view, name="Login"),
    path('careercompass/logout', logout_view, name="Logout"),
    path('careercompass/signup', sigup_view, name="signup"),
    path('careercompass/assessment', assessment_view, name="assessment"),
    path('careercompass/user-dashboard', UserDashboardView, name="userdashboard" )
]
print(f'path func: {path}')
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
