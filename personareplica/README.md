# PersonaReplica: AI Persona Simulation System

An agentic AI system that automatically detects the expert persona a user needs and generates responses that authentically match that persona's communication style.

**Current Implementation: Medical & Interview Coach (MVP)**

---

## 🎯 Project Overview

PersonaReplica solves a fundamental problem with modern AI assistants: they're one-size-fits-all. A doctor and a tutor both know facts, but what makes them effective is **HOW they communicate** — empathy timing, questioning style, vocabulary, formality.

This system learns communication styles from real behavioral corpora and applies them to generate authentic persona-consistent responses.

### Key Features (MVP)

- **Agentic Router**: LLM-powered persona selection from queries
- **Agentic RAG**: Intelligent retrieval strategy (semantic, keyword, hybrid, none)
- **Style Metrics**: 7 quantified communication dimensions per persona
- **Few-Shot Examples**: Retrieved corpus examples injected into generation prompt
- **Persona Scoring**: Accuracy measurement using cosine similarity
- **Two Personas**: Doctor (Medical) & Interview Coach

---

## 📁 Project Structure

```
personareplica/
├── api/                          # FastAPI layer (future)
│   └── __init__.py
├── data/
│   ├── raw/                      # Downloaded HuggingFace datasets
│   │   ├── medical.jsonl
│   │   └── interview.jsonl
│   └── processed/                # Normalized data
│       ├── medical/processed.jsonl
│       └── interview/processed.jsonl
├── engine/
│   ├── agentic_router.py         # LLM call #1: Select persona
│   ├── prompt_builder.py         # Build system prompt from metrics + examples
│   └── inference.py              # Orchestrate full pipeline
├── persona/
│   ├── builder.py                # Extract metrics & build FAISS indices
│   ├── scorer.py                 # Score responses via cosine similarity
│   └── profiles/                 # Built persona profiles (JSON)
│       ├── doctor_empathetic_v1.json
│       └── interview_coach_v1.json
├── retrieval/
│   ├── agentic_rag.py            # LLM call #2: Decide retrieval strategy
│   └── indices/                  # FAISS indices + text references
│       ├── doctor_empathetic_v1.index
│       ├── doctor_empathetic_v1_texts.json
│       └── ...
├── scripts/
│   ├── download_data.py          # Download HuggingFace datasets
│   ├── preprocess.py             # Normalize data to standard schema
│   ├── build_persona.py          # Build personas from corpus
│   ├── verify_setup.py           # Verify environment setup
│   ├── test_engine.py            # End-to-end pipeline test
│   └── test_agentic_rag.py       # Test routing & RAG decisions
├── memory/
│   └── memory.py                 # Placeholder for future Redis memory
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd e:/backup\ 2026/Projects/PersonaReplica/personareplica

# Create virtual environment (recommended)
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=gsk_your_key_here
```

**Get your Groq API key:**
- Go to https://console.groq.com/keys
- Generate a new API key
- Paste into `.env`

### Step 3: Download & Preprocess Data

```bash
# Download datasets from HuggingFace
python scripts/download_data.py

# Normalize to standard schema
python scripts/preprocess.py
```

### Step 4: Build Personas

```bash
# Extract style metrics and build FAISS indices
python scripts/build_persona.py
```

This creates:
- `persona/profiles/doctor_empathetic_v1.json` (style metrics)
- `retrieval/indices/doctor_empathetic_v1.index` (FAISS index)
- `retrieval/indices/doctor_empathetic_v1_texts.json` (reference texts)
- Same for `interview_coach_v1`

### Step 5: Verify Setup

```bash
python scripts/verify_setup.py
```

Should show ✓ all checks passing.

### Step 6: Test the Pipeline

```bash
# Test full 5-step pipeline
python scripts/test_engine.py

# Test routing and RAG decisions
python scripts/test_agentic_rag.py
```

---

## 🔄 The 5-Step Pipeline (No Memory)

The system processes queries through this agentic pipeline:

