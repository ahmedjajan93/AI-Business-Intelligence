# 📊 InsightAgent – Business Intelligence Agent

InsightAgent is an AI-powered business intelligence tool built using LangChain and Streamlit. It scrapes company websites, retrieves insights using LLMs, generates SWOT analyses, and provides mock financial/news data.

---

## 🔧 Features

- 🌐 Scrape and analyze website content
- 🤖 Ask natural language questions about companies
- 📊 Generate AI-powered SWOT analyses
- 📰 Mock company news headlines
- 💹 Mock stock market data

---

## 📁 Project Structure

```
BUSINESS_INTELLIGENCE_AGENT/
│
├── index_store/               # FAISS vectorstore index files
│   └── faiss_index
│
├── tools/                    # Business tools
│   ├── news_tool.py
│   ├── stock_tool.py
│   └── swot_tool.py
│
├── utils/                    # Utility functions
│   ├── embedder.py
│   ├── faiss_utils.py
│   └── web_scraper.py
│
├── agent.py                  # Builds LangChain QA agent
├── app.py                    # Streamlit app UI
├── README.md
└── requirements.txt
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
$ git clone https://github.com/yourusername/business_intelligence_agent.git
$ cd business_intelligence_agent

# 2. Create and activate virtual environment (optional)
$ python -m venv venv
$ source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Run the Streamlit app
$ streamlit run app.py
```

---

## 🌐 Deployment

You can deploy this on [Streamlit Cloud](https://streamlit.io/cloud) by linking your GitHub repo. One-click deploy!

---

## 🧠 Tech Stack

- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io)
- [FAISS](https://github.com/facebookresearch/faiss)
- [OpenAI / OpenRouter](https://openrouter.ai) (or plug in any LLM)
- [HuggingFace Embeddings](https://huggingface.co)

---

## 📌 Note

Mock data is used for news and stock tools. You can easily replace these with APIs (e.g., NewsAPI, Yahoo Finance, etc).

---

## 💼 Made for Jobs

This is a real-world LLM product you can showcase to employers. Modular, production-ready, and extensible.
