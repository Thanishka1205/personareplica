# Education Persona Setup Guide

## Quick Start

This guide walks you through setting up PersonaReplica with the education domain using the OpenAssistant/oasst2 dataset.

## Prerequisites

1. Python 3.8+
2. Virtual environment activated
3. Dependencies installed (see main README.md)
4. API keys configured in `.env`:
   - `GROQ_API_KEY` for routing and RAG decisions
   - `HUGGINGFACE_TOKEN` for dataset access (optional, public datasets)

## Step-by-Step Setup

### 1. Download Education Dataset

```bash
cd personareplica
python scripts/download_data.py
```

**What this does**:
- Downloads OpenAssistant/oasst2 dataset for education domain
- Downloads ChatDoctor-HealthCareMagic-100k for medical domain
- Saves raw data to `data/raw/education.jsonl` and `data/raw/medical.jsonl`
- Falls back to dummy data if HuggingFace download fails

**Expected output**:
```
================================================================
Downloading Datasets for PersonaReplica
================================================================

MEDICAL DOMAIN
----------------------------------------
Downloading medical dataset...
  Attempting to load 'lavita/ChatDoctor-HealthCareMagic-100k'...
  [OK] Loaded medical dataset with XXXXX examples
Saved XXXXX records to e:/backup 2026/Projects/PersonaReplica/personareplica/data/raw/medical.jsonl

EDUCATION DOMAIN
----------------------------------------
Downloading education dataset...
  Attempting to load 'OpenAssistant/oasst2'...
  [OK] Loaded education dataset with XXXXX examples
Saved XXXXX records to e:/backup 2026/Projects/PersonaReplica/personareplica/data/raw/education.jsonl
```

### 2. Preprocess the Data

```bash
python scripts/preprocess.py
```

**What this does**:
- Normalizes raw JSONL data to standard schema
- Extracts input/response pairs
- Assigns domain and persona_id
- Saves to `data/processed/{domain}/processed.jsonl`

**Expected output**:
```
Starting data preprocessing for PersonaReplica...
Processing e:/backup 2026/.../data/raw/medical.jsonl...
Saved XXX normalized records to e:/backup 2026/.../data/processed/medical/processed.jsonl
Processing e:/backup 2026/.../data/raw/education.jsonl...
Saved XXX normalized records to e:/backup 2026/.../data/processed/education/processed.jsonl

Preprocessing completed!
```

### 3. Build Personas

```bash
python scripts/build_persona.py
```

**What this does**:
- Loads processed datasets
- Extracts style metrics (7 dimensions)
- Generates embeddings using SentenceTransformer
- Builds FAISS indices for semantic search
- Saves persona profiles and indices

**Expected output**:
```
Starting persona building for PersonaReplica...

============================================================
Building: Doctor Empathetic (Medical Domain)
============================================================
Loading corpus from: .../data/processed/medical/processed.jsonl
Loaded XXX medical examples

Building persona: doctor_empathetic_v1
  Corpus size: XXX examples
  Style metrics computed:
    avg_sentence_length: X.XXX
    empathy_score: X.XXX
    question_rate: X.XXX
    formality_score: X.XXX
    lexical_diversity: X.XXX
    hedging_rate: X.XXX
    avg_response_length: XX.XXX
  Embedding XXX responses...
  Profile saved to .../persona/profiles/doctor_empathetic_v1.json
  Index saved to .../retrieval/indices/doctor_empathetic_v1.index
  Texts saved to .../retrieval/indices/doctor_empathetic_v1_texts.json
✓ Doctor persona built successfully!

============================================================
Building: Teacher Supportive (Education Domain)
============================================================
Loading corpus from: .../data/processed/education/processed.jsonl
Loaded XXX education examples

Building persona: teacher_supportive_v1
  Corpus size: XXX examples
  Style metrics computed:
    [similar output]
✓ Teacher persona built successfully!

============================================================
Persona Building Completed!
============================================================

Personas ready:
  ✓ doctor_empathetic_v1
  ✓ teacher_supportive_v1

Next step: python scripts/verify_setup.py
```

### 4. Verify Setup

```bash
python scripts/verify_setup.py
```

**What this does**:
- Checks that all required files exist
- Validates persona profiles
- Verifies FAISS indices
- Tests basic loading functionality

**Expected output**:
```
============================================================
PersonaReplica Setup Verification
============================================================

✓ Checking persona files...
  ✓ doctor_empathetic_v1
  ✓ teacher_supportive_v1

✓ Checking FAISS indices...
  ✓ doctor_empathetic_v1.index
  ✓ teacher_supportive_v1.index

✓ All checks passed!

============================================================
Setup Verification Complete
============================================================
```

