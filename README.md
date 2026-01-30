# Job Market Skill Analyzer

An automated system that analyzes real-world job descriptions to identify
the most in-demand technical skills and recommend what to focus on for
future job readiness.

## Motivation
Students often rely on guesswork to decide which skills to learn.
This project replaces guesswork with data-driven insights derived from
actual job descriptions.

## What This Project Does
- Fetches job-related emails programmatically
- Extracts job descriptions from email bodies and linked documents
- Cleans and normalizes unstructured text
- Deterministically extracts technical skills
- Aggregates skill demand across roles
- Uses an LLM to synthesize learning priorities

## Pipeline Overview
1. Email ingestion (Gmail API)
2. HTML and document parsing
3. Skill extraction using rule-based matching
4. Frequency aggregation
5. LLM-based prioritization and insights

## Example Output
- Python, Machine Learning, SQL, and AWS emerge as foundational skills
- GenAI skills (LLMs, RAG) show strong and growing demand
- Production skills differentiate industry-ready candidates

## Tech Stack
- Python
- Gmail API
- BeautifulSoup
- Google Docs public endpoints
- Deterministic NLP
- Large Language Models (for synthesis only)

## Why This Matters
This project demonstrates:
- End-to-end system thinking
- Real-world data handling
- Hybrid rule-based + LLM design
- Token-efficient AI usage
- Automation readiness

## Future Work
- Monthly automation
- Trend analysis over time
- Visualization dashboard
- Skill gap analysis

---

