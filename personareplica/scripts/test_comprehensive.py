#!/usr/bin/env python3
"""
Comprehensive testing for PersonaReplica with edge cases.
Tests routing accuracy, RAG quality, and edge cases.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.agentic_router import get_router
from retrieval.agentic_rag import AgenticRAG


def test_medical_routing():
    """Test medical query routing with edge cases."""
    print("\n" + "="*70)
    print("TESTING MEDICAL ROUTING")
    print("="*70)
    
    router = get_router()
    
    test_queries = [
        # Clear medical queries
        ("I have a fever and headache", "doctor_empathetic_v1"),
        ("What should I do for chest pain?", "doctor_empathetic_v1"),
        ("My child has a rash", "doctor_empathetic_v1"),
        ("I'm experiencing nausea and dizziness", "doctor_empathetic_v1"),
        ("What are the symptoms of diabetes?", "doctor_empathetic_v1"),
        
        # Edge cases - medical terms
        ("I need a prescription refill", "doctor_empathetic_v1"),
        ("When should I see a doctor?", "doctor_empathetic_v1"),
        ("Is this infection serious?", "doctor_empathetic_v1"),
    ]
    
    correct = 0
    total = len(test_queries)
    
    for query, expected_persona in test_queries:
        result = router.route(query)
        actual_persona = result['persona_id']
        confidence = result['confidence']
        is_correct = actual_persona == expected_persona
        
        if is_correct:
            correct += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"\n{status} Query: {query}")
        print(f"   Expected: {expected_persona}")
        print(f"   Got: {actual_persona} (confidence: {confidence:.2f})")
        if not is_correct:
            print(f"   Reasoning: {result['reasoning']}")
    
    accuracy = (correct / total) * 100
    print(f"\n{'='*70}")
    print(f"Medical Routing Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    print(f"{'='*70}")
    
    return accuracy


def test_education_routing():
    """Test education query routing with edge cases."""
    print("\n" + "="*70)
    print("TESTING EDUCATION ROUTING")
    print("="*70)
    
    router = get_router()
    
    test_queries = [
        # Clear education queries
        ("Can you explain photosynthesis?", "teacher_supportive_v1"),
        ("How do I solve quadratic equations?", "teacher_supportive_v1"),
        ("What's the Pythagorean theorem?", "teacher_supportive_v1"),
        ("Help me understand Shakespeare", "teacher_supportive_v1"),
        ("I'm struggling with algebra", "teacher_supportive_v1"),
        
        # Edge cases - academic subjects
        ("Explain Newton's laws of motion", "teacher_supportive_v1"),
        ("What's the difference between mitosis and meiosis?", "teacher_supportive_v1"),
        ("How do I write a good essay?", "teacher_supportive_v1"),
        ("What is calculus?", "teacher_supportive_v1"),
        ("Help me with my chemistry homework", "teacher_supportive_v1"),
        
        # Technical/programming (should go to education)
        ("How do I solve a dynamic programming problem?", "teacher_supportive_v1"),
        ("Explain recursion to me", "teacher_supportive_v1"),
        ("What's the best way to learn algorithms?", "teacher_supportive_v1"),
    ]
    
    correct = 0
    total = len(test_queries)
    
    for query, expected_persona in test_queries:
        result = router.route(query)
        actual_persona = result['persona_id']
        confidence = result['confidence']
        is_correct = actual_persona == expected_persona
        
        if is_correct:
            correct += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"\n{status} Query: {query}")
        print(f"   Expected: {expected_persona}")
        print(f"   Got: {actual_persona} (confidence: {confidence:.2f})")
        if not is_correct:
            print(f"   Reasoning: {result['reasoning']}")
    
    accuracy = (correct / total) * 100
    print(f"\n{'='*70}")
    print(f"Education Routing Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    print(f"{'='*70}")
    
    return accuracy


def test_ambiguous_queries():
    """Test ambiguous queries that could go either way."""
    print("\n" + "="*70)
    print("TESTING AMBIGUOUS QUERIES")
    print("="*70)
    
    router = get_router()
    
    test_queries = [
        "What causes stress?",  # Could be medical or educational
        "How does the brain work?",  # Could be medical or educational
        "What is anxiety?",  # Could be medical or educational
        "Tell me about the human body",  # Could be medical or educational
    ]
    
    for query in test_queries:
        result = router.route(query)
        print(f"\nQuery: {query}")
        print(f"  → Routed to: {result['persona_id']}")
        print(f"  → Confidence: {result['confidence']:.2f}")
        print(f"  → Reasoning: {result['reasoning'][:100]}...")


def test_rag_quality():
    """Test RAG retrieval quality."""
    print("\n" + "="*70)
    print("TESTING RAG QUALITY")
    print("="*70)
    
    # Test medical RAG
    print("\n📍 Medical RAG:")
    medical_rag = AgenticRAG("doctor_empathetic_v1")
    
    medical_query = "What should I do for a persistent cough?"
    result = medical_rag.retrieve(medical_query)
    
    print(f"Query: {medical_query}")
    print(f"Strategy: {result['decision']['strategy']}")
    print(f"Examples: {len(result['examples'])}")
    print(f"Reasoning: {result['decision']['reasoning'][:150]}...")
    
    if result['examples']:
        print(f"\nTop Example Preview:")
        print(f"  {result['examples'][0][:100]}...")
    
    # Test education RAG
    print("\n📍 Education RAG:")
    education_rag = AgenticRAG("teacher_supportive_v1")
    
    education_query = "Explain the water cycle"
    result = education_rag.retrieve(education_query)
    
    print(f"Query: {education_query}")
    print(f"Strategy: {result['decision']['strategy']}")
    print(f"Examples: {len(result['examples'])}")
    print(f"Reasoning: {result['decision']['reasoning'][:150]}...")
    
    if result['examples']:
        print(f"\nTop Example Preview:")
        print(f"  {result['examples'][0][:100]}...")


def test_edge_cases():
    """Test edge cases and unusual inputs."""
    print("\n" + "="*70)
    print("TESTING EDGE CASES")
    print("="*70)
    
    router = get_router()
    
    edge_cases = [
        "Hello",  # Greeting only
        "Can you help me?",  # Generic help
        "I need advice",  # Very vague
        "Tell me something",  # No context
        "What do you think?",  # Opinion question
        "",  # Empty string (will test error handling)
    ]
    
    for query in edge_cases:
        if not query:
            print(f"\n⚠️  Empty query test - skipping")
            continue
            
        result = router.route(query)
        print(f"\nQuery: '{query}'")
        print(f"  → Routed to: {result['persona_id']}")
        print(f"  → Confidence: {result['confidence']:.2f}")


def main():
    """Run comprehensive tests."""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║           PersonaReplica - Comprehensive Testing                ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Run all tests
        medical_accuracy = test_medical_routing()
        education_accuracy = test_education_routing()
        test_ambiguous_queries()
        test_rag_quality()
        test_edge_cases()
        
        # Final summary
        print("\n" + "="*70)
        print("FINAL SUMMARY")
        print("="*70)
        print(f"Medical Routing Accuracy: {medical_accuracy:.1f}%")
        print(f"Education Routing Accuracy: {education_accuracy:.1f}%")
        overall = (medical_accuracy + education_accuracy) / 2
        print(f"Overall Routing Accuracy: {overall:.1f}%")
        
        if overall >= 90:
            print("\n✅ Excellent! System is performing very well.")
        elif overall >= 75:
            print("\n⚠️  Good, but there's room for improvement.")
        else:
            print("\n❌ Needs improvement. Consider adjusting keywords or LLM prompts.")
        
        print("\n" + "="*70)
        print("✓ All tests completed!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
