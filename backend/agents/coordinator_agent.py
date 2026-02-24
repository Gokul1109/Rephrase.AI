"""
Coordinator Agent - Orchestrates all AI agents for message rephrasing
Uses LangGraph for multi-agent coordination
"""

from typing import Dict, List, Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

from .intent_emotion_agent import IntentEmotionAgent
from .clarity_agent import ClarityAgent
from .jira_agent import JiraAgent
from .calendar_agent import CalendarAgent


class AgentState(TypedDict):
    """State shared between agents"""
    original_message: str
    chat_history: List[Dict[str, str]]
    jira_context: Dict[str, Any]
    calendar_context: Dict[str, Any]
    intent_analysis: Dict[str, Any]
    clarity_analysis: Dict[str, Any]
    jira_suggestion: str
    calendar_suggestion: str
    final_message: str
    analysis: Dict[str, Any]


class CoordinatorAgent:
    """Coordinates multiple AI agents to produce optimal message rephrasing"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
            temperature=0.7
        )
        
        # Initialize individual agents
        self.intent_emotion_agent = IntentEmotionAgent()
        self.clarity_agent = ClarityAgent()
        self.jira_agent = JiraAgent()
        self.calendar_agent = CalendarAgent()
        
        # Build the agent graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build LangGraph workflow for multi-agent coordination"""
        
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("intent_emotion", self._intent_emotion_node)
        workflow.add_node("clarity", self._clarity_node)
        workflow.add_node("jira", self._jira_node)
        workflow.add_node("calendar", self._calendar_node)
        workflow.add_node("synthesizer", self._synthesize_node)
        
        # Define the flow
        workflow.set_entry_point("intent_emotion")
        workflow.add_edge("intent_emotion", "clarity")
        workflow.add_edge("clarity", "jira")
        workflow.add_edge("jira", "calendar")
        workflow.add_edge("calendar", "synthesizer")
        workflow.add_edge("synthesizer", END)
        
        return workflow.compile()
    
    def _intent_emotion_node(self, state: AgentState) -> AgentState:
        """Process intent and emotion analysis"""
        analysis = self.intent_emotion_agent.analyze(
            state['original_message'],
            state.get('chat_history', [])
        )
        state['intent_analysis'] = analysis
        return state
    
    def _clarity_node(self, state: AgentState) -> AgentState:
        """Process clarity analysis"""
        analysis = self.clarity_agent.analyze(state['original_message'])
        state['clarity_analysis'] = analysis
        return state
    
    def _jira_node(self, state: AgentState) -> AgentState:
        """Process Jira context"""
        suggestion = self.jira_agent.enhance_with_context(
            state['original_message'],
            state.get('jira_context', {})
        )
        state['jira_suggestion'] = suggestion
        return state
    
    def _calendar_node(self, state: AgentState) -> AgentState:
        """Process calendar context"""
        suggestion = self.calendar_agent.enhance_with_context(
            state['original_message'],
            state.get('calendar_context', {})
        )
        state['calendar_suggestion'] = suggestion
        return state
    
    def _synthesize_node(self, state: AgentState) -> AgentState:
        """Synthesize all agent outputs into final message"""
        
        # Create synthesis prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant that synthesizes multiple suggestions to create 
            the optimal workplace communication message. Consider:
            - Intent and emotional tone
            - Clarity and specificity
            - Project context from Jira
            - Calendar and availability context
            
            Create a message that is professional, clear, empathetic, and contextually aware."""),
            ("user", """Original message: {original_message}
            
Intent Analysis: {intent_analysis}
Clarity Analysis: {clarity_analysis}
Jira Context Suggestion: {jira_suggestion}
Calendar Context Suggestion: {calendar_suggestion}

