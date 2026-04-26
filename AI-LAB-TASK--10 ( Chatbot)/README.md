# 🎓 Greenfield University — AdmissionBot

A Flask-based University Admission Chatbot powered by the **Groq API** — **100% FREE**, no credit card required.

---

## Why Groq API? ✅ Truly Free!

| Feature | Detail |
|---|---|
| 💰 Cost | **Completely FREE** (generous daily limits) |
| 💳 Credit Card | **Not required** |
| ⚡ Speed | Fastest AI inference available |
| 🔑 Sign Up | Takes ~1 minute |
| 🔗 Link | https://console.groq.com |

---

## Project Structure

```
uni_chatbot/
├── app.py               ← Flask backend (Groq API)
├── requirements.txt     ← Python dependencies
├── README.md
└── templates/
    └── index.html       ← Frontend UI
```

---

## Setup Instructions

### Step 1: Get Your FREE Groq API Key (1 minute)
1. Go to 👉 **https://console.groq.com**
2. Click **Sign Up** (Google/GitHub login supported)
3. Go to **API Keys** → **Create API Key**
4. Copy your key — it starts with `gsk_...`

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Your API Key

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=gsk_your_key_here
```

**Mac / Linux:**
```bash
export GROQ_API_KEY=gsk_your_key_here
```

**Or paste directly in `app.py`** (line 12) for quick testing:
```python
client = Groq(api_key="gsk_your_key_here")
```

### Step 4: Run the App
```bash
python app.py
```

### Step 5: Open in Browser
👉 http://localhost:5000

---

## Features

- 💬 Conversational AI via **Groq + LLaMA 3** (free & fast)
- 🎓 Expert knowledge of Greenfield University admissions
- 📋 8 quick-topic sidebar buttons
- 🌗 Dark gold-and-navy academic theme
- 📱 Responsive — works on mobile
- 🔄 Conversation history + reset button
- ⌨️ Enter to send, Shift+Enter for newline

## Topics the Bot Knows

| Topic | Details |
|-------|---------|
| Admission Requirements | GPA, SAT/ACT, essays, letters |
| Application Deadlines | Fall, Spring, Rolling admissions |
| Programs | Engineering, Business, Arts, Law, Medical |
| Tuition | Domestic & International rates |
| Financial Aid | Scholarships, FAFSA, grants |
| International Students | F-1 visa, IELTS/TOEFL |
| Transfer Students | Requirements, deadlines |
| Campus Life | Housing, dining, clubs, sports |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python Flask |
| AI Engine | Groq API (LLaMA 3 8B) — **Free** |
| Frontend | HTML5, CSS3, Vanilla JS |
| Fonts | Playfair Display + DM Sans |
