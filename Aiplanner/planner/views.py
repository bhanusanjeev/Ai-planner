from django.shortcuts import render

# Home Dashboard
def home(request):
    return render(request, "planner/home.html")

# Basic Pages
def about(request):
    return render(request, "planner/about.html")

def stats(request):
    return render(request, "planner/stats.html")

def profile(request):
    return render(request, "planner/profile.html")

# Habits Page (CRUD in future)
def habits(request):
    return render(request, "planner/habits.html")

# Daily Planner Page
def planner(request):
    return render(request, "planner/planner.html")

# AI Recommendations
def ai_recommendations(request):
    return render(request, "planner/ai.html")

# Streak Dashboard
def streaks(request):
    return render(request, "planner/streaks.html")

# Settings Page
def settings_page(request):
    return render(request, "planner/settings.html")

# Login Page
def login_page(request):
    return render(request, "planner/login.html")

# Register Page
def register_page(request):
    return render(request, "planner/register.html")

# AI Chat Assistant
def ai_chat(request):
    return render(request, "planner/ai-chat.html")
