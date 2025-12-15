from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Habit, HabitLog
from django.contrib.auth.decorators import login_required
from .models import UserSettings
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .utils.analytics import calculate_user_stats 
from .models import Habit, HabitLog
from .utils.streaks import get_streak_data
import json
import requests
from .utils.analytics import calculate_user_stats
from .utils.streaks import get_streak_data
from django.contrib.auth.decorators import login_required
from .utils.ai_engine import get_ai_suggestions
import markdown
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils.analytics import calculate_user_stats
from .models import Habit, HabitLog
from .utils.ai_engine import ask_ai_chatbot 
from django.http import HttpResponse

def home(request):
    return HttpResponse("AI Planner is Live 🚀")


@login_required(login_url="login")
def stats(request):
    user = request.user
    today = timezone.localdate()

    # All active habits for this user
    habits = Habit.objects.filter(user=user, is_active=True)
    total_habits = habits.count()

    # ---------- LAST 7 DAYS COMPLETION ----------
    last_7_days = []
    for i in range(6, -1, -1):        # 6 .. 0  (oldest -> today)
        day = today - timedelta(days=i)

        done_count = HabitLog.objects.filter(
            habit__in=habits,
            date=day,
            status="done",
        ).count()

        pct = int(round(done_count * 100 / total_habits)) if total_habits else 0

        last_7_days.append({
            "label": day.strftime("%a"),   # Mon, Tue...
            "pct": pct,
        })

    today_score = last_7_days[-1]["pct"] if last_7_days else 0
    weekly_avg_score = (
        int(round(sum(d["pct"] for d in last_7_days) / len(last_7_days)))
        if last_7_days else 0
    )

    # ---------- BEST STREAK (over full history) ----------
    logs_by_day = HabitLog.objects.filter(
        habit__in=habits,
        status="done",
    ).values("date").annotate(done_count=Count("id"))

    done_dates = {row["date"] for row in logs_by_day}

    best_streak = 0
    current_streak = 0

    if done_dates:
        current_date = min(done_dates)
        last_date = max(done_dates)

        while current_date <= last_date:
            if current_date in done_dates:
                current_streak += 1
                best_streak = max(best_streak, current_streak)
            else:
                current_streak = 0
            current_date += timedelta(days=1)

    # ---------- COMPLETED HABITS BY “CATEGORY” ----------
    # If you later add a Habit.category field, you can compute real buckets.
    # For now we just use total done counts and fake 4 segments evenly.
    total_done = HabitLog.objects.filter(
        habit__in=habits,
        status="done",
    ).count()

    # Split into 4 buckets so bars don’t look empty
    morning = int(total_done * 0.30)
    work = int(total_done * 0.25)
    health = int(total_done * 0.25)
    evening = total_done - (morning + work + health)

    raw_bars = [
        ("Morning", morning),
        ("Work", work),
        ("Health", health),
        ("Evening", evening),
    ]

    max_count = max((c for _, c in raw_bars), default=0)
    category_bars = []
    for label, count in raw_bars:
        height = 20 if max_count == 0 else int(20 + 60 * count / max_count)
        category_bars.append({
            "label": label,
            "height": height,
            "count": count,
        })

    # ---------- HABIT TREND BARS (heights for last 7 days) ----------
    trend_bars = []
    for d in last_7_days:
        height = 10 if d["pct"] == 0 else int(15 + 65 * d["pct"] / 100)
        trend_bars.append({
            "label": d["label"],
            "height": height,
            "pct": d["pct"],
        })

    context = {
        "today_score": today_score,
        "weekly_avg_score": weekly_avg_score,
        "best_streak": best_streak,
        "category_bars": category_bars,
        "trend_bars": trend_bars,
    }
    return render(request, "planner/stats.html", context)

@login_required
def delete_account(request):
    return render(request, "planner/delete_account.html")
@login_required
def confirm_delete_account(request):

    if request.method != "POST":
        return redirect("delete_account")  # prevent accidental delete on GET

    user = request.user  # store user BEFORE logout

    # Delete user’s habits & logs
    Habit.objects.filter(user=user).delete()
    HabitLog.objects.filter(habit__user=user).delete()

    # Delete actual user
    user.delete()

    # Logout AFTER deleting user (but safely)
    logout(request)

    messages.success(request, "Your account has been deleted.")
    return redirect("home")


@login_required
def change_password(request):

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check old password
        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect!")
            return redirect("change_password")

        # Check confirm
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match!")
            return redirect("change_password")

        # Save new password
        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)  # Keep user logged in

        messages.success(request, "Password changed successfully!")
        return redirect("profile")

    return render(request, "planner/change_password.html")

@login_required
def settings_page(request):

    # Ensure settings object exists
    settings_obj, created = UserSettings.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Notifications
        settings_obj.daily_reminders = bool(request.POST.get("daily_reminders"))
        settings_obj.ai_suggestions = bool(request.POST.get("ai_suggestions"))
        settings_obj.weekly_summary = bool(request.POST.get("weekly_summary"))

        # AI & Habit preferences
        settings_obj.smart_tracking = bool(request.POST.get("smart_tracking"))
        settings_obj.ai_tips = bool(request.POST.get("ai_tips"))

        settings_obj.save()

        messages.success(request, "Settings updated successfully!")
        return redirect("settings")

    return render(request, "planner/settings.html", {"settings": settings_obj})


