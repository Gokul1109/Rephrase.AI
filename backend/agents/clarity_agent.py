"""
Clarity Agent
Analyzes message clarity and suggests improvements for vague or unclear messages
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


class ClarityAgent:
    """Analyzes and improves message clarity"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
            temperature=0.7
        )
    
    def analyze(self, message: str) -> Dict[str, Any]:
        """
        Analyze message clarity
        
        Args:
            message: The message to analyze
            
        Returns:
            Dictionary with clarity score and improvement suggestions
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in clear workplace communication. Analyze the message for:
            1. Clarity score (0-10, where 10 is perfectly clear)
            2. Specific issues (vagueness, ambiguity, missing context)
            3. Improvement suggestions
            
            Return a JSON response."""),
            ("user", """Message: "{message}"

Analyze this message and return JSON with:
{{
    "clarity_score": 0-10,
    "issues": ["list of clarity issues"],
    "vague_terms": ["terms that need clarification"],
    "missing_context": ["what context is missing"],
    "improved_version": "a clearer version of the message"
}}""")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({'message': message})
            
            # Parse response
            import json
            result = json.loads(response.content)
            
            return result
            
        except Exception as e:
            # Fallback analysis
            word_count = len(message.split())
            has_question_words = any(word in message.lower() for word in ['what', 'when', 'where', 'who', 'how', 'why'])
            
            clarity_score = 5
            if word_count < 3:
                clarity_score = 2
            elif word_count > 10 and '?' not in message:
                clarity_score = 7
            
            return {
                'clarity_score': clarity_score,
                'issues': ['Message may be too brief'] if word_count < 3 else [],
                'vague_terms': [],
                'missing_context': ['Consider adding more specific details'],
                'improved_version': f"Could you please clarify: {message}"
            }
