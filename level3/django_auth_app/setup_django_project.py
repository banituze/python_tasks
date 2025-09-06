#!/usr/bin/env python3
"""
Django Project Setup Script
Automatically creates and configures a Django web application with authentication.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error running command: {command}")
        print(f"Error output: {result.stderr}")
        sys.exit(1)
    return result

def create_file(path, content):
    """Create a file with given content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

def setup_django_project():
    """Set up the Django project with authentication"""
    
    print(" Setting up Django Authentication Project")
    print("=" * 50)
    
    # Check if Django is installed
    try:
        import django
        print(f" Django {django.VERSION} is installed")
    except ImportError:
        print(" Django is not installed. Installing...")
        run_command(f"{sys.executable} -m pip install django")
        run_command(f"{sys.executable} -m pip install django-crispy-forms")
        run_command(f"{sys.executable} -m pip install crispy-bootstrap5")
    
    # Create Django project
    if not os.path.exists('auth_project'):
        print("\n Creating Django project...")
        run_command("django-admin startproject auth_project .")
    else:
        print(" Django project already exists")
    
    # Create accounts app
    if not os.path.exists('accounts'):
        print("\n Creating accounts app...")
        run_command("python manage.py startapp accounts")
    else:
        print(" Accounts app already exists")
    
    # Create necessary directories
    os.makedirs('templates/accounts', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    
    print("\n Creating configuration files...")
    
    # Settings.py configuration
    settings_content = '''"""
Django settings for auth_project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'auth_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'auth_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login/Logout URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email Configuration (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production, use real email backend:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'
'''
    
    create_file('auth_project/settings.py', settings_content)
    
    # Main URLs configuration
    main_urls_content = '''"""
URL configuration for auth_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
'''
    
    create_file('auth_project/urls.py', main_urls_content)
    
    # Accounts URLs
    accounts_urls_content = '''"""
URL configuration for accounts app.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Password reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]
'''
    
    create_file('accounts/urls.py', accounts_urls_content)
    
    # Views
    views_content = '''"""
Views for accounts app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'accounts/profile.html', context)
'''
    
    create_file('accounts/views.py', views_content)
    
    # Forms
    forms_content = '''"""
Forms for accounts app.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """Extended user registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    """User profile update form"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
'''
    
    create_file('accounts/forms.py', forms_content)
    
    # Models
    models_content = '''"""
Models for accounts app.
"""
from django.db import models
from django.contrib.auth.models import User

# You can extend the User model with additional fields if needed
class Profile(models.Model):
    """User profile model for additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
'''
    
    create_file('accounts/models.py', models_content)
    
    # Admin configuration
    admin_content = '''"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
'''
    
    create_file('accounts/admin.py', admin_content)
    
    print("\n Creating templates...")
    
    # Base template
    base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django Auth App{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Django Auth</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'profile' %}">Profile</a>
                    <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                    <span class="navbar-text">Welcome, {{ user.username }}!</span>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">Login</a>
                    <a class="nav-link" href="{% url 'register' %}">Register</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}
        {% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
    
    create_file('templates/base.html', base_template)
    
    # Home template
    home_template = '''{% extends 'base.html' %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <h1>Welcome to Django Authentication App</h1>
        <p class="lead">This application demonstrates Django's built-in authentication system.</p>
        
        {% if user.is_authenticated %}
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Welcome back, {{ user.first_name|default:user.username }}!</h5>
                    <p class="card-text">You are successfully logged in.</p>
                    <a href="{% url 'profile' %}" class="btn btn-primary">View Profile</a>
                </div>
            </div>
        {% else %}
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Get Started</h5>
                    <p class="card-text">Create an account or log in to access all features.</p>
                    <a href="{% url 'register' %}" class="btn btn-primary">Register</a>
                    <a href="{% url 'login' %}" class="btn btn-outline-primary">Login</a>
                </div>
            </div>
        {% endif %}
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h6>Features</h6>
            </div>
            <div class="card-body">
                <ul class="list-unstyled">
                    <li> User Registration</li>
                    <li> User Login/Logout</li>
                    <li> Password Reset</li>
                    <li> Profile Management</li>
                    <li> Role-based Permissions</li>
                    <li> Secure Authentication</li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    create_file('templates/home.html', home_template)
    
    # Login template
    login_template = '''{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}Login - Django Auth App{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h4 class="mb-0">Login</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form|crispy }}
                    <button type="submit" class="btn btn-primary">Login</button>
                </form>
                <hr>
                <div class="text-center">
                    <small>
                        <a href="{% url 'password_reset' %}">Forgot password?</a>
                    </small>
                </div>
                <div class="text-center mt-2">
                    <small>
                        Don't have an account? <a href="{% url 'register' %}">Register here</a>
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    create_file('templates/accounts/login.html', login_template)
    
    # Register template
    register_template = '''{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}Register - Django Auth App{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h4 class="mb-0">Create Account</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form|crispy }}
                    <button type="submit" class="btn btn-primary">Register</button>
                </form>
                <hr>
                <div class="text-center">
                    <small>
                        Already have an account? <a href="{% url 'login' %}">Login here</a>
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    create_file('templates/accounts/register.html', register_template)
    
    # Profile template
    profile_template = '''{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}Profile - Django Auth App{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h4 class="mb-0">Update Profile</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form|crispy }}
                    <button type="submit" class="btn btn-primary">Update</button>
                </form>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h6>Account Information</h6>
            </div>
            <div class="card-body">
                <p><strong>Username:</strong> {{ user.username }}</p>
                <p><strong>Email:</strong> {{ user.email }}</p>
                <p><strong>Date Joined:</strong> {{ user.date_joined|date:"M d, Y" }}</p>
                <p><strong>Last Login:</strong> {{ user.last_login|date:"M d, Y H:i" }}</p>
                <p><strong>Staff Status:</strong> 
                    {% if user.is_staff %}
                        <span class="badge bg-success">Staff</span>
                    {% else %}
                        <span class="badge bg-secondary">Regular User</span>
                    {% endif %}
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    create_file('templates/accounts/profile.html', profile_template)
    
    # Password reset templates
    password_reset_template = '''{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}Password Reset - Django Auth App{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h4 class="mb-0">Password Reset</h4>
            </div>
            <div class="card-body">
                <p>Enter your email address and we'll send you a link to reset your password.</p>
                <form method="post">
                    {% csrf_token %}
                    {{ form|crispy }}
                    <button type="submit" class="btn btn-primary">Send Reset Email</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    create_file('templates/accounts/password_reset.html', password_reset_template)
    
    # CSS
    css_content = '''/* Custom styles for Django Auth App */

body {
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: bold;
}

.card {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border: none;
}

.card-header {
    background-color: #007bff;
    color: white;
    border-bottom: none;
}

.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
}

.btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}

.alert {
    border-radius: 0.5rem;
}

.list-unstyled li {
    padding: 0.25rem 0;
}

.navbar-text {
    margin-left: 1rem;
    color: #rgba(255,255,255,.5) !important;
}
'''
    
    create_file('static/css/style.css', css_content)
    
    print("\n Running database migrations...")
    run_command("python manage.py makemigrations", check=False)
    run_command("python manage.py migrate", check=False)
    
    print("\n Django Authentication Project Setup Complete!")
    print("\n Next steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the development server: python manage.py runserver")
    print("3. Visit http://127.0.0.1:8000/ to see your app")
    print("4. Visit http://127.0.0.1:8000/admin/ for admin panel")
    
    print("\n Optional: Configure email settings in settings.py for password reset")

if __name__ == "__main__":
    setup_django_project()


