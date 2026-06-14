#!/usr/bin/env python3
"""
Test AgenticRAG: Verify routing decisions and retrieval strategies.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.agentic_router import get_router
from retrieval.agentic_rag import AgenticRAG

def test_router():
    """Test the agentic router."""
    print("\n" + "="*70)
    print("TESTING AGENTIC ROUTER")
    print("="*70)
    
    router = get_router()
    
    test_queries = [
        "I have a fever and headache, what should I do?",
        "How do I solve a dynamic programming problem in an interview?",
        "What's the best way to prepare for a technical interview?",
        "I'm experiencing chest pain and shortness of breath",
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        routing = router.route(query)
        print(f"  Routed to: {routing['persona_id']}")
        print(f"  Confidence: {routing['confidence']:.2f}")
        print(f"  Reasoning: {routing['reasoning']}")

def test_rag_medical():
    """Test RAG for medical persona."""
    print("\n" + "="*70)
    print("TESTING AGENTIC RAG - MEDICAL PERSONA")
    print("="*70)
    
    rag = AgenticRAG("doctor_empathetic_v1")
    
    medical_queries = [
        "I have a severe headache",
        "What are the symptoms of flu?",
        "I'm experiencing fatigue and dizziness"
    ]
    
    for query in medical_queries:
        print(f"\nQuery: {query}")
        result = rag.retrieve(query)
        
        decision = result['decision']
        print(f"  Strategy: {decision['strategy']}")
        print(f"  Num Examples: {decision['num_examples']}")
        print(f"  Rerank: {decision['rerank']}")
        print(f"  Reasoning: {decision['reasoning']}")
        print(f"  Examples Retrieved: {len(result['examples'])}")
        
        if result['examples']:
            print(f"  Top Example: {result['examples'][0][:100]}...")

def test_rag_education():
    """Test RAG for education teacher persona."""
    print("\n" + "="*70)
    print("TESTING AGENTIC RAG - EDUCATION TEACHER PERSONA")
    print("="*70)
    
    rag = AgenticRAG("teacher_supportive_v1")
    
    education_queries = [
        "Can you help me understand photosynthesis?",
        "How do I solve quadratic equations?",
        "What's the difference between mitosis and meiosis?"
    ]
    
    for query in education_queries:
        print(f"\nQuery: {query}")
        result = rag.retrieve(query)
        
        decision = result['decision']
        print(f"  Strategy: {decision['strategy']}")
        print(f"  Num Examples: {decision['num_examples']}")
        print(f"  Rerank: {decision['rerank']}")
        print(f"  Reasoning: {decision['reasoning']}")
        print(f"  Examples Retrieved: {len(result['examples'])}")
        
        if result['examples']:
            print(f"  Top Example: {result['examples'][0][:100]}...")

def main():
    """Run all RAG tests."""
    print("="*70)
    print("PersonaReplica AgenticRAG Test")
    print("="*70)
    print("Tests routing and RAG decision making:")
    print("  - Router: Select best persona for query")
    print("  - RAG: Decide retrieval strategy and execute")
    
    try:
        test_router()
        test_rag_medical()
        test_rag_education()
        
        print("\n" + "="*70)
        print("✓ All tests completed!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())