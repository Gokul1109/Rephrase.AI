"""
Jira Agent
Enhances messages with project context from Jira tasks (using mock data)
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


class JiraAgent:
    """Enhances messages with Jira project context"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
            temperature=0.7
        )
    
    def enhance_with_context(self, message: str, jira_context: Dict[str, Any]) -> str:
        """
        Enhance message with Jira task context
        
        Args:
            message: Original message
            jira_context: Dictionary with active_tasks
            
        Returns:
            Enhanced message with Jira context
        """
        
        if not jira_context or not jira_context.get('active_tasks'):
            return message
        
        # Format tasks
        tasks_text = "\n".join([
            f"- {task['key']}: {task['summary']} (Due: {task.get('due_date', 'No deadline')}, Priority: {task.get('priority', 'Medium')})"
            for task in jira_context['active_tasks'][:3]  # Top 3 tasks
        ])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant that enhances workplace messages with project context.
            When a message references work items, deadlines, or tasks, add relevant context from Jira.
            Keep the tone professional and helpful."""),
            ("user", """Original message: "{message}"

Active Jira Tasks:
{tasks}

If the message relates to these tasks, enhance it with relevant context (task ID, deadline, priority).
Return ONLY the enhanced message without explanation.""")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                'message': message,
                'tasks': tasks_text
            })
            
            return response.content.strip()
            
        except Exception as e:
            return message
