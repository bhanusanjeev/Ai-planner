from django.utils import timezone
from datetime import timedelta
from planner.models import Habit, HabitLog

def get_streak_data(user):
    today = timezone.localdate()

    # All habits of user
    habits = Habit.objects.filter(user=user, is_active=True)

    # ---------- CURRENT STREAK ----------
    streak = 0
    check_day = today

    while True:
        logs = HabitLog.objects.filter(
            habit__in=habits,
            date=check_day,
            status="done"
        ).exists()

        if logs:
            streak += 1
            check_day -= timedelta(days=1)
        else:
            break

    # ---------- BEST STREAK ----------
    # Count all consecutive "done groups"
    best_streak = 0
    current = 0

    last_30_days = [today - timedelta(days=i) for i in range(30)]

    for date in last_30_days[::-1]:
        day_done = HabitLog.objects.filter(
            habit__in=habits, date=date, status="done"
        ).exists()

        if day_done:
            current += 1
            best_streak = max(best_streak, current)
        else:
            current = 0

    # ---------- TREND (last 7 days) ----------
    trend = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        day_logs = HabitLog.objects.filter(
            habit__in=habits, date=date, status="done"
        ).count()
        trend.append(day_logs)

    # ---------- COMPLETION BAR GRAPH ----------
    # Total habits per day
    total_habits = habits.count()

    completion_rate = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        done = HabitLog.objects.filter(
            habit__in=habits, date=date, status="done"
        ).count()

        percent = int((done / total_habits) * 100) if total_habits > 0 else 0
        completion_rate.append(percent)

    return {
        "current_streak": streak,
        "best_streak": best_streak,
        "trend": trend,
        "completion_rate": completion_rate
    }
