# PersonaReplica - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites Check
```bash
# 1. Python 3.8+ installed?
python --version

# 2. In the right directory?
cd "e:/backup 2026/Projects/PersonaReplica/personareplica"

# 3. Virtual environment activated?
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Dependencies installed?
pip install -r requirements.txt

# 5. API key configured?
# Create .env file with: GROQ_API_KEY=your_key_here
```

### One-Command Setup
```bash
python scripts/run_full_setup.py
```

This automatically:
- ✅ Downloads datasets (medical + education)
- ✅ Preprocesses data
- ✅ Builds personas
- ✅ Verifies setup
- ✅ Runs tests

**Time**: 5-15 minutes (depending on dataset download)

---

## 📚 What You Get

### Two Personas

#### 1. Doctor Empathetic (Medical)
```python
persona_id: "doctor_empathetic_v1"
domain: "medical"
style: Empathetic, cautious, professional
dataset: ChatDoctor-HealthCareMagic-100k
```

**Example Query**: "I have a fever and headache"
**Response Style**: Empathetic, asks clarifying questions, provides cautious guidance

#### 2. Supportive Teacher (Education)
```python
persona_id: "teacher_supportive_v1"
domain: "education"
style: Patient, encouraging, explanatory
dataset: OpenAssistant/oasst2
```

**Example Query**: "Can you explain photosynthesis?"
**Response Style**: Step-by-step explanations, checks understanding, supportive tone

---

## 🎯 Quick Test

After setup completes:

### Test 1: Medical Query
```python
from engine.inference import PersonaInference

engine = PersonaInference()
response = engine.generate_response(
    query="I have a terrible headache, what should I do?",
    max_tokens=200
)
print(response)
# Should route to doctor_empathetic_v1
```

### Test 2: Education Query
```python
response = engine.generate_response(
    query="Can you help me understand photosynthesis?",
    max_tokens=200
)
print(response)
# Should route to teacher_supportive_v1
```

---

## 📁 What Got Created

```
personareplica/
├── data/
│   ├── raw/
│   │   ├── medical.jsonl          (dataset)
│   │   └── education.jsonl        (dataset)
│   └── processed/
│       ├── medical/processed.jsonl
│       └── education/processed.jsonl
│
├── persona/profiles/
│   ├── doctor_empathetic_v1.json
│   └── teacher_supportive_v1.json  ← NEW
│
└── retrieval/indices/
    ├── doctor_empathetic_v1.index
    ├── teacher_supportive_v1.index  ← NEW
    └── *_texts.json files
```

---

## 🔧 Individual Commands

If you prefer step-by-step:

```bash
# Step 1: Download datasets
python scripts/download_data.py

# Step 2: Preprocess
python scripts/preprocess.py

# Step 3: Build personas
python scripts/build_persona.py

# Step 4: Verify
python scripts/verify_setup.py

# Step 5: Test
python scripts/test_agentic_rag.py
```

---

## 🐛 Quick Troubleshooting

### Error: "GROQ_API_KEY not found"
```bash
# Create .env file in personareplica/ directory
echo "GROQ_API_KEY=your_key_here" > .env

# Get free API key: https://console.groq.com/
```

### Error: Module not found
```bash
pip install -r requirements.txt

# If specific module missing:
pip install groq sentence-transformers faiss-cpu python-dotenv numpy
```

### Error: Dataset download fails
```bash
# System automatically falls back to dummy data (3 examples)
# Or manually retry:
python scripts/download_data.py
```

### Error: Path not found
```bash
# Make sure you're in the right directory:
cd personareplica
pwd  # Should end with /personareplica
```

---

## 📊 Verify Success

After setup, check:

```bash
# Check persona profiles exist
ls persona/profiles/
# Should show: doctor_empathetic_v1.json, teacher_supportive_v1.json

# Check FAISS indices exist
ls retrieval/indices/
# Should show: *_v1.index and *_texts.json files

# Run verification
python scripts/verify_setup.py
# Should show: ✓ All checks passed!
```

---

## 🎓 Next Steps

### Learn More
- 📖 Full details: `EDUCATION_IMPLEMENTATION_COMPLETE.md`
- 📖 Setup help: `EDUCATION_SETUP_GUIDE.md`
- 📖 Code changes: `CHANGES_SUMMARY.md`
- 📖 Architecture: `README.md`

### Customize
1. Adjust style metrics in persona profiles
2. Add more training examples to corpora
3. Modify routing keywords
4. Fine-tune RAG strategies

### Extend
1. Add more domains (support, mentorship)
2. Create sub-personas (Math Teacher, Science Teacher)
3. Implement difficulty levels
4. Add conversation history

---

## 💡 Common Use Cases

### Use Case 1: Educational Chatbot
```python
# Student asks for homework help
query = "I don't understand how to factor polynomials"
response = engine.generate_response(query)
# Routes to teacher_supportive_v1
# Provides step-by-step guidance
```

### Use Case 2: Medical Guidance Bot
```python
# User reports symptoms
query = "I've had a persistent cough for a week"
response = engine.generate_response(query)
# Routes to doctor_empathetic_v1
# Asks clarifying questions, suggests consulting doctor
```

### Use Case 3: Multi-Domain Assistant
```python
# System automatically selects right persona
queries = [
    "What causes headaches?",           # → Medical
    "Explain the water cycle",          # → Education
    "How do I solve this equation?",    # → Education
    "What should I do for allergies?"   # → Medical
]

for query in queries:
    response = engine.generate_response(query)
    print(f"Query: {query}\n{response}\n")
```

---

## ⚡ Performance Tips

1. **First Run**: Initial setup takes 10-15 minutes
2. **Subsequent Runs**: Inference is fast (<2 seconds)
3. **Dataset Size**: Larger corpus = better responses
4. **GPU**: FAISS can use GPU for faster search (optional)

---

## 🔗 Quick Links

| Resource | Purpose |
|----------|---------|
| `QUICK_START.md` | This file - get started fast |
| `EDUCATION_IMPLEMENTATION_COMPLETE.md` | Full implementation details |
| `EDUCATION_SETUP_GUIDE.md` | Detailed setup instructions |
| `CHANGES_SUMMARY.md` | What changed from v1.0 |
| `MIGRATION_TO_EDUCATION.md` | Technical migration guide |

---

## ✅ Success Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env file with GROQ_API_KEY
- [ ] Ran `run_full_setup.py` successfully
- [ ] Both persona profiles created
- [ ] Verification script passed
- [ ] Test queries work correctly

---

## 🆘 Need Help?

1. **Setup issues**: Check `EDUCATION_SETUP_GUIDE.md`
2. **Code questions**: See inline comments in source files
3. **Architecture**: Review `README.md` and `PROJECT_MAP.md`
4. **Errors**: Look for similar issues in troubleshooting sections

---

## 🎉 You're Ready!

Your PersonaReplica system with Medical and Education personas is set up and ready to use.

**Start using it**:
```python
from engine.inference import PersonaInference

engine = PersonaInference()

# Try any query!
response = engine.generate_response("Your question here")
print(response)
```

Happy building! 🚀
