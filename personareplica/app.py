#!/usr/bin/env python3
"""
PersonaReplica - Interactive Web Interface
Run with: streamlit run app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from engine.inference import PersonaInference
from engine.agentic_router import get_router

# Page config
st.set_page_config(
    page_title="PersonaReplica",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'engine' not in st.session_state:
    with st.spinner("Loading PersonaReplica system..."):
        st.session_state.engine = PersonaInference()
if 'router' not in st.session_state:
    st.session_state.router = get_router()

# Title and description
st.title("🤖 PersonaReplica")
st.markdown("""
**Dual-Persona AI System** with intelligent routing between Medical and Education domains.

Ask any question and watch the system:
1. Route to the appropriate persona
2. Retrieve relevant examples
3. Generate a persona-consistent response
""")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Max tokens slider
    max_tokens = st.slider(
        "Response Length (tokens)",
        min_value=50,
        max_value=500,
        value=200,
        step=50
    )
    
    # Show routing info toggle
    show_routing = st.checkbox("Show Routing Details", value=True)
    show_rag = st.checkbox("Show RAG Details", value=True)
    
    st.divider()
    
    # Persona info
    st.header("📊 Available Personas")
    
    st.subheader("🏥 Doctor Empathetic")
    st.caption("**Domain:** Medical")
    st.caption("**Style:** Empathetic, cautious, professional")
    st.caption("**Keywords:** fever, pain, symptoms, health, medical")
    
    st.subheader("📚 Teacher Supportive")
    st.caption("**Domain:** Education")
    st.caption("**Style:** Patient, encouraging, explanatory")
    st.caption("**Keywords:** learn, study, explain, math, science")
    
    st.divider()
    
    # Quick examples
    st.header("💡 Example Queries")
    
    if st.button("🏥 Medical: Headache", use_container_width=True):
        st.session_state.example_query = "I have a severe headache, what should I do?"
    
    if st.button("📚 Education: Photosynthesis", use_container_width=True):
        st.session_state.example_query = "Can you explain photosynthesis to me?"
    
    if st.button("🏥 Medical: Flu symptoms", use_container_width=True):
        st.session_state.example_query = "What are the symptoms of the flu?"
    
    if st.button("📚 Education: Algebra", use_container_width=True):
        st.session_state.example_query = "How do I solve quadratic equations?"
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show metadata if available
            if "metadata" in message and message["role"] == "assistant":
                metadata = message["metadata"]
                
                if show_routing:
                    with st.expander("🔀 Routing Details"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Persona", metadata["routing"]["persona_id"])
                            st.caption(f"Domain: {metadata['routing'].get('domain', 'N/A')}")
                        with col2:
                            st.metric("Confidence", f"{metadata['routing']['confidence']:.2f}")
                        
                        st.text_area(
                            "Reasoning",
                            metadata["routing"]["reasoning"],
                            height=100,
                            disabled=True
                        )
                
                if show_rag and "rag" in metadata:
                    with st.expander("🔍 RAG Details"):
                        rag = metadata["rag"]
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Strategy", rag["decision"]["strategy"])
                        with col2:
                            st.metric("Examples", rag["decision"]["num_examples"])
                        with col3:
                            st.metric("Rerank", "✓" if rag["decision"].get("rerank") else "✗")
                        
                        st.text_area(
                            "RAG Reasoning",
                            rag["decision"]["reasoning"][:200] + "...",
                            height=80,
                            disabled=True
                        )
                        
                        if rag["examples"]:
                            st.caption(f"**Top Example:** {rag['examples'][0][:150]}...")

# Chat input
if prompt := st.chat_input("Ask a medical or educational question..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)
    
    # Generate response
    with chat_container:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Get routing info first
                routing_info = st.session_state.router.route(prompt)
                
                # Generate full response
                response, metadata = st.session_state.engine.generate_response_with_metadata(
                    query=prompt,
                    max_tokens=max_tokens
                )
                
                # Add routing info to metadata
                metadata["routing"] = routing_info
                
                # Display response
                st.markdown(response)
    
    # Add assistant message to chat
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "metadata": metadata
    })
    
    st.rerun()

# Handle example query button clicks
if 'example_query' in st.session_state:
    prompt = st.session_state.example_query
    del st.session_state.example_query
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.spinner("Thinking..."):
        routing_info = st.session_state.router.route(prompt)
        response, metadata = st.session_state.engine.generate_response_with_metadata(
            query=prompt,
            max_tokens=max_tokens
        )
        metadata["routing"] = routing_info
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "metadata": metadata
    })
    
    st.rerun()

# Footer
st.divider()
st.caption("🤖 PersonaReplica v2.0 - Education & Medical Domains | Built with Groq, FAISS, and Sentence Transformers")
