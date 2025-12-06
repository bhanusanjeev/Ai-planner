# planner/utils/ai_engine.py
from groq import Groq
from django.conf import settings
client = Groq(api_key=settings.GROQ_API_KEY)

def get_ai_suggestions(analytics: dict) -> str:
    """
    Call Groq and return AI suggestions in clean Markdown, 
    using the user's REAL analytics.
    """

    today_score = analytics.get("today_score", 0)
    weekly_avg = analytics.get("weekly_avg_score", 0)
    current_streak = analytics.get("current_streak", 0)
    best_streak = analytics.get("best_streak", 0)
    done_today = analytics.get("count_done_today", 0)
    missed_today = analytics.get("count_missed_today", 0)

    prompt = f"""
You are an expert habit & productivity coach.
You are helping a SINGLE user based on their analytics.

User analytics (numbers you MUST reference explicitly):
- Today's Score: {today_score}%
- Weekly Average Score: {weekly_avg}%
- Current Streak: {current_streak} days
- Best Streak: {best_streak} days
- Habits done today: {done_today}
- Habits missed today: {missed_today}

YOUR JOB:
1. First, write ONE short summary line that mentions
   at least 3 of these exact numbers (today, weekly, streak, done/missed).
2. Then write EXACTLY 5 bullet point suggestions in Markdown.

FORMATTING RULES (VERY IMPORTANT):
- Use this format ONLY:
  - ✅ **Title:** short explanation...
- Each suggestion must be on its own line starting with "- ".
- Add an emoji at the START of each bullet (like ✅, 🔥, 📊, ⏰, 🎯).
- Do NOT use the '•' character anywhere.
- Do NOT put all bullets in one long paragraph.
- NO code blocks, NO tables, just pure Markdown bullets.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a concise, structured coach for habit tracking dashboards."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
    )

    ai_text = response.choices[0].message.content

    # Safety: if the model still uses "•", normalize it to real Markdown bullets
    ai_text = ai_text.replace("•", "-")

    return ai_text





client = Groq(api_key=settings.GROQ_API_KEY)

def ask_ai_chatbot(user_message, context_block):
    model_name = "llama-3.1-8b-instant"   # ✔ Use active working model

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a habit improvement AI coach."},
            {"role": "system", "content": context_block},
            {"role": "user", "content": user_message},
        ]
    )

    return response.choices[0].message.content

