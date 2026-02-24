"""
Intent & Emotion Agent
Analyzes message intent and emotional tone based on chat history
"""

from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


class IntentEmotionAgent:
    """Analyzes intent and emotional tone of messages"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
            temperature=0.7
        )
    
    def analyze(self, message: str, chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze message for intent and emotional tone
        
        Args:
            message: The message to analyze
            chat_history: Previous conversation context
            
        Returns:
            Dictionary with intent, emotion, and tone analysis
        """
        
        # Format chat history
        history_text = "\n".join([
            f"{msg.get('role', 'user')}: {msg.get('content', '')}"
            for msg in chat_history[-5:]  # Last 5 messages
        ]) if chat_history else "No previous context"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in workplace communication analysis. Analyze the message for:
            1. Intent (question, request, update, complaint, etc.)
            2. Emotional tone (urgent, casual, formal, frustrated, friendly, etc.)
            3. Suggested tone improvements
            
            Consider the chat history for context. Return a JSON response."""),
            ("user", """Message: "{message}"
            
Chat History:
{chat_history}

Analyze this message and return JSON with:
{{
    "detected_intent": "the primary intent",
    "detected_tone": "the emotional tone",
    "suggested_tone": "recommended tone for professionalism",
    "tone_issues": ["list of tone problems if any"],
    "recommended_approach": "how to improve the message"
}}""")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                'message': message,
                'chat_history': history_text
            })
            
            # Parse response
            import json
            result = json.loads(response.content)
            
            return result
            
        except Exception as e:
            # Fallback analysis
            return {
                'detected_intent': 'general_message',
                'detected_tone': 'neutral',
                'suggested_tone': 'professional_friendly',
                'tone_issues': [],
                'recommended_approach': 'Add context and politeness markers'
            }