Synthesize these into one optimal message. Return ONLY the rephrased message without explanation.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            'original_message': state['original_message'],
            'intent_analysis': state['intent_analysis'],
            'clarity_analysis': state['clarity_analysis'],
            'jira_suggestion': state['jira_suggestion'],
            'calendar_suggestion': state['calendar_suggestion']
        })
        
        state['final_message'] = response.content.strip()
        
        # Compile analysis summary
        state['analysis'] = {
            'intent': state['intent_analysis'],
            'clarity': state['clarity_analysis'],
            'tone_improvement': state['intent_analysis'].get('suggested_tone', 'neutral'),
            'clarity_score': state['clarity_analysis'].get('clarity_score', 0)
        }
        
        return state
    
    def rephrase(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method to rephrase a message using all agents
        
        Args:
            message: Original message to rephrase
            context: Dictionary containing jira_context, calendar_context, chat_history
            
        Returns:
            Dictionary with rephrased message and analysis
        """
        
        initial_state = AgentState(
            original_message=message,
            chat_history=context.get('chat_history', []),
            jira_context=context.get('jira_context', {}),
            calendar_context=context.get('calendar_context', {}),
            intent_analysis={},
            clarity_analysis={},
            jira_suggestion='',
            calendar_suggestion='',
            final_message='',
            analysis={}
        )
        
        # Run the workflow
        final_state = self.workflow.invoke(initial_state)
        # Calculate confidence score (example logic, replace with your own)
        confidence_score = self.calculate_confidence(message, final_state['final_message'])
    
        return {
        'rephrased_message': final_state['final_message'],
        'confidence_score': confidence_score,
        'analysis': final_state['analysis'],
        'suggestions': {
            'jira': final_state['jira_suggestion'],
            'calendar': final_state['calendar_suggestion']
        }
    }
    
    def calculate_confidence(self, original: str, rephrased: str) -> float:
        """
        Use the LLM to calculate a confidence score for the rephrased message.
        
        Args:
            original: Original message
            rephrased: Rephrased message
            
        Returns:
            Confidence score as a float (0.0 to 1.0)
        """
        # Create a prompt for the LLM to evaluate the rephrased message
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI evaluator that assesses the quality of rephrased messages.
        Your task is to evaluate how well the rephrased message improves the original message
        in terms of smoothness, politeness, clarity, and contextual relevance. Focus on short, professional, and polite
        communication. Consider the following criteria:
        - Does the rephrased message retain the meaning of the original?
        - Is the tone appropriate for a professional setting?
        - Does the rephrased message improve clarity and readability?
        - Is the rephrased message contextually relevant?
        Provide a confidence score between 0.0 and 1.0 as a single numeric value.
        Return only the numeric value without any explanation or additional text."""),
            ("user", f"""Original message: {original}
        
Rephrased message: {rephrased}

Evaluate the rephrased message and provide a confidence score (0.0 to 1.0).""")
        ])
        
        # Use the LLM to generate the confidence score
        chain = prompt | self.llm
        response = chain.invoke({})
        
        # Debug logs to inspect the response
        print(f"Original: {original}")
        print(f"Rephrased: {rephrased}")
        print(f"LLM Response: {response.content.strip()}")  # Log the raw response
        
        try:
            # Extract the numeric value from the response
            import re
            match = re.search(r"([0-1](?:\.\d+)?)", response.content.strip())
            if match:
                confidence_score = float(match.group(1))
                # Ensure the score is within the valid range
                return max(0.0, min(confidence_score, 1.0))
            else:
                raise ValueError("No valid confidence score found in the response.")
        except ValueError as e:
            # If parsing fails, log the error and return a default confidence score
            print(f"Error parsing confidence score: {e}")
            print("Returning default confidence score: 0.50")
            return 0.5
    
    def analyze_only(self, message: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Analyze message without rephrasing"""
        
        if chat_history is None:
            chat_history = []
        
        intent_analysis = self.intent_emotion_agent.analyze(message, chat_history)
        clarity_analysis = self.clarity_agent.analyze(message)
        
        return {
            'intent': intent_analysis,
            'clarity': clarity_analysis,
            'tone': intent_analysis.get('detected_tone', 'neutral'),
            'clarity_score': clarity_analysis.get('clarity_score', 0),
            'issues': clarity_analysis.get('issues', [])
        }
