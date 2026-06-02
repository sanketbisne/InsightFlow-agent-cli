# ruff: noqa

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import google.auth

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from google.adk.plugins.bigquery_agent_analytics_plugin import (
    BigQueryAgentAnalyticsPlugin,
    BigQueryLoggerConfig,
)

from google.cloud import bigquery


# =============================================================================
# GCP ENVIRONMENT SETUP
# =============================================================================

_, project_id = google.auth.default()

os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


# =============================================================================
# TOOL 1 - ANALYZE CSV
# =============================================================================

def greet_user(message: str) -> str:
    """
    Greets the user.

    Args:
        message: User greeting

    Returns:
        Greeting response
    """

    return """
Hi 👋 I am your AI Analytics Agent.

I can help you with:
- CSV analysis
- Bar charts
- Pie charts
- AI insights
- Trend analysis
- Executive summaries

Upload or place a CSV file in the project folder and ask me to analyze it 🚀
"""
def analyze_csv(file_path: str) -> str:
    """
    Analyze CSV file.

    Args:
        file_path: Path to CSV file

    Returns:
        CSV summary
    """

    try:
        df = pd.read_csv(file_path)

        return f"""
✅ CSV Analysis Complete

📁 File:
{file_path}

📊 Dataset Information
- Rows: {df.shape[0]}
- Columns: {df.shape[1]}

📌 Column Names:
{list(df.columns)}

🔍 Sample Data:
{df.head(5).to_string()}
"""

    except Exception as e:
        return f"❌ Error analyzing CSV: {str(e)}"


# =============================================================================
# TOOL 2 - GENERATE BAR CHART
# =============================================================================

def generate_bar_chart(file_path: str) -> str:
    """
    Generate bar chart from CSV.

    Args:
        file_path: Path to CSV file

    Returns:
        Chart generation result
    """

    try:
        df = pd.read_csv(file_path)

        numeric_columns = df.select_dtypes(include=["number"]).columns

        if len(numeric_columns) == 0:
            return "❌ No numeric columns found."

        column = numeric_columns[0]

        plt.figure(figsize=(10, 5))

        df[column].head(10).plot(kind="bar")

        plt.title(f"Bar Chart for {column}")
        plt.xlabel("Index")
        plt.ylabel(column)

        plt.tight_layout()

        chart_path = "bar_chart.png"

        plt.savefig(chart_path)

        return f"""
✅ Bar chart generated successfully.

📈 Chart Column:
{column}

📁 Chart saved at:
{chart_path}
"""

    except Exception as e:
        return f"❌ Error generating chart: {str(e)}"


# =============================================================================
# TOOL 3 - GENERATE PIE CHART
# =============================================================================

def generate_pie_chart(file_path: str) -> str:
    """
    Generate pie chart from CSV.

    Args:
        file_path: Path to CSV file

    Returns:
        Pie chart generation result
    """

    try:
        df = pd.read_csv(file_path)

        numeric_columns = df.select_dtypes(include=["number"]).columns

        if len(numeric_columns) == 0:
            return "❌ No numeric columns found."

        column = numeric_columns[0]

        plt.figure(figsize=(7, 7))

        df[column].head(5).plot(kind="pie", autopct="%1.1f%%")

        plt.ylabel("")

        pie_chart_path = "pie_chart.png"

        plt.tight_layout()

        plt.savefig(pie_chart_path)

        return f"""
✅ Pie chart generated successfully.

📈 Chart Column:
{column}

📁 Chart saved at:
{pie_chart_path}
"""

    except Exception as e:
        return f"❌ Error generating pie chart: {str(e)}"


# =============================================================================
# TOOL 3.5 - GENERATE INFOGRAPHIC
# =============================================================================

