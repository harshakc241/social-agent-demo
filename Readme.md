# Social Media Agent — Content idea & caption generator (30-min prototype)

## What this is
A minimal Streamlit demo that generates social media post ideas, captions, and hashtags from a topic using OpenAI or a deterministic offline fallback. Designed to be implemented in ~30 minutes for a hackathon/prototype.

## Features (what works in the demo)
- Input: topic, platform, tone, number of posts
- Model select: choose your model or `offline` fallback
- Force strict JSON prompt to simplify parsing
- Download generated posts as CSV or JSON
- Robust fallback when API key or package missing

## Quick run (local)
1. Clone repo
2. Create venv (optional)
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # mac/linux
   .venv\Scripts\activate      # windows
