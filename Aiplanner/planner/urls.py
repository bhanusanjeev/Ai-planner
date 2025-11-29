# dashboard/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    # Basic Pages
    path("about/", views.about, name="about"),
    path("stats/", views.stats, name="stats"),
    path("profile/", views.profile, name="profile"),

    # Additional Pages
    path("habits/", views.habits, name="habits"),
    path("planner/", views.planner, name="planner"),
    path("ai-suggestions/", views.ai_recommendations, name="ai_suggestions"),
    path("streaks/", views.streaks, name="streaks"),
    path("settings/", views.settings_page, name="settings"),

    # Auth Pages
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),

    # AI Chat Page
    path("ai-chat/", views.ai_chat, name="ai_chat"),
]

