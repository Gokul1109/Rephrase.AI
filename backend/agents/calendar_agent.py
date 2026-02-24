"""
Calendar Agent
Enhances messages with calendar/availability context (using mock data)
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import os


class CalendarAgent:
    """Enhances messages with calendar and availability context"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
            temperature=0.7
        )
    
    def enhance_with_context(self, message: str, calendar_context: Dict[str, Any]) -> str:
        """
        Enhance message with calendar/availability context
        
        Args:
            message: Original message
            calendar_context: Dictionary with events and availability
            
        Returns:
            Enhanced message with calendar context
        """
        
        if not calendar_context or not calendar_context.get('events'):
            return message
        
        # Check if message is requesting meeting or immediate response
        meeting_keywords = ['talk', 'meet', 'call', 'discuss', 'chat', 'connect']
        urgent_keywords = ['now', 'asap', 'urgent', 'immediately']
        
        is_meeting_request = any(keyword in message.lower() for keyword in meeting_keywords)
        is_urgent = any(keyword in message.lower() for keyword in urgent_keywords)
        
        if not (is_meeting_request or is_urgent):
            return message
        
        # Format calendar events
        events_text = "\n".join([
            f"- {event['title']} ({event['start_time']} - {event['end_time']})"
            for event in calendar_context['events'][:5]
        ])
        
        next_free = calendar_context.get('next_free_slot', 'later today')
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant that enhances workplace messages with calendar awareness.
            When someone requests an immediate meeting or response, check their calendar and suggest better timing.
            Be respectful of their schedule and professional in tone."""),
            ("user", """Original message: "{message}"

Current Calendar:
{events}

Next free slot: {next_free}

If the message requests immediate availability but the person is busy, suggest the next available time.
Return ONLY the enhanced message without explanation.""")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                'message': message,
                'events': events_text,
                'next_free': next_free
            })
            
            return response.content.strip()
            
        except Exception as e:
            return message
