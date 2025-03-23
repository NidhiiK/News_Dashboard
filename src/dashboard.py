import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import json
import pandas as pd
from fetch_news import fetch_news
from nlp_processor import get_topics, detect_bias
from rl_agent import QLAgent

# Load or fetch articles
if "articles" not in st.session_state:
    st.session_state.articles = []
if "saved" not in st.session_state:
    st.session_state.saved = []

# UI
st.title("Adaptive News Dashboard")
domains = st.multiselect("Select Domains", ["sports", "technology", "finance", "entertainment", "politics"])
scope = st.radio("Scope", ["All", "National", "International"])
if st.button("Fetch News"):
    if not domains:
        st.warning("Please select at least one domain to fetch news.")
    else:
        st.session_state.articles = fetch_news(domains, scope.lower())
        if not st.session_state.articles:
            st.error("Failed to fetch news. Check API key or internet connection.")

if st.session_state.articles:
    # NLP and RL setup
    topics, lda_model, corpus, dictionary = get_topics(st.session_state.articles)
    agent = QLAgent(num_states=len(topics), num_actions=2)
    
    # Display articles
    st.subheader("Recommended Articles")
    for i, article in enumerate(st.session_state.articles[:5]):  # Top 5 for demo
        bias = detect_bias(article)
        st.write(f"**{article['title']}** ({article['source']['name']}) {'[POTENTIAL BIAS]' if bias else ''}")
        if st.button(f"Save {i}", key=f"save_{i}"):
            st.session_state.saved.append(article)
            agent.update(i % len(topics), 1, 1, (i + 1) % len(topics))  # Reward for save
        if st.button(f"Click {i}", key=f"click_{i}"):
            agent.update(i % len(topics), 0, 1, (i + 1) % len(topics))  # Reward for click
    
    # Saved articles
    st.subheader("Saved Articles")
    for s in st.session_state.saved:
        st.write(f"**{s['title']}**")

    # Topics
    st.subheader("Discovered Topics")
    for topic in topics:
        st.write(topic)

if __name__ == "__main__":
    # Run with: streamlit run src/dashboard.py
    pass