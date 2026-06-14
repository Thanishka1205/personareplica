#!/usr/bin/env python3
"""
PromptBuilder: Constructs system prompts from persona profiles and retrieved examples.

Maps style metrics to behavioral instructions that guide generation.
Injects few-shot examples to demonstrate communication style.
"""

import json
from pathlib import Path
from typing import List, Dict

class PromptBuilder:
    """Build persona-aware system prompts."""
    
    def __init__(self, persona_id: str):
        """
        Initialize prompt builder for a persona.
        
        Args:
            persona_id: Persona identifier
        """
        self.persona_id = persona_id
        self.profile = self._load_profile()
    
    def _load_profile(self) -> Dict:
        """Load persona profile JSON."""
        profiles_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica/persona/profiles")
        profile_path = profiles_dir / f"{self.persona_id}.json"
        
        if not profile_path.exists():
            raise FileNotFoundError(f"Profile not found: {profile_path}")
        
        with open(profile_path, 'r') as f:
            return json.load(f)
    
    def metrics_to_instructions(self, metrics: Dict[str, float]) -> str:
        """
        Convert style metrics into behavioral instructions.
        
        Args:
            metrics: Dict of style metrics (empathy_score, question_rate, etc.)
        
        Returns:
            String of human-readable instructions to inject into system prompt
        """
        instructions = []
        
        # Empathy score
        empathy = metrics.get('empathy_score', 0.5)
        if empathy >= 0.8:
            instructions.append("- Show deep empathy and genuine concern for the user's situation.")
            instructions.append("- Acknowledge emotions and validate their feelings before providing solutions.")
        elif empathy >= 0.5:
            instructions.append("- Show moderate empathy and understanding of their concerns.")
            instructions.append("- Acknowledge their situation before moving to solutions.")
        else:
            instructions.append("- Maintain professional tone with minimal emotional engagement.")
        
        # Question rate
        question_rate = metrics.get('question_rate', 0.1)
        if question_rate >= 0.25:
            instructions.append("- Ask clarifying questions frequently to guide the user's thinking.")
            instructions.append("- Use Socratic method: lead with questions rather than direct answers.")
        elif question_rate >= 0.15:
            instructions.append("- Ask some clarifying questions to understand the situation better.")
        else:
            instructions.append("- Minimize questions; focus on clear, direct information delivery.")
        
        # Formality score
        formality = metrics.get('formality_score', 0.3)
        if formality >= 0.7:
            instructions.append("- Use formal, technical language and professional terminology.")
            instructions.append("- Structure responses with clear sections and formal transitions.")
        elif formality >= 0.4:
            instructions.append("- Use moderately formal language while remaining approachable.")
        else:
            instructions.append("- Use casual, conversational tone to put user at ease.")
        
        # Hedging rate
        hedging = metrics.get('hedging_rate', 0.3)
        if hedging >= 0.5:
            instructions.append("- Use hedging language (might, may, could, possibly) to express uncertainty.")
            instructions.append("- Avoid absolute statements; qualify claims with appropriate caveats.")
        else:
            instructions.append("- Be confident and direct; avoid unnecessary hedging language.")
        
        # Lexical diversity
        diversity = metrics.get('lexical_diversity', 0.4)
        if diversity >= 0.6:
            instructions.append("- Use varied vocabulary to keep responses engaging and non-repetitive.")
        else:
            instructions.append("- Use simple, clear vocabulary that's easy to understand.")
        
        # Response length
        avg_length = metrics.get('avg_response_length', 50)
        if avg_length > 150:
            instructions.append("- Provide detailed, thorough responses with full context.")
        elif avg_length > 80:
            instructions.append("- Provide moderately detailed responses balancing depth and brevity.")
        else:
            instructions.append("- Keep responses concise and to the point.")
        
        return "\n".join(instructions)
    
    def build_system_prompt(self, examples: List[str], user_query: str = None) -> str:
        """
        Build complete system prompt with metrics and examples.
        
        Args:
            examples: List of few-shot example responses from retrieved corpus
            user_query: Optional current user query for context
        
        Returns:
            Complete system prompt string
        """
        metrics = self.profile.get('style_metrics', {})
        domain = self.profile.get('domain', 'general')
        
        # Build base system prompt
        system_prompt = f"""You are a {domain.title()} Expert Assistant.

YOUR COMMUNICATION STYLE:
{self.metrics_to_instructions(metrics)}

You are an expert in {domain} matters. Your goal is to provide helpful, accurate, and appropriately styled responses.
"""
        
        # Add few-shot examples if available
        if examples:
            system_prompt += "\n\nLEARN FROM THESE STYLE EXAMPLES:\n"
            system_prompt += "These are examples of how to communicate in your style:\n\n"
            
            for i, example in enumerate(examples[:5], 1):  # Limit to top-5 examples
                # Truncate long examples
                if len(example) > 300:
                    example_text = example[:300] + "..."
                else:
                    example_text = example
                system_prompt += f"Example {i}:\n{example_text}\n\n"
        
        # Add query-specific context if provided
        if user_query:
            system_prompt += f"\nCurrent User Query: \"{user_query}\"\n"
            system_prompt += "Apply your style to provide a response that matches these examples.\n"
        
        return system_prompt
    
    def format_for_inference(self, system_prompt: str, user_message: str) -> Dict:
        """
        Format prompt and user message for LLM inference.
        
        Args:
            system_prompt: System prompt string
            user_message: User's input message
        
        Returns:
            Dict with 'system' and 'messages' keys for LLM API
        """
        return {
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

def main():
    """Test prompt building."""
    # Test medical persona
    print("=== Medical Persona Prompt ===")
    medical_builder = PromptBuilder("doctor_empathetic_v1")
    
    medical_examples = [
        "I understand you're concerned about your symptoms. Let me ask you a few questions to better understand what's happening.",
        "It's completely normal to feel worried about these symptoms. Many people experience similar concerns."
    ]
    
    medical_prompt = medical_builder.build_system_prompt(
        examples=medical_examples,
        user_query="I have a severe headache"
    )
    print(medical_prompt)
    print("\n" + "="*50 + "\n")
    
    # Test education persona
    print("=== Education Persona Prompt ===")
    education_builder = PromptBuilder("teacher_supportive_v1")
    
    education_examples = [
        "That's an excellent question! Let me guide you through the approach step by step. What do you already understand about this concept?",
        "Before we solve it, let's break down the problem. What are the key constraints you need to consider?"
    ]
    
    education_prompt = education_builder.build_system_prompt(
        examples=education_examples,
        user_query="How do I solve this math problem?"
    )
    print(education_prompt)

if __name__ == "__main__":
    main()