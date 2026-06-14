#!/usr/bin/env python3
"""
AgenticRouter: LLM-based persona selection.

Routes incoming queries to the best persona using Groq LLaMA 3.3 70B.
"""

import json
from typing import Dict
from dotenv import load_dotenv
import os

_groq_client = None

def get_groq_client():
    """Lazy load Groq client."""
    global _groq_client
    if _groq_client is None:
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")
        try:
            from groq import Groq
            _groq_client = Groq(api_key=api_key)
        except ImportError:
            raise ImportError("groq package not installed. Install with: pip install groq")
    return _groq_client

# Registered personas
REGISTERED_PERSONAS = {
    "doctor_empathetic_v1": {
        "name": "Doctor",
        "domain": "medical",
        "description": "Empathetic medical professional. High empathy, high hedging, low question rate."
    },
    "teacher_supportive_v1": {
        "name": "Supportive Teacher",
        "domain": "education",
        "description": "Patient and encouraging educator. Clear explanations, high question rate, supportive tone."
    }
}

class AgenticRouter:
    """Router that selects the best persona for a query."""
    
    def __init__(self):
        """Initialize router with registered personas."""
        self.personas = REGISTERED_PERSONAS
        self.client = get_groq_client()
    
    def route(self, query: str) -> Dict:
        """
        Route a query to the best persona.
        
        LLM call #1: Select persona_id + confidence + reasoning
        
        Args:
            query: User's input query
        
        Returns:
            Dict with:
            - persona_id: Selected persona ID
            - confidence: float [0.0, 1.0]
            - reasoning: str explaining the choice
        """
        # Build persona descriptions for the prompt
        personas_desc = "\n".join([
            f"- {pid}: {info['name']} ({info['domain']}) - {info['description']}"
            for pid, info in self.personas.items()
        ])
        
        # Create routing prompt
        prompt = f"""You are an expert routing agent. Analyze the user query and select the best persona from the available options.

Available Personas:
{personas_desc}

User Query: "{query}"

Select the BEST matching persona. Consider:
1. Domain relevance (medical, interview, etc.)
2. Communication style fit
3. Expertise match

Respond in JSON format:
{{
  "persona_id": "...",
  "confidence": 0.0-1.0,
  "reasoning": "..."
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Fast routing model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.2
            )
            
            response_text = response.choices[0].message.content
            
            # Parse JSON response
            try:
                decision = json.loads(response_text)
                
                # Validate persona_id
                if decision.get("persona_id") not in self.personas:
                    # Fallback to first persona if invalid
                    decision["persona_id"] = list(self.personas.keys())[0]
                    decision["confidence"] = 0.5
                    decision["reasoning"] = f"Invalid persona, defaulted to {decision['persona_id']}"
                
                return decision
            except json.JSONDecodeError:
                # Fallback routing based on keywords
                return self._fallback_route(query)
        except Exception as e:
            print(f"Error in routing LLM call: {e}")
            return self._fallback_route(query)
    
    def _fallback_route(self, query: str) -> Dict:
        """
        Fallback routing using keyword matching.
        
        Used when LLM fails or response is invalid.
        """
        query_lower = query.lower()
        
        # Medical keywords
        medical_keywords = ['fever', 'headache', 'pain', 'symptom', 'doctor', 'medical', 
                           'health', 'disease', 'treatment', 'diagnose', 'hospital', 'illness',
                           'medicine', 'sick', 'hurt', 'injury', 'bleeding', 'swelling',
                           'infection', 'allergy', 'prescription', 'clinic', 'patient',
                           'chest pain', 'breathing', 'cough', 'nausea', 'dizzy']
        
        # Education keywords
        education_keywords = ['learn', 'teach', 'homework', 'study', 'explain', 
                             'understand', 'lesson', 'subject', 'grade', 'school', 'class',
                             'math', 'science', 'history', 'algebra', 'equation', 'solve',
                             'calculate', 'formula', 'theorem', 'theory', 'concept',
                             'essay', 'writing', 'reading', 'literature', 'physics',
                             'chemistry', 'biology', 'geometry', 'calculus', 'test',
                             'exam', 'quiz', 'assignment', 'problem', 'question',
                             'photosynthesis', 'mitosis', 'meiosis', 'quadratic',
                             'pythagorean', 'shakespeare', 'grammar', 'vocabulary',
                             'interview', 'technical', 'prepare', 'practice', 'coding',
                             'programming', 'algorithm', 'data structure']
        
        medical_score = sum(query_lower.count(kw) for kw in medical_keywords)
        education_score = sum(query_lower.count(kw) for kw in education_keywords)
        
        if education_score > medical_score:
            return {
                "persona_id": "teacher_supportive_v1",
                "confidence": 0.6,
                "reasoning": "Fallback: Education keywords detected"
            }
        else:
            return {
                "persona_id": "doctor_empathetic_v1",
                "confidence": 0.6,
                "reasoning": "Fallback: Medical keywords detected or no clear match"
            }

# Singleton instance
_router = None

def get_router() -> AgenticRouter:
    """Get or create singleton router instance."""
    global _router
    if _router is None:
        _router = AgenticRouter()
    return _router

def main():
    """Test the router with sample queries."""
    router = get_router()
    
    test_queries = [
        "I have a terrible headache and fever, what should I do?",
        "Can you help me understand photosynthesis?",
        "How do I solve quadratic equations?",
        "My stomach hurts after eating spicy food"
    ]
    
    for query in test_queries:
        result = router.route(query)
        print(f"Query: {query}")
        print(f"  Routed to: {result['persona_id']} (confidence: {result['confidence']:.2f})")
        print(f"  Reasoning: {result['reasoning']}\n")

if __name__ == "__main__":
    main()