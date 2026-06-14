#!/usr/bin/env python3
"""
Verify the setup: Check environment, dependencies, data, indices, and configuration.
"""

import os
import json
from pathlib import Path
import sys

def check_python_version():
    """Check Python version."""
    print("✓ Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (need 3.8+)")
        return False

def check_env_file():
    """Check if .env file exists and has required keys."""
    print("\n✓ Checking .env file...")
    env_path = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/.env")
    
    if not env_path.exists():
        print(f"  ✗ .env file not found at {env_path}")
        print("  → Create it with: GROQ_API_KEY=your_key_here")
        return False
    
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    if 'GROQ_API_KEY' not in env_content:
        print("  ✗ GROQ_API_KEY not set in .env")
        return False
    
    print("  ✓ .env file exists with GROQ_API_KEY")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    print("\n✓ Checking dependencies...")
    required_packages = [
        'fastapi',
        'sentence_transformers',
        'faiss',
        'rank_bm25',
        'torch',
        'groq',
        'pydantic',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n  Install with: pip install {' '.join(missing)}")
        return False
    return True

def check_data_files():
    """Check if raw data files exist."""
    print("\n✓ Checking data files...")
    base_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/data")
    
    required_files = [
        "raw/medical.jsonl",
        "raw/interview.jsonl",
        "processed/medical/processed.jsonl",
        "processed/interview/processed.jsonl"
    ]
    
    all_exist = True
    for filepath in required_files:
        full_path = base_dir / filepath
        if full_path.exists():
            print(f"  ✓ {filepath}")
        else:
            print(f"  ✗ {filepath} (missing)")
            all_exist = False
    
    return all_exist

def check_persona_files():
    """Check if persona profiles and indices exist."""
    print("\n✓ Checking persona files...")
    profiles_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/persona/profiles")
    indices_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/retrieval/indices")
    
    personas = ["doctor_empathetic_v1", "teacher_supportive_v1"]
    all_exist = True
    
    for persona in personas:
        profile_path = profiles_dir / f"{persona}.json"
        index_path = indices_dir / f"{persona}.index"
        texts_path = indices_dir / f"{persona}_texts.json"
        
        has_profile = profile_path.exists()
        has_index = index_path.exists()
        has_texts = texts_path.exists()
        
        if has_profile and has_index and has_texts:
            print(f"  ✓ {persona}")
        else:
            print(f"  ✗ {persona}")
            if not has_profile:
                print(f"    - Missing profile: {profile_path}")
            if not has_index:
                print(f"    - Missing index: {index_path}")
            if not has_texts:
                print(f"    - Missing texts: {texts_path}")
            all_exist = False
    
    return all_exist

def check_directory_structure():
    """Check if all required directories exist."""
    print("\n✓ Checking directory structure...")
    required_dirs = [
        "personareplica",
        "personareplica/api",
        "personareplica/data",
        "personareplica/data/raw",
        "personareplica/data/processed",
        "personareplica/scripts",
        "personareplica/engine",
        "personareplica/persona",
        "personareplica/persona/profiles",
        "personareplica/retrieval",
        "personareplica/retrieval/indices",
        "personareplica/memory"
    ]
    
    base_path = Path("e:/backup 2026/Projects/PersonaReplica")
    all_exist = True
    
    for dir_path in required_dirs:
        full_path = base_path / dir_path
        if full_path.exists() and full_path.is_dir():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path}")
            all_exist = False
    
    return all_exist

def main():
    """Run all verification checks."""
    print("="*60)
    print("PersonaReplica Setup Verification")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        (".env Configuration", check_env_file),
        ("Dependencies", check_dependencies),
        ("Directory Structure", check_directory_structure),
        ("Data Files", check_data_files),
        ("Persona Files", check_persona_files),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Error during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\n✓ Setup verification complete! Ready to run the engine.")
        print("\nNext steps:")
        print("  1. Run: python scripts/download_data.py")
        print("  2. Run: python scripts/preprocess.py")
        print("  3. Run: python scripts/build_persona.py")
        print("  4. Run: python engine/inference.py")
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())