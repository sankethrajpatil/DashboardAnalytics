"""Reusable Reflex UI components."""

from __future__ import annotations

import reflex as rx

from src.state import DashboardState


DEEP_SPACE_NAVY = "#0B1221"
SOFT_GRAPHITE = "#1E2635"
SLATE_GREY = "#8A93A6"
FROST_WHITE = "#F5F7FA"
ELECTRIC_CYAN = "#3EE7E0"
AZURE_PULSE_BLUE = "#4C8DFF"
RISK_RED = "#FF5A5F"
SUCCESS_GREEN = "#4CD964"


def metric_card(title: str, value: str, accent_color: str, icon_symbol: str, trend_text: str) -> rx.Component:
	"""Render one executive summary metric tile."""
	is_positive_trend = trend_text.startswith("+")
	return rx.box(
		rx.hstack(
			rx.badge(
				icon_symbol,
				background="rgba(62, 231, 224, 0.16)",
				color=ELECTRIC_CYAN,
				border="1px solid rgba(62, 231, 224, 0.45)",
				border_radius="10px",
				padding="0.25rem 0.45rem",
			),
			rx.badge(
				trend_text,
				background=rx.cond(is_positive_trend, "rgba(76, 217, 100, 0.16)", "rgba(255, 90, 95, 0.16)"),
				color=rx.cond(is_positive_trend, SUCCESS_GREEN, RISK_RED),
				border=rx.cond(is_positive_trend, "1px solid rgba(76, 217, 100, 0.5)", "1px solid rgba(255, 90, 95, 0.5)"),
				border_radius="999px",
				padding="0.2rem 0.55rem",
			),
			justify="between",
			align="center",
			width="100%",
		),
		rx.text(
			title,
			font_size="12px",
			color=SLATE_GREY,
			text_transform="uppercase",
			letter_spacing="0.08em",
			font_family="Inter, SF Pro, Poppins, sans-serif",
		),
		rx.text(
			value,
			font_size="56px",
			line_height="1",
			font_weight="700",
			color=FROST_WHITE,
			font_family="Inter, SF Pro, Poppins, sans-serif",
		),
		rx.text(
			"vs prior range",
			font_size="13px",
			color=SLATE_GREY,
			font_family="Inter, SF Pro, Poppins, sans-serif",
		),
		padding="1.1rem 1.2rem",
		border_radius="12px",
		background=SOFT_GRAPHITE,
		border=f"1px solid {accent_color}",
		box_shadow="0 10px 28px rgba(62, 231, 224, 0.12)",
		transition="all 180ms ease",
		_hover={"transform": "translateY(-2px)", "box_shadow": "0 16px 32px rgba(76, 141, 255, 0.2)"},
		width="100%",
	)


def analytics_mode_tabs() -> rx.Component:
	"""Render top-level analytics mode tabs."""
	return rx.hstack(
		_mode_tab("Overview", "overview"),
		_mode_tab("Spend", "spend"),
		_mode_tab("Risk", "risk"),
		_mode_tab("Forecast", "forecast"),
		spacing="2",
		width="100%",
		flex_wrap="wrap",
	)


def dashboard_controls_panel() -> rx.Component:
	"""Render dashboard controls and action utilities in the analytics area."""
	return rx.vstack(
		rx.hstack(
			rx.hstack(
				rx.text(
					"Filters",
					font_size="14px",
					font_weight="700",
					color=FROST_WHITE,
					font_family="Inter, SF Pro, Poppins, sans-serif",
				),
				rx.button(
					rx.cond(DashboardState.show_filters, "Hide Filters", "Show Filters"),
					on_click=DashboardState.toggle_filters,
					background="rgba(62, 231, 224, 0.14)",
					border="1px solid #3EE7E0",
					color=ELECTRIC_CYAN,
					border_radius="999px",
					padding="0.35rem 0.75rem",
					font_size="12px",
					transition="all 220ms ease-in-out",
					_hover={"box_shadow": "0 0 18px rgba(62, 231, 224, 0.25)"},
				),
				rx.button(
					rx.cond(DashboardState.show_advanced_filters, "Advanced -", "Advanced +"),
					on_click=DashboardState.toggle_advanced_filters,
					background="rgba(76, 141, 255, 0.14)",
					border="1px solid #4C8DFF",
					color="#CFE0FF",
					border_radius="999px",
					padding="0.35rem 0.75rem",
					font_size="12px",
				),
				spacing="2",
				align="center",
			),
			time_range_selector(),
			justify="between",
			width="100%",
			align="center",
		),
		rx.box(width="100%", height="1px", background="#2A3650"),
		_filter_chip_row(),
		rx.cond(
			DashboardState.show_filters,
			rx.vstack(
				rx.hstack(
					_filter_control("Sector", DashboardState.sector_options, DashboardState.selected_sector, DashboardState.set_sector),
					_filter_control("PO Status", DashboardState.po_status_options, DashboardState.selected_po_status, DashboardState.set_po_status),
					time_range_selector(compact=True),
					spacing="2",
					width="100%",
					align="end",
				),
				rx.box(
					rx.hstack(
						_filter_control("Addressable", DashboardState.addressable_options, DashboardState.selected_addressable, DashboardState.set_addressable),
						_filter_control("Risk Status", DashboardState.risk_status_options, DashboardState.selected_risk_status, DashboardState.set_risk_status),
						spacing="2",
						width="100%",
					),
					max_height=rx.cond(DashboardState.show_advanced_filters, "180px", "0px"),
					overflow="hidden",
					opacity=rx.cond(DashboardState.show_advanced_filters, "1", "0"),
					transition="all 260ms ease-in-out",
					width="100%",
				),
				spacing="2",
				width="100%",
				align="stretch",
			),
			rx.box(),
		),
		rx.button(
			"Export PDF Summary",
			on_click=DashboardState.export_report,
			width="100%",
			background=AZURE_PULSE_BLUE,
			color=DEEP_SPACE_NAVY,
			font_family="Inter, SF Pro, Poppins, sans-serif",
			font_weight="700",
			border_radius="12px",
			transition="all 180ms ease",
			_hover={"box_shadow": "0 10px 22px rgba(76, 141, 255, 0.35)", "transform": "translateY(-1px)"},
		),
		rx.cond(
			DashboardState.last_action_message != "",
			rx.box(
				rx.text(DashboardState.last_action_message, color=SUCCESS_GREEN, size="3"),
				background="#11211A",
				padding="0.85rem",
				border_radius="12px",
				border=f"1px solid {SUCCESS_GREEN}",
				width="100%",
			),
			rx.box(),
		),
		width="100%",
		spacing="4",
		padding="1rem",
		border_radius="12px",
		background=SOFT_GRAPHITE,
		border="1px solid #253047",
		box_shadow="0 10px 24px rgba(0, 0, 0, 0.25)",
		align="stretch",
	)


def _filter_chip_row() -> rx.Component:
	return rx.hstack(
		rx.foreach(
			DashboardState.active_filter_chips,
			lambda chip: rx.badge(
				chip,
				background="rgba(62, 231, 224, 0.15)",
				color=ELECTRIC_CYAN,
				border="1px solid rgba(62, 231, 224, 0.4)",
				border_radius="999px",
				padding="0.25rem 0.6rem",
			),
		),
		spacing="2",
		flex_wrap="wrap",
		width="100%",
	)


def time_range_selector(compact: bool = False) -> rx.Component:
	"""Render futuristic pill selector for Today, Week, and Month views."""
	caption = rx.cond(compact, rx.box(), rx.text("Time Range", font_size="12px", weight="bold", color=SLATE_GREY))
	return rx.vstack(
		caption,
		rx.hstack(
			_time_range_pill("Today", "today"),
			_time_range_pill("This Week", "week"),
			_time_range_pill("This Month", "month"),
			spacing="1",
			padding="0.25rem",
			background="#111A2A",
			border="1px solid #2A3650",
			border_radius="999px",
			width="fit-content",
			flex_shrink="0",
		),
		spacing="1",
		align="start",
		flex_shrink="0",
	)


