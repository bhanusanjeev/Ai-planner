from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    CATEGORY_CHOICES = (
        ("morning", "Morning"),
        ("afternoon", "Afternoon"),
        ("evening", "Evening"),
        ("night", "Night"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="morning")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HabitLog(models.Model):
    STATUS_CHOICES = (
        ("done", "Done"),
        ("missed", "Missed"),
    )

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="done")
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("habit", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.habit.name} - {self.date} - {self.status}"


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Notification settings
    daily_reminders = models.BooleanField(default=True)
    ai_suggestions = models.BooleanField(default=True)
    weekly_summary = models.BooleanField(default=False)

    # Advanced preferences
    smart_tracking = models.BooleanField(default=False)
    ai_tips = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Settings"
