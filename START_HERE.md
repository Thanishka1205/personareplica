# PersonaReplica: START HERE 📖

**Welcome to the PersonaReplica AI Persona Simulation System!**

This is your index file. Start here to navigate the project.

---

## 🚀 Quick Navigation

### 👤 I want to...

**Get the system running in 30 minutes**
→ Go to: [`SETUP_GUIDE.md`](SETUP_GUIDE.md)

**Understand how it works**
→ Go to: [`README.md`](personareplica/README.md)

**See the architecture**
→ Go to: [`PROJECT_MAP.md`](PROJECT_MAP.md)

**Find code examples**
→ Go to: [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)

**Understand design decisions**
→ Go to: [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md)

**See what's been implemented**
→ Go to: [`IMPLEMENTATION_COMPLETE.md`](IMPLEMENTATION_COMPLETE.md)

**Find a specific file**
→ Go to: [`FILE_MANIFEST.md`](FILE_MANIFEST.md)

**Get a visual overview**
→ Go to: [`VISUAL_SUMMARY.md`](VISUAL_SUMMARY.md)

---

## 📚 Documentation Map

```
                      START HERE (Index)
                            ↓
                    ┌───────┴────────┐
                    │                │
            Need Setup?         Need Details?
                    │                │
                    ↓                ↓
             SETUP_GUIDE.md    README.md
                    │           /    |    \
                    │          /     |     \
                    │         /      |      \
                    │        /       |       \
              IMPLEMENT   LEARN   UNDERSTAND EXTEND
                    │        │        │       │
                    │        │        │       │
                    ↓        ↓        ↓       ↓
           verify_setup  PROJECT   IMPLEMENTATION  QUICK_
           test_engine     MAP      SUMMARY      REFERENCE
           test_rag
```

---

## 🎯 By Role

### 👨‍💻 Developer (Setup & Customize)
1. Read: `SETUP_GUIDE.md` (30-45 min setup)
2. Read: `QUICK_REFERENCE.md` (code patterns)
3. Read: `PROJECT_MAP.md` (architecture)
4. Run: `personareplica/scripts/` tests
5. Customize: Add personas, adjust metrics

**Key files**:
- `engine/agentic_router.py` - Routing logic
- `retrieval/agentic_rag.py` - Retrieval logic
- `persona/builder.py` - Metric extraction
- `scripts/test_engine.py` - Main test

### 🏗️ Architect (Understand Design)
1. Read: `IMPLEMENTATION_SUMMARY.md` (design decisions)
2. Read: `PROJECT_MAP.md` (architecture)
3. Review: `VISUAL_SUMMARY.md` (diagrams)
4. Study: Core modules in `engine/` and `retrieval/`

**Key concepts**:
- 5-step agentic pipeline
- LLM-driven routing & RAG decisions
- Style metrics → behavioral instructions
- Cosine similarity scoring

### 📊 Data Scientist (Personas & Metrics)
1. Read: `IMPLEMENTATION_SUMMARY.md` (persona info)
2. Study: `persona/builder.py` (metric extraction)
3. Explore: `persona/profiles/` (sample profiles)
4. Modify: Add new personas or metrics

**Key components**:
- 7 quantified style metrics per persona
- FAISS indices with L2-normalization
- Centroid-based negative filtering
- Cross-encoder optional reranking

### 🎓 Student (Learn the System)
1. Start: `README.md` (complete overview)
2. Understand: `PROJECT_MAP.md` (architecture)
3. Explore: `VISUAL_SUMMARY.md` (diagrams)
4. Deep dive: `IMPLEMENTATION_SUMMARY.md` (details)
5. Practice: `QUICK_REFERENCE.md` (code examples)

---

## 📂 Project Structure at a Glance

```
e:\backup 2026\Projects\PersonaReplica\
│
├─ 📖 DOCUMENTATION (Start Here)
│  ├─ README.md                    ← Full project docs
│  ├─ SETUP_GUIDE.md               ← Step-by-step setup
│  ├─ IMPLEMENTATION_SUMMARY.md    ← Technical details
│  ├─ PROJECT_MAP.md               ← Architecture
│  ├─ QUICK_REFERENCE.md           ← Code snippets
│  ├─ VISUAL_SUMMARY.md            ← Diagrams
│  ├─ FILE_MANIFEST.md             ← File listing
│  └─ IMPLEMENTATION_COMPLETE.md   ← Summary
│
└─ 💻 CODE
   └─ personareplica/
      ├─ engine/                   ← Routing & prompt building
      ├─ retrieval/                ← RAG system
      ├─ persona/                  ← Persona management
      ├─ scripts/                  ← Setup & testing
      ├─ data/                     ← Corpora
      ├─ .env.example              ← Configuration
      └─ requirements.txt          ← Dependencies
```

---

## ⏱️ Timeline

### Phase 1: Setup (30-45 min)
1. **Env Setup** (10 min) → `SETUP_GUIDE.md` Phase 1
2. **Data** (10 min) → `SETUP_GUIDE.md` Phase 2
3. **Personas** (15 min) → `SETUP_GUIDE.md` Phase 3
4. **Verify** (5 min) → `SETUP_GUIDE.md` Phase 4

### Phase 2: Testing (10-15 min)
1. **Router Test** (3 min) → `SETUP_GUIDE.md` Phase 5
2. **Full Pipeline** (10 min) → `SETUP_GUIDE.md` Phase 6

### Phase 3: Using (Ongoing)
1. **Custom Queries** → Use `PersonaEngine.process()`
2. **Add Personas** → Follow `README.md` "Extend"
3. **Customize Metrics** → Edit `persona/builder.py`

---

## 🎯 Success Checklist

