#!/usr/bin/env python3
"""
Build personas script: Extract style metrics and create FAISS indices.

This script wraps persona/builder.py and orchestrates the persona building
process for both medical and interview coach domains.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona.builder import PersonaBuilder


def main():
    """Build both personas from processed data."""
    print("Starting persona building for PersonaReplica...\n")
    
    builder = PersonaBuilder()
    
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
    print("  ✓ doctor_empathetic_v1")
    print("  ✓ teacher_supportive_v1")
    print("\nNext step: python scripts/verify_setup.py")
    
    return 0


if __name__ == "__main__":
    exit(main())
