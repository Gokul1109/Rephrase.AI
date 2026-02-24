# Rephrase.AI - Quick Start Guide

## 🚀 Getting Started

### Prerequisites

- **Python 3.11** (Important: Not 3.9 or 3.13 - compatibility issues exist)
- Node.js 16 or higher
- OpenAI API key (or other LLM provider)

## 📦 Installation

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment with Python 3.11
# Windows - if multiple Python versions installed:
py -3.11 -m venv venv
# OR if Python 3.11 is default:
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file in backend folder with:
# OPENAI_API_KEY=sk-your-actual-key
# FLASK_ENV=development
# FLASK_DEBUG=True
# PORT=5000
# CORS_ORIGINS=http://localhost:3000
```

> **⚠️ Python Version**: Must use Python 3.11. Python 3.13 causes pydantic-core errors.

### 2. Frontend Setup

```bash
# Navigate to frontend (open new terminal)
cd frontend

# Install dependencies
npm install
```

## ▶️ Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
venv\Scripts\activate  # Windows
python app.py
```

Backend runs on: `http://localhost:5000`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm start
```
The app features a **dual-person chat interface** with real-time AI suggestions:

1. Open `http://localhost:3000` in your browser
2. **Switch users**: Toggle between John Doe and Sarah Smith
3. **Type a message**: Start typing (e.g., "Update?" or "Need this today")
4. **Get AI suggestions**: After 3+ characters and 0.2s pause, suggestions appear in golden box
5. **Use or ignore**: Click "Use This →" to apply suggestion, or keep typing
6. **Send message**: Press Enter or click Send button
7. **View context**: Check Jira tasks and calendar in the interface
8. **Message history**: All sent messages are saved to `backend/data/chat_history.json`

### Example Messages to Try

- "Update?" → Becomes polite check-in with context
- "Need this today" → Adds Jira deadline information
- "Can we talk now?" → Considers calendar availability
- "Fix this" → Transforms to helpful, clear request
2. Type a message (e.g., "Update?", "Need this today")
3. Click "✨ Rephrase with AI"
4. See AI-powered suggestions with context from Jira and Calendar
5. Click examples to try them out
6. View current context to see what data the AI uses

## 🧪 Testing the API

### Health Check

```bash
curl http://localhost:5000/api/health
```

### Rephrase a Message

```bash
curl -X POST http://localhost:5000/api/rephrase \
  -H "Content-Type: application/json" \
  -d '{"message": "Update?", "user_id": "test_user"}'
```

### Get Examples

```bash
curl http://localhost:5000/api/examples
```

### Get Context

```bash
curl http://localhost:5000/api/context?user_id=default_user
```

## 📝 Example Messages to Try

1. **Short/Vague**: "Update?"
2. **Urgent Tone**: "Do this now"
3. **Technical/Unclear**: "Pointer mismatch maybe copying wrong"
4. **Deadline Request**: "Need this today"
5. **Meeting Request**: "Can we talk now?"
6. **General Request**: "Fix this"

## 🔧 Configuration

### Environment Variables (.env)

```env
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
MODEL_NAME=gpt-3.5-turbo  # or gpt-4
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
CORS_ORIGINS=http://localhost:3000
```

### Using Different LLM Providers

The system uses LangChain, so you can switch to other providers:

**For Anthropic Claude:**

```python
# In agents/*.py, change:
from langchain_anthropic import ChatAnthropic
self.llm = ChatAnthropic(model="claude-3-sonnet-20240229")
```

**For Local Models (Ollama):**

```python
from langchain_community.llms import Ollama
self.llm = Ollama(model="llama2")
```

## 🐛 Troubleshooting

### Backend won't start

- Check Python version: `python --version` (need 3.9+)
- Verify virtual environment is activated
- Ensure OPENAI_API_KEY is set in .env

### Frontend won't start

- Check Node version: `node --version` (need 16+)
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is already in use

### AI responses are slow or fail

- Verify your OpenAI API key is valid
- Check your OpenAI account has credits
- Try using gpt-3.5-turbo instead of gpt-4 (faster)

### CORS errors

- Ensure backend is running on port 5000
- Check CORS_ORIGINS in backend .env matches frontend URL

## 📊 Mock Data

All data is stored in `backend/data/`:

- `jira_tasks.json` - Sample project tasks
- `calendar_events.json` - Sample calendar events
- `chat_history.json` - Sample conversation history

Feel free to modify these files to test different scenarios!

## 🎨 Customization

### Adding New Agents

1. Create new agent file in `backend/agents/`
2. Follow the pattern of existing agents
3. Add to coordinator workflow in `coordinator_agent.py`

### Modifying UI

All React components are in `frontend/src/components/`
Styling is in separate CSS files for each component

## 🔐 Security Notes

- Never commit your `.env` file with real API keys
- The `.env.example` is provided as a template
- For production, use environment variables or secure secret management

## 📚 Next Steps

- Integrate real Jira API
- Add Slack/Teams integration
- Implement user authentication
- Add message history tracking
- Create browser extension
- Build analytics dashboard

## 💡 Tips

- Use shorter messages for faster AI responses
- The AI considers context from Jira and Calendar automatically
- Click examples to see how different scenarios are handled
- View context panel to understand what data AI uses

## 🆘 Support

For issues or questions:

1. Check the troubleshooting section
2. Review the README.md
3. Check backend logs in terminal
4. Verify API endpoints with curl

Happy rephrasing! ✨
