<div align="center">
  <img src="docs/hero_banner.png" alt="InsightFlow AI Banner" width="100%" style="border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);" />

  <br/><br/>

  [![agents-cli](https://img.shields.io/badge/Built_with-agents--cli_v0.3.0-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://pypi.org/project/google-agents-cli/)
  [![Google ADK](https://img.shields.io/badge/Google_ADK-Framework-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white)](https://google.github.io/adk-docs/)
  [![Gemini](https://img.shields.io/badge/Gemini_Flash-Latest-blueviolet?style=for-the-badge)](https://deepmind.google/technologies/gemini/)
  [![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Cloud Run](https://img.shields.io/badge/Cloud_Run-Ready-34A853?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/run)

  <br/>
  <p><b>Your AI-powered personal Data Analyst. Scaffolded with <code>agents-cli</code> — upload a CSV, get instant charts & insights.</b></p>
</div>

---

## 📖 Overview

**InsightFlow AI** is a production-ready agentic AI application built using **[google-agents-cli](https://google.github.io/agents-cli/)**—Google's unified CLI tool for the full Agent Development Kit (ADK) development lifecycle.

By declaring intent through config, writing custom Python tool logic, and utilizing Gemini's reasoning engine, InsightFlow automatically processes CSV files, generates rich visualizations, and extracts business intelligence.

---

## 🏗️ Technical Architecture

The following diagram illustrates how the `agents-cli` orchestrates the local development, model execution, deployment, and monitoring paths.

<div align="center">
  <img src="docs/agents_cli_architecture.png" alt="agents-cli Technical Architecture" width="90%" style="border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin: 20px 0;" />
  <p><i>System Architecture: CLI Interface ➜ Manifest Config ➜ Agent Logic (ADK) ➜ Gemini Reasoning ➜ Deployments & Telemetry</i></p>
</div>

---

## 🔄 Agent Development Lifecycle (ADLC)

`agents-cli` structures the lifecycle of your Agentic workflows into 6 distinct stages:

<div align="center">
  <img src="docs/agents_cli_lifecycle.png" alt="Agent Development Lifecycle" width="90%" style="border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin: 20px 0;" />
  <p><i>The 6-Step Developer Loop enabled by agents-cli</i></p>
</div>

---

## 🚀 Getting Started

### Prerequisites
- **[uv](https://docs.astral.sh/uv/)** — Extremely fast Python package installer and manager.
- **google-agents-cli** — Install globally via:
  ```bash
  uv tool install google-agents-cli
  ```
- **Google Cloud SDK** — Configured with active credentials:
  ```bash
  gcloud auth application-default login
  ```

### 1. Project Initialization & Setup
The repository comes pre-scaffolded with all necessary configuration. Install the project dependencies using the CLI:
```bash
agents-cli install
```

### 2. Run the Interactive Local Server
While `agents-cli playground` launches the default development interface, for full chart visualization (which serves static assets from `/charts/`), launch the FastAPI application directly:
```bash
uv run uvicorn app.fast_api_app:app --host 127.0.0.1 --port 8080 --reload
```
Once started, navigate to:
👉 **[http://127.0.0.1:8080/dev-ui/?app=app](http://127.0.0.1:8080/dev-ui/?app=app)**

---

## 🧪 Testing and Quality Evaluation

Agent development requires robust testing loops to measure agent prompt stability and tool correctness.

### Local Quality Evals (LLM-as-a-Judge)
Run the built-in evaluation set to test model outputs against expectations defined in `tests/eval/evalsets/`:
```bash
agents-cli eval run
```

### Unit & Integration Testing
Execute standard unit tests and API integration suites:
```bash
# Run pytest test suite
uv run pytest tests/unit tests/integration -v

# Run agent static analysis
agents-cli lint
```

---

## 🛠️ Custom Agent Capabilities

Scaffolded under `app/agent.py`, the agent leverages customized Python tool execution to perform data operations:

| Capability Tool | Description | Input Context |
| :--- | :--- | :--- |
| `analyze_csv` | Parses CSV metadata, columns, shape, and structure | CSV File Path |
| `generate_bar_chart` | Dynamically maps sales metrics to clean Matplotlib bar charts | CSV Column |
| `generate_pie_chart` | Formulates category distribution percentages as pie charts | CSV Column |
| `generate_infographic` | Combines analysis metrics into a single multi-chart visual layout | CSV Path |
| `generate_insights` | Evaluates charts and generates strategic executive advice | CSV + Graph context |
| `save_csv_content` | Saves pasted raw CSV content locally for analysis tools | Raw text block |

---

## 📁 Repository Structure

```text
insightflow-ai/
├── agents-cli-manifest.yaml   # Declarative agents-cli configuration manifest
├── GEMINI.md                  # Developer guidelines and agent context
├── Dockerfile                 # Cloud Run containerization schema
├── pyproject.toml             # Dependencies managed via uv
├── app/
│   ├── agent.py               # Main Agent definition, instructions, and tools
│   ├── fast_api_app.py        # FastAPI server running the dev-ui and chart assets
│   └── app_utils/
│       ├── telemetry.py       # OpenTelemetry context for tracing
│       └── typing.py          # Shared type validation
├── deployment/
│   └── terraform/             # Cloud Infrastructure (Cloud Run, BigQuery, IAM)
├── docs/                      # UI images and architecture assets
└── tests/
    ├── unit/                  # Local logic unit tests
    ├── integration/           # Endpoint integration tests
    └── eval/                  # Golden dataset evaluations
```

---

## ☁️ Production Deployment

Deploy the agent to Google Cloud Run with single-command ease:

```bash
# Set your active GCP Project
gcloud config set project <YOUR_PROJECT_ID>

# Provision required project infrastructure
agents-cli infra single-project

# Package, build, and deploy the agent app
agents-cli deploy
```

---

> [!TIP]
> Utilize the **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** for AI-assisted development. Context definitions are configured inside `GEMINI.md`.

> [!NOTE]
> All telemetry (user prompts, tool execution paths, token counts) is exported directly to Google Cloud BigQuery for enterprise-grade analytics and observability.

---

<div align="center">
  <sub>Scaffolded with <b>agents-cli</b> · Powered by <b>Google ADK</b> & <b>Gemini</b> · Deployed on <b>Cloud Run</b></sub>
</div>
