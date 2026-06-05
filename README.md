<div align="center">
  <img src="docs/hero_banner.png" alt="InsightFlow AI Banner" width="100%" style="border-radius: 12px;" />

  <br/><br/>

  [![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/)
  [![Gemini](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white)](https://deepmind.google/technologies/gemini/)
  [![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![License](https://img.shields.io/badge/License-Apache_2.0-orange?style=for-the-badge)](LICENSE)

  <br/>
  <p><b>Your AI-powered personal Data Analyst. Upload a CSV, get instant charts & insights.</b></p>
</div>

---

## 📖 What is InsightFlow AI?

**InsightFlow AI** is a production-ready agentic AI system built on **Google ADK** and powered by **Gemini**. It acts as your personal data analyst — simply provide a CSV file and it automatically generates beautiful visualizations, extracts trends, and delivers executive-level insights in seconds.

> Built as a full showcase of the **Agent Development Lifecycle (ADLC)** — from local development all the way to GCP Cloud Run deployment.

---

## 🏗️ Architecture

<div align="center">
  <img src="docs/architecture.png" alt="InsightFlow AI Architecture" width="80%" style="border-radius: 12px; margin: 16px 0;" />
</div>

| Layer | Technology | Purpose |
|---|---|---|
| 🤖 **AI Agent** | Google ADK + Gemini Flash | Orchestrates tools, reasons over data |
| ⚡ **Backend** | FastAPI + Uvicorn | Serves the dev UI + chart endpoints |
| ☁️ **AI Platform** | Google Vertex AI | Hosts Gemini model inference |
| 📊 **Telemetry** | BigQuery + OpenTelemetry | Logs traces and agent analytics |
| 🏗️ **Infra** | Terraform + Cloud Run | One-click GCP deployment |

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **Bar Charts** | Instant bar chart from any numeric column in your CSV |
| 🥧 **Pie Charts** | Distribution breakdown rendered inline in the chat |
| 📈 **Infographic Dashboards** | Combined bar + pie chart overview in one view |
| 💡 **AI Insights** | Gemini-powered trend analysis and business recommendations |
| 📂 **CSV Handling** | Upload a file or paste raw CSV content directly into chat |
| 🔍 **BigQuery Observability** | Full agent telemetry exported to BigQuery automatically |

---

## 🚀 Quick Start

### Prerequisites

- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — fast Python package manager
- **agents-cli** — `uv tool install google-agents-cli`
- **Google Cloud SDK** — with Vertex AI API enabled and `gcloud auth application-default login`

### 1. Install Dependencies

```bash
uvx google-agents-cli setup
agents-cli install
```

### 2. Run the Dev Server

```bash
uv run uvicorn app.fast_api_app:app --host 127.0.0.1 --port 8080 --reload
```

Open **http://127.0.0.1:8080/dev-ui/?app=app** in your browser.

### 3. Chat with Your Agent

Upload a CSV or paste data directly. Try prompts like:

```
📌 "Generate a bar chart from sales_data.csv"
📌 "Show me a pie chart of Revenue by Region"
📌 "Analyze this dataset and give me AI insights"
```

---

## 📁 Project Structure

```text
insightflow-ai/
├── app/
│   ├── agent.py               # ADK agent — tools for charts, insights & CSV handling
│   ├── fast_api_app.py        # FastAPI server with /charts/ image endpoint
│   └── app_utils/
│       ├── telemetry.py       # OpenTelemetry setup
│       └── typing.py          # Shared type definitions
├── tests/
│   ├── unit/                  # Unit tests (CSV handling, tool logic)
│   ├── integration/           # E2E API tests
│   └── eval/                  # ADK eval datasets for LLM quality testing
├── deployment/
│   └── terraform/             # Cloud Run + IAM + BigQuery Terraform configs
├── docs/                      # Images and documentation assets
├── Dockerfile                 # Container image for Cloud Run
├── pyproject.toml             # Python dependencies (managed via uv)
└── agents-cli-manifest.yaml   # Declarative agent config
```

---

## ☁️ Deploy to Google Cloud

Deploy to Cloud Run with a single command:

```bash
gcloud config set project <YOUR_PROJECT_ID>
agents-cli deploy
```

The Terraform configs in `deployment/terraform/` provision:
- Cloud Run service
- BigQuery dataset for telemetry
- IAM service accounts
- GCS bucket for artifacts
- Cloud Build CI/CD triggers

---

## 🧪 Running Tests

```bash
# Unit tests
uv run pytest tests/unit/ -v

# Integration tests (requires running server)
uv run pytest tests/integration/ -v

# ADK eval suite
uv run adk eval app tests/eval/eval_config.yaml
```

---

## 🛠️ Agent Tools Reference

| Tool | Description |
|---|---|
| `analyze_csv` | Loads CSV and returns shape, columns, and sample rows |
| `generate_bar_chart` | Creates a bar chart PNG served at `/charts/bar_chart.png` |
| `generate_pie_chart` | Creates a pie chart PNG served at `/charts/pie_chart.png` |
| `generate_infographic` | Combined bar + pie dashboard at `/charts/infographic.png` |
| `generate_insights` | Returns AI-driven trend summary and recommendations |
| `save_csv_content` | Saves raw pasted CSV text to a temp file for tool use |

---

## 💡 Tips

> [!TIP]
> Use the [Gemini CLI](https://github.com/google-gemini/gemini-cli) for AI-assisted development. Project context is pre-configured in `GEMINI.md`.

> [!NOTE]
> Charts are served via the `/charts/` endpoint. Do **not** use `agents-cli playground` for chart rendering — run directly via `uvicorn app.fast_api_app:app` to activate the chart serving route.

> [!IMPORTANT]
> Ensure `GOOGLE_CLOUD_PROJECT` is set and `gcloud auth application-default login` has been run before starting the server.

---

<div align="center">
  <sub>Built with ❤️ using <b>Google ADK</b>, <b>Gemini</b>, and <b>FastAPI</b></sub>
</div>
