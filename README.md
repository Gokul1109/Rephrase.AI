# Rephrase.AI - Workplace Communication Assistant

An AI-powered assistant designed to improve workplace communication in real-time by addressing clarity, tone, and context in remote work environments.

## 🎯 Problem Statement

Remote work communication faces several challenges:

- 97% of workers over-explain messages to clarify tone
- Virtual messages miss emotion and nonverbal cues
- Cultural gaps lead to misinterpretation
- Poor communication erodes trust and productivity

## 🚀 Solution

Rephrase.AI provides real-time AI-powered message enhancement through:

- **Intent & Emotion Analysis**: Detects tone from chat history
- **Clarity Enhancement**: Makes vague messages clear
- **Jira Context Integration**: Adds project context from tasks
- **Calendar Awareness**: Respects meeting schedules
- **Combined Intelligent Rewriting**: Merges all context for optimal suggestions

## 🏗️ Architecture

### Backend (Python + LangChain/LangGraph)

- Multi-agent AI system for context-aware rephrasing
- REST API endpoints
- Mock data integration (Jira, Calendar)

### Frontend (React + Node.js)

- Real-time message input
- Instant AI suggestions
- Clean, intuitive UI

## 📋 Prerequisites

- **Python 3.11** (Important: 3.13 has compatibility issues, 3.11 recommended)
- Node.js 16+
- OpenAI API key (or other LLM provider)

## � Quick Start Guide

### Step 1: Get Your OpenAI API Key 🔑

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-...`)
5. Keep it safe!

> **💡 Tip:** New OpenAI accounts get free trial credits ($5). Check your balance at [platform.openai.com/account/billing](https://platform.openai.com/account/billing)

### Step 2: Setup Backend (Python) 🐍

Open PowerShell or Command Prompt:

```powershell
# Navigate to backend
cd backend

# Create virtual environment with Python 3.11
# If you have multiple Python versions:
py -3.11 -m venv venv
# Or if Python 3.11 is your default:
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# You should see (venv) in your terminal now

# Install dependencies
pip install -r requirements.txt
```

> **⚠️ Important**: Use Python 3.11, not 3.13. Python 3.13 has compatibility issues with pydantic-core and tiktoken packages.

### Step 3: Add Your OpenAI API Key ⚙️

**IMPORTANT: This is where you add your API key!**

1. In the `backend` folder, create a new file named `.env`
2. Open it with Notepad or any text editor
3. Copy and paste this content:

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

### Step 4: Start Backend Server 🚀

In the same PowerShell (with venv activated):

```powershell
python app.py
```

**You should see:**

```
🚀 Rephrase.AI Backend starting on port 5000...
📝 API Documentation: http://localhost:5000/api/health

 * Running on http://127.0.0.1:5000
```

✅ **Backend is running!** Leave this terminal open.

### Step 5: Setup Frontend (React) ⚛️

Open a **NEW PowerShell window**:

```powershell
# Navigate to frontend
cd C:\Users\tejas\Desktop\daman\frontend

# Install dependencies (takes 1-2 minutes)
npm install

# Start the app
npm start
```

**Browser will auto-open to:** `http://localhost:3000`

✅ **Done! You're all set!**

### Step 6: Try It Out 🎉

The application features a **dual-person chat interface** with real-time AI suggestions:

1. **Switch between users**: Toggle between "John Doe" and "Sarah Smith" using the user switcher
2. **Type a message**: Start typing in the chat input (e.g., "Update?")
3. **Get AI suggestions**: After typing 3+ characters and pausing for 0.2 seconds, a **golden suggestion box** appears on the right
4. **Use suggestions**: Click "Use This →" to replace your message with the AI-enhanced version
5. **Send messages**: Press Enter or click Send to post the message to chat
6. **View history**: All messages are automatically saved to `backend/data/chat_history.json`

**Features:**
- Real-time suggestions while typing (no button click needed!)
- Context-aware based on chat history
- Jira task integration (shows deadlines, priorities)
- Calendar awareness (suggests meeting times)
- Message persistence (stored in JSON)

## 🧪 Quick Tests

**Test if backend is working:**

```powershell
curl http://localhost:5000/api/health
```

Should return: `{"status":"healthy"...}`

**Test if frontend is working:**
Open browser to: `http://localhost:3000`

## 📝 Example Messages to Try

| Type This          | AI Transforms To                                                                     |
| ------------------ | ------------------------------------------------------------------------------------ |
| `Update?`          | "Just checking in—do you have any updates when you get a moment?"                    |
| `Do this now`      | "Please prioritize this task"                                                        |
| `Need this today`  | "Could you please prioritize this task today? It's due by 5PM in Jira."              |
| `Can we talk now?` | "Noticed you're in meetings—can we connect after 3 PM when you're free?"             |
| `Fix this`         | "Could you take a look at this when you get a chance? Let me know if you need help." |

## ⚠️ Common Issues & Solutions

### ❌ "No module named 'flask'" or similar errors

**Fix:** Virtual environment not activated or packages not installed

