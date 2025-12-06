from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Habit, HabitLog

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description", "user__username")

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ("habit", "date", "status")
    list_filter = ("status", "date")
    search_fields = ("habit__name",)
