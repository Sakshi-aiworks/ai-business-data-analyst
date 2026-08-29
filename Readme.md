# 🤖 AI Business Data Analyst

An AI-powered data analysis application that allows users to upload business data in **CSV or Excel format** and ask questions about the data using natural language.

## 📌 Project Status

🚧 **Currently in development**

This project is being developed step by step as a portfolio project and as the foundation for a future AI-powered business automation service.

---

## 🎯 Project Goal

The goal is to build an AI Data Analyst that can:

* Read CSV and Excel files
* Clean and process business data
* Analyze sales, profit, products, and regions
* Understand questions asked in natural language
* Use Python/Pandas for accurate calculations
* Use an LLM to understand user questions and explain results
* Generate useful business insights
* Create charts and reports
* Eventually support multiple files and databases

---

## 🏗️ Planned Architecture

```text
                    USER
                      │
                      ▼
              AI DATA ANALYST
                      │
                      ▼
             QUESTION UNDERSTANDING
                      │
                      ▼
             PYTHON / PANDAS
                      │
             ┌────────┴────────┐
             ▼                 ▼
          CSV/Excel        SQL Database
             │                 │
             └────────┬────────┘
                      ▼
                 DATA ANALYSIS
                      │
                      ▼
                    LLM
                      │
             ┌────────┴────────┐
             ▼                 ▼
        Explanation         Charts
             │                 │
             └────────┬────────┘
                      ▼
                 FINAL ANSWER
```

---

## 🛠️ Technology Stack

### Current

* Python 3.13
* Pandas
* OpenPyXL
* CSV
* Excel

### Planned

* LLM / Generative AI
* AI Agent framework
* Streamlit or web interface
* SQL
* RAG
* AWS
* API integration
* Data visualization
* Automated reporting

---

## 📂 Project Structure

```text
AI_Business_Data_Analyst/
│
├── data/
│   └── sales_data.csv
│
├── src/
│   ├── data_loader.py
│   ├── analysis.py
│   └── main.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

### File Purpose

**`data/`**
Contains sample datasets used for development and testing.

**`data_loader.py`**
Loads CSV and Excel files into Pandas DataFrames.

**`analysis.py`**
Contains reusable functions for calculating sales, profit, product performance, and regional performance.

**`main.py`**
Entry point of the current application. Loads the data and runs the analysis functions.

**`README.md`**
Project documentation and notes.

**`.gitignore`**
Prevents unnecessary files such as virtual environments and Python cache files from being uploaded to GitHub.

---

## 📊 Current Features

The current version can:

* Load CSV files
* Load Excel files
* Calculate total sales
* Calculate total profit
* Find the top-performing product
* Calculate sales by region
* Calculate sales by product

---

## 🔮 Future Features

The project will gradually be upgraded to support:

### Phase 1 — Data Analysis

* CSV/Excel processing
* Data cleaning
* Business calculations

### Phase 2 — AI

* Natural-language questions
* LLM integration
* AI-generated explanations

### Phase 3 — Agent

* Tool/function calling
* Automatic selection of analysis functions
* Multi-step reasoning
* Error handling

### Phase 4 — Advanced Analytics

* Charts
* Trend analysis
* Forecasting
* Automated reports

### Phase 5 — Production

* Web interface
* AWS deployment
* Authentication
* Database integration
* Monitoring
* Scalable architecture

---

## 🧠 Example Questions

The final AI Agent should be able to answer questions such as:

```text
What are the total sales?

Which product generated the highest revenue?

Which region performed the best?

What was the total profit?

Compare sales between regions.

Which product should management focus on?

Give me a summary of the business performance.
```

---

## 🔐 Important Security Note

API keys, passwords, credentials, private datasets, and other secrets must **never be committed to GitHub**.

Sensitive configuration will be stored using environment variables or other secure methods.

---

## 📈 Business Use Case

This project is designed as a foundation for an AI automation service.

Potential future customers could use the system to:

* Analyze sales data
* Automate monthly reports
* Generate management summaries
* Ask questions about business data
* Reduce manual Excel analysis
* Connect business data sources to AI

---

## 👩‍💻 Development Approach

This project is being built incrementally:

```text
Data Processing
      ↓
Python Analysis
      ↓
AI Integration
      ↓
AI Agent
      ↓
Web Application
      ↓
Cloud Deployment
      ↓
Business Product
```

The priority is to build a reliable data-analysis foundation first and then add AI capabilities.

---

## 🚀 Current Development Step

**Day 2 — Project Setup & Data Analysis Engine**

Current focus:

1. Set up Python environment
2. Install Pandas and OpenPyXL
3. Create sample sales data
4. Build data-loading functions
5. Build reusable analysis functions
6. Test the basic analysis engine

---

## 📌 Disclaimer

This project uses sample business data for development and demonstration purposes. No confidential or real customer data should be uploaded during development.