```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

### ❌ "OpenAI API key not found" or "Incorrect API key"

**Fix:** Check your `.env` file

1. File must be named `.env` (not `.env.example`)
2. Must be in `backend` folder
3. Key must start with `sk-`
4. No spaces: `OPENAI_API_KEY=sk-your-key`
5. Restart backend after fixing

### ❌ Frontend shows "Failed to fetch" or CORS errors

**Fix:** Backend not running

1. Check if backend terminal is still running
2. Visit `http://localhost:5000/api/health` to verify
3. Restart backend if needed

### ❌ "Port 5000 is already in use"

**Fix:** Another app is using port 5000

```powershell
# Option 1: Kill the process
netstat -ano | findstr :5000
# Note the PID, then: taskkill /PID <number> /F

# Option 2: Change port in backend\.env
PORT=5001
```

### ❌ AI responses are slow (>10 seconds)

**Fix:** Use faster model

### Chat Interface

The application provides a modern chat interface where two users (John Doe and Sarah Smith) can communicate:

1. **Open**: `http://localhost:3000` in your browser
2. **Select User**: Click the user toggle to switch between John and Sarah
3. **Type Message**: Start typing in the input field (minimum 3 characters)
4. **See Suggestions**: After a brief pause (0.2s), AI suggestions appear in the golden box
5. **Apply or Ignore**: Click "Use This →" to use the suggestion, or keep typing to ignore it
6. **Send**: Press Enter or click Send button to post the message

### AI Enhancement Features

Get real-time AI suggestions for:
- **Tone improvement**: Converts casual → professional or urgent → polite
- **Clarity enhancement**: Makes vague messages specific and actionable
- **Context-aware rewrites**: Includes Jira task deadlines and calendar availability
- **Message persistence**: All sent messages are saved to `backend/data/chat_history.json`

- Check: [platform.openai.com/account/billing](https://platform.openai.com/account/billing)
- Add payment method or wait for quota reset

## 🎮 Usage

1. Open `http://localhost:3000` in your browser
2. Type a message in the input field
3. Get real-time AI suggestions for:
   - Tone improvement
   - Clarity enhancement
   - Context-aware rewrites based on Jira tasks and calendar

## 🤖 AI Agents

### 1. Intent & Emotion Agent

- Analyzes chat history for emotional context
- Detects tone (urgent, casual, formal)
- Example: "Update?" → "Just checking in—do you have any updates when you get a moment?"

### 2. Clarity Agent

- Identifies vague or unclear messages
- Suggests specific, actionable language
- Example: "Pointer mismatch maybe copying wrong" → "I suspect a pointer mismatch might be causing the copy issue."

### 3. Jira Agent

- Reads mock Jira task data
- Adds project context and deadlines
- Example: "Need this today" → "Could you please prioritize this task today? It's due by 5PM in Jira."

### 4. Calendar Agent

- Checks mock calendar availability
- Suggests appropriate timing
- Example: "Can we talk now?" → "Noticed you're in meetings—can we connect after 3 PM when you're free?"

### 5. Coordinator Agent

- Combines insights from all agents
- Produces final optimized message

## 📁 Project Structure

```
daman/
├── backend/
│   ├── agents/           # AI agent implementations
│   ├── data/            # Mock data files
│   ├── models/          # Data models
│   ├── routes/          # API endpoints
│   ├── utils/           # Helper functions
│   ├── app.py           # Main Flask application
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   └── App.js
│   └── package.json
└── README.md
```

## 🧪 Example Transformations

| Original           | Rephrased                                                                            |
| ------------------ | ------------------------------------------------------------------------------------ |
| "Do this now"      | "Please prioritize this task"                                                        |
| "Update?"          | "Just checking in—do you have any updates when you get a moment?"                    |
| "Fix this"         | "Could you take a look at this when you get a chance? Let me know if you need help." |
| "Can we talk now?" | "Noticed you're in meetings—can we connect after 3 PM when you're free?"             |

## 🔬 Research Questions Addressed

**RQ1**: How does using AI rephrasing tools affect employee engagement and feeling valued in remote work?

- Measures: Message tone improvement, clarity scores, user satisfaction

**RQ2**: How can organizations compare the ROI of training programs versus AI tools?

- Metrics: Time saved, communication quality, implementation cost

## 📊 Mock Data

The system uses mock data for demonstration:

- `backend/data/jira_tasks.json` - Sample project tasks
- `backend/data/calendar_events.json` - Sample meeting schedules
- `backend/data/chat_history.json` - Sample conversation history

## 🚀 Deployment

### Using Docker (Optional)

```bash
docker-compose up
```

## 🤝 Contributing

This is a research prototype demonstrating AI-powered workplace communication enhancement.

## 📝 License

MIT License

## 🔗 API Endpoints

- `POST /api/rephrase` - Rephrase a message
- `POST /api/analyze` - Analyze message intent and emotion
- `GET /api/context` - Get current user context (Jira, Calendar)
- `GET /api/health` - Health check

## 💡 Future Enhancements

- Real Jira/Calendar integration
- Multi-language support
- Custom tone preferences
- Team communication analytics
- Browser extensions for Slack/Teams
