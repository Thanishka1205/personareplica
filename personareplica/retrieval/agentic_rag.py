#!/usr/bin/env python3
"""
AgenticRAG: Intelligent retrieval strategy selection and execution.

Decides whether to use semantic search, BM25 keyword search, hybrid, or no retrieval.
Optionally applies cross-encoder reranking (local, no LLM cost).
"""

import json
import faiss
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv
import os

# Lazy load Groq only when needed
_groq_client = None
_embedder = None
_bm25_indices = {}

def get_embedder():
    """Lazy load sentence embedder."""
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedder

def get_groq_client():
    """Lazy load Groq client."""
    global _groq_client
    if _groq_client is None:
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")
        try:
            from groq import Groq
            _groq_client = Groq(api_key=api_key)
        except ImportError:
            raise ImportError("groq package not installed. Install with: pip install groq")
    return _groq_client

class AgenticRAG:
    def __init__(self, persona_id: str):
        """
        Initialize AgenticRAG for a specific persona.
        
        Args:
            persona_id: Persona identifier (e.g., 'doctor_empathetic_v1')
        """
        self.persona_id = persona_id
        self.embedder = get_embedder()
        self.embedding_dim = 384
        self.faiss_index = None
        self.faiss_texts = None
        self.bm25_index = None
        self.profile = None
        self._load_resources()
    
    def _load_resources(self):
        """Load FAISS index, BM25 index, and profile for this persona."""
        indices_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/retrieval/indices")
        
        # Load FAISS index
        faiss_path = indices_dir / f"{self.persona_id}.index"
        if faiss_path.exists():
            self.faiss_index = faiss.read_index(str(faiss_path))
        else:
            print(f"Warning: FAISS index not found at {faiss_path}")
        
        # Load texts for reference
        texts_path = indices_dir / f"{self.persona_id}_texts.json"
        if texts_path.exists():
            with open(texts_path, 'r', encoding='utf-8') as f:
                self.faiss_texts = json.load(f)
        else:
            print(f"Warning: Texts file not found at {texts_path}")
        
        # Load profile for centroid
        profiles_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/persona/profiles")
        profile_path = profiles_dir / f"{self.persona_id}.json"
        if profile_path.exists():
            with open(profile_path, 'r', encoding='utf-8') as f:
                self.profile = json.load(f)
        else:
            print(f"Warning: Profile not found at {profile_path}")
        
        # Build BM25 index lazily if we have texts
        if self.faiss_texts:
            self._build_bm25_index()
    
    def _build_bm25_index(self):
        """Build BM25 index from texts."""
        if self.persona_id in _bm25_indices:
            self.bm25_index = _bm25_indices[self.persona_id]
            return
        
        # Tokenize texts for BM25
        corpus_tokens = [text.lower().split() for text in self.faiss_texts]
        self.bm25_index = BM25Okapi(corpus_tokens)
        _bm25_indices[self.persona_id] = self.bm25_index
    
    def decide_retrieval_strategy(self, query: str) -> Dict:
        """
        LLM call #2: Decide retrieval strategy.
        
        Returns dict with:
        - strategy: 'semantic' | 'keyword' | 'hybrid' | 'none'
        - num_examples: int (0-7)
        - rerank: bool
        - reasoning: str
        """
        client = get_groq_client()
        
        # Craft decision prompt
        prompt = f"""You are a retrieval strategy optimizer. Given a query and persona, decide:
1. Strategy: semantic (if query is similar to typical requests), keyword (if query has unique terms), hybrid (both apply), none (no retrieval needed)
2. num_examples: How many examples to retrieve (0-7). Higher for technical queries, lower for common ones.
3. rerank: Should we rerank results for quality? (true/false)

Persona: {self.persona_id}
Query: "{query}"

Respond in JSON format:
{{
  "strategy": "...",
  "num_examples": ...,
  "rerank": ...,
  "reasoning": "..."
}}"""
        
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Use faster model for routing
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            response_text = response.choices[0].message.content
            # Try to parse JSON from response
            try:
                decision = json.loads(response_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, extract from text
                decision = {
                    "strategy": "semantic",
                    "num_examples": 3,
                    "rerank": False,
                    "reasoning": f"Fallback decision from: {response_text[:100]}"
                }
            
            return decision
        except Exception as e:
            print(f"Error in decision LLM call: {e}")
            # Fallback to default strategy
            return {
                "strategy": "semantic",
                "num_examples": 3,
                "rerank": False,
                "reasoning": f"Fallback due to error: {str(e)}"
            }
    
    def semantic_search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Semantic search using FAISS.
        
        Returns list of (text, similarity_score) tuples.
        """
        if not self.faiss_index or not self.faiss_texts:
            return []
        
        # Embed query
        query_embedding = self.embedder.encode([query], convert_to_numpy=True)
        query_embedding = query_embedding.astype(np.float32)
        
        # L2 normalize
        query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        
        # Search
        distances, indices = self.faiss_index.search(query_embedding, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.faiss_texts):
                # Normalize distance to [0, 1]
                similarity = (dist + 1.0) / 2.0
                results.append((self.faiss_texts[idx], float(similarity)))
        
        return results
    
    def keyword_search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Keyword search using BM25.
        
        Returns list of (text, bm25_score) tuples.
        """
        if not self.bm25_index or not self.faiss_texts:
            return []
        
        # Tokenize query
        query_tokens = query.lower().split()
        
        # BM25 scores
        scores = self.bm25_index.get_scores(query_tokens)
        
        # Get top-k indices
        top_indices = np.argsort(scores)[::-1][:k]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0:  # Only include positive scores
                results.append((self.faiss_texts[idx], float(scores[idx])))
        
        return results
    
    def negative_filter(self, candidates: List[Tuple[str, float]], 
                       threshold: float = 0.25) -> List[Tuple[str, float]]:
        """
        Remove off-persona examples by checking similarity to centroid.
        
        Args:
            candidates: List of (text, score) tuples
            threshold: Minimum cosine similarity to centroid
        
        Returns:
            Filtered candidates above threshold
        """
        if not self.profile or not candidates:
            return candidates
        
        centroid = np.array(self.profile['centroid'], dtype=np.float32)
        filtered = []
        
        for text, score in candidates:
            # Embed candidate text
            text_embedding = self.embedder.encode([text], convert_to_numpy=True)
            text_embedding = text_embedding.astype(np.float32)
            text_embedding = text_embedding / np.linalg.norm(text_embedding, axis=1, keepdims=True)
            
            # Compute similarity to centroid
            similarity = float(np.dot(text_embedding[0], centroid))
            
            # Normalize to [0, 1]
            similarity_normalized = (similarity + 1.0) / 2.0
            
            if similarity_normalized >= threshold:
                filtered.append((text, score))
        
        return filtered
    
    def retrieve(self, query: str) -> Dict:
        """
        Execute the agentic RAG pipeline.
        
        Returns dict with:
        - examples: list of retrieved example strings
        - decision: decision dict from LLM
        - retrieval_details: details about what was retrieved
        """
        # Step 1: Decide strategy (LLM call #2)
        decision = self.decide_retrieval_strategy(query)
        strategy = decision.get('strategy', 'semantic')
        num_examples = min(decision.get('num_examples', 3), 7)
        should_rerank = decision.get('rerank', False)
        
        examples = []
        retrieval_details = {
            "strategy": strategy,
            "num_examples": num_examples,
            "rerank": should_rerank,
            "decision_reasoning": decision.get('reasoning', ''),
            "semantic_examples": [],
            "keyword_examples": [],
            "reranker_used": False
        }
        
        # Step 2: Execute retrieval
        if strategy == "semantic":
            candidates = self.semantic_search(query, k=num_examples)
            retrieval_details["semantic_examples"] = [c[0] for c in candidates]
        elif strategy == "keyword":
            candidates = self.keyword_search(query, k=num_examples)
            retrieval_details["keyword_examples"] = [c[0] for c in candidates]
        elif strategy == "hybrid":
            semantic_results = self.semantic_search(query, k=num_examples // 2 + 1)
            keyword_results = self.keyword_search(query, k=num_examples // 2 + 1)
            
            # Merge and deduplicate
            seen = set()
            candidates = []
            for text, score in semantic_results + keyword_results:
                if text not in seen:
                    seen.add(text)
                    candidates.append((text, score))
            
            retrieval_details["semantic_examples"] = [c[0] for c in semantic_results]
            retrieval_details["keyword_examples"] = [c[0] for c in keyword_results]
        else:  # "none"
            candidates = []
        
        # Step 3: Negative filter
        candidates = self.negative_filter(candidates, threshold=0.25)
        
        # Step 4: Optional reranking (local cross-encoder, no LLM cost)
        if should_rerank and candidates:
            try:
                from sentence_transformers import CrossEncoder
                reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
                
                # Score all candidates
                texts_only = [c[0] for c in candidates]
                scores = reranker.predict([[query, text] for text in texts_only])
                
                # Re-rank
                scored_candidates = list(zip(texts_only, scores))
                scored_candidates.sort(key=lambda x: x[1], reverse=True)
                
                candidates = [(text, float(score)) for text, score in scored_candidates]
                retrieval_details["reranker_used"] = True
            except Exception as e:
                print(f"Reranking failed (fallback to no rerank): {e}")
        
        # Extract just the texts
        examples = [c[0] for c in candidates]
        
        return {
            "examples": examples,
            "decision": decision,
            "retrieval_details": retrieval_details
        }

def main():
    """Test AgenticRAG with sample queries."""
    # Test medical persona
    print("=== Testing Medical RAG ===")
    medical_rag = AgenticRAG("doctor_empathetic_v1")
    
    medical_query = "I have a severe headache and fever"
    result = medical_rag.retrieve(medical_query)
    
    print(f"Query: {medical_query}")
    print(f"Strategy: {result['decision']['strategy']}")
    print(f"Examples retrieved: {len(result['examples'])}")
    for i, example in enumerate(result['examples'], 1):
        print(f"  {i}. {example[:80]}...")
    
    # Test education persona
    print("\n=== Testing Education RAG ===")
    education_rag = AgenticRAG("teacher_supportive_v1")
    
    education_query = "Can you help me understand photosynthesis?"
    result = education_rag.retrieve(education_query)
    
    print(f"Query: {education_query}")
    print(f"Strategy: {result['decision']['strategy']}")
    print(f"Examples retrieved: {len(result['examples'])}")
    for i, example in enumerate(result['examples'], 1):
        print(f"  {i}. {example[:80]}...")

if __name__ == "__main__":
    main()