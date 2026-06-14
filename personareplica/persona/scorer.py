#!/usr/bin/env python3
"""
PersonaScorer: Measure how well a response matches a persona using cosine similarity.
"""

import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import Tuple

class PersonaScorer:
    def __init__(self):
        """Initialize the scorer with embeddings model."""
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384
        self.indices = {}  # Cache loaded indices
        self.profiles = {}  # Cache loaded profiles
    
    def load_profile(self, persona_id: str) -> dict:
        """Load persona profile from JSON."""
        if persona_id in self.profiles:
            return self.profiles[persona_id]
        
        profiles_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/persona/profiles")
        profile_path = profiles_dir / f"{persona_id}.json"
        
        if not profile_path.exists():
            raise FileNotFoundError(f"Profile not found: {profile_path}")
        
        with open(profile_path, 'r') as f:
            profile = json.load(f)
        
        self.profiles[persona_id] = profile
        return profile
    
    def load_index(self, persona_id: str) -> faiss.Index:
        """Load FAISS index from file."""
        if persona_id in self.indices:
            return self.indices[persona_id]
        
        indices_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/retrieval/indices")
        index_path = indices_dir / f"{persona_id}.index"
        
        if not index_path.exists():
            raise FileNotFoundError(f"Index not found: {index_path}")
        
        index = faiss.read_index(str(index_path))
        self.indices[persona_id] = index
        return index
    
    def score_response(self, response: str, persona_id: str) -> Tuple[float, dict]:
        """
        Score a response against a persona's communication style.
        
        Uses cosine similarity between the response embedding and the persona's 
        FAISS index to measure how well it matches.
        
        Score formula: (raw_inner_product + 1) / 2 normalizes [-1, 1] to [0, 1]
        
        Args:
            response: Generated response text
            persona_id: Persona to score against
        
        Returns:
            Tuple of (score, details_dict)
            - score: float in [0.0, 1.0]
            - details_dict: dict with breakdown info
        """
        # Load profile and index
        profile = self.load_profile(persona_id)
        index = self.load_index(persona_id)
        
        # Embed response
        response_embedding = self.embedder.encode([response], convert_to_numpy=True)
        response_embedding = response_embedding.astype(np.float32)
        
        # L2 normalize
        response_embedding = response_embedding / np.linalg.norm(response_embedding, axis=1, keepdims=True)
        
        # Search in index (returns top-k by inner product)
        k = 5  # Compare to top-5 examples
        distances, indices = index.search(response_embedding, k)
        
        # distances[0] contains inner products with top-k examples
        mean_similarity = float(distances[0][0])  # Similarity to most similar example
        
        # Normalize to [0, 1]: (inner_product + 1) / 2
        # Inner products on L2-normalized vectors range from -1 to 1
        score = (mean_similarity + 1.0) / 2.0
        
        # Determine if response is flagged (below quality threshold)
        quality_threshold = 0.72
        is_flagged = score < quality_threshold
        
        details = {
            "persona_id": persona_id,
            "domain": profile.get("domain"),
            "raw_similarity": float(mean_similarity),
            "accuracy_score": float(score),
            "is_flagged": is_flagged,
            "quality_threshold": quality_threshold,
            "top_k_similarities": distances[0].tolist()[:k]
        }
        
        return score, details

def main():
    """Test the PersonaScorer."""
    scorer = PersonaScorer()
    
    # Test responses
    test_responses = [
        ("I understand you're concerned about your health. Let me ask you a few questions to better understand your situation.", "doctor_empathetic_v1"),
        ("That's an excellent question. Let me guide you through the concepts step by step. What do you already know about this topic?", "teacher_supportive_v1"),
    ]
    
    for response, persona_id in test_responses:
        try:
            score, details = scorer.score_response(response, persona_id)
            print(f"\nResponse: {response[:60]}...")
            print(f"Persona: {persona_id}")
            print(f"Score: {score:.3f}")
            print(f"Details: {json.dumps(details, indent=2)}")
        except FileNotFoundError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()