🚀 AI Habit Tracker — Ultimate README

A modern, AI-powered habit tracking system built with Django + Groq LLaMA AI, offering streak tracking, analytics, personalized suggestions, and a smart AI chat coach.

Beautiful UI. Fully responsive. Fast AI responses.
Made with consistency, discipline, and pure fire. 🔥

🌟 Table of Contents

Overview

Purpose

Features

Architecture

Database Schema

Setup & Installation

Environment Variables

Running Locally

AI Engine (Groq + LLaMA)

API Endpoints

Frontend / UI

Deployment Guide

Troubleshooting

Contributing

Author

🧠 Overview

AI Habit Tracker is a productivity platform that blends habit tracking, data analytics, and AI coaching into one powerful tool.

It doesn’t just track habits;
it explains your patterns, analyzes your weaknesses, and guides improvement using AI.

This project features:

Daily / weekly scores

Streaks + habit analytics

AI suggestions

AI chat coach that understands your progress

Mobile responsive dashboard

🎯 Purpose

The main purpose is to help users:

Build and maintain habits

Understand why they miss habits

Get personalized improvement strategies

Stay accountable with streaks and analytics

Get motivation from an AI coach

This is not “just another habit tracker”…
This one thinks.

✨ Features
🧩 Habit Management

Add habits

Toggle daily completion

Delete habits

Automatic streak calculation

📊 Analytics Dashboard

Today score

Weekly average

Streak count

Best streak

Simple, clear visual UI

🤖 AI Features
AI Suggestions

Explains your performance

Gives improvements

Adds emojis + bullet formatting

Uses live analytics

AI Chat Coach

Full conversation memory

Reads habit history + logs

Generates coaching advice

Fast responses via Groq LLaMA

Shows typing animation (optional UI)

🎨 UI Highlights

Neon gradient glass theme

Fully responsive (mobile + desktop)

Sidebar + topbar layout

Beautiful cards and animations

🏗️ Architecture
project/
│
├── planner/
│   ├── views.py
│   ├── models.py
│   ├── utils/
│   │    ├── stats.py          # analytics calculation
│   │    └── ai_engine.py      # Groq API integration
│   ├── templates/
│   └── static/
│
└── Aiplanner/settings.py

🗄️ Database Schema
Habit Model
Field	Type	Description
id	Integer	Primary Key
user	FK(User)	Owner
name	String	Habit title
created_at	DateTime	Timestamp
HabitLog Model
Field	Type	Description
id	Integer	Primary Key
habit	FK(Habit)	Habit reference
date	Date	Log date
status	String	Done / Not Done
Relationship Diagram
User ───< Habit ───< HabitLog

Analytics (Computed)

today_score

weekly_avg_score

current_streak

best_streak

🛠️ Setup & Installation
1️⃣ Clone the Repo
git clone https://github.com/your-username/ai-habit-tracker.git
cd ai-habit-tracker

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Create .env file
GROQ_API_KEY=your-api-key-here
SECRET_KEY=your-django-secret
DEBUG=True

5️⃣ Apply Migrations
python manage.py migrate

6️⃣ Run the Server
python manage.py runserver


Visit →
http://127.0.0.1:8000/

🔑 Environment Variables

Your .env must contain:

GROQ_API_KEY=
SECRET_KEY=
DEBUG=


In settings.py:

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

▶️ Running Locally

Start server:

python manage.py runserver


AI Chat test route:

/ai-chat/


AI Suggestions:

/ai_suggestions/

🤖 AI Engine

AI powered by Groq LLaMA3 (llama3-8b-8192).

How It Works

System collects:

streaks

scores

weekly average

logs

Builds context block

Sends to Groq ChatCompletion

AI returns structured coaching

Chat history stored in session

AI Context Example
User Stats:
Today Score: 60%
Weekly Avg: 54%
Streak: 4 days

Recent Logs:
- Reading: Done
- Workout: Not Done

🌐 API Endpoints
Habit Endpoints
Method	Endpoint	Description
GET	/habits/	List habits
POST	/habits/	Add habit
GET	/delete_habit/<id>/	Delete habit
POST	/toggle_habit_today/<id>/	Toggle status
AI Endpoints
Method	Endpoint	Description
GET	/ai_suggestions/	AI summary
POST	/ai-chat/	AI conversation
🎨 Frontend / UI

Built using Django Templates + Custom CSS.

Includes:

Sidebar navigation

Topbar with profile

Beautiful glassmorphism cards

Neon gradients

Smooth animations

Fully redesigned responsive UI

Chat UI features:

Bubble layout

Auto scroll

Smooth transitions

🚀 Deployment Guide
Deploy on ⭐ Render
Steps:
1. Push repo → GitHub
2. Create Render Web Service
3. Add environment variables:
GROQ_API_KEY
SECRET_KEY
DEBUG=False

4. Build command:
pip install -r requirements.txt

5. Start command:
gunicorn Aiplanner.wsgi

6. Collect static:
python manage.py collectstatic

🛠️ Troubleshooting
❌ AI not responding

Wrong or missing API key

Restart server

Check Groq model name

❌ CSS not loading

Browser cache

Static files missing

Wrong STATIC_URL

❌ Chat errors

Missing session

Incorrect context keys

🤝 Contributing

Fork repo

Create feature branch

Write clean commits

Open pull request

Coding rules:

Follow PEP8

Use utility modules

Keep prompts clean

Comment AI logic

👤 Author
Built by: Bhanu Sanjeev

A project born from discipline, growth, and passion.
Designed, coded, and perfected with dedication.

Special Thanks

ChatGPT — AI coding partner throughout the build.
