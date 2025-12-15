from django.urls import path
from . import views
from .views import logout_user
from .views import home

urlpatterns = [
    path("", home, name="home"),
]


urlpatterns = [

    # ----- AUTH -----
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", logout_user, name="logout"),

    # ----- HOME -----
    path("", views.home, name="home"),

    # ----- HABITS -----
    path("habits/", views.habits, name="habits"),
    path("habits/<int:habit_id>/toggle/", views.toggle_habit_today, name="toggle_habit_today"),
    path("habit/delete/<int:habit_id>/", views.delete_habit, name="delete_habit"),

    # ----- ANALYTICS -----
    path("stats/", views.stats, name="stats"),
    path("streaks/", views.streaks, name="streaks"),

    # ----- AI -----
    path("ai-suggestions/", views.ai_recommendations, name="ai_suggestions"),
    path("ai-chat/", views.ai_chat, name="ai_chat"),

    # ----- BASIC PAGES -----
    path("about/", views.about, name="about"),
    path("planner/", views.planner, name="planner"),
    path("profile/", views.profile, name="profile"),

    # ----- SETTINGS -----
    path("settings/", views.settings_page, name="settings"),
    path("change-password/", views.change_password, name="change_password"),

    # ----- DELETE ACCOUNT -----
    path("delete-account/", views.delete_account, name="delete_account"),
    path("delete-account/confirm/", views.confirm_delete_account, name="confirm_delete_account"),
]
