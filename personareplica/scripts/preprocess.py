#!/usr/bin/env python3
"""
Preprocess raw JSONL files into normalized schema.
"""

import json
import os
from pathlib import Path

def normalize_medical_record(record):
    """Normalize a medical record to the standard schema."""
    # ChatDoctor format: instruction, input, output
    # Fallback: input/response, question/answer formats
    instruction = record.get('instruction', '').strip()
    input_text = record.get('input', '').strip()
    output_text = record.get('output', '').strip()
    
    # For ChatDoctor: combine instruction+input as "input", output as "response"
    if instruction and output_text:
        full_input = f"{instruction.rstrip('?')}? {input_text}" if input_text else instruction
        response_text = output_text
    else:
        # Fallback to other formats
        full_input = record.get('input') or record.get('question') or record.get('prompt') or ''
        response_text = record.get('response') or record.get('answer') or record.get('output') or ''
    
    # Clean up text
    full_input = str(full_input).strip()
    response_text = str(response_text).strip()
    
    # Only include if both fields are non-empty
    if not full_input or not response_text:
        return None
    
    return {
        "input": full_input,
        "response": response_text,
        "domain": "medical",
        "persona_id": "doctor_empathetic_v1"
    }

def normalize_education_record(record):
    """Normalize an education record to the standard schema."""
    # OpenAssistant format may have different fields
    input_text = record.get('input') or record.get('question') or record.get('prompt') or record.get('text') or ''
    response_text = record.get('response') or record.get('answer') or record.get('output') or ''
    
    input_text = str(input_text).strip()
    response_text = str(response_text).strip()
    
    # Only include if both fields are non-empty
    if not input_text or not response_text:
        return None
    
    return {
        "input": input_text,
        "response": response_text,
        "domain": "education",
        "persona_id": "teacher_supportive_v1"
    }

def process_dataset(input_path, output_path, normalize_func):
    """Process a single dataset file."""
    print(f"Processing {input_path}...")
    
    normalized_records = []
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    normalized = normalize_func(record)
                    normalized_records.append(normalized)
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping invalid JSON on line {line_num}: {e}")
                except Exception as e:
                    print(f"Warning: Error processing record on line {line_num}: {e}")
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_path}")
        return False
    
    # Save normalized data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for record in normalized_records:
            f.write(json.dumps(record) + '\n')
    
    print(f"Saved {len(normalized_records)} normalized records to {output_path}")
    return True

def main():
    """Main preprocessing function."""
    print("Starting data preprocessing for PersonaReplica...")
    
    base_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica")
    raw_dir = base_dir / "data" / "raw"
    processed_dir = base_dir / "data" / "processed"
    
    # Process medical dataset
    medical_raw = raw_dir / "medical.jsonl"
    medical_processed = processed_dir / "medical" / "processed.jsonl"
    process_dataset(str(medical_raw), str(medical_processed), normalize_medical_record)
    
    # Process education dataset
    education_raw = raw_dir / "education.jsonl"
    education_processed = processed_dir / "education" / "processed.jsonl"
    process_dataset(str(education_raw), str(education_processed), normalize_education_record)
    
    print("\nPreprocessing completed!")

if __name__ == "__main__":
    main()