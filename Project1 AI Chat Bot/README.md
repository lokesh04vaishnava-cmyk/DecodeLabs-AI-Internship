# Project 1 — Rule-Based AI Chatbot (ICHIGO)

## Overview
A rule-based chatbot built in Python that uses dictionary lookups (O(1)) instead of if-elif chains (O(n)) to respond to user input. When a user's message doesn't match any predefined rule, the bot falls back to the Groq LLaMA API for an open-ended AI response — combining deterministic reliability with generative flexibility.

## Features
- Continuous input loop with clean exit command (`exit` / `quit`)
- Input sanitization (lowercase + whitespace stripping)
- Dictionary-based knowledge base with 15+ intents
- Two-layer matching: exact match → keyword scan fallback
- Hybrid architecture: unmatched queries are answered by Groq's LLaMA 3.3 model
- Packaged as a standalone Windows `.exe` using PyInstaller

## Tech Stack
- Python 3.12
- Groq API (`llama-3.3-70b-versatile`)

## Setup
This project requires a Groq API key set as an environment variable.

**Windows (Command Prompt):**
```bash
set GROQ_API_KEY=your_key_here
```

**Windows (permanent):**
Search "Environment Variables" → Edit the system environment variables → New User Variable → Name: `GROQ_API_KEY`, Value: your key. Restart your terminal/IDE after.

## How to Run
```bash
pip install groq
python Ichigo.py
```

## Architecture
