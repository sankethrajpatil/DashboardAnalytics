from __future__ import annotations

from pathlib import Path

from src.agent.workflow import compute_metrics_node, generate_charts_node, load_data_node


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_chart_titles_and_traces_are_generated() -> None:
	loaded = load_data_node({"config": {"project_root": str(PROJECT_ROOT)}})
	computed = compute_metrics_node(loaded)
	charted = generate_charts_node(computed)

	charts = charted["charts"]
	assert charts["sector_treemap"]["layout"]["title"]["text"] == "Sector-Wise Spend Treemap"
	assert charts["root_cause_variance"]["layout"]["title"]["text"] == "Root Cause Variance Bar Chart"
	assert charts["trend_and_seasonality"]["layout"]["title"]["text"] == "Trend & Seasonality Line Chart"
	assert charts["risk_heatmap"]["layout"]["title"]["text"] == "Risk Heatmap"
	assert charts["aging_risk_histogram"]["layout"]["title"]["text"] == "Aging Risk Histogram"
	assert charts["root_cause_variance"]["layout"]["barmode"] == "group"
	assert "yaxis2" in charts["trend_and_seasonality"]["layout"]


def test_root_cause_bar_contains_expected_categories() -> None:
	loaded = load_data_node({"config": {"project_root": str(PROJECT_ROOT)}})
	computed = compute_metrics_node(loaded)
	charted = generate_charts_node(computed)

	y_values = charted["charts"]["root_cause_variance"]["data"][0]["y"]
	assert set(y_values) == {"Overspend", "Price Variance", "Timing"}


def test_risk_heatmap_is_five_by_five() -> None:
	loaded = load_data_node({"config": {"project_root": str(PROJECT_ROOT)}})
	computed = compute_metrics_node(loaded)
	charted = generate_charts_node(computed)

	heatmap = charted["charts"]["risk_heatmap"]["data"][0]
	assert heatmap["z"]["shape"] == "5, 5"