# ----------------------------------------------------
# HABITS
# ----------------------------------------------------
def habits(request):
    # Block access if not logged in
    if not request.user.is_authenticated:
        return redirect("login")

    today = timezone.localdate()
    habits_qs = Habit.objects.filter(user=request.user, is_active=True)

    # CREATE NEW HABIT
    if request.method == "POST" and "habit_name" in request.POST:
        name = request.POST.get("habit_name", "").strip()
        desc = request.POST.get("habit_description", "").strip()
        category = request.POST.get("category", "morning")  # NEW

        if name:
            Habit.objects.create(
                user=request.user,
                name=name,
                description=desc,
                category=category
            )
        return redirect("habits")

    # BUILD CONTEXT
    habits_data = []
    for h in habits_qs:
        log = HabitLog.objects.filter(habit=h, date=today).first()
        done_today = log.status == "done" if log else False

        habits_data.append({
            "habit": h,
            "done_today": done_today
        })

    return render(request, "planner/habits.html", {"habit_data": habits_data})




def delete_habit(request, habit_id):
    if not request.user.is_authenticated:
        return redirect("login")
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    habit.delete()
    return redirect("habits")



def toggle_habit_today(request, habit_id):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method != "POST":
        return redirect("habits")

    today = timezone.localdate()
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)

    log, created = HabitLog.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={"status": "done"},
    )

    if not created:
        log.status = "missed" if log.status == "done" else "done"
        log.save()

    return redirect("habits")



# ----------------------------------------------------
# HOME
# ----------------------------------------------------
def home(request):
    # Logged out → Landing page
    if not request.user.is_authenticated:
        return render(request, "planner/landing.html")

    today = timezone.localdate()

    # Active habits for this user
    habits = Habit.objects.filter(user=request.user, is_active=True)

    habit_data = []
    for h in habits:
        log = HabitLog.objects.filter(habit=h, date=today).first()
        done_today = log.status == "done" if log else False

        habit_data.append(
            {
                "habit": h,
                "done_today": done_today,
            }
        )

    # 🧠 Live analytics
    stats = calculate_user_stats(request.user)

    return render(
        request,
        "planner/home.html",
        {
            "habit_data": habit_data,
            "stats": stats,
        },
    )

# ----------------------------------------------------
# AUTH
# ----------------------------------------------------
def register_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Email check
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
        )

        login(request, user)
        return redirect("home")

    return render(request, "planner/register.html")


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

    # IMPORTANT: return the login page for GET
    return render(request, "planner/login.html")




def logout_user(request):
    logout(request)
    return redirect("login")

def profile(request):

    habits = Habit.objects.filter(user=request.user, is_active=True)

    total_habits = habits.count()

    today = timezone.localdate()
    completed_today = HabitLog.objects.filter(
        habit__in=habits,
        date=today,
        status="done"
    ).count()

    active_habits = habits.filter(is_active=True).count()

    context = {
        "total_habits": total_habits,
        "completed_today": completed_today,
        "active_habits": active_habits,
    }

    return render(request, "planner/profile.html", context)
@login_required
def streaks(request):
    if not request.user.is_authenticated:
        return redirect("login")

    data = get_streak_data(request.user)

    return render(request, "planner/streaks.html", {
        "streak": data["current_streak"],
        "best_streak": data["best_streak"],
        "trend": data["trend"],
        "completion": data["completion_rate"]
    })

@login_required
def ai_recommendations(request):
    if not request.user.is_authenticated:
        return redirect("login")

    stats = calculate_user_stats(request.user)

    # Get Markdown output from AI
    ai_markdown = get_ai_suggestions(stats)

    # Convert to HTML
    ai_html = markdown.markdown(ai_markdown)

    return render(request, "planner/ai_suggestions.html", {
        "stats": stats,
        "ai_html": ai_html
    })
@login_required
def ai_chat(request):

    # Initialize chat history inside session
    if "chat_history" not in request.session:
        request.session["chat_history"] = []  

    # ---------- GET Request ----------
    if request.method == "GET":
        return render(request, "planner/ai_chat.html", {
            "history": request.session["chat_history"]
        })

    # ---------- POST MESSAGE ----------
    user_message = request.POST.get("message", "").strip()

    if not user_message:
        return render(request, "planner/ai_chat.html", {
            "history": request.session["chat_history"],
            "error": "Message cannot be empty!"
        })

    # Collect analytics context (same logic you have)
    stats = calculate_user_stats(request.user)

    today_score = stats.get("today_score", 0)
    weekly_score = stats.get("weekly_avg_score", 0)
    current_streak = stats.get("current_streak", 0)
    best_streak = stats.get("best_streak", 0)

    habits = Habit.objects.filter(user=request.user)
    logs = HabitLog.objects.filter(habit__user=request.user).order_by("-date")[:14]

    # Build context block
    context_block = f"""
Your Habit Analytics Summary:
- Today Score: {today_score}%
- Weekly Average: {weekly_score}%
- Current Streak: {current_streak}
- Best Streak: {best_streak}

Habits:
"""
    for h in habits:
        context_block += f"- {h.name}\n"

    context_block += "\nRecent Logs:\n"
    for log in logs:
        context_block += f"- {log.habit.name}: {log.date} → {log.status}\n"

    # Ask AI
    ai_response = ask_ai_chatbot(user_message, context_block)

    # Update chat session history
    history = request.session["chat_history"]
    history.append({"sender": "user", "text": user_message})
    history.append({"sender": "ai", "text": ai_response})
    request.session["chat_history"] = history  # save session

    return render(request, "planner/ai_chat.html", {
        "history": history
    })


# ----------------------------------------------------
# STATIC PAGES
# ----------------------------------------------------
def about(request):
    return render(request, "planner/about.html")


def planner(request):
    return render(request, "planner/planner.html")
