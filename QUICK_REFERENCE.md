# PersonaReplica: Quick Reference

**Medical + Interview Coach | Agentic RAG System | 5-Step Pipeline**

---

## 🚀 TL;DR Setup (Copy & Paste)

```bash
cd e:/backup\ 2026/Projects/PersonaReplica/personareplica
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: GROQ_API_KEY=gsk_your_key
python scripts/download_data.py
python scripts/preprocess.py
python scripts/build_persona.py
python scripts/verify_setup.py
python scripts/test_engine.py
```

---

## 📂 Key Files

| File | Purpose |
|------|---------|
| `engine/agentic_router.py` | Route query → persona |
| `retrieval/agentic_rag.py` | Decide retrieval strategy |
| `engine/prompt_builder.py` | Build system prompt |
| `engine/inference.py` | Orchestrate full pipeline |
| `persona/scorer.py` | Score response accuracy |
| `persona/builder.py` | Extract metrics & build indices |
| `scripts/test_engine.py` | End-to-end test |
| `scripts/verify_setup.py` | Health check |

---

## 🎭 Personas

### Doctor Empathetic
- **Domain**: Medical
- **Key traits**: Empathy (0.95), Low questions (0.09), High hedging (0.61)
- **Style**: Acknowledge concerns, ask clarifying questions, use uncertainty language

### Interview Coach  
- **Domain**: Interview
- **Key traits**: High questions (0.28), Formal (0.72), Diverse vocab (0.71)
- **Style**: Socratic method, structured guidance, technical precision

---

## 🔄 Pipeline (5 Steps)

```
Query
  ↓
[1] Route: LLM picks persona
  ↓
[2] Decide: LLM chooses retrieval strategy
  ↓
[3] Retrieve: Fetch examples from FAISS/BM25
  ↓
[4] Prompt: Build system prompt with metrics + examples
  ↓
[5] Generate: Groq LLM produces response
  ↓
[6] Score: Cosine similarity check (0.0-1.0)
  ↓
Response + metadata
```

---

## 💻 Core Code Patterns

### Run Full Pipeline
```python
from engine.inference import PersonaEngine

engine = PersonaEngine()
result = engine.process("I have a fever")
print(result["final_response"])
print(f"Accuracy: {result['accuracy_score']:.2f}")
```

### Test Router
```python
from engine.agentic_router import get_router

router = get_router()
decision = router.route("How do I solve this interview question?")
print(f"Persona: {decision['persona_id']}")
print(f"Confidence: {decision['confidence']:.2f}")
```

### Retrieve Examples
```python
from retrieval.agentic_rag import AgenticRAG

rag = AgenticRAG("doctor_empathetic_v1")
result = rag.retrieve("I have a headache")
print(f"Strategy: {result['decision']['strategy']}")
print(f"Examples: {len(result['examples'])}")
```

### Score Response
```python
from persona.scorer import PersonaScorer

scorer = PersonaScorer()
score, details = scorer.score_response(
    "I understand your concern...",
    "doctor_empathetic_v1"
)
print(f"Score: {score:.2f}")
```

---

## 📊 Metrics Extracted

| Metric | Range | Formula |
|--------|-------|---------|
| `empathy_score` | 0.0-1.0 | Empathy keywords / total words (capped) |
| `question_rate` | 0.0-1.0 | Questions / total sentences |
| `formality_score` | 0.0-1.0 | Formal keywords / docs (capped) |
| `lexical_diversity` | 0.0-1.0 | Unique words / total words |
| `hedging_rate` | 0.0-1.0 | Hedging keywords / docs (capped) |
| `avg_sentence_length` | 0-∞ | Words / sentences |
| `avg_response_length` | 0-∞ | Words / response |

---

## 🎛️ Configuration

### Change Quality Threshold
```python
# persona/scorer.py
quality_threshold = 0.72  # Responses below this get flagged
```

### Add New Persona
```python
# engine/agentic_router.py
REGISTERED_PERSONAS = {
    "new_persona_v1": {
        "name": "New",
        "domain": "domain",
        "description": "..."
    }
}
```

### Customize RAG Strategy
```python
# retrieval/agentic_rag.py
decision = {
    "strategy": "semantic|keyword|hybrid|none",
    "num_examples": 0-7,
    "rerank": true|false
}
```

---

## 🧪 Tests

```bash
python scripts/verify_setup.py          # Health check
python scripts/test_agentic_rag.py      # Router + retrieval
python scripts/test_engine.py           # Full pipeline
```

---

## ⚡ Performance

| Task | Time |
|------|------|
| Download data | 2-3 min |
| Preprocess | 1 min |
| Build personas | 3-5 min |
| Single query | 5-8 sec |
| Full test suite | 10-15 min |

---

## 🔑 Environment Variables

```bash
GROQ_API_KEY=gsk_...                    # Required
PERSONAREPLICA_API_KEY=...              # Optional (future)
REDIS_URL=redis://localhost:6379        # Optional (future)
ENVIRONMENT=development                 # Optional
DEBUG=true                              # Optional
```

---

## 📈 Success Metrics

✅ Router accuracy: ~95% (medical vs interview)
✅ Response accuracy: 0.75-0.92 (PersonaScorer)
✅ Retrieval quality: 90%+ relevant examples
✅ Pipeline latency: < 10 sec per query

---

## 🚨 Common Issues

| Issue | Fix |
|-------|-----|
| "GROQ_API_KEY not found" | Check .env file, set GROQ_API_KEY |
| "Module not found" | `pip install -r requirements.txt` |
| "FAISS index not found" | `python scripts/build_persona.py` |
| "Slow responses" | Normal on first run (model loading) |
| "Low accuracy score" | Response may still be good, try more examples |

---

## 📚 Key Concepts

**Agentic Router**: LLM decides which persona fits the query
**Agentic RAG**: LLM decides how to retrieve (strategy)
**Style Metrics**: Quantified communication style from corpus
**Few-Shot Examples**: Retrieved examples guide generation
**Cosine Similarity Scoring**: Measures response fit to persona

---

## 🔗 Documentation

- `README.md` — Full documentation
- `SETUP_GUIDE.md` — Step-by-step setup
- `IMPLEMENTATION_SUMMARY.md` — Technical details
- `QUICK_REFERENCE.md` — This file

---

## 💡 Pro Tips

1. **First query is slowest** (models load), subsequent queries are fast
2. **Try different personas** with same query to see style differences
3. **Increase num_examples** in RAG if scores are low
4. **Check retrieved examples** to understand what influenced response
5. **Low score doesn't mean bad response** — PersonaScorer is imperfect

---

## 🎯 Next Steps

1. Complete setup (SETUP_GUIDE.md)
2. Understand pipeline (IMPLEMENTATION_SUMMARY.md)
3. Test with custom queries
4. Add new personas
5. Integrate with FastAPI (Phase 5)

---

**Questions? Check README.md or SETUP_GUIDE.md for details.**