```
USER QUERY
    ↓
[STEP 1] AgenticRouter (LLM call #1)
    → Reads query, selects best persona + confidence
    ↓
[STEP 2] AgenticRAG (LLM call #2)
    → Decides strategy: semantic | keyword | hybrid | none
    → Sets num_examples (0-7) and rerank flag
    ↓
[STEP 3] Retrieve Examples
    → FAISS semantic search (per-persona IndexFlatIP)
    → BM25 keyword search (optional)
    → Negative filter (remove off-persona examples)
    → Cross-encoder rerank (optional, local no-LLM)
    ↓
[STEP 4] PromptBuilder
    → System prompt = style metrics + 7 behavioral instructions + few-shot examples
    ↓
[STEP 5] Groq LLM (LLaMA 3.3 70B)
    → Generate persona-styled response
    ↓
[STEP 6] PersonaScorer
    → Embed response, measure cosine similarity to persona corpus
    → Return accuracy_score [0.0-1.0], flag if < 0.72
    ↓
API RESPONSE
    → response + accuracy_score + routing_decision + retrieval_details + reranker_used
```

---

## 📊 Personas

### 1. Doctor (Empathetic)

**Profile Metrics:**
- `empathy_score`: 0.95 (very high)
- `question_rate`: 0.09 (low)
- `hedging_rate`: 0.61 (medium)
- `formality_score`: 0.45 (moderate)
- `lexical_diversity`: 0.52

**Behavior:**
- Acknowledges emotions and validates feelings
- Shows deep medical concern
- Uses hedging language ("might", "could", "possibly")
- Relatively direct (few clarifying questions)

**Example Response:**
> I understand you're concerned about your symptoms. That must be worrying. Let me ask—how long have you had the fever? Have you taken your temperature? This information will help me understand what might be happening.

### 2. Interview Coach (Structured)

**Profile Metrics:**
- `question_rate`: 0.28 (high)
- `formality_score`: 0.72 (high)
- `lexical_diversity`: 0.71 (high)
- `empathy_score`: 0.55 (moderate)
- `hedging_rate`: 0.25 (low)

**Behavior:**
- Frequent clarifying questions (Socratic method)
- Formal, technical language
- High vocabulary variety
- Confident assertions with low hedging

**Example Response:**
> That's an excellent question. Before we dive into solutions, let me ask: what constraints are most important here—latency, throughput, or consistency? Understanding these will help you design the optimal architecture. What are your initial thoughts?

---

## 🧪 Testing

### Unit/Integration Tests

```bash
# Run the full pipeline on sample queries
python scripts/test_engine.py

# Output:
# ✓ Routing decisions
# ✓ Retrieved examples
# ✓ Generated responses
# ✓ Accuracy scores
```

### Router Accuracy

```bash
python scripts/test_agentic_rag.py
```

Tests:
- Router routes medical queries → doctor_empathetic_v1
- Router routes interview queries → interview_coach_v1
- RAG retrieves domain-relevant examples
- No cross-domain bleed

### Persona Accuracy

After generation, PersonaScorer measures:
- **Score Formula**: `(cosine_similarity + 1) / 2` normalizes to [0, 1]
- **Quality Threshold**: 0.72
- **Below 0.72**: Response flagged as potential off-persona

---

## 📝 Configuration

### Style Metrics (Auto-Extracted)

The `PersonaBuilder` extracts 7 metrics from corpus:

| Metric | Formula | Example |
|--------|---------|---------|
| `avg_sentence_length` | words / sentences | 15 words/sentence |
| `empathy_score` | empathy keywords / total words (capped 1.0) | 0.95 |
| `question_rate` | questions / total sentences | 0.28 |
| `formality_score` | formal keywords / docs (capped 1.0) | 0.72 |
| `lexical_diversity` | unique words / total words | 0.71 |
| `hedging_rate` | hedging keywords / docs (capped 1.0) | 0.61 |
| `avg_response_length` | words / response | 120 |

These drive `PromptBuilder` instructions automatically—no manual prompt tuning needed.

### Retrieval Strategy Decisions

AgenticRAG's LLM call decides:

```python
{
    "strategy": "semantic" | "keyword" | "hybrid" | "none",
    "num_examples": 0-7,
    "rerank": true | false,
    "reasoning": "..."
}
```

**Decision Logic:**
- `semantic`: For queries similar to typical requests
- `keyword`: For queries with unique terms
- `hybrid`: When both apply
- `none`: For very common requests

