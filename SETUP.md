# Rephrase.AI - Complete Setup Guide

## ⚡ Quick Setup (5 Minutes)

### 1️⃣ Get OpenAI API Key
- Visit: https://platform.openai.com/api-keys
- Sign up/Login → Create new secret key
- Copy it (starts with `sk-`)

### 2️⃣ Install Python 3.11
**Important**: Must be Python 3.11 (not 3.9, 3.13)

Download from: https://www.python.org/downloads/release/python-3110/

Verify: `python --version` should show `3.11.x`

### 3️⃣ Backend Setup

```bash
cd backend
py -3.11 -m venv venv          # Create virtual environment
.\venv\Scripts\activate         # Windows
pip install -r requirements.txt # Install packages
```

**Create `.env` file:**
1. In the `backend` folder, create a new file named `.env`
2. Add the following content:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# CORS Settings
CORS_ORIGINS=http://localhost:3000
```

3. Replace `sk-your-actual-api-key-here` with your real OpenAI API key

### 4️⃣ Frontend Setup

```bash
cd frontend
npm install  # Takes 1-2 minutes
```

### 5️⃣ Run the App

**Terminal 1 (Backend):**
```bash
cd backend
.\venv\Scripts\activate
python app.py
```
✅ Backend running on http://localhost:5000

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```
✅ Frontend opens at http://localhost:3000

---

## 🎯 How to Use

1. **Switch Users**: Toggle between John Doe and Sarah Smith
2. **Type Message**: Start typing (3+ characters)
3. **See AI Suggestion**: Golden box appears after 0.2s pause
4. **Apply Suggestion**: Click "Use This →" or ignore and keep typing
5. **Send**: Press Enter to post message

**All messages are automatically saved to `backend/data/chat_history.json`**

---

## 🔧 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (must be 3.11)
- Activate venv: `.\venv\Scripts\activate`
- Verify .env file exists with valid API key

### Frontend errors
- Delete `node_modules` folder
- Run `npm install` again
- Make sure backend is running first

### "Module not found" errors
- Make sure venv is activated (you see `(venv)` in terminal)
- Run `pip install -r requirements.txt` again

### OpenAI errors
- Check API key in `.env` file
- Verify credits at: https://platform.openai.com/account/billing
- Make sure no spaces around `=` in `.env`

---

## 📁 Project Structure

```
daman/
├── backend/
│   ├── agents/              # AI agent logic
│   ├── data/                # Mock Jira/Calendar/Chat data
│   │   └── chat_history.json  # Saved messages
│   ├── utils/               # Helper functions
│   ├── app.py              # Flask server
│   ├── requirements.txt     # Python packages
│   └── .env                # API keys (YOU CREATE THIS)
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   └── ChatInterface.js  # Main chat UI
│   │   └── services/       # API calls
│   ├── package.json        # Node packages
│   └── public/
├── README.md               # Full documentation
├── QUICKSTART.md          # Quick reference
└── SETUP.md              # This file
```

---

## ✅ Verification Checklist

Before sharing this project, verify:

- [ ] Python 3.11 installed
- [ ] Node.js 16+ installed
- [ ] `backend/.env` file exists with valid `OPENAI_API_KEY`
- [ ] `backend/requirements.txt` present
- [ ] `frontend/package.json` present
- [ ] Both servers start without errors
- [ ] Chat interface loads at http://localhost:3000
- [ ] AI suggestions appear when typing
- [ ] Messages save to `backend/data/chat_history.json`

---

## 🎓 For New Users

**Give them:**
1. This entire `daman` folder
2. This SETUP.md file
3. Instructions to get their own OpenAI API key

**They need to:**
1. Install Python 3.11
2. Install Node.js 16+
3. Get OpenAI API key
4. Follow steps 3-5 above

**That's it!** The project is self-contained and ready to run.
