"""
Rephrase.AI Backend Application
Main Flask application for AI-powered workplace communication assistant
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from agents.coordinator_agent import CoordinatorAgent
from utils.context_loader import ContextLoader

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000'))

# Initialize coordinator agent
coordinator = CoordinatorAgent()
context_loader = ContextLoader()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Rephrase.AI Backend',
        'version': '1.0.0'
    })


@app.route('/api/rephrase', methods=['POST'])
def rephrase_message():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        original_message = data['message']
        user_id = data.get('user_id', 'default_user')
        context_options = data.get('context', {})
        
        # Debug: Log incoming data
        print("[DEBUG] Incoming data:", data)
        
        # Load context data
        context = context_loader.load_context(
            user_id=user_id,
            include_jira=context_options.get('include_jira', True),
            include_calendar=context_options.get('include_calendar', True),
            chat_history=context_options.get('chat_history', []),

            contextual_suggestions=original_message  
        )
        
        # Debug: Log loaded context
        print("[DEBUG] Loaded context:", context)
        
        # Get rephrased message and confidence score from coordinator agent
        result = coordinator.rephrase(original_message, context)
        rephrased_message = result['rephrased_message']
        confidence_score = result['confidence_score']
        
        # Debug: Log rephrase result
        print("[DEBUG] Rephrase result:", result)
        
        # Append confidence score to the rephrased message
        rephrased_with_confidence = f"{rephrased_message} ({confidence_score:.2f})"
        
        return jsonify({
            'success': True,
            'original': original_message,
            'rephrased': rephrased_with_confidence,
            'analysis': result['analysis'],
            'suggestions': result['suggestions']
        })
        
    except Exception as e:
        # Debug: Log exception details
        import traceback
        print("[DEBUG] Exception occurred:", traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_message():
    """
    Analyze message without rephrasing
    Returns intent, emotion, clarity score
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        chat_history = data.get('chat_history', [])
        
        # Analyze message
        analysis = coordinator.analyze_only(message, chat_history)
        
        return jsonify({
            'success': True,
            'message': message,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/context', methods=['GET'])
def get_context():
    """
    Get current user context (Jira tasks, Calendar events)
    """
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        context = context_loader.load_context(
            user_id=user_id,
            include_jira=True,
            include_calendar=True
        )
        
        return jsonify({
            'success': True,
            'context': context
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example transformations"""
    examples = [
        {
            "original": "Do this now",
            "rephrased": "Please prioritize this task",
            "category": "Tone"
        },
        {
            "original": "Update?",
            "rephrased": "Just checking in—do you have any updates when you get a moment?",
            "category": "Intent + Emotion"
        },
        {
            "original": "Pointer mismatch maybe copying wrong",
            "rephrased": "I suspect a pointer mismatch might be causing the copy issue.",
            "category": "Clarity"
        },
        {
            "original": "Need this today",
            "rephrased": "Could you please prioritize this task today? It's due by 5PM in Jira.",
            "category": "Jira Context"
        },
        {
            "original": "Can we talk now?",
            "rephrased": "Noticed you're in meetings—can we connect after 3 PM when you're free?",
            "category": "Calendar Context"
        },
        {
            "original": "Fix this",
            "rephrased": "Could you take a look at this when you get a chance? Let me know if you need help.",
            "category": "Combined"
        }
    ]
    
    return jsonify({
        'success': True,
        'examples': examples
    })


@app.route('/api/save_message', methods=['POST'])
def save_message():
    """Save a chat message to history"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        sender = data.get('sender', 'default_user')
        message = data['message']
        
        # Save message to chat history
        success = context_loader.save_message(sender, message)
        
        return jsonify({
            'success': success,
            'message': 'Message saved' if success else 'Failed to save message'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"\n🚀 Rephrase.AI Backend starting on port {port}...")
    print(f"📝 API Documentation: http://localhost:{port}/api/health\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
