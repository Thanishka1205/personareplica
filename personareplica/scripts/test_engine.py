#!/usr/bin/env python3
"""
Test engine end-to-end: Multi-turn test across both personas.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.inference import PersonaEngine

def test_medical_domain():
    """Test medical persona with multiple queries."""
    print("\n" + "="*70)
    print("TESTING MEDICAL DOMAIN (Doctor Empathetic)")
    print("="*70)
    
    engine = PersonaEngine()
    
    medical_queries = [
        "I've had a persistent cough for two weeks, what could it be?",
        "I'm experiencing severe chest pain, should I go to the hospital?",
        "How can I manage my diabetes more effectively?"
    ]
    
    for i, query in enumerate(medical_queries, 1):
        print(f"\n--- Medical Query {i} ---")
        print(f"Q: {query}\n")
        
        result = engine.process(query)
        
        if result["success"]:
            print(f"A: {result['final_response']}\n")
            print(f"Accuracy Score: {result['accuracy_score']:.3f}")
            print(f"Persona: {result['steps']['routing']['persona_id']}")
            print(f"Retrieval Strategy: {result['steps']['retrieval']['decision']['strategy']}")
            print(f"Examples Retrieved: {len(result['steps']['retrieval']['semantic_examples'])}")
        else:
            print(f"ERROR: {result.get('error', 'Unknown error')}")

def test_interview_domain():
    """Test interview coach persona with multiple queries."""
    print("\n" + "="*70)
    print("TESTING INTERVIEW DOMAIN (Interview Coach)")
    print("="*70)
    
    engine = PersonaEngine()
    
    interview_queries = [
        "How do I approach a system design interview question about designing a URL shortener?",
        "What's the best way to solve coding problems during a technical interview?",
        "How can I explain my thought process clearly in an interview?"
    ]
    
    for i, query in enumerate(interview_queries, 1):
        print(f"\n--- Interview Query {i} ---")
        print(f"Q: {query}\n")
        
        result = engine.process(query)
        
        if result["success"]:
            print(f"A: {result['final_response']}\n")
            print(f"Accuracy Score: {result['accuracy_score']:.3f}")
            print(f"Persona: {result['steps']['routing']['persona_id']}")
            print(f"Retrieval Strategy: {result['steps']['retrieval']['decision']['strategy']}")
            print(f"Examples Retrieved: {len(result['steps']['retrieval']['semantic_examples'])}")
        else:
            print(f"ERROR: {result.get('error', 'Unknown error')}")

def main():
    """Run all tests."""
    print("="*70)
    print("PersonaReplica End-to-End Engine Test")
    print("="*70)
    print("This test runs the full 5-step pipeline (without memory):")
    print("  1. AgenticRouter - Select persona")
    print("  2. AgenticRAG - Retrieve examples")
    print("  3. PromptBuilder - Build system prompt")
    print("  4. Groq LLM - Generate response")
    print("  5. PersonaScorer - Score accuracy")
    
    try:
        test_medical_domain()
        test_interview_domain()
        
        print("\n" + "="*70)
        print("[OK] All tests completed!")
        print("="*70)
        
    except Exception as e:
        print(f"\n[FAILED] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())