def predictive_insight_card() -> rx.Component:
	"""Render styled predictive insight card near spend trend charts."""
	return rx.box(
		rx.hstack(
			rx.badge(
				"AI",
				background="rgba(62, 231, 224, 0.18)",
				color=ELECTRIC_CYAN,
				border="1px solid rgba(62, 231, 224, 0.45)",
				border_radius="10px",
				padding="0.25rem 0.45rem",
			),
			rx.vstack(
				rx.text("Claude Variance Insight", weight="bold", color=FROST_WHITE, font_size="14px"),
				rx.text(
					DashboardState.variance_explanation,
					white_space="pre-wrap",
					color="#D6E3F7",
					size="3",
					font_family="Inter, SF Pro, Poppins, sans-serif",
				),
				spacing="1",
				align="stretch",
			),
			spacing="3",
			align="start",
			width="100%",
		),
		padding="1rem",
		border_radius="12px",
		background="#111A2A",
		border=f"1px solid {ELECTRIC_CYAN}",
		box_shadow="0 10px 24px rgba(62, 231, 224, 0.12)",
		transition="all 200ms ease-in-out",
		_hover={"transform": "translateY(-1px)", "box_shadow": "0 14px 28px rgba(62, 231, 224, 0.2)"},
		width="100%",
	)


def risk_owner_card(risk: dict) -> rx.Component:
	"""Render a single open-risk action card."""
	return rx.box(
		rx.hstack(
			rx.vstack(
				rx.text(
					f"Risk {risk['risk_id']}",
					weight="bold",
					color=FROST_WHITE,
					font_family="Inter, SF Pro, Poppins, sans-serif",
				),
				rx.text(
					risk["risk_description"],
					color=SLATE_GREY,
					size="3",
					font_family="Inter, SF Pro, Poppins, sans-serif",
				),
				rx.hstack(
					rx.badge(
						risk["risk_status"],
						background="#3A2B14",
						color="#FFC043",
						border_radius="999px",
					),
					rx.badge(
						f"{risk['days_open']} days open",
						background="#3B1F2A",
						color=RISK_RED,
						border_radius="999px",
					),
					spacing="2",
				),
				spacing="2",
				align="start",
				width="100%",
			),
			rx.button(
				risk["risk_owner"],
				on_click=DashboardState.email_risk_owner(risk["risk_id"]),
				background=ELECTRIC_CYAN,
				color=DEEP_SPACE_NAVY,
				border_radius="12px",
				font_weight="700",
				_hover={"box_shadow": "0 10px 20px rgba(62, 231, 224, 0.3)"},
				white_space="nowrap",
			),
			justify="between",
			align="start",
			width="100%",
		),
		padding="1rem",
		border_radius="12px",
		background="#111A2A",
		border="1px solid #27324A",
		box_shadow="0 8px 18px rgba(62, 231, 224, 0.08)",
		width="100%",
	)


