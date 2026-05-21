# SojournAI
# Autonomous Multi-Agent Travel Orchestration Engine ✈️

An enterprise-ready, stateful multi-agent system engineered using **LangGraph** and **LangChain**. The system takes unstructured lifestyle queries from users, breaks down tasks across discrete multi-agent graph nodes, retrieves live flight pricing through external cloud infrastructure tools, and executes mathematical arbitration loops to verify cost limits.

##  State Graph System Architecture

The workflow is designed as a directed acyclic state machine running on LangGraph nodes:

```text
  [START] ──> [Ideation Node] ──> [Financial Check Node] ──> [Arbitrator Node] ──> [END]
                   │                       │                      │
          (Selects Candidates)    (Invokes Apify Tools)   (Enforces Budget Guardrail)


## 🚀 Setup & Local Reproduction Instructions

1. **Clone the repository to your workstation:**
   ```bash
   git clone [https://github.com/subhomishachakraborty/SojournAI.git](https://github.com/subhomishachakraborty/SojournAI.git)
pip install -r requirements.txt
# On macOS/Linux:
export GOOGLE_API_KEY="your_google_gemini_key_here"
export APIFY_API_TOKEN="your_apify_token_here"

# On Windows (Command Prompt):
set GOOGLE_API_KEY="your_google_gemini_key_here"
set APIFY_API_TOKEN="your_apify_token_here"
python app.py
