# planner/utils/analytics.py

from datetime import timedelta
from django.utils import timezone

from planner.models import Habit, HabitLog


def calculate_user_stats(user):
    """
    Compute analytics for a given user using ONLY:
    - Habit (user, is_active)
    - HabitLog (habit, date, status)

    Returns a dict usable in templates.
    """

    today = timezone.localdate()

    # All active habits for this user
    habits_qs = Habit.objects.filter(user=user, is_active=True)
    total_habits = habits_qs.count()

    # ---------- 1. TODAY COMPLETION ----------
    done_today = (
        HabitLog.objects.filter(
            habit__user=user,
            date=today,
            status="done",
        )
        .values("habit")
        .distinct()
        .count()
    )

    if total_habits > 0:
        today_score = round(done_today / total_habits * 100)
    else:
        today_score = 0

    # ---------- 2. 7-DAY TREND + WEEKLY SCORE ----------
    trend = []
    weekly_sum = 0
    weekly_days_with_habits = 0

    for i in range(6, -1, -1):  # 6 days ago → today
        day = today - timedelta(days=i)
        done_count = (
            HabitLog.objects.filter(
                habit__user=user,
                date=day,
                status="done",
            )
            .values("habit")
            .distinct()
            .count()
        )

        if total_habits > 0:
            percent = round(done_count / total_habits * 100)
        else:
            percent = 0

        trend.append(
            {
                "date": day,
                "label": day.strftime("%a"),  # Mon, Tue...
                "percent": percent,
            }
        )

        if total_habits > 0:
            weekly_sum += percent
            weekly_days_with_habits += 1

    weekly_score = (
        round(weekly_sum / weekly_days_with_habits)
        if weekly_days_with_habits > 0
        else 0
    )

    # ---------- 3. CURRENT STREAK & BEST STREAK ----------
    def day_fully_completed(day):
        """
        A 'perfect' day = all active habits were done.
        """
        if total_habits == 0:
            return False

        done_cnt = (
            HabitLog.objects.filter(
                habit__user=user,
                date=day,
                status="done",
            )
            .values("habit")
            .distinct()
            .count()
        )
        return done_cnt == total_habits

    # current streak: go backwards from today
    current_streak = 0
    ptr_day = today
    while day_fully_completed(ptr_day):
        current_streak += 1
        ptr_day = ptr_day - timedelta(days=1)

    # best streak in last 60 days
    best_streak = 0
    streak = 0
    for i in range(0, 60):
        day = today - timedelta(days=i)
        if day_fully_completed(day):
            streak += 1
            best_streak = max(best_streak, streak)
        else:
            streak = 0

    # ---------- 4. HABIT LEADERBOARD (last 14 days) ----------
    leaderboard = []
    window_start = today - timedelta(days=13)  # 14-day window

    for habit in habits_qs:
        logs = HabitLog.objects.filter(
            habit=habit,
            date__gte=window_start,
            date__lte=today,
        )
        if not logs.exists():
            continue

        done_days = (
            logs.filter(status="done").values("date").distinct().count()
        )
        total_window_days = 14
        percent = round(done_days / total_window_days * 100)

        leaderboard.append(
            {
                "habit": habit,
                "percent": percent,
                "done_days": done_days,
            }
        )

    leaderboard = sorted(
        leaderboard,
        key=lambda x: x["percent"],
        reverse=True,
    )[:5]  # top 5

    # ---------- 5. LOG VOLUME (7 days) ----------
    volume = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count_logs = HabitLog.objects.filter(
            habit__user=user,
            date=day,
        ).count()

        volume.append(
            {
                "label": day.strftime("%a"),
                "count": count_logs,
            }
        )

    return {
        "today_score": today_score,
        "weekly_score": weekly_score,
        "current_streak": current_streak,
        "best_streak": best_streak,
        "total_habits": total_habits,
        "done_today": done_today,
        "trend": trend,                  # 7-day completion %
        "habit_leaderboard": leaderboard, # top habits last 14 days
        "volume": volume,                # raw logs per day
    }