def generate_infographic(file_path: str) -> str:
    """
    Generate an infographic dashboard (bar and pie chart) from CSV.

    Args:
        file_path: Path to CSV file

    Returns:
        Infographic generation result
    """

    try:
        df = pd.read_csv(file_path)

        numeric_columns = df.select_dtypes(include=["number"]).columns

        if len(numeric_columns) == 0:
            return "❌ No numeric columns found."

        column = numeric_columns[0]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bar chart
        df[column].head(10).plot(kind="bar", ax=ax1)
        ax1.set_title(f"Bar Chart for {column}")
        ax1.set_xlabel("Index")
        ax1.set_ylabel(column)

        # Pie chart
        df[column].head(5).plot(kind="pie", autopct="%1.1f%%", ax=ax2)
        ax2.set_ylabel("")
        ax2.set_title(f"Distribution of {column}")

        plt.suptitle(f"CSV Analytics Infographic: {file_path}", fontsize=16)
        plt.tight_layout()

        infographic_path = "infographic.png"
        plt.savefig(infographic_path)
        plt.close()

        return f"""
✅ Infographic dashboard generated successfully.

📈 Analyzed Column:
{column}

📁 Dashboard saved at:
{infographic_path}
"""
    except Exception as e:
        return f"❌ Error generating infographic: {str(e)}"


# =============================================================================
# TOOL 4 - GENERATE AI INSIGHTS
# =============================================================================

def generate_insights(file_path: str) -> str:
    """
    Generate AI insights from CSV.

    Args:
        file_path: Path to CSV file

    Returns:
        AI insights
    """

    try:
        df = pd.read_csv(file_path)

        numeric_cols = df.select_dtypes(include=["number"]).columns

        insights = f"""
📊 AI Insights Report

✅ Dataset Summary
- Total Rows: {df.shape[0]}
- Total Columns: {df.shape[1]}
- Numeric Columns: {len(numeric_cols)}

📌 Top Columns:
{list(df.columns[:5])}

📈 Recommendations:
- Review trends in numeric data
- Detect anomalies and outliers
- Use dashboards for executive reporting
- Build forecasting models for predictions

🚀 AI Observation:
This dataset appears suitable for analytics and visualization workflows.
"""

        return insights

    except Exception as e:
        return f"❌ Error generating insights: {str(e)}"


# =============================================================================
# ROOT AGENT
# =============================================================================

root_agent = Agent(
    name="csv_analytics_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""
You are an AI CSV Analytics Agent.

When the user says:
- hi
- hello
- hey

Greet them warmly like this:

"Hi 👋 I am your AI Analytics Agent.

I can help you:
- analyze CSV files
- generate bar charts
- create pie charts
- generate AI insights
- explain trends and analytics"

Your responsibilities:
- Analyze CSV files
- Generate charts and infographics
- Create executive summaries
- Explain data trends
- Generate AI insights

CRITICAL RULE:
Whenever the user provides a prompt with a CSV file or asks to analyze an uploaded CSV file, you MUST automatically use the `generate_infographic` tool to create a visual infographic chart for them.

When users ask:
- analyze CSV
- generate charts
- visualize data
- explain trends

Automatically use the available tools.

Always behave like a professional AI Data Analyst.
""",
    tools=[
        analyze_csv,
        generate_bar_chart,
        generate_pie_chart,
        generate_infographic,
        generate_insights,
        greet_user,
    ],
)


# =============================================================================
# BIGQUERY ANALYTICS PLUGIN
# =============================================================================

_plugins = []

_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

_dataset_id = os.environ.get(
    "BQ_ANALYTICS_DATASET_ID",
    "adk_agent_analytics",
)

_location = os.environ.get(
    "GOOGLE_CLOUD_LOCATION",
    "asia-south1",
)

if _project_id:
    try:
        bq = bigquery.Client(project=_project_id)

        bq.create_dataset(
            f"{_project_id}.{_dataset_id}",
            exists_ok=True,
        )

        _plugins.append(
            BigQueryAgentAnalyticsPlugin(
                project_id=_project_id,
                dataset_id=_dataset_id,
                location=_location,
                config=BigQueryLoggerConfig(
                    gcs_bucket_name=os.environ.get(
                        "BQ_ANALYTICS_GCS_BUCKET"
                    ),
                    connection_id=os.environ.get(
                        "BQ_ANALYTICS_CONNECTION_ID"
                    ),
                ),
            )
        )

    except Exception as e:
        logging.warning(
            f"Failed to initialize BigQuery Analytics: {e}"
        )


# =============================================================================
# ADK APPLICATION
# =============================================================================

app = App(
    root_agent=root_agent,
    name="app",
    plugins=_plugins,
)