def chart_card(
	chart_id: str,
	title: str,
	figure,
	* ,
	on_hover=None,
) -> rx.Component:
	"""Render a consistent chart card with Expand action."""
	chart_component = rx.cond(
		on_hover is None,
		rx.plotly(data=figure, width="100%", height="100%"),
		rx.plotly(data=figure, on_hover=on_hover, width="100%", height="100%"),
	)
	return rx.box(
		rx.vstack(
			rx.hstack(
				rx.text(
					title,
					font_size="14px",
					font_weight="600",
					color=FROST_WHITE,
					font_family="Inter, SF Pro, Poppins, sans-serif",
				),
				rx.button(
					"Expand",
					on_click=DashboardState.open_chart_modal(chart_id),
					background="rgba(76, 141, 255, 0.14)",
					color="#DCE9FF",
					border="1px solid #4C8DFF",
					border_radius="10px",
					padding="0.4rem 0.65rem",
					font_size="12px",
					font_weight="600",
					transition="all 200ms ease-in-out",
					_hover={"transform": "translateY(-1px)", "box_shadow": "0 10px 20px rgba(76, 141, 255, 0.28)"},
				),
				justify="between",
				align="center",
				width="100%",
			),
			rx.box(chart_component, width="100%", flex="1", min_height="0"),
			spacing="3",
			align="stretch",
			height="100%",
		),
		background=SOFT_GRAPHITE,
		border="1px solid #253047",
		border_radius="12px",
		padding="1rem",
		box_shadow="0 10px 24px rgba(76, 141, 255, 0.1)",
		height="430px",
		min_height="430px",
		overflow="hidden",
	)


def expanded_chart_modal() -> rx.Component:
	"""Render full-screen expanded chart overlay for detailed inspection."""
	return rx.cond(
		DashboardState.expanded_chart_id != "",
		rx.box(
			rx.box(
				rx.vstack(
					rx.hstack(
						rx.text(_expanded_chart_title(), font_size="18px", font_weight="700", color=FROST_WHITE),
						rx.button(
							"Close",
							on_click=DashboardState.close_chart_modal,
							background="rgba(255, 90, 95, 0.18)",
							color="#FFD9DA",
							border="1px solid #FF5A5F",
							border_radius="10px",
							padding="0.45rem 0.75rem",
						),
						justify="between",
						width="100%",
						align="center",
					),
					rx.text(_expanded_chart_description(), color=SLATE_GREY, font_size="13px"),
					rx.box(
						_expanded_chart_component(),
						height="68vh",
						width="100%",
					),
					rx.box(
						rx.text("Additional Insights", color=ELECTRIC_CYAN, font_weight="600", font_size="13px"),
						rx.text(_expanded_chart_insight(), color="#D7E4F7", font_size="13px"),
						background="#111A2A",
						border="1px solid #2A3650",
						border_radius="12px",
						padding="0.85rem",
						width="100%",
					),
					spacing="3",
					align="stretch",
				),
				background="#0B1221",
				border="1px solid #2A3650",
				border_radius="14px",
				padding="1rem",
				width="min(1200px, 92vw)",
				height="90vh",
				box_shadow="0 26px 60px rgba(0, 0, 0, 0.48)",
			),
			position="fixed",
			inset="0",
			display="flex",
			align_items="center",
			justify_content="center",
			background="rgba(6, 10, 18, 0.74)",
			z_index="60",
			transition="opacity 220ms ease-in-out",
		),
		rx.box(),
	)


def _expanded_chart_title() -> rx.Var:
	return rx.cond(
		DashboardState.expanded_chart_id == "sector_treemap",
		"Sector-Wise Spend Composition",
		rx.cond(
			DashboardState.expanded_chart_id == "root_cause_variance",
			"Root Cause Variance Breakdown",
			rx.cond(
				DashboardState.expanded_chart_id == "trend_and_seasonality",
				"Trend and Seasonality",
				rx.cond(
					DashboardState.expanded_chart_id == "risk_heatmap",
					"Risk Heatmap",
					"Aging Risk Histogram",
				),
			),
		),
	)


def _expanded_chart_description() -> rx.Var:
	return rx.cond(
		DashboardState.expanded_chart_id == "sector_treemap",
		"Shows sector-level spend concentration and share proportions with full legend visibility.",
		rx.cond(
			DashboardState.expanded_chart_id == "root_cause_variance",
			"Displays grouped variance drivers with complete axis context for root-cause interpretation.",
			rx.cond(
				DashboardState.expanded_chart_id == "trend_and_seasonality",
				"Shows monthly spend trend, cumulative variance, and predictive marker line in full scale.",
				rx.cond(
					DashboardState.expanded_chart_id == "risk_heatmap",
					"Displays full 5x5 severity matrix with non-overlapping legend and complete labels.",
					"Shows unresolved risk age distribution with full bins and axis labels.",
				),
			),
		),
	)