**After Setup:**
- [ ] `verify_setup.py` shows ✅ all checks passing
- [ ] `test_engine.py` produces responses for both personas
- [ ] `test_agentic_rag.py` shows correct routing
- [ ] All 4 documentation files readable

**After Testing:**
- [ ] Medical queries route to `doctor_empathetic_v1`
- [ ] Interview queries route to `interview_coach_v1`
- [ ] Retrieved examples are domain-relevant
- [ ] Responses score > 0.72 accuracy

**For Customization:**
- [ ] Can modify persona profiles
- [ ] Can add new style metrics
- [ ] Can add new personas
- [ ] Can adjust RAG strategies

---

## 💡 Key Concepts (5 min Read)

### Agentic Routing
Instead of hardcoded rules, an LLM (Groq Mixtral) reads the query and picks the best persona. More flexible, better results.

### Intelligent RAG
Instead of always doing semantic search, an LLM decides the strategy:
- **Semantic**: Query is similar to typical requests
- **Keyword**: Query has unique terms
- **Hybrid**: Both apply
- **None**: Don't retrieve

### Style Metrics
7 quantified dimensions extracted from real corpus:
- **empathy_score**: 0-1 (how empathetic?)
- **question_rate**: 0-1 (how many questions?)
- **formality_score**: 0-1 (how formal?)
- **lexical_diversity**: 0-1 (vocabulary variety)
- **hedging_rate**: 0-1 (uncertainty language)
- **avg_sentence_length**: 0-∞ (short/long sentences)
- **avg_response_length**: 0-∞ (detailed/brief)

### Few-Shot Learning
Retrieved examples from the corpus are injected into the system prompt, showing the LLM how to respond in persona voice.

### Accuracy Scoring
After generation, a PersonaScorer measures cosine similarity between the response and the persona's corpus, giving a 0-1 accuracy score.

---

## 🔗 File Relationships

```
SETUP (You are here)
  ↓
SETUP_GUIDE.md (Follow this)
  ├─→ Download data
  ├─→ Preprocess
  └─→ Build personas
      ↓
      Uses: personareplica/scripts/
      Creates: persona/profiles/
      Creates: retrieval/indices/
  ↓
README.md (Understand this)
  ├─→ Full documentation
  ├─→ Concepts explained
  └─→ Troubleshooting
  ↓
PROJECT_MAP.md (Learn this)
  ├─→ Architecture diagrams
  ├─→ Data flows
  └─→ Component relationships
  ↓
QUICK_REFERENCE.md (Use this)
  ├─→ Code patterns
  ├─→ Configuration examples
  └─→ Common tasks
```

---

## 🆘 Stuck? Here's Help

**"I don't know where to start"**
→ Go to: `SETUP_GUIDE.md` Phase 1

**"I don't understand the architecture"**
→ Go to: `PROJECT_MAP.md` + `VISUAL_SUMMARY.md`

**"I want to understand the code"**
→ Go to: `QUICK_REFERENCE.md` + `README.md`

**"I got an error during setup"**
→ Go to: `SETUP_GUIDE.md` "Troubleshooting"

**"I want to add a new persona"**
→ Go to: `README.md` "How to Extend"

**"What's actually implemented?"**
→ Go to: `IMPLEMENTATION_COMPLETE.md`

**"Where's file X?"**
→ Go to: `FILE_MANIFEST.md`

---

## 🎓 Learning Path

**Time**: 2-3 hours total

1. **Understand** (30 min)
   - Read: `README.md` (project overview)
   - Read: `VISUAL_SUMMARY.md` (diagrams)

2. **Setup** (45 min)
   - Follow: `SETUP_GUIDE.md` (step-by-step)

3. **Test** (15 min)
   - Run: `scripts/test_engine.py`
   - Run: `scripts/test_agentic_rag.py`

4. **Learn** (30 min)
   - Study: `PROJECT_MAP.md` (architecture)
   - Study: `QUICK_REFERENCE.md` (patterns)

5. **Use** (30 min)
   - Write custom scripts
   - Add your own personas
   - Customize metrics

---

## 🚀 Your First Steps

### Right Now (5 min)
1. Read this file (you're doing it! ✓)
2. Skim `README.md` (2 min)
3. Skim `VISUAL_SUMMARY.md` (2 min)

### Next (30-45 min)
1. Follow `SETUP_GUIDE.md` Phase 1-4 (setup environment)
2. Run `verify_setup.py` (check everything)

### Then (10 min)
1. Run `test_engine.py` (full pipeline)
2. Run `test_agentic_rag.py` (routing & RAG)

### Finally
1. Try custom queries
2. Read `PROJECT_MAP.md` (deep dive)
3. Customize personas or metrics

---

## 📞 Questions?

Most questions answered in one of these files:
- **Setup/Installation**: `SETUP_GUIDE.md`
- **How it works**: `README.md` or `PROJECT_MAP.md`
- **Code patterns**: `QUICK_REFERENCE.md`
- **Why designed this way**: `IMPLEMENTATION_SUMMARY.md`
- **What's where**: `FILE_MANIFEST.md`

---

## ✨ You're Ready!

Everything is implemented. All documentation is written. All tests are ready.

**Next step**: Open `SETUP_GUIDE.md` and follow Phase 1.

---

**PersonaReplica MVP** ✅ Ready for setup, testing, and customization!

🎭 AI that learns persona style from real data.

---

### Quick Links
- Setup: [`SETUP_GUIDE.md`](SETUP_GUIDE.md)
- Docs: [`README.md`](personareplica/README.md)
- Architecture: [`PROJECT_MAP.md`](PROJECT_MAP.md)
- Code: [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)
- Implementation: [`IMPLEMENTATION_COMPLETE.md`](IMPLEMENTATION_COMPLETE.md)
