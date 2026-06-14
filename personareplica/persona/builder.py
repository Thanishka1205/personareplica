#!/usr/bin/env python3
"""
PersonaBuilder: Extract style metrics from corpus and build FAISS indices.
"""

import json
import os
import re
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Tuple
import faiss

class PersonaBuilder:
    def __init__(self):
        """Initialize the persona builder with embeddings model."""
        print("Loading sentence embeddings model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384
    
    def extract_style_metrics(self, corpus: List[str]) -> Dict[str, float]:
        """
        Extract 7 style metrics from a corpus of responses.
        
        Returns:
            Dict with keys: avg_sentence_length, empathy_score, question_rate, 
            formality_score, lexical_diversity, hedging_rate, avg_response_length
        """
        metrics = {}
        
        # 1. Average sentence length
        sentences = []
        for text in corpus:
            sents = re.split(r'[.!?]+', text)
            sentences.extend([s.strip() for s in sents if s.strip()])
        
        if sentences:
            avg_sentence_length = np.mean([len(s.split()) for s in sentences])
        else:
            avg_sentence_length = 0
        metrics['avg_sentence_length'] = float(avg_sentence_length)
        
        # 2. Empathy score (based on empathy keywords - capped at 1.0)
        empathy_keywords = ['understand', 'feel', 'care', 'compassion', 'empathize', 
                          'concerned', 'sorry', 'help', 'support', 'listen']
        empathy_count = sum(corpus.count(kw) for text in corpus for kw in empathy_keywords)
        total_words = sum(len(text.split()) for text in corpus)
        empathy_score = min((empathy_count / max(total_words, 1)) * 10, 1.0)
        metrics['empathy_score'] = float(empathy_score)
        
        # 3. Question rate (ratio of sentences ending with ?)
        question_count = sum(text.count('?') for text in corpus)
        total_sentences = len(sentences) if sentences else 1
        question_rate = question_count / max(total_sentences, 1)
        metrics['question_rate'] = float(question_rate)
        
        # 4. Formality score (based on formal language - capped at 1.0)
        formal_keywords = ['therefore', 'furthermore', 'consequently', 'moreover',
                          'however', 'nevertheless', 'regarding', 'pertaining']
        formal_count = sum(1 for text in corpus for kw in formal_keywords if kw in text.lower())
        formality_score = min((formal_count / max(len(corpus), 1)) * 2, 1.0)
        metrics['formality_score'] = float(formality_score)
        
        # 5. Lexical diversity (unique words / total words)
        all_words = []
        for text in corpus:
            words = text.lower().split()
            all_words.extend(words)
        
        if all_words:
            lexical_diversity = len(set(all_words)) / len(all_words)
        else:
            lexical_diversity = 0
        metrics['lexical_diversity'] = float(lexical_diversity)
        
        # 6. Hedging rate (uncertain language - capped at 1.0)
        hedging_keywords = ['might', 'may', 'could', 'possibly', 'probably', 
                           'perhaps', 'seem', 'appear', 'suggest']
        hedging_count = sum(1 for text in corpus for kw in hedging_keywords if kw in text.lower())
        hedging_rate = min((hedging_count / max(len(corpus), 1)) * 2, 1.0)
        metrics['hedging_rate'] = float(hedging_rate)
        
        # 7. Average response length
        avg_response_length = np.mean([len(text.split()) for text in corpus]) if corpus else 0
        metrics['avg_response_length'] = float(avg_response_length)
        
        return metrics
    
    def build_persona(self, persona_id: str, domain: str, corpus: List[Dict]) -> Tuple[Dict, str]:
        """
        Build a persona profile and FAISS index from corpus.
        
        Args:
            persona_id: Unique persona identifier
            domain: Domain name (e.g., 'medical', 'interview')
            corpus: List of dicts with 'input', 'response', 'domain', 'persona_id'
        
        Returns:
            Tuple of (profile_dict, index_path)
        """
        if not corpus:
            print(f"Warning: Empty corpus for persona {persona_id}")
            return None, None
        
        print(f"\nBuilding persona: {persona_id}")
        print(f"  Corpus size: {len(corpus)} examples")
        
        # Extract responses
        responses = [item['response'] for item in corpus]
        
        # Compute style metrics
        style_metrics = self.extract_style_metrics(responses)
        print(f"  Style metrics computed:")
        for key, val in style_metrics.items():
            print(f"    {key}: {val:.3f}")
        
        # Embed all responses
        print(f"  Embedding {len(responses)} responses...")
        embeddings = self.embedder.encode(responses, show_progress_bar=False, convert_to_numpy=True)
        embeddings = embeddings.astype(np.float32)
        
        # L2 normalize for cosine similarity
        embeddings_normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Compute centroid for negative filtering
        centroid = np.mean(embeddings_normalized, axis=0)
        
        # Build FAISS index (IndexFlatIP for cosine similarity on normalized vectors)
        index = faiss.IndexFlatIP(self.embedding_dim)
        index.add(embeddings_normalized)
        
        # Prepare profile
        profile = {
            "persona_id": persona_id,
            "domain": domain,
            "corpus_size": len(corpus),
            "style_metrics": style_metrics,
            "centroid": centroid.tolist(),
            "embedding_dim": self.embedding_dim
        }
        
        # Save profile JSON
        profiles_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/persona/profiles")
        profiles_dir.mkdir(parents=True, exist_ok=True)
        profile_path = profiles_dir / f"{persona_id}.json"
        
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=2)
        print(f"  Profile saved to {profile_path}")
        
        # Save FAISS index
        indices_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/retrieval/indices")
        indices_dir.mkdir(parents=True, exist_ok=True)
        index_path = indices_dir / f"{persona_id}.index"
        faiss.write_index(index, str(index_path))
        print(f"  Index saved to {index_path}")
        
        # Save texts for reference
        texts_path = indices_dir / f"{persona_id}_texts.json"
        with open(texts_path, 'w') as f:
            json.dump(responses, f, indent=2)
        print(f"  Texts saved to {texts_path}")
        
        return profile, str(index_path)
    
    def load_corpus_from_jsonl(self, filepath: str) -> List[Dict]:
        """Load corpus from JSONL file."""
        corpus = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    corpus.append(json.loads(line))
        return corpus

def main():
    """Build personas for medical and education domains."""
    builder = PersonaBuilder()
    
    base_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica")
    
    # Build medical persona
    medical_corpus_path = base_dir / "data" / "processed" / "medical" / "processed.jsonl"
    if medical_corpus_path.exists():
        medical_corpus = builder.load_corpus_from_jsonl(str(medical_corpus_path))
        builder.build_persona("doctor_empathetic_v1", "medical", medical_corpus)
    else:
        print(f"Warning: Medical corpus not found at {medical_corpus_path}")
    
    # Build education persona
    education_corpus_path = base_dir / "data" / "processed" / "education" / "processed.jsonl"
    if education_corpus_path.exists():
        education_corpus = builder.load_corpus_from_jsonl(str(education_corpus_path))
        builder.build_persona("teacher_supportive_v1", "education", education_corpus)
    else:
        print(f"Warning: Education corpus not found at {education_corpus_path}")
    
    print("\nPersona building completed!")

if __name__ == "__main__":
    main()