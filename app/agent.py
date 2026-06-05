# ruff: noqa

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import google.auth
import io
import base64

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
def _load_csv(file_path_or_content: str) -> pd.DataFrame:
    """
    Loads a DataFrame from a file path or raw CSV content string.
    """
    if not os.path.exists(file_path_or_content) and ("," in file_path_or_content or "\n" in file_path_or_content):
        return pd.read_csv(io.StringIO(file_path_or_content))
    return pd.read_csv(file_path_or_content)


def save_csv_content(csv_content: str, file_name: str = "temp_data.csv") -> str:
    """
    Saves raw CSV content to a file in the workspace so other tools can access it.

    Args:
        csv_content: The raw CSV data string.
        file_name: The name of the file to save (e.g., 'sales_data.csv'). Defaults to 'temp_data.csv'.

    Returns:
        Confirmation message with the path.
    """
    try:
        # Clean filename to prevent path traversal
        file_name = os.path.basename(file_name)
        if not file_name.endswith(".csv"):
            file_name += ".csv"
        
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(csv_content.strip())
            
        return f"Successfully saved CSV content to '{file_name}'."
    except Exception as e:
        return f"❌ Error saving CSV content: {str(e)}"


def analyze_csv(file_path: str) -> str:
    """
    Analyze CSV file.

    Args:
        file_path: Path to CSV file

    Returns:
        CSV summary
    """

    try:
        df = _load_csv(file_path)

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
# CHART HELPERS & PALETTE
# =============================================================================

CHART_COLORS = ["#1A365D", "#2B6CB0", "#319795", "#4FD1C5", "#90CDF4", "#718096", "#E2E8F0", "#4A5568"]

