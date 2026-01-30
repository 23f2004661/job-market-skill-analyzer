# Job Market Skill Analyzer

> Data-driven insights into in-demand technical skills from real job descriptions

An automated system that analyzes job descriptions from placement cell emails to identify the most sought-after technical skills, helping students make informed decisions about what to learn for career readiness.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Gmail API](https://img.shields.io/badge/Gmail_API-EA4335?style=flat&logo=gmail&logoColor=white)

## 💡 Motivation

Students often rely on guesswork or anecdotal advice when deciding which technical skills to prioritize. This project replaces guesswork with **data-driven insights** extracted from actual job descriptions shared by my college's placement cell, providing a realistic view of industry demands.

## 🎯 What This Does

- **Automated Email Ingestion** - Fetches job-related emails programmatically via Gmail API
- **Content Extraction** - Parses job descriptions from email bodies and linked documents
- **Text Normalization** - Cleans and standardizes unstructured job posting data
- **Skill Identification** - Deterministically extracts technical skills using rule-based NLP
- **Demand Analysis** - Aggregates skill frequencies across multiple job roles
- **AI-Powered Insights** - Uses LLM to synthesize learning priorities and recommendations

## 🔄 Pipeline Overview
```
College Placement Emails (Gmail)
    ↓
Email Ingestion (Gmail API)
    ↓
HTML & Document Parsing (BeautifulSoup, Google Docs API)
    ↓
Text Cleaning & Normalization
    ↓
Skill Extraction (Rule-based NLP)
    ↓
Frequency Aggregation
    ↓
LLM-Based Synthesis (Insights & Recommendations)
    ↓
Actionable Learning Roadmap
```

## 📊 Example Insights

Based on analysis of placement cell job postings:

- **Foundational Skills**: Python, Machine Learning, SQL, and AWS emerge as must-haves
- **Emerging Demand**: GenAI skills (LLMs, RAG, prompt engineering) show strong growth
- **Industry Differentiators**: Production skills (Docker, CI/CD, monitoring) separate job-ready candidates
- **Domain-Specific**: Data engineering roles prioritize Spark and ETL pipelines

## 🛠️ Tech Stack

**Data Collection**
- Gmail API - Automated email retrieval
- Google Docs API - Document content extraction

**Processing**
- Python 3.x - Core language
- BeautifulSoup - HTML parsing
- Deterministic NLP - Rule-based skill matching

**Analysis**
- Pandas - Data aggregation
- Large Language Models - Insight synthesis (token-efficient usage)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Gmail API credentials
- Google Cloud project with APIs enabled

The script will:
1. Authenticate with Gmail
2. Fetch placement cell emails
3. Extract and parse job descriptions
4. Analyze skill frequencies
5. Generate prioritized recommendations

## 📈 Why This Matters

This project demonstrates:

✅ **End-to-End System Thinking** - Complete pipeline from data collection to insights  
✅ **Real-World Data Handling** - Working with messy, unstructured job postings  
✅ **Hybrid AI Design** - Combining rule-based extraction with LLM synthesis  
✅ **Token Efficiency** - Strategic LLM usage only where needed  
✅ **Automation-Ready** - Scalable architecture for continuous monitoring  

## 🎓 Data Source

This project uses **real job descriptions from my college's placement cell emails**, providing authentic insights into what companies are actually looking for when recruiting on campus. This makes the analysis directly relevant to current students and recent graduates.

## 🚧 Future Enhancements

- [ ] **Monthly Automation** - Scheduled analysis of new job postings
- [ ] **Trend Analysis** - Track skill demand changes over time
- [ ] **Interactive Dashboard** - Visualize skill frequencies and trends
- [ ] **Skill Gap Analysis** - Compare personal skills against market demand
- [ ] **Role-Specific Insights** - Separate analysis for SDE, Data Science, DevOps roles
- [ ] **Salary Correlation** - Link skills to compensation data

## 🔐 Privacy & Ethics

- Only analyzes publicly shared job descriptions from placement emails
- No personal candidate data is stored or processed
- Email credentials remain local and are never shared

💼 **Built with real placement data to help students make data-driven career decisions**

⭐ If this project helped you identify skills to learn, consider giving it a star!