def _expanded_chart_insight() -> rx.Var:
	return rx.cond(
		DashboardState.expanded_chart_id == "root_cause_variance",
		DashboardState.variance_explanation,
		rx.cond(
			DashboardState.expanded_chart_id == "trend_and_seasonality",
			"Review the predictive marker trajectory to compare recent direction against monthly volatility.",
			"Use full-scale legend and labels here to validate category concentration and outliers before action.",
		),
	)


def _expanded_chart_component() -> rx.Component:
	return rx.cond(
		DashboardState.expanded_chart_id == "sector_treemap",
		rx.plotly(data=DashboardState.sector_treemap_figure, width="100%", height="100%"),
		rx.cond(
			DashboardState.expanded_chart_id == "root_cause_variance",
			rx.plotly(data=DashboardState.root_cause_variance_figure, width="100%", height="100%"),
			rx.cond(
				DashboardState.expanded_chart_id == "trend_and_seasonality",
				rx.plotly(data=DashboardState.trend_and_seasonality_figure, width="100%", height="100%"),
				rx.cond(
					DashboardState.expanded_chart_id == "risk_heatmap",
					rx.plotly(data=DashboardState.risk_heatmap_figure, width="100%", height="100%"),
					rx.plotly(data=DashboardState.aging_risk_histogram_figure, width="100%", height="100%"),
				),
			),
		),
	)


def _filter_control(label: str, options, value, on_change) -> rx.Component:
	return rx.vstack(
		rx.text(
			label,
			font_size="12px",
			weight="bold",
			color=SLATE_GREY,
			font_family="Inter, SF Pro, Poppins, sans-serif",
		),
		rx.select(
			options,
			value=value,
			on_change=on_change,
			width="100%",
			border_radius="12px",
			background="#111A2A",
			border="1px solid #2A3650",
			color=FROST_WHITE,
			height="34px",
		),
		spacing="1",
		align="stretch",
		width="100%",
	)


def _mode_tab(label: str, mode: str) -> rx.Component:
	is_active = DashboardState.active_mode == mode
	return rx.button(
		label,
		on_click=DashboardState.set_active_mode(mode),
		padding="0.45rem 0.85rem",
		border_radius="999px",
		font_size="12px",
		font_weight="600",
		font_family="Inter, SF Pro, Poppins, sans-serif",
		background=rx.cond(is_active, "rgba(62, 231, 224, 0.18)", "rgba(138, 147, 166, 0.14)"),
		color=rx.cond(is_active, ELECTRIC_CYAN, FROST_WHITE),
		border=rx.cond(is_active, f"1px solid {ELECTRIC_CYAN}", "1px solid #2A354A"),
		transition="all 180ms ease",
		_hover={"transform": "translateY(-1px)", "border_color": ELECTRIC_CYAN},
	)


def _time_range_pill(label: str, value: str) -> rx.Component:
	is_active = DashboardState.selected_time_range == value
	return rx.button(
		label,
		on_click=DashboardState.set_time_range(value),
		padding="0.4rem 0.8rem",
		border_radius="999px",
		font_size="12px",
		font_weight="600",
		white_space="nowrap",
		font_family="Inter, SF Pro, Poppins, sans-serif",
		background=rx.cond(is_active, "rgba(62, 231, 224, 0.2)", "transparent"),
		color=rx.cond(is_active, ELECTRIC_CYAN, FROST_WHITE),
		border=rx.cond(is_active, "1px solid #3EE7E0", "1px solid transparent"),
		transition="all 220ms ease-in-out",
		_hover={
			"border_color": "#3EE7E0",
			"box_shadow": "0 0 18px rgba(62, 231, 224, 0.24)",
		},
	)
