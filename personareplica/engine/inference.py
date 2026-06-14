#!/usr/bin/env python3
"""
PersonaEngine: Orchestrates the full 7-step agentic pipeline.

Without memory, the pipeline is:
1. AgenticRouter - Select persona
2. AgenticRAG - Retrieve examples
3. PromptBuilder - Build system prompt
4. Groq LLM - Generate response
5. PersonaScorer - Score response
6. Return full result with all metadata
"""

import os
from typing import Dict
from dotenv import load_dotenv

from engine.agentic_router import get_router
from retrieval.agentic_rag import AgenticRAG
from engine.prompt_builder import PromptBuilder
from persona.scorer import PersonaScorer

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

class PersonaEngine:
    """Orchestrates the full agentic pipeline."""
    
    def __init__(self):
        """Initialize engine components."""
        self.router = get_router()
        self.scorer = PersonaScorer()
        self.rag_instances = {}  # Cache RAG instances per persona
        self.groq_client = get_groq_client()
    
    def get_rag(self, persona_id: str) -> AgenticRAG:
        """Get or create RAG instance for persona."""
        if persona_id not in self.rag_instances:
            self.rag_instances[persona_id] = AgenticRAG(persona_id)
        return self.rag_instances[persona_id]
    
    def process(self, query: str) -> Dict:
        """
        Full agentic pipeline: Route -> RAG -> Prompt -> Generate -> Score.
        
        Returns comprehensive dict with all intermediate steps and final response.
        """
        result = {
            "query": query,
            "steps": {},
            "final_response": "",
            "accuracy_score": 0.0,
            "success": False
        }
        
        try:
            # STEP 1: AgenticRouter (LLM call #1)
            print(f"\n[STEP 1] Routing query...")
            routing_result = self.router.route(query)
            persona_id = routing_result["persona_id"]
            
            result["steps"]["routing"] = {
                "persona_id": persona_id,
                "confidence": routing_result["confidence"],
                "reasoning": routing_result["reasoning"]
            }
            print(f"  [>>] Routed to: {persona_id} (confidence: {routing_result['confidence']:.2f})")
            
            # STEP 2: AgenticRAG (LLM call #2)
            print(f"\n[STEP 2] Retrieving examples...")
            rag = self.get_rag(persona_id)
            retrieval_result = rag.retrieve(query)
            
            examples = retrieval_result["examples"]
            result["steps"]["retrieval"] = retrieval_result["retrieval_details"]
            result["steps"]["retrieval"]["decision"] = retrieval_result["decision"]
            print(f"  [>>] Retrieved {len(examples)} examples")
            print(f"  [>>] Strategy: {retrieval_result['decision']['strategy']}")
            
            # STEP 3: PromptBuilder
            print(f"\n[STEP 3] Building persona prompt...")
            prompt_builder = PromptBuilder(persona_id)
            system_prompt = prompt_builder.build_system_prompt(examples, user_query=query)
            result["steps"]["prompt_building"] = {
                "system_prompt_length": len(system_prompt),
                "examples_injected": len(examples)
            }
            print(f"  [>>] System prompt built ({len(system_prompt)} chars)")
            
            # STEP 4: Groq LLM Generation (LLM call #3)
            print(f"\n[STEP 4] Generating response with Groq...")
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Use main model for generation
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            generated_response = response.choices[0].message.content
            result["steps"]["generation"] = {
                "model": "llama-3.3-70b-versatile",
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else 0,
                "response_length": len(generated_response)
            }
            result["final_response"] = generated_response
            print(f"  [>>] Response generated ({len(generated_response)} chars)")
            
            # STEP 5: PersonaScorer
            print(f"\n[STEP 5] Scoring response accuracy...")
            accuracy_score, scoring_details = self.scorer.score_response(generated_response, persona_id)
            result["steps"]["scoring"] = scoring_details
            result["accuracy_score"] = accuracy_score
            print(f"  [>>] Accuracy score: {accuracy_score:.3f}")
            if scoring_details['is_flagged']:
                print(f"  ⚠️  Response flagged (below threshold {scoring_details['quality_threshold']})")
            
            result["success"] = True
            
            return result
        
        except Exception as e:
            result["error"] = str(e)
            print(f"\n[FAILED] Error in pipeline: {e}")
            import traceback
            traceback.print_exc()
            return result

def main():
    """Test the full engine with sample queries."""
    engine = PersonaEngine()
    
    test_queries = [
        "I've been experiencing severe headaches and a fever for three days. What could be wrong?",
        "How should I approach a system design interview question about scaling a chat application?",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {query}")
        print('='*60)
        
        result = engine.process(query)
        
        if result["success"]:
            print(f"\n{'='*60}")
            print(f"FINAL RESPONSE:")
            print('='*60)
            print(result["final_response"])
            print(f"\nAccuracy Score: {result['accuracy_score']:.3f}")
        else:
            print(f"\n[FAILED] Pipeline failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()


# Alias for backwards compatibility
PersonaInference = PersonaEngine

# Add convenience method for Streamlit app
def _generate_response_with_metadata(self, query: str, max_tokens: int = 200):
    """Generate response and return tuple of (response, metadata)."""
    result = self.process(query)
    
    if result["success"]:
        metadata = {
            "rag": {
                "decision": result["steps"]["retrieval"]["decision"],
                "examples": []
            },
            "accuracy_score": result["accuracy_score"]
        }
        return result["final_response"], metadata
    else:
        return f"Error: {result.get('error', 'Unknown error')}", {}

# Patch method onto class
PersonaEngine.generate_response_with_metadata = _generate_response_with_metadata
