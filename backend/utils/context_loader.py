"""
Context Loader Utility
Loads mock data from JSON files for Jira and Calendar context
"""
import re
from collections import defaultdict, Counter
import json
import os
from typing import Dict, List, Any
from datetime import datetime
from utils.contextual_suggestions import get_contextual_suggestion
from pathlib import Path


class ContextLoader:
    """Loads context data for AI agents"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    def load_jira_context(self, user_id: str = None) -> Dict[str, Any]:
        """Load Jira tasks for user"""
        
        try:
            with open(os.path.join(self.data_dir, 'jira_tasks.json'), 'r') as f:
                all_tasks = json.load(f)
            
            # Filter active tasks (In Progress or high priority)
            active_tasks = [
                task for task in all_tasks
                if task['status'] in ['In Progress', 'In Review'] or task['priority'] in ['High', 'Critical']
            ]
            
            return {
                'active_tasks': active_tasks,
                'total_tasks': len(all_tasks)
            }
            
        except Exception as e:
            print(f"Error loading Jira context: {e}")
            return {'active_tasks': [], 'total_tasks': 0}
    
    def load_calendar_context(self, user_id: str = None) -> Dict[str, Any]:
        """Load calendar events for user"""
        
        try:
            with open(os.path.join(self.data_dir, 'calendar_events.json'), 'r') as f:
                events = json.load(f)
            
            # Filter today's events
            today = datetime.now().strftime('%Y-%m-%d')
            today_events = [e for e in events if e['date'] == today]
            
            # Find next available slot
            available_slots = [e for e in today_events if e['type'] == 'available']
            next_free_slot = available_slots[0]['start_time'] if available_slots else 'end of day'
            
            return {
                'events': today_events,
                'next_free_slot': next_free_slot,
                'busy_until': self._get_busy_until(today_events)
            }
            
        except Exception as e:
            print(f"Error loading calendar context: {e}")
            return {'events': [], 'next_free_slot': 'unknown', 'busy_until': None}
    
    def load_chat_history(self, user_id: str = None, limit: int = 10) -> List[Dict[str, str]]:
        """Load recent chat history"""
        
        try:
            with open(os.path.join(self.data_dir, 'chat_history.json'), 'r') as f:
                history = json.load(f)
            
            # Return recent messages in format expected by agents
            return [
                {
                    'role': 'user' if msg['sender'] == user_id else 'assistant',
                    'content': msg['message']
                }
                for msg in history[-limit:]
            ]
            
        except Exception as e:
            print(f"Error loading chat history: {e}")
            return []
    def load_contextual_suggestions(self, user_input: str) -> str:
     
        try:
            # Path to the chat history file
            chat_path = Path(os.path.join(self.data_dir, "chat_history.json"))
            
            # Ensure the chat history file exists
            if not chat_path.exists():
                print(f"Chat history file not found at {chat_path}")
                return "No chat history available for suggestions."
            
            # Generate contextual suggestion using the provided user input
            return get_contextual_suggestion(chat_path, user_input)
        
        except Exception as e:
            print(f"Error generating contextual suggestions: {e}")
            return "Error generating suggestions."
    
    
    
    def load_context(
        self, 
        user_id: str = 'default_user',
        include_jira: bool = True,
        include_calendar: bool = True,
        chat_history: List[Dict[str, str]] = None,
        contextual_suggestions: str = None  # Change to str
    ) -> Dict[str, Any]:
        """Load all context data"""
        
        context = {}
        
        if include_jira:
            context['jira_context'] = self.load_jira_context(user_id)
        
        if include_calendar:
            context['calendar_context'] = self.load_calendar_context(user_id)
        
        if chat_history is not None:
            context['chat_history'] = chat_history
        else:
            context['chat_history'] = self.load_chat_history(user_id)
        if contextual_suggestions:
            context['contextual_suggestion'] = self.load_contextual_suggestions(contextual_suggestions)
        
        return context
    
    def _get_busy_until(self, events: List[Dict[str, Any]]) -> str:
        """Get the time user is busy until"""
        
        busy_events = [
            e for e in events 
            if e['status'] in ['confirmed', 'busy'] and e['type'] != 'available'
        ]
        
        if not busy_events:
            return None
        
        # Get latest end time
        latest_event = max(busy_events, key=lambda e: e['end_time'])
        return latest_event['end_time']
    
    def save_message(self, sender: str, message: str, timestamp: str = None) -> bool:
        """Save a chat message to history"""
        
        try:
            history_file = os.path.join(self.data_dir, 'chat_history.json')
            
            # Load existing history
            try:
                with open(history_file, 'r') as f:
                    history = json.load(f)
            except FileNotFoundError:
                history = []
            
            # Add new message
            new_message = {
                'sender': sender,
                'message': message,
                'timestamp': timestamp or datetime.now().isoformat()
            }
            history.append(new_message)
            
            # Save back to file
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving message: {e}")
            return False
