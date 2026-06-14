#!/usr/bin/env python3
"""
Full setup script for PersonaReplica with Education domain.

This script runs the complete pipeline:
1. Download datasets (medical + education)
2. Preprocess data
3. Build personas
4. Verify setup
5. Run tests

Usage:
    python scripts/run_full_setup.py [--skip-download] [--skip-tests]
"""

import sys
import subprocess
from pathlib import Path
import argparse


def run_script(script_name: str, description: str) -> bool:
    """Run a Python script and return success status."""
    print("\n" + "=" * 70)
    print(f"STEP: {description}")
    print("=" * 70)
    print(f"Running: python scripts/{script_name}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, f"scripts/{script_name}"],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✓ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {description} failed with error!")
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error in {description}!")
        print(f"Error: {e}")
        return False


def main():
    """Run the full setup pipeline."""
    parser = argparse.ArgumentParser(
        description="Run full PersonaReplica setup pipeline"
    )
    parser.add_argument(
        '--skip-download',
        action='store_true',
        help='Skip dataset download step (use existing data)'
    )
    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='Skip final testing step'
    )
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║           PersonaReplica - Full Setup Pipeline                  ║
    ║           Education + Medical Domain Implementation             ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Change to personareplica directory
    base_dir = Path(__file__).parent.parent
    print(f"Working directory: {base_dir}\n")
    
    steps = []
    
    # Step 1: Download datasets
    if not args.skip_download:
        steps.append(("download_data.py", "Download Datasets"))
    else:
        print("\n⏭  Skipping dataset download (--skip-download flag)\n")
    
    # Step 2: Preprocess data
    steps.append(("preprocess.py", "Preprocess Data"))
    
    # Step 3: Build personas
    steps.append(("build_persona.py", "Build Personas"))
    
    # Step 4: Verify setup
    steps.append(("verify_setup.py", "Verify Setup"))
    
    # Step 5: Run tests
    if not args.skip_tests:
        steps.append(("test_agentic_rag.py", "Run Tests"))
    else:
        print("\n⏭  Skipping tests (--skip-tests flag)\n")
    
    # Execute pipeline
    success = True
    completed_steps = 0
    total_steps = len(steps)
    
    for script_name, description in steps:
        if not run_script(script_name, description):
            success = False
            print(f"\n❌ Pipeline failed at step: {description}")
            print(f"   Completed: {completed_steps}/{total_steps} steps")
            break
        completed_steps += 1
    
    # Final summary
    print("\n" + "=" * 70)
    if success:
        print("SUCCESS: Full Setup Pipeline Completed!")
        print("=" * 70)
        print("""
        ✓ All steps completed successfully!
        
        Your PersonaReplica system is now ready with:
        
        Personas:
          • doctor_empathetic_v1 (Medical domain)
          • teacher_supportive_v1 (Education domain)
        
        Files created:
          • Persona profiles in persona/profiles/
          • FAISS indices in retrieval/indices/
          • Processed data in data/processed/
        
        Next steps:
          1. Test with custom queries: python scripts/test_engine.py
          2. Integrate into your application
          3. Review EDUCATION_SETUP_GUIDE.md for more info
        
        """)
    else:
        print("FAILED: Setup Pipeline Incomplete")
        print("=" * 70)
        print(f"""
        ✗ Pipeline stopped at step {completed_steps + 1}/{total_steps}
        
        Troubleshooting:
          1. Check error messages above
          2. Verify dependencies: pip install -r requirements.txt
          3. Check .env file has GROQ_API_KEY
          4. Review EDUCATION_SETUP_GUIDE.md
          5. Try running failed step individually
        
        Run individual steps:
          python scripts/download_data.py
          python scripts/preprocess.py
          python scripts/build_persona.py
          python scripts/verify_setup.py
          python scripts/test_agentic_rag.py
        """)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
