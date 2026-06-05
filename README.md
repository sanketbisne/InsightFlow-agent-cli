<div align="center">
  <img src="docs/hero_banner.png" alt="agents-cli Banner" width="100%" style="border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.35);" />

  <br/><br/>

  [![agents-cli](https://img.shields.io/badge/Built_with-agents--cli_v0.3.0-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://pypi.org/project/google-agents-cli/)
  [![Google ADK](https://img.shields.io/badge/Google_ADK-Framework-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white)](https://google.github.io/adk-docs/)
  [![Gemini](https://img.shields.io/badge/Gemini_Flash-Latest-blueviolet?style=for-the-badge)](https://deepmind.google/technologies/gemini/)
  [![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

  <br/>
  <p><b>An AI CSV Analytics Agent scaffolded and managed using Google's <code>agents-cli</code>.</b></p>
</div>

---

## 📖 Introduction

**InsightFlow AI** is a production-grade agentic application created using **`agents-cli`**—Google's unified CLI tool for the full Agent Development Lifecycle (ADLC). 

This project serves as a blueprint showing how to scaffold, build, evaluate, and deploy a Gemini-powered agent that takes CSV data inputs, runs custom Python tools, and outputs rich infographic summaries dynamically.

---

## 🏗️ Simple Architecture Flow

The system processes data through a simple sequential pipeline:

<div align="center">
  <img src="docs/agents_cli_architecture.png" alt="agents-cli Simple Architecture Flow" width="85%" style="border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); margin: 20px 0;" />
</div>

1. **User / CLI:** Developer creates or deploys the agent with `agents-cli`, or a client sends prompts.
2. **CSV File Input:** User uploads a `.csv` file or pastes raw CSV text directly into the chat interface.
3. **agents-cli Agent App:** The core agent app (`app/agent.py`) coordinates instructions, system prompts, and tools.
4. **Vertex AI (Gemini Reasoning):** Gemini decides which tools to invoke based on the user's query.
5. **AI-Generated Infographic Chart:** The agent runs custom data analysis tools and outputs visual chart files (`/charts/infographic.png`).

---

## 🔄 Simple agents-cli Lifecycle

`agents-cli` manages the entire agent project lifecycle from local setup to cloud production:

<div align="center">
  <img src="docs/agents_cli_lifecycle.png" alt="Simple agents-cli Lifecycle Flow" width="85%" style="border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); margin: 20px 0;" />
</div>

---

## 📊 Walkthrough: Generating an Infographic from CSV

Here is a step-by-step example of how the agent consumes a CSV dataset and outputs an infographic dashboard.

### 1. Launch the Application Locally
Run the FastAPI development server to enable local static chart rendering:
```bash
# Install agent dependencies
agents-cli install

# Start the uvicorn development server
uv run uvicorn app.fast_api_app:app --host 127.0.0.1 --port 8080 --reload
```
Open your browser and navigate to: **[http://127.0.0.1:8080/dev-ui/?app=app](http://127.0.0.1:8080/dev-ui/?app=app)**.

### 2. Provide a CSV Dataset
Paste raw CSV text directly in the playground chat or reference a local file:
```csv
Product,Revenue,Units Sold
Widgets,12000,300
Gadgets,18000,450
Gizmos,8500,210
Thingamabobs,15000,380
Doohickeys,9500,240
```

### 3. Ask the Agent for a Visualization
```text
"Analyze this data and generate an infographic dashboard"
```

### 4. Under the Hood Execution
* The agent detects raw CSV text and calls `save_csv_content(csv_content)` to store it as `temp_data.csv`.
* The agent calls `generate_infographic("temp_data.csv")`.
* Matplotlib renders a dual-visualization dashboard:
  - Left Panel: **Bar chart** comparing sales volume.
  - Right Panel: **Pie chart** showing distribution percentages.
* The infographic is saved to `/charts/infographic.png`.
* The agent responds with the inline markdown tag `![Infographic](/charts/infographic.png)` showing the visual dashboard in your chat view.

---

## 🛠️ CLI Command Reference

Manage your agent lifecycle using the official `agents-cli` commands:

| Command | Purpose |
| :--- | :--- |
| **`agents-cli setup`** | Install tools and skills to detected coding agents |
| **`agents-cli create [name]`** | Create a new GCP-based AI agent project from templates |
| **`agents-cli install`** | Install project dependencies |
| **`agents-cli playground`** | Start the local interactive agent playground |
| **`agents-cli run`** | Run the agent with a single prompt (non-interactive) |
| **`agents-cli eval generate`** | Run agent inference over defined evaluation cases |
| **`agents-cli eval grade`** | Grade generated traces and evaluate agent quality |
| **`agents-cli scaffold enhance .`** | Add deployment targets or CI/CD pipelines to a project |
| **`agents-cli scaffold upgrade`** | Upgrade the project structure and dependencies to the latest version |
| **`agents-cli infra`** | Provision Google Cloud infrastructure resources via Terraform |
| **`agents-cli deploy`** | Build container image and deploy the agent to Google Cloud Run |
| **`agents-cli lint`** | Run code quality checks on the agent configuration and code |

---

## 🧪 Testing & Evaluation

### Programmatic Quality Evals
Run inference over the evaluation set to generate traces, then grade the results:
```bash
# 1. Run agent inference over eval cases
agents-cli eval generate

# 2. Grade generated traces and view scores
agents-cli eval grade
```

### Unit & Integration Testing
Execute standard unit tests and API integration suites:
```bash
# Run pytest test suite
uv run pytest tests/unit tests/integration -v

# Run agent static checks
agents-cli lint
```

---

## 📁 Repository Map

```text
insightflow-ai/
├── agents-cli-manifest.yaml   # Declares agent type, layout config, and GCP region
├── GEMINI.md                  # Development guidelines for AI coding tools
├── Dockerfile                 # Container setup for production build
├── pyproject.toml             # Python libraries (Pandas, Matplotlib, FastAPI)
├── app/
│   ├── agent.py               # Core instructions, Gemini config, and custom chart tools
│   ├── fast_api_app.py        # Backend routes, static assets, and dev-ui mounts
│   └── app_utils/
│       ├── telemetry.py       # Observability logs integration
│       └── typing.py          # Shared runtime types
├── docs/                      # UI images and architecture assets
└── tests/
    ├── unit/                  # Local tool testing
    ├── integration/           # E2E server testing
    └── eval/                  # Golden test metrics
```

---

## ☁️ Deployment to Google Cloud Run

Deploy the agent to Google Cloud Run with single-command ease:

```bash
# 1. Select target project
gcloud config set project <YOUR_PROJECT_ID>

# 2. Provision Google Cloud infrastructure (BigQuery, IAM, GCS)
agents-cli infra single-project

# 3. Deploy the application service
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
