# Adaptive Multimodal News Dashboard

A Python-based dashboard for personalized news recommendations using NLP (LDA), reinforcement learning, and bias detection.

## Features

- Fetches news by country (default: India) and domain.
- Saves articles to a separate tab with persistent storage.
- Supports light/dark mode.

## Tech Stack

- Python, Streamlit, Gensim, SpaCy, NewsAPI, RL

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Add your NewsAPI key to `src/fetch_news.py`
3. Run: `streamlit run src/dashboard.py`