### 5. Test the System

```bash
python scripts/test_agentic_rag.py
```

**What this tests**:
- Router: Persona selection for different query types
- RAG: Retrieval strategy decisions
- Medical domain queries → doctor_empathetic_v1
- Education domain queries → teacher_supportive_v1

**Sample queries tested**:
- Medical: "I have a fever and headache"
- Education: "Can you explain photosynthesis?"
- Education: "How do I solve quadratic equations?"

## File Structure After Setup

```
personareplica/
├── data/
│   ├── raw/
│   │   ├── medical.jsonl          # Raw medical data
│   │   └── education.jsonl        # Raw education data
│   └── processed/
│       ├── medical/
│       │   └── processed.jsonl    # Normalized medical data
│       └── education/
│           └── processed.jsonl    # Normalized education data
│
├── persona/
│   └── profiles/
│       ├── doctor_empathetic_v1.json      # Medical persona profile
│       └── teacher_supportive_v1.json     # Education persona profile
│
└── retrieval/
    └── indices/
        ├── doctor_empathetic_v1.index         # Medical FAISS index
        ├── doctor_empathetic_v1_texts.json    # Medical reference texts
        ├── teacher_supportive_v1.index        # Education FAISS index
        └── teacher_supportive_v1_texts.json   # Education reference texts
```

## Troubleshooting

### Issue: Dataset download fails

**Solution**: The system will automatically fall back to dummy data. You can:
1. Check your internet connection
2. Verify HuggingFace dataset availability
3. Use the dummy data for testing (3 examples per domain)

### Issue: "GROQ_API_KEY not found"

**Solution**: 
1. Create a `.env` file in the `personareplica/` directory
2. Add your Groq API key: `GROQ_API_KEY=your_key_here`
3. Get a free key at: https://console.groq.com/

### Issue: Module not found errors

**Solution**:
```bash
pip install -r requirements.txt
```

Make sure your virtual environment is activated.

### Issue: FAISS import errors

**Solution**:
```bash
# CPU version
pip install faiss-cpu

# Or GPU version (if you have CUDA)
pip install faiss-gpu
```

### Issue: Path errors on Windows

**Solution**: The code uses forward slashes in paths. This should work on Windows, but if you encounter issues:
1. Check that the base directory path is correct
2. Ensure no special characters in the path
3. Run from within the `personareplica/` directory

## Testing Individual Components

### Test Router Only

```bash
cd personareplica/engine
python agentic_router.py
```

### Test RAG Only

```bash
cd personareplica/retrieval
python agentic_rag.py
```

### Test Prompt Builder Only

```bash
cd personareplica/engine
python prompt_builder.py
```

### Test Persona Scorer Only

```bash
cd personareplica/persona
python scorer.py
```

## Expected Persona Characteristics

### teacher_supportive_v1

**Style Metrics** (approximate values, actual values depend on corpus):
- `avg_sentence_length`: 12-15 words
- `empathy_score`: 0.1-0.3 (supportive but not overly emotional)
- `question_rate`: 0.3-0.5 (high - encourages thinking)
- `formality_score`: 0.2-0.4 (semi-formal)
- `lexical_diversity`: 0.7-0.9 (varied vocabulary)
- `hedging_rate`: 0.1-0.3 (some uncertainty for open questions)
- `avg_response_length`: 20-40 words

**Example Responses**:
- "That's a great question! Let me break down photosynthesis step by step. What do you already know about how plants make their food?"
- "I see you're working on quadratic equations. Let's start with the basics. Can you tell me what form this equation is in?"
- "Don't worry, essay writing takes practice! Let's begin with your thesis statement. What's the main point you want to argue?"

### doctor_empathetic_v1

**Style Metrics**:
- Higher empathy score (0.3-0.5)
- Higher hedging rate (0.3-0.5 - medical caution)
- Lower question rate (0.2-0.3)
- Professional formality (0.5-0.7)

## Next Steps

Once setup is complete:

1. **Integrate into your application** - Use the inference engine
2. **Add more domains** - Follow the same pattern for support, mentorship, etc.
3. **Fine-tune personas** - Adjust style metrics or add custom profiles
4. **Scale the system** - Add more examples to corpora for better performance

## References

- Main README: `README.md`
- Migration Guide: `MIGRATION_TO_EDUCATION.md`
- Project Map: `PROJECT_MAP.md`
- API Documentation: See individual module docstrings
