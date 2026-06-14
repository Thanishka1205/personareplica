# PersonaReplica: Step-by-Step Setup Guide

**Goal**: Get the agentic medical & interview coach system running end-to-end.

**Time Estimate**: 30-45 minutes (including dependency installation)

---

## ✅ Pre-Setup Checklist

- [ ] Groq API key ready (https://console.groq.com/keys)
- [ ] Python 3.10+ installed (`python --version`)
- [ ] At least 2GB free disk space (for FAISS indices + data)
- [ ] Internet connection (for downloading datasets & models)

---

## 📋 Phase 1: Environment Setup (5-10 min)

### Step 1.1: Navigate to project

```bash
cd e:/backup\ 2026/Projects/PersonaReplica/personareplica
```

### Step 1.2: Create Python virtual environment

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

**Verify**: Prompt should show `(venv)` prefix

### Step 1.3: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 1.4: Install dependencies

```bash
pip install -r requirements.txt
```

⏱️ **This may take 5-10 minutes** (especially torch & transformers)

**Expected output**:
```
Successfully installed fastapi-0.104.1 sentence-transformers-2.2.2 faiss-cpu-1.8.0 ... (17 packages)
```

### Step 1.5: Create .env file

```bash
# Copy template
cp .env.example .env

# Edit .env with your editor (nano, vim, or VS Code)
# Add your Groq API key:
# GROQ_API_KEY=gsk_your_key_here
```

**Verify .env exists**:
```bash
cat .env
# Should show GROQ_API_KEY=gsk_...
```

---

## 📥 Phase 2: Data Download & Preprocessing (5-10 min)

### Step 2.1: Download datasets

```bash
python scripts/download_data.py
```

**Expected output**:
```
Starting dataset download for PersonaReplica...
Downloading medical dataset...
Loaded med_dialog dataset with N examples
Downloading interview dataset...
Loaded interview dataset with N examples

Saved dataset to e:/backup 2026/Projects/PersonaReplica/personareplica/data/raw/medical.jsonl
Saved dataset to e:/backup 2026/Projects/PersonaReplica/personareplica/data/raw/interview.jsonl

Dataset download completed!
```

**Verify files created**:
```bash
ls data/raw/
# Should show: medical.jsonl, interview.jsonl
```

### Step 2.2: Preprocess data

```bash
python scripts/preprocess.py
```

**Expected output**:
```
Starting data preprocessing for PersonaReplica...
Processing e:/backup 2026/Projects/PersonaReplica/personareplica/data/raw/medical.jsonl...
Saved 100 normalized records to e:/backup 2026/Projects/PersonaReplica/personareplica/data/processed/medical/processed.jsonl
Processing e:/backup 2026/Projects/PersonaReplica/personareplica/data/raw/interview.jsonl...
Saved 75 normalized records to e:/backup 2026/Projects/PersonaReplica/personareplica/data/processed/interview/processed.jsonl

Preprocessing completed!
```

**Verify**:
```bash
ls data/processed/
# Should show: medical/, interview/
ls data/processed/medical/
# Should show: processed.jsonl
```

---

## 🏗️ Phase 3: Persona Building (10-15 min)

### Step 3.1: Build persona indices

```bash
python scripts/build_persona.py
```

**Expected output**:
```
Loading sentence embeddings model...
Building persona: doctor_empathetic_v1
  Corpus size: 100 examples
  Style metrics computed:
    avg_sentence_length: 12.50
    empathy_score: 0.95
    question_rate: 0.09
    formality_score: 0.45
    lexical_diversity: 0.52
    hedging_rate: 0.61
    avg_response_length: 150.00
  Embedding 100 responses...
  Profile saved to e:/backup 2026/Projects/PersonaReplica/personareplica/persona/profiles/doctor_empathetic_v1.json
  Index saved to e:/backup 2026/Projects/PersonaReplica/personareplica/retrieval/indices/doctor_empathetic_v1.index
  Texts saved to e:/backup 2026/Projects/PersonaReplica/personareplica/retrieval/indices/doctor_empathetic_v1_texts.json

Building persona: interview_coach_v1
  Corpus size: 75 examples
  Style metrics computed:
    avg_sentence_length: 14.20
    empathy_score: 0.55
    question_rate: 0.28
    formality_score: 0.72
    lexical_diversity: 0.71
    hedging_rate: 0.25
    avg_response_length: 180.00
  ...

Persona building completed!
```

**Verify files created**:
```bash
ls persona/profiles/
# Should show: doctor_empathetic_v1.json, interview_coach_v1.json

ls retrieval/indices/
# Should show: doctor_empathetic_v1.index, doctor_empathetic_v1_texts.json, 
#             interview_coach_v1.index, interview_coach_v1_texts.json
```

**Check profile contents**:
```bash
# On Windows (PowerShell)
Get-Content persona/profiles/doctor_empathetic_v1.json | ConvertFrom-Json | Format-Table

# On Linux/Mac
cat persona/profiles/doctor_empathetic_v1.json | python -m json.tool
```

---

## ✅ Phase 4: Verify Setup (2-3 min)

### Step 4.1: Run verification script

```bash
python scripts/verify_setup.py
```

**Expected output** (all checks should ✓ PASS):
```
============================================================
PersonaReplica Setup Verification
============================================================
✓ Checking Python version...
  ✓ Python 3.10.11
✓ Checking .env file...
  ✓ .env file exists with GROQ_API_KEY
✓ Checking dependencies...
  ✓ fastapi
  ✓ sentence_transformers
  ✓ faiss
  ✓ rank_bm25
  ✓ torch
  ✓ groq
  ✓ pydantic
  ✓ dotenv
✓ Checking directory structure...
  ✓ personareplica
  ✓ personareplica/api
  ✓ personareplica/data
  ...
✓ Checking data files...
  ✓ raw/medical.jsonl
  ✓ raw/interview.jsonl
  ✓ processed/medical/processed.jsonl
  ✓ processed/interview/processed.jsonl
✓ Checking persona files...
  ✓ doctor_empathetic_v1
  ✓ interview_coach_v1

============================================================
SUMMARY
============================================================
✓ PASS: Python Version
✓ PASS: .env Configuration
✓ PASS: Dependencies
✓ PASS: Directory Structure
✓ PASS: Data Files
✓ PASS: Persona Files

Total: 6/6 passed

✓ Setup verification complete! Ready to run the engine.

Next steps:
  1. Run: python scripts/test_agentic_rag.py
  2. Run: python scripts/test_engine.py
```

⚠️ **If any check fails**: Review the error and fix before proceeding.

---

## 🧪 Phase 5: Test Routing & RAG (5 min)

### Step 5.1: Test router and retrieval

```bash
python scripts/test_agentic_rag.py
```

**Expected output**:
```
======================================================================
PersonaReplica AgenticRAG Test
======================================================================
Tests routing and RAG decision making:
  - Router: Select best persona for query
  - RAG: Decide retrieval strategy and execute

======================================================================
TESTING AGENTIC ROUTER
======================================================================

Query: I have a fever and headache, what should I do?
  Routed to: doctor_empathetic_v1
  Confidence: 0.95
  Reasoning: High medical symptom keywords detected

Query: How do I solve a dynamic programming problem in an interview?
  Routed to: interview_coach_v1
  Confidence: 0.92
  Reasoning: Interview and technical language detected

...

======================================================================
TESTING AGENTIC RAG - MEDICAL PERSONA
======================================================================

Query: I have a severe headache
  Strategy: semantic
  Num Examples: 5
  Rerank: false
  Reasoning: Direct symptom query, semantic search optimal
  Examples Retrieved: 5
  Top Example: I have a fever and headache. I'm quite worried...

...

======================================================================
✓ All tests completed!
======================================================================
```

**What to verify**:
- ✓ Router correctly identifies medical vs interview queries
- ✓ RAG retrieves examples per query
- ✓ Strategy decisions vary by query type
- ✓ No errors or exceptions

---

## 🚀 Phase 6: Run Full Pipeline (10 min)

### Step 6.1: Test end-to-end engine

```bash
python scripts/test_engine.py
```

**Expected output** (for each query):
```
==============================================================
QUERY: I've been experiencing severe headaches and a fever for three days. What could be wrong?
==============================================================

[STEP 1] Routing query...
  → Routed to: doctor_empathetic_v1 (confidence: 0.95)

[STEP 2] Retrieving examples...
  → Retrieved 5 examples
  → Strategy: semantic

[STEP 3] Building persona prompt...
  → System prompt built (1450 chars)

[STEP 4] Generating response with Groq...
  → Response generated (234 chars)

[STEP 5] Scoring response accuracy...
  → Accuracy score: 0.85
  ✓ PASS (> 0.72 threshold)

==============================================================
FINAL RESPONSE:
==============================================================
I understand you're experiencing a concerning combination of symptoms. 
A fever and headache together could indicate several things - commonly a viral 
infection, like the flu. However, it might also be a sign of something that needs 
more attention, such as a bacterial infection or other condition...

Accuracy Score: 0.85
```

**What to verify**:
- ✓ All 5 steps complete without errors
- ✓ Routing identifies correct persona
- ✓ Examples retrieved from correct domain
- ✓ Response contains persona-appropriate language
- ✓ Accuracy score > 0.72 (no flags)

⏱️ **Note**: First run may take 30+ seconds as models are loaded into memory. Subsequent runs are faster.

---

## 🎉 Phase 7: Success Verification

If all steps completed successfully, you now have:

✅ **Working agentic pipeline** with:
- AgenticRouter (persona selection)
- AgenticRAG (strategy decision + retrieval)
- PromptBuilder (style-aware prompts)
- Groq LLM generation
- PersonaScorer (accuracy measurement)

✅ **Two fully functional personas**:
- Doctor (medical, empathetic)
- Interview Coach (technical, structured)

✅ **Complete test coverage**:
- Router accuracy tests
- RAG decision tests
- Full pipeline e2e tests

✅ **Production-ready code structure** with:
- Clear separation of concerns
- Modular architecture
- Extensive error handling
- Configurable thresholds

---

## 🐛 Troubleshooting

### Problem: "GROQ_API_KEY not found"
**Solution**:
```bash
# Check .env file
cat .env

# Verify key is set correctly
echo $GROQ_API_KEY  # Should print: gsk_...

# If not set, edit .env and reload shell
source venv/Scripts/activate  # Windows: venv\Scripts\activate
```

### Problem: "ModuleNotFoundError: No module named 'sentence_transformers'"
**Solution**:
```bash
pip install -r requirements.txt
```

### Problem: "Slow responses / Timeout"
**Reasons**:
- First request loads models (normal, ~30s)
- Large responses take longer
- Groq API may be slow

**Solution**: Retry after a few seconds

### Problem: "FAISS index not found"
**Solution**:
```bash
# Rebuild personas
python scripts/build_persona.py

# Verify
ls retrieval/indices/
```

### Problem: "Low accuracy scores (< 0.72)"
**Solution**:
- Response may still be good despite low score
- Try increasing num_examples in RAG decision
- Check persona style metrics in profile JSON

### Problem: "Cross-encoder reranking error"
**Solution**:
- Not critical (fallback to no reranking)
- Try: `pip install sentence-transformers --upgrade`

---

## 📊 Performance Expectations

| Operation | Time | Details |
|-----------|------|---------|
| Download data | 2-3 min | Depends on internet |
| Preprocess | 1 min | Normalize 200 records |
| Build personas | 3-5 min | Embed corpus + build FAISS |
| Verify setup | 10 sec | Check files & dependencies |
| Test router | 30 sec | 4 queries with LLM routing |
| Test engine | 5-10 min | 2 queries with full pipeline |
| **Total** | **20-40 min** | Varies by internet/hardware |

**Single query inference**: 5-8 seconds (with 3 LLM calls)

---

## 📚 After Setup: What's Next?

### To test custom queries:

```python
# Create a simple test script
from engine.inference import PersonaEngine

engine = PersonaEngine()
result = engine.process("Your custom query here")
print(result["final_response"])
print(f"Score: {result['accuracy_score']:.2f}")
```

### To add a new persona:

1. Get corpus data (JSONL format)
2. Add to `REGISTERED_PERSONAS` in `agentic_router.py`
3. Save to `data/raw/` and preprocess
4. Run `python scripts/build_persona.py`

### To customize style metrics:

Edit `persona/builder.py` → `extract_style_metrics()`

---

## ✅ Final Checklist

- [ ] Virtual environment activated (`(venv)` in prompt)
- [ ] Dependencies installed (`pip install -r requirements.txt` ✓)
- [ ] .env file created with GROQ_API_KEY
- [ ] Data downloaded (medical.jsonl, interview.jsonl)
- [ ] Data preprocessed (processed.jsonl files)
- [ ] Personas built (profiles JSON + indices)
- [ ] Verification passed (verify_setup.py ✓)
- [ ] Router test passed (test_agentic_rag.py ✓)
- [ ] Full pipeline test passed (test_engine.py ✓)

**If all boxes checked**: ✅ **You're ready to use PersonaReplica!**

---

## 🆘 Getting Help

If you encounter issues:

1. **Check the README**: `personareplica/README.md`
2. **Review implementation summary**: `IMPLEMENTATION_SUMMARY.md`
3. **Check error messages carefully** - they usually indicate the fix
4. **Run verify_setup.py** - it diagnoses most problems
5. **Ask a clarifying question** - I'm here to help!

---

## 🎓 Learning Path

After setup, explore:

1. **Understanding personas**: `cat persona/profiles/doctor_empathetic_v1.json`
2. **How routing works**: Read `engine/agentic_router.py`
3. **RAG strategy**: Read `retrieval/agentic_rag.py`
4. **Prompt building**: Read `engine/prompt_builder.py`
5. **Scoring logic**: Read `persona/scorer.py`
6. **Full pipeline**: Read `engine/inference.py`

---

**Ready to start? Begin with Phase 1, Step 1.1!** 🚀
