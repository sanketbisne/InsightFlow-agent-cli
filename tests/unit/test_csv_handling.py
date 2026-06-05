# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pandas as pd
from app.agent import (
    _load_csv,
    save_csv_content,
    generate_bar_chart,
    generate_pie_chart,
    generate_infographic,
    generate_insights,
)

RAW_CSV_DATA = """Date,Region,Category,Product,Revenue,Units,Profit,Rating
2025-01-02,North America,Laptop,MacBook Pro,24000,12,6000,4.8
2025-01-05,Europe,Mobile,iPhone 15,35000,35,14000,4.7
2025-01-08,Asia,Tablet,iPad Air,16800,28,5040,4.5
"""


def test_load_csv_from_content() -> None:
    """Test loading a dataframe directly from raw string content."""
    df = _load_csv(RAW_CSV_DATA)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 3
    assert list(df.columns) == [
        "Date",
        "Region",
        "Category",
        "Product",
        "Revenue",
        "Units",
        "Profit",
        "Rating",
    ]


def test_save_csv_content() -> None:
    """Test saving CSV content to a file in the workspace using the tool."""
    filename = "test_temp_data_save.csv"
    try:
        res = save_csv_content(RAW_CSV_DATA, filename)
        assert "Successfully saved" in res
        assert os.path.exists(filename)

        # Verify content
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        assert "Date,Region,Category" in content

        # Test loading from the saved file path
        df = _load_csv(filename)
        assert df.shape[0] == 3
    finally:
        if os.path.exists(filename):
            os.remove(filename)


def test_visualization_tools_with_raw_content() -> None:
    """Test that all analytics and visualization tools execute successfully on raw content."""
    try:
        bar_chart_res = generate_bar_chart(RAW_CSV_DATA)
        assert "Bar chart generated successfully" in bar_chart_res
        assert "![Bar Chart](bar_chart.png)" in bar_chart_res

        pie_chart_res = generate_pie_chart(RAW_CSV_DATA)
        assert "Pie chart generated successfully" in pie_chart_res
        assert "![Pie Chart](pie_chart.png)" in pie_chart_res

        infographic_res = generate_infographic(RAW_CSV_DATA)
        assert "Infographic dashboard generated successfully" in infographic_res
        assert "![Infographic](infographic.png)" in infographic_res

        insights_res = generate_insights(RAW_CSV_DATA)
        assert "AI Insights Report" in insights_res
        assert "Total Rows: 3" in insights_res
    finally:
        for filename in ["bar_chart.png", "pie_chart.png", "infographic.png"]:
            if os.path.exists(filename):
                os.remove(filename)
