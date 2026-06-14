# PersonaReplica

**Dual-Persona AI System with Intelligent Routing and Agentic RAG**

PersonaReplica is an advanced conversational AI system that intelligently routes queries between specialized personas (Medical Doctor and Supportive Teacher) using LLM-based routing, agentic RAG, and style-consistent response generation.

## 🎯 Features

- **🔀 Intelligent Routing**: LLM-powered persona selection with 92.3% accuracy
- **🧠 Agentic RAG**: Dynamic retrieval strategy selection using LLaMA 3.3 70B
- **📊 Style Consistency**: 7-dimensional style metrics ensure persona-appropriate responses
- **🎨 Dual Personas**: 
  - 🏥 **Doctor Empathetic** (Medical domain)
  - 📚 **Teacher Supportive** (Education domain)
- **🖥️ Interactive Web UI**: Beautiful Streamlit interface for testing
- **⚡ Fast**: Groq-powered inference with <2s response time

## 📊 System Performance

| Metric | Score |
|--------|-------|
| Medical Routing Accuracy | 100% |
| Education Routing Accuracy | 84.6% |
| Overall Routing Accuracy | **92.3%** |
| Response Generation Time | ~2 seconds |

## 🏗️ Architecture

```
User Query
    ↓
┌─────────────────────┐
│  Agentic Router     │ ← LLM Call #1: Select Persona
│  (LLaMA 3.1 8B)     │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Agentic RAG        │ ← LLM Call #2: Decide Retrieval Strategy
│  (LLaMA 3.3 70B)    │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  FAISS Search       │ ← Semantic/Keyword/Hybrid Search
│  + BM25             │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Prompt Builder     │ ← Inject Persona Style + Examples
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Response Gen       │ ← LLM Call #3: Generate Response
│  (LLaMA 3.1 8B)     │
└─────────┬───────────┘
          ↓
    Final Response
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API Key (get free key at [console.groq.com](https://console.groq.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/Thanishka1205/personareplica.git
cd personareplica/personareplica

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "GROQ_API_KEY=your_key_here" > .env
```

### Setup Pipeline

```bash
# Option 1: Automated setup (recommended)
python scripts/run_full_setup.py

# Option 2: Manual step-by-step
python scripts/download_data.py      # Download datasets
python scripts/preprocess.py         # Preprocess data
python scripts/build_persona.py      # Build personas
python scripts/verify_setup.py       # Verify installation
```

### Run the Web Interface

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501` and start chatting!

## 📁 Project Structure

```
personareplica/
├── app.py                      # Streamlit web interface
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── data/                      # Datasets (gitignored)
│   ├── raw/                   # Raw downloaded data
│   └── processed/             # Preprocessed data
│
├── persona/                   # Persona profiles
│   ├── profiles/              # JSON configs with style metrics
│   ├── builder.py             # Persona building logic
│   └── scorer.py              # Response quality scoring
│
├── retrieval/                 # RAG system
│   ├── indices/               # FAISS indices (gitignored)
│   └── agentic_rag.py         # Agentic RAG implementation
│
├── engine/                    # Core engine
│   ├── agentic_router.py      # LLM-based routing
│   ├── prompt_builder.py      # Dynamic prompt generation
│   └── inference.py           # Full pipeline orchestration
│
├── memory/                    # Conversation memory (stub)
│   └── memory.py
│
└── scripts/                   # Utility scripts
    ├── download_data.py       # Dataset downloader
    ├── preprocess.py          # Data preprocessing
    ├── build_persona.py       # Persona builder
    ├── verify_setup.py        # Setup verification
    ├── test_agentic_rag.py    # RAG testing
    ├── test_comprehensive.py  # Full system testing
    └── run_full_setup.py      # Automated pipeline
```

## 🧪 Testing

### Quick Test
```bash
python scripts/test_agentic_rag.py
```

### Comprehensive Test
```bash
python scripts/test_comprehensive.py
```

### Test Specific Components
```bash
# Test routing only
cd personareplica/engine
python agentic_router.py

# Test RAG only
cd personareplica/retrieval
python agentic_rag.py
```

## 📊 Personas

### 🏥 Doctor Empathetic (doctor_empathetic_v1)

**Domain**: Medical  
**Dataset**: ChatDoctor-HealthCareMagic-100k  
**Style Characteristics**:
- High empathy (0.8+)
- High hedging (medical caution)
- Professional formality
- Detailed responses

**Example Queries**:
- "I have a fever and headache"
- "What are the symptoms of diabetes?"
- "Is this chest pain serious?"

### 📚 Teacher Supportive (teacher_supportive_v1)

**Domain**: Education  
**Dataset**: OpenAssistant/oasst2  
**Style Characteristics**:
- High question rate (Socratic method)
- Supportive and encouraging tone
- Clear explanations
- Step-by-step guidance

**Example Queries**:
- "Can you explain photosynthesis?"
- "How do I solve quadratic equations?"
- "What's the difference between mitosis and meiosis?"

## 🔧 Configuration

### Environment Variables

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

### Persona Configuration

Personas are configured in `persona/profiles/*.json`:
```json
{
  "persona_id": "doctor_empathetic_v1",
  "domain": "medical",
  "style_metrics": {
    "avg_sentence_length": 11.73,
    "empathy_score": 0.116,
    "question_rate": 0.010,
    "formality_score": 0.224,
    "lexical_diversity": 0.079,
    "hedging_rate": 1.0,
    "avg_response_length": 101.73
  }
}
```

## 📚 Documentation

- [Quick Start Guide](QUICK_START.md)
- [Setup Guide](EDUCATION_SETUP_GUIDE.md)
- [Implementation Details](EDUCATION_IMPLEMENTATION_COMPLETE.md)
- [Changes Summary](CHANGES_SUMMARY.md)
- [Documentation Index](DOCUMENTATION_INDEX.md)

## 🛠️ Tech Stack

- **LLM**: Groq (LLaMA 3.1 8B, LLaMA 3.3 70B)
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Vector DB**: FAISS (IndexFlatIP for cosine similarity)
- **Keyword Search**: BM25
- **Datasets**: HuggingFace Datasets
- **Web UI**: Streamlit
- **API**: FastAPI (optional)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Datasets**: 
  - ChatDoctor-HealthCareMagic-100k by [lavita](https://huggingface.co/lavita)
  - OpenAssistant/oasst2 by [OpenAssistant](https://huggingface.co/OpenAssistant)
- **LLM Provider**: [Groq](https://groq.com)
- **Embeddings**: [SentenceTransformers](https://www.sbert.net/)
- **Vector Search**: [FAISS by Meta](https://github.com/facebookresearch/faiss)

## 📧 Contact

Thanishka - [@Thanishka1205](https://github.com/Thanishka1205)

Project Link: [https://github.com/Thanishka1205/personareplica](https://github.com/Thanishka1205/personareplica)

---

**Built with ❤️ using Groq, FAISS, and Python**
