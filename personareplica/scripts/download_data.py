#!/usr/bin/env python3
"""
Download HuggingFace datasets for multiple domains.
"""

import os
import json
from pathlib import Path
from datasets import load_dataset

# Domain dataset mappings from HuggingFace
DOMAIN_DATASETS = {
    "medical": ("lavita/ChatDoctor-HealthCareMagic-100k", None),
    "education": ("OpenAssistant/oasst2", None),
    "support": ("bitext/Bitext-customer-support-llm-chatbot-training-dataset", None),
    "interview": ("anon8231489123/ShareGPT_Vicuna_unfiltered", None),
    "mentorship": ("anon8231489123/ShareGPT_Vicuna_unfiltered", None),
}

# For this MVP, we focus on medical and education
ACTIVE_DOMAINS = {
    "medical": DOMAIN_DATASETS["medical"],
    "education": DOMAIN_DATASETS["education"],
}

def download_domain_dataset(domain: str):
    """Download a dataset for the specified domain."""
    print(f"Downloading {domain} dataset...")
    
    if domain not in ACTIVE_DOMAINS:
        print(f"Domain '{domain}' not configured. Available: {list(ACTIVE_DOMAINS.keys())}")
        return None
    
    dataset_id, config_name = ACTIVE_DOMAINS[domain]
    
    try:
        # Try to load the dataset
        print(f"  Attempting to load '{dataset_id}'...")
        if config_name:
            dataset = load_dataset(dataset_id, config_name, split="train")
        else:
            dataset = load_dataset(dataset_id, split="train")
        
        print(f"  [OK] Loaded {domain} dataset with {len(dataset)} examples")
        return dataset
    
    except Exception as e:
        print(f"  [FAILED] Could not load from HuggingFace: {e}")
        print(f"  Creating dummy {domain} dataset for demonstration...")
        return create_dummy_dataset(domain)

def create_dummy_dataset(domain: str):
    """Create dummy dataset for a domain."""
    if domain == "medical":
        dummy_data = [
            {
                "input": "I have a fever and headache",
                "response": "I understand you're feeling unwell. Let me ask a few questions to better understand your symptoms. How long have you had the fever?"
            },
            {
                "input": "What are the symptoms of diabetes?",
                "response": "Common symptoms include increased thirst, frequent urination, unexplained weight loss, and fatigue. However, I recommend consulting with a healthcare provider for proper diagnosis."
            },
            {
                "input": "I'm feeling anxious about my test results",
                "response": "It's completely normal to feel anxious waiting for medical results. Would you like to talk about what's specifically worrying you?"
            }
        ]
    elif domain == "education":
        dummy_data = [
            {
                "input": "Can you explain photosynthesis?",
                "response": "Photosynthesis is the process plants use to convert sunlight into energy. Let me break it down: plants take in carbon dioxide and water, then use sunlight to create glucose and oxygen. What aspect would you like to understand better?"
            },
            {
                "input": "I'm struggling with algebra",
                "response": "Algebra can be challenging at first, but let's work through it together. What specific concept are you finding difficult? Is it solving equations, working with variables, or something else?"
            },
            {
                "input": "How do I improve my essay writing?",
                "response": "Great question! Strong essays have a clear structure: introduction with thesis, body paragraphs with evidence, and a conclusion. Let's start by looking at your thesis statement. What's the main argument you want to make?"
            }
        ]
    else:
        dummy_data = [
            {"input": "Hello", "response": "Hi there! How can I help you today?"}
        ]
    
    print(f"  Created {len(dummy_data)} dummy examples")
    return dummy_data

def save_dataset_as_jsonl(dataset, filepath: str):
    """Save dataset to JSONL format."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    saved_count = 0
    with open(filepath, 'w', encoding='utf-8') as f:
        for record in dataset:
            # Extract input and response fields (handle different formats)
            if isinstance(record, dict):
                # ChatDoctor format: instruction, input, output
                if "instruction" in record and "output" in record:
                    instruction = record.get("instruction", "").strip()
                    input_text = record.get("input", "").strip()
                    # Combine instruction and input if both exist
                    if input_text:
                        full_input = f"{instruction} {input_text}".strip()
                    else:
                        full_input = instruction
                    item = {
                        "input": full_input,
                        "response": record["output"]
                    }
                # Standard input/response format
                elif "input" in record and "response" in record:
                    item = {
                        "input": record["input"],
                        "response": record["response"]
                    }
                # Question/answer format
                elif "question" in record and "answer" in record:
                    item = {
                        "input": record["question"],
                        "response": record["answer"]
                    }
                # Text field only
                elif "text" in record:
                    item = {
                        "input": record.get("text", ""),
                        "response": record.get("text", "")
                    }
                else:
                    # Skip records we can't parse
                    continue
                
                # Only save if both fields are non-empty
                if item["input"].strip() and item["response"].strip():
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
                    saved_count += 1
            else:
                continue
    
    print(f"Saved {saved_count} records to {filepath}")

def main():
    """Download datasets for all active domains."""
    print("="*60)
    print("Downloading Datasets for PersonaReplica")
    print("="*60 + "\n")
    
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    for domain in ACTIVE_DOMAINS.keys():
        print(f"\n{domain.upper()} DOMAIN")
        print("-" * 40)
        
        # Download dataset
        dataset = download_domain_dataset(domain)
        
        if dataset:
            # Save to JSONL
            output_path = data_dir / f"{domain}.jsonl"
            save_dataset_as_jsonl(dataset, str(output_path))
            print(f"  Saved to: {output_path}\n")
        else:
            print(f"  [SKIP] Could not download {domain} dataset\n")
    
    print("="*60)
    print("Dataset Download Completed!")
    print("="*60)
    print(f"\nFiles saved to: {data_dir}")
    print("\nNext step: python scripts/preprocess.py")

if __name__ == "__main__":
    main()