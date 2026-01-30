# Job Market Skill Analyzer

> Data-driven insights into in-demand technical skills from real job descriptions

An automated system that analyzes job descriptions from placement cell emails to identify the most sought-after technical skills, helping students make informed decisions about what to learn for career readiness.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Gmail API](https://img.shields.io/badge/Gmail_API-EA4335?style=flat&logo=gmail&logoColor=white)

## 💡 Motivation

Students often rely on guesswork when deciding which technical skills to prioritize. This project replaces guesswork with **data-driven insights** extracted from actual job descriptions shared by my college's placement cell.

## 🎯 What This Does

- **Automated Email Ingestion** - Fetches job-related emails via Gmail API
- **Content Extraction** - Parses job descriptions from email bodies and linked documents
- **Skill Identification** - Deterministically extracts technical skills using rule-based NLP
- **Demand Analysis** - Aggregates skill frequencies across multiple job roles
- **AI-Powered Insights** - Uses LLM to synthesize learning priorities and recommendations

## 🔄 Pipeline
```
Gmail (Placement Emails) → Parse & Clean → NLP Extraction → 
Frequency Analysis → LLM Synthesis → Learning Roadmap
```

## 📊 Example Insights

From analysis of placement cell job postings:

- **Foundational**: Python, Machine Learning, SQL, AWS
- **Emerging**: GenAI (LLMs, RAG, fine-tuning), HuggingFace
- **Production**: Docker, CI/CD, Microservices
- **Specialized**: Spark, ETL, LLMOps

## 📁 Output Files

- **`OutputNLP.json`** - Raw skill frequencies from rule-based extraction
- **`OutputLLM.json`** - Synthesized insights and learning recommendations from AI analysis

Sample from `OutputNLP.json`:
```json
{
  "skill": "microservices",
  "count": 3
},
{
  "skill": "fine-tuning",
  "count": 3
}
```

## 🛠️ Tech Stack

**Data Collection**: Gmail API, Google Docs API  
**Processing**: Python, BeautifulSoup, Rule-based NLP  
**Analysis**: Pandas, Large Language Models (token-efficient synthesis)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Gmail API credentials
- Google Cloud project with APIs enabled

### Usage
```bash
pip install -r requirements.txt
python analyzer.py
```

Output files generated:
- `OutputNLP.json` - Skill frequency data
- `OutputLLM.json` - AI-generated insights

## 📈 Why This Matters

✅ **End-to-end pipeline** from data collection to insights  
✅ **Real-world data** from actual campus recruitment  
✅ **Hybrid design** combining rule-based + LLM approaches  
✅ **Token-efficient** AI usage  
✅ **Automation-ready** for continuous monitoring

## 🎓 Data Source

Uses **real job descriptions from my college's placement cell emails**, providing authentic insights into what companies actually seek when recruiting on campus.

## 🚧 Future Work

- [ ] Monthly automated analysis
- [ ] Trend tracking over time
- [ ] Interactive visualization dashboard
- [ ] Personal skill gap analysis
- [ ] Role-specific breakdowns (SDE, Data Science, DevOps)

## 🔐 Privacy

- Only analyzes publicly shared job descriptions
- No personal candidate data stored
- Credentials remain local

---

💼 **Built with real placement data to help students make informed career decisions**

⭐ If this helped you identify skills to learn, consider giving it a star!
