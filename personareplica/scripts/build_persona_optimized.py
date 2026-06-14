#!/usr/bin/env python3
"""
Optimized persona building with progress tracking and batching.
Handles large datasets (100k+ examples) efficiently.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona.builder import PersonaBuilder


def main():
    """Build both personas from processed data with optimization."""
    print("Starting OPTIMIZED persona building for PersonaReplica...\n")
    print("⚠️  Note: Building with full dataset will take 10-20 minutes")
    print("    You can limit corpus size for testing by editing this script\n")
    
    builder = PersonaBuilder()
    
    # Option to limit corpus size for faster testing
    # Set to None for full dataset, or a number like 5000 for testing
    MAX_CORPUS_SIZE = None  # Change to 5000 for quick testing
    
    # Build medical doctor persona
    print("=" * 60)
    print("Building: Doctor Empathetic (Medical Domain)")
    print("=" * 60)
    
    medical_corpus_path = (
        Path(__file__).parent.parent / 
        "data" / "processed" / "medical" / "processed.jsonl"
    )
    
    if medical_corpus_path.exists():
        print(f"Loading corpus from: {medical_corpus_path}")
        medical_corpus = builder.load_corpus_from_jsonl(str(medical_corpus_path))
        print(f"Loaded {len(medical_corpus)} medical examples")
        
        # Optionally limit corpus size
        if MAX_CORPUS_SIZE and len(medical_corpus) > MAX_CORPUS_SIZE:
            print(f"⚠️  Limiting to {MAX_CORPUS_SIZE} examples for faster processing")
            medical_corpus = medical_corpus[:MAX_CORPUS_SIZE]
        
        builder.build_persona(
            persona_id="doctor_empathetic_v1",
            domain="medical",
            corpus=medical_corpus
        )
        print("✓ Doctor persona built successfully!\n")
    else:
        print(f"✗ Medical corpus not found at {medical_corpus_path}")
        print("  Run: python scripts/preprocess.py\n")
        return 1
    
    # Build education teacher persona
    print("=" * 60)
    print("Building: Teacher Supportive (Education Domain)")
    print("=" * 60)
    
    education_corpus_path = (
        Path(__file__).parent.parent / 
        "data" / "processed" / "education" / "processed.jsonl"
    )
    
    if education_corpus_path.exists():
        print(f"Loading corpus from: {education_corpus_path}")
        education_corpus = builder.load_corpus_from_jsonl(
            str(education_corpus_path)
        )
        print(f"Loaded {len(education_corpus)} education examples")
        
        # Optionally limit corpus size
        if MAX_CORPUS_SIZE and len(education_corpus) > MAX_CORPUS_SIZE:
            print(f"⚠️  Limiting to {MAX_CORPUS_SIZE} examples for faster processing")
            education_corpus = education_corpus[:MAX_CORPUS_SIZE]
        
        builder.build_persona(
            persona_id="teacher_supportive_v1",
            domain="education",
            corpus=education_corpus
        )
        print("✓ Teacher persona built successfully!\n")
    else:
        print(f"✗ Education corpus not found at {education_corpus_path}")
        print("  Run: python scripts/preprocess.py\n")
        return 1
    
    print("=" * 60)
    print("Persona Building Completed!")
    print("=" * 60)
    print("\nPersonas ready:")
    print(f"  ✓ doctor_empathetic_v1 ({len(medical_corpus)} examples)")
    print(f"  ✓ teacher_supportive_v1 ({len(education_corpus)} examples)")
    print("\nNext step: python scripts/verify_setup.py")
    print("\nFor comprehensive testing: python scripts/test_comprehensive.py")
    
    return 0


if __name__ == "__main__":
    exit(main())