def _prepare_chart_data(df: pd.DataFrame, numeric_col: str) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    """
    Identifies a categorical column, aggregates (sums) numeric data by that category,
    and returns styled sub-dataframes for bar chart and pie chart.
    
    Returns:
        (bar_data, pie_data, category_column_name)
    """
    categorical_columns = df.select_dtypes(include=["object", "category", "str", "string"]).columns
    category_col = None
    
    # Try to find a suitable column for grouping
    for c in ["Product", "Category", "Region", "Month", "Date"]:
        if c in df.columns:
            category_col = c
            break
    if not category_col and len(categorical_columns) > 0:
        category_col = categorical_columns[0]
        
    if category_col:
        # Group and sum
        grouped = df.groupby(category_col)[numeric_col].sum().reset_index()
        # Sort descending
        grouped = grouped.sort_values(by=numeric_col, ascending=False)
        bar_data = grouped.head(10)
        pie_data = grouped.head(5)
        return bar_data, pie_data, category_col
    else:
        # Fallback to index if no categorical column is present
        df_copy = df.copy()
        df_copy["Index"] = df_copy.index.astype(str)
        bar_data = df_copy.head(10)
        pie_data = df_copy.head(5)
        return bar_data, pie_data, "Index"


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
        df = _load_csv(file_path)

        numeric_columns = df.select_dtypes(include=["number"]).columns

        if len(numeric_columns) == 0:
            return "❌ No numeric columns found."

        column = numeric_columns[0]

        bar_data, _, category_col = _prepare_chart_data(df, column)

        # Apply a clean modern style if available
        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot bars
        ax.bar(bar_data[category_col], bar_data[column], color=CHART_COLORS[:len(bar_data)], width=0.6)

        ax.set_title(f"Top 10 {column} by {category_col}", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel(category_col, fontsize=12, labelpad=10)
        ax.set_ylabel(column, fontsize=12, labelpad=10)
        plt.xticks(rotation=45, ha='right')
        ax.grid(True, linestyle="--", alpha=0.5)

        plt.tight_layout()
        chart_path = os.path.join(os.getcwd(), "bar_chart.png")
        plt.savefig(chart_path, format="png", dpi=150)
        plt.close()

        return f"""
✅ Bar chart generated successfully.

📈 Chart Column: {column}

![Bar Chart](/charts/bar_chart.png)
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
        df = _load_csv(file_path)

        numeric_columns = df.select_dtypes(include=["number"]).columns

        if len(numeric_columns) == 0:
            return "❌ No numeric columns found."

        column = numeric_columns[0]

        _, pie_data, category_col = _prepare_chart_data(df, column)

        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        fig, ax = plt.subplots(figsize=(8, 8))

        wedges, texts, autotexts = ax.pie(
            pie_data[column],
            labels=pie_data[category_col],
            autopct="%1.1f%%",
            colors=CHART_COLORS[:len(pie_data)],
            startangle=140,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5, "antialiased": True}
        )

        for text in texts:
            text.set_fontsize(11)
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_color("white")
            autotext.set_weight("bold")

        ax.set_title(f"Distribution of {column} by {category_col}", fontsize=14, fontweight="bold", pad=15)

        plt.tight_layout()
        chart_path = os.path.join(os.getcwd(), "pie_chart.png")
        plt.savefig(chart_path, format="png", dpi=150)
        plt.close()

        return f"""
✅ Pie chart generated successfully.

📈 Chart Column: {column}

![Pie Chart](/charts/pie_chart.png)
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
        df = _load_csv(file_path)

        numeric_columns = df.select_dtypes(include=["number"]).columns

        if len(numeric_columns) == 0:
            return "❌ No numeric columns found."

        column = numeric_columns[0]

        bar_data, pie_data, category_col = _prepare_chart_data(df, column)

        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # 1. Bar chart on ax1
        ax1.bar(bar_data[category_col], bar_data[column], color=CHART_COLORS[:len(bar_data)], width=0.6)
        ax1.set_title(f"Top 10 {column} by {category_col}", fontsize=13, fontweight="bold", pad=10)
        ax1.set_xlabel(category_col, fontsize=11)
        ax1.set_ylabel(column, fontsize=11)
        ax1.grid(True, linestyle="--", alpha=0.5)
        ax1.tick_params(axis='x', rotation=45)

        # 2. Pie chart on ax2
        wedges, texts, autotexts = ax2.pie(
            pie_data[column],
            labels=pie_data[category_col],
            autopct="%1.1f%%",
            colors=CHART_COLORS[:len(pie_data)],
            startangle=140,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5, "antialiased": True}
        )
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_color("white")
            autotext.set_weight("bold")
        ax2.set_title(f"Distribution of {column} by {category_col}", fontsize=13, fontweight="bold", pad=10)

        display_name = file_path if len(file_path) < 50 else "Raw CSV Data"
        plt.suptitle(f"CSV Analytics Infographic: {display_name}", fontsize=16, fontweight="bold", y=0.98)
        plt.tight_layout()
        chart_path = os.path.join(os.getcwd(), "infographic.png")
        plt.savefig(chart_path, format="png", dpi=150)
        plt.close()

        return f"""
✅ Infographic dashboard generated successfully.

📈 Analyzed Column: {column}

![Infographic](/charts/infographic.png)
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
        df = _load_csv(file_path)

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

CRITICAL RULE 1:
Whenever the user provides a prompt with a CSV file or asks to analyze an uploaded CSV file, you should automatically use the `generate_infographic` tool to create a visual infographic dashboard for them. However, if the user explicitly requests a specific visualization type (such as only a 'pie chart' or a 'bar chart'), you MUST use the corresponding dedicated tool (`generate_pie_chart` or `generate_bar_chart`) instead of the general infographic dashboard.

CRITICAL RULE 2:
If the user provides raw CSV content directly inside their text prompt/message instead of a file or file path, you MUST first save the raw CSV content to a file using the `save_csv_content` tool (you can name the file 'temp_data.csv' or another appropriate name). Once saved, use the resulting file path to run the infographic/analytics tools.

CRITICAL RULE 3 - ALWAYS SHOW CHARTS INLINE:
When a chart tool returns a response that contains a markdown image tag like ![...](data:image/png;base64,...), you MUST copy that EXACT full image markdown tag character-for-character into your reply to the user. Do NOT summarize it, describe it, omit it, or replace it with words like "chart has been generated". The image tag must appear in your reply exactly as returned by the tool so it renders inline in the chat. This is mandatory for every chart response.

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
        save_csv_content,
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