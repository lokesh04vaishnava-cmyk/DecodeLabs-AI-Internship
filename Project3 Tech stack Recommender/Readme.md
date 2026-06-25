# Project 3 — Tech Stack Recommender (AI Recommendation Logic)

## Overview
A content-based recommendation engine that maps a user's skills to the most relevant career/job roles using TF-IDF vectorization and Cosine Similarity. Built without requiring historical user interaction data — works from item attributes alone.

## Features
- Accepts 3 user-input skills
- Converts skills + job roles into TF-IDF weighted vectors (shared vocabulary space)
- Calculates Cosine Similarity between user profile and every job role
- Returns Top-3 ranked recommendations with match percentage
- Content-based filtering — avoids the "Item Cold Start" problem entirely

## Tech Stack
- Python 3.12
- scikit-learn (TfidfVectorizer, cosine_similarity)
- pandas

## How to Run
```bash
pip install scikit-learn pandas numpy
python recommender.py
```

## Sample Run