---

## 🔌 Environment Variables

```bash
# Required
GROQ_API_KEY=gsk_your_key_here

# Optional (future)
PERSONAREPLICA_API_KEY=your_api_key_here
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=

# Development
ENVIRONMENT=development
DEBUG=true
```

---

## 📦 Dependencies

**Core:**
- `fastapi` — Web framework (future API)
- `groq` — LLM inference
- `sentence-transformers` — Embeddings (all-MiniLM-L6-v2)
- `faiss-cpu` — Vector search
- `rank-bm25` — Keyword retrieval

**Data:**
- `numpy` — Numerical operations
- `torch` — Transformer backbone
- `datasets` — HuggingFace data loading

**Future:**
- `redis` — Memory/caching
- `streamlit` — Chat UI
- `pydantic` — API validation

---

## 🎓 How to Extend

### Add a New Persona

1. **Get corpus data** (JSONL with `{"input": "...", "response": "..."}`)
2. **Add to persona registry** in `engine/agentic_router.py`:
   ```python
   REGISTERED_PERSONAS = {
       "your_persona_id": {
           "name": "Your Persona",
           "domain": "domain",
           "description": "..."
       }
   }
   ```
3. **Save to `data/raw/your_domain.jsonl`**
4. **Run pipeline**:
   ```bash
   python scripts/preprocess.py
   python scripts/build_persona.py
   ```
5. **Verify**:
   ```bash
   python scripts/verify_setup.py
   python scripts/test_engine.py
   ```

### Customize Style Metrics

Edit `persona/builder.py` → `extract_style_metrics()`:
```python
def extract_style_metrics(self, corpus: List[str]) -> Dict[str, float]:
    # Add your own metrics here
    # Each metric should normalize to [0.0, 1.0]
    metrics['my_metric'] = ...
    return metrics
```

Then in `engine/prompt_builder.py`, add instructions:
```python
my_metric = metrics.get('my_metric', 0.5)
if my_metric >= 0.7:
    instructions.append("Your instruction based on high my_metric")
```

---

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
- Check `.env` file exists in project root
- Verify key is set: `GROQ_API_KEY=gsk_...`
- Run `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GROQ_API_KEY'))"`

### "Profile not found"
- Run `python scripts/build_persona.py` to build profiles
- Verify `persona/profiles/doctor_empathetic_v1.json` exists

### "FAISS index not found"
- Run `python scripts/build_persona.py`
- Check `retrieval/indices/` directory

### "Slow responses"
- First request warms up model (normal)
- Check Groq API status: https://status.groq.com

### "Low accuracy scores (< 0.72)"
- Check if response matches persona style
- Increase `num_examples` in RAG decision
- Review persona style metrics in profile JSON

---

## 🚧 Roadmap (Future Phases)

**Phase 5: Memory & API Layer**
- Redis-based conversation memory (10-turn sliding window)
- FastAPI endpoints for `/chat/`, `/stats/`, `/persona/create`
- Rate limiting (slowapi)
- API key authentication

**Phase 6: UI & Integration**
- Streamlit chat interface
- Live persona selection dropdown
- Retrieval decision visualization
- Persona accuracy badges

**Phase 7: Testing & Eval**
- Unit tests (builder, scorer, RAG, router)
- Integration tests (full pipeline)
- Persona eval on held-out test set
- Router accuracy measurement

---

## 📄 License

Personal project for demonstration.

---

## ✨ Key Insights

1. **Style is Learnable**: Communication style comes from corpus data, not prompt engineering
2. **Agentic Decisions**: Every decision (routing, retrieval strategy) is made by LLM, not hardcoded
3. **Measurable Quality**: Every response gets scored against real behavior patterns
4. **Few-Shot Matters**: Retrieved examples are more important than metric instructions alone
5. **No Memory (MVP)**: Focusing on routing + RAG excellence before multi-turn complexity

---

**Ready to build?** Start with:
```bash
python scripts/download_data.py && \
python scripts/preprocess.py && \
python scripts/build_persona.py && \
python scripts/verify_setup.py && \
python scripts/test_engine.py
```

Good luck! 🚀
