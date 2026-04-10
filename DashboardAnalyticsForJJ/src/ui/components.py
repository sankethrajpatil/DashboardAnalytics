"""Reusable Reflex UI components — enterprise analytics dashboard.

Design system following Material/Carbon/Fluent BI UX patterns:
- 4/8/12/16/24 px spacing scale
- Consistent typography hierarchy: label → title → value
- 12-column responsive grid via CSS grid
- Compact, high-density information layout
"""

from __future__ import annotations

import reflex as rx

from src.state import DashboardState

# ═══════════════════════════════════════════════════════════════
# Design Tokens
# ═══════════════════════════════════════════════════════════════

# Palette
BG = "#0B1221"
BG_CARD = "#1E2635"
BG_INPUT = "#111A2A"
T1 = "#F5F7FA"          # primary text
T2 = "#D7E4F7"          # secondary text
T3 = "#8A93A6"          # muted / labels
T4 = "#6B7D99"          # hint
CYAN = "#3EE7E0"
BLUE = "#4C8DFF"
PURPLE = "#A66BFF"
GREEN = "#4CD964"
RED = "#FF5A5F"
AMBER = "#FFC043"
BORDER = "#253047"
BORDER_SUBTLE = "#1E2A3E"

# Typography
FONT = "Inter, SF Pro, Poppins, sans-serif"

# Spacing scale (px): 4 8 12 16 24 32
SP4 = "4px"
SP8 = "8px"
SP12 = "12px"
SP16 = "16px"
SP24 = "24px"

# Radii
R_SM = "6px"
R_MD = "10px"
R_LG = "14px"
R_PILL = "999px"

# Transitions
EASE = "all 180ms cubic-bezier(.4,0,.2,1)"


# ═══════════════════════════════════════════════════════════════
# 1. Filter Bar — unified strip with clear hierarchy
# ═══════════════════════════════════════════════════════════════


def dashboard_controls_panel() -> rx.Component:
    """Unified filter bar: date pills | dropdowns | toggle/export actions."""
    return rx.vstack(
        # ── primary row ──
        rx.hstack(
            _time_range_pills(),
            _filter_select("Sector", DashboardState.sector_options,
                           DashboardState.selected_sector, DashboardState.set_sector),
            _filter_select("PO Status", DashboardState.po_status_options,
                           DashboardState.selected_po_status, DashboardState.set_po_status),
            rx.spacer(),
            # advanced toggle — subtle icon+label button
            rx.el.button(
                rx.hstack(
                    rx.icon("sliders-horizontal", size=13),
                    rx.cond(DashboardState.show_advanced_filters, "Less", "More"),
                    spacing="1", align="center",
                ),
                on_click=DashboardState.toggle_advanced_filters,
                title="Advanced filters",
                background="transparent",
                color=T3,
                border="none",
                font_size="12px",
                font_family=FONT,
                cursor="pointer",
                padding="4px 8px",
                border_radius=R_SM,
                transition=EASE,
                _hover={"color": CYAN, "background": "rgba(62,231,224,0.06)"},
            ),
            # hide/show toggle — icon+label
            rx.el.button(
                rx.hstack(
                    rx.icon(
                        rx.cond(DashboardState.show_filters, "eye-off", "eye"),
                        size=13,
                    ),
                    rx.cond(DashboardState.show_filters, "Hide", "Filters"),
                    spacing="1", align="center",
                ),
                on_click=DashboardState.toggle_filters,
                title="Toggle filter visibility",
                background="transparent",
                color=T3,
                border="none",
                font_size="12px",
                font_family=FONT,
                cursor="pointer",
                padding="4px 8px",
                border_radius=R_SM,
                transition=EASE,
                _hover={"color": CYAN, "background": "rgba(62,231,224,0.06)"},
            ),
            # export — ghost button with icon
            rx.el.button(
                rx.hstack(
                    rx.icon("download", size=13),
                    "Export",
                    spacing="1", align="center",
                ),
                on_click=DashboardState.export_report,
                title="Export PDF summary",
                background="transparent",
                color=T3,
                border=f"1px solid {BORDER}",
                font_size="12px",
                font_weight="500",
                font_family=FONT,
                cursor="pointer",
                padding="4px 10px",
                border_radius=R_SM,
                transition=EASE,
                _hover={"color": BLUE, "border_color": BLUE,
                        "background": "rgba(76,141,255,0.06)"},
            ),
            spacing="3",
            align="center",
            width="100%",
            flex_wrap="wrap",
        ),
        # ── advanced row (animated slide) ──
        rx.box(
            rx.hstack(
                _filter_select("Addressable", DashboardState.addressable_options,
                               DashboardState.selected_addressable, DashboardState.set_addressable),
                _filter_select("Risk Status", DashboardState.risk_status_options,
                               DashboardState.selected_risk_status, DashboardState.set_risk_status),
                spacing="3",
                width="100%",
            ),
            max_height=rx.cond(
                DashboardState.show_filters & DashboardState.show_advanced_filters,
                "60px", "0px",
            ),
            opacity=rx.cond(
                DashboardState.show_filters & DashboardState.show_advanced_filters,
                "1", "0",
            ),
            overflow="hidden",
            transition="all 250ms ease-in-out",
            width="100%",
        ),
        # ── active chip summary ──
        _filter_chip_row(),
        # ── status toast ──
        rx.cond(
            DashboardState.last_action_message != "",
            rx.hstack(
                rx.icon("circle-check", size=14, color=GREEN),
                rx.text(DashboardState.last_action_message, color=GREEN, size="2"),
                spacing="2", align="center",
                background="rgba(76,217,100,0.08)",
                padding="4px 10px",
                border_radius=R_MD,
                border=f"1px solid rgba(76,217,100,0.25)",
                width="100%",
            ),
            rx.box(),
        ),
        # outer container
        width="100%",
        spacing="2",
        padding="8px 12px",
        border_radius=R_LG,
        background=BG_CARD,
        border=f"1px solid {BORDER}",
    )


def _time_range_pills() -> rx.Component:
    """Single unified date range selector — no duplicates."""
    return rx.hstack(
        _tr_pill("Today", "today"),
        _tr_pill("Week", "week"),
        _tr_pill("Month", "month"),
        spacing="1",
        padding="3px",
        background=BG_INPUT,
        border=f"1px solid {BORDER}",
        border_radius=R_PILL,
        flex_shrink="0",
    )


def _tr_pill(label: str, value: str) -> rx.Component:
    active = DashboardState.selected_time_range == value
    return rx.el.button(
        label,
        on_click=DashboardState.set_time_range(value),
        background=rx.cond(active, "rgba(62,231,224,0.18)", "transparent"),
        color=rx.cond(active, CYAN, T3),
        border=rx.cond(active, f"1px solid {CYAN}", "1px solid transparent"),
        border_radius=R_PILL,
        padding="3px 10px",
        font_size="11px",
        font_weight="600",
        font_family=FONT,
        cursor="pointer",
        white_space="nowrap",
        transition=EASE,
        _hover={"color": CYAN},
    )


def _filter_select(label: str, options, value, on_change) -> rx.Component:
    """Compact labelled dropdown — right-sized for its container."""
    return rx.hstack(
        rx.text(label, font_size="11px", color=T3, font_family=FONT,
                white_space="nowrap", flex_shrink="0"),
        rx.select(
            options,
            value=value,
            on_change=on_change,
            size="1",
            radius="medium",
        ),
        spacing="2",
        align="center",
        flex_shrink="0",
    )


def _filter_chip_row() -> rx.Component:
    return rx.cond(
        DashboardState.show_filters,
        rx.hstack(
            rx.foreach(
                DashboardState.active_filter_chips,
                lambda chip: rx.el.span(
                    chip,
                    style={
                        "background": "rgba(62,231,224,0.10)",
                        "color": CYAN,
                        "border": f"1px solid rgba(62,231,224,0.30)",
                        "border-radius": R_PILL,
                        "padding": "2px 8px",
                        "font-size": "11px",
                        "font-family": FONT,
                        "white-space": "nowrap",
                    },
                ),
            ),
            spacing="2",
            flex_wrap="wrap",
            width="100%",
        ),
        rx.box(),
    )


# keep legacy name for imports that use it
def time_range_selector(compact: bool = False) -> rx.Component:
    """Backward-compat wrapper."""
    return _time_range_pills()


# ═══════════════════════════════════════════════════════════════
# 2. KPI Band — compact horizontal row, all KPIs visible at once
# ═══════════════════════════════════════════════════════════════


def metric_card(
    title: str, value: str, accent_color: str,
    icon_symbol: str, trend_text: str,
) -> rx.Component:
    """Compact KPI tile: accent bar | label + value + trend badge."""
    is_positive = trend_text.startswith("+")
    trend_color = rx.cond(is_positive, GREEN, RED)
    trend_bg = rx.cond(is_positive,
                       "rgba(76,217,100,0.12)", "rgba(255,90,95,0.12)")
    return rx.box(
        rx.hstack(
            # accent bar
            rx.box(
                width="3px",
                height="100%",
                border_radius="2px",
                background=accent_color,
                flex_shrink="0",
            ),
            rx.vstack(
                # title + trend
                rx.hstack(
                    rx.text(
                        title, font_size="11px", color=T3,
                        text_transform="uppercase", letter_spacing="0.06em",
                        font_family=FONT, white_space="nowrap",
                    ),
                    rx.el.span(
                        trend_text,
                        style={
                            "font-size": "10px",
                            "font-weight": "600",
                            "font-family": FONT,
                            "padding": "1px 6px",
                            "border-radius": R_PILL,
                            "white-space": "nowrap",
                        },
                        color=trend_color,
                        background=trend_bg,
                    ),
                    spacing="2",
                    align="center",
                ),
                # value
                rx.text(
                    value,
                    font_size="26px",
                    line_height="1.1",
                    font_weight="700",
                    color=T1,
                    font_family=FONT,
                ),
                spacing="1",
                align="start",
                justify="center",
                flex="1",
            ),
            spacing="3",
            align="stretch",
            height="100%",
        ),
        padding="8px 12px",
        border_radius=R_MD,
        background=BG_CARD,
        border=f"1px solid {BORDER}",
        transition=EASE,
        _hover={
            "border_color": accent_color,
            "box_shadow": f"0 4px 16px rgba(62,231,224,0.10)",
        },
        height="72px",
        min_width="0",
        flex="1",
    )


# ═══════════════════════════════════════════════════════════════
# 3. Chart Card — reusable template: header | body | no Plotly title
# ═══════════════════════════════════════════════════════════════


def chart_card(
    chart_id: str,
    title: str,
    figure,
    *,
    on_hover=None,
) -> rx.Component:
    """Chart card: header (title left, expand right) | chart body.

    Plotly titles are intentionally removed — the card header is the
    single source of truth for the chart name, preventing overlap with
    legends or annotations.
    """
    chart_el = rx.cond(
        on_hover is None,
        rx.plotly(data=figure, width="100%", height="100%"),
        rx.plotly(data=figure, on_hover=on_hover, width="100%", height="100%"),
    )
    return rx.box(
        rx.vstack(
            # ── header ──
            rx.hstack(
                rx.text(
                    title, font_size="13px", font_weight="600",
                    color=T1, font_family=FONT, white_space="nowrap",
                    overflow="hidden", text_overflow="ellipsis",
                ),
                rx.spacer(),
                rx.el.button(
                    rx.icon("maximize-2", size=14),
                    on_click=DashboardState.open_chart_modal(chart_id),
                    title="Expand chart",
                    background="transparent",
                    color=T4,
                    border="none",
                    border_radius=R_SM,
                    padding="4px",
                    cursor="pointer",
                    display="inline-flex",
                    align_items="center",
                    justify_content="center",
                    transition=EASE,
                    _hover={"color": CYAN, "background": "rgba(62,231,224,0.08)"},
                ),
                align="center",
                width="100%",
                padding_bottom=SP8,
                border_bottom=f"1px solid {BORDER_SUBTLE}",
            ),
            # ── chart body ──
            rx.box(chart_el, width="100%", flex="1", min_height="0"),
            spacing="2",
            align="stretch",
            height="100%",
        ),
        background=BG_CARD,
        border=f"1px solid {BORDER}",
        border_radius=R_LG,
        padding="12px",
        transition=EASE,
        _hover={"border_color": "rgba(62,231,224,0.20)"},
        height="380px",
        min_height="380px",
        overflow="hidden",
    )


# ═══════════════════════════════════════════════════════════════
# 4. Risk Action List — compact table rows, scrollable
# ═══════════════════════════════════════════════════════════════

_RISK_SCROLL = {
    "&::-webkit-scrollbar": {"width": "4px"},
    "&::-webkit-scrollbar-track": {"background": "transparent"},
    "&::-webkit-scrollbar-thumb": {"background": "rgba(62,231,224,0.20)", "border_radius": "8px"},
    "scrollbar-width": "thin",
    "scrollbar-color": "rgba(62,231,224,0.20) transparent",
}


def risk_action_list() -> rx.Component:
    """Scrollable risk action table with fixed header and column labels."""
    return rx.vstack(
        # header
        rx.hstack(
            rx.hstack(
                rx.icon("shield-alert", size=15, color=CYAN),
                rx.text(
                    "Risk Owner Actions", font_size="13px",
                    font_weight="600", color=T1, font_family=FONT,
                ),
                spacing="2", align="center",
            ),
            rx.spacer(),
            rx.el.span(
                DashboardState.open_risks.length().to(str),
                style={
                    "font-size": "11px", "font-weight": "600",
                    "color": CYAN, "background": "rgba(62,231,224,0.10)",
                    "padding": "2px 8px", "border-radius": R_PILL,
                    "font-family": FONT,
                },
            ),
            align="center",
            width="100%",
            padding_bottom=SP8,
        ),
        # column labels
        rx.hstack(
            rx.text("Risk", font_size="10px", color=T4, width="28%",
                    text_transform="uppercase", letter_spacing="0.06em", font_family=FONT),
            rx.text("Owner", font_size="10px", color=T4, width="20%",
                    text_transform="uppercase", letter_spacing="0.06em", font_family=FONT),
            rx.text("Status", font_size="10px", color=T4, width="18%",
                    text_transform="uppercase", letter_spacing="0.06em", font_family=FONT),
            rx.text("Age", font_size="10px", color=T4, width="14%",
                    text_transform="uppercase", letter_spacing="0.06em", font_family=FONT),
            rx.text("Action", font_size="10px", color=T4, width="20%",
                    text_transform="uppercase", letter_spacing="0.06em", font_family=FONT,
                    text_align="right"),
            width="100%",
            padding="0 4px",
        ),
        rx.box(width="100%", height="1px", background=BORDER_SUBTLE),
        # scrollable rows
        rx.box(
            rx.foreach(DashboardState.open_risks, _risk_row),
            width="100%",
            display="flex",
            flex_direction="column",
            gap=SP4,
            overflow_y="auto",
            max_height="320px",
            padding_right="2px",
            **_RISK_SCROLL,
        ),
        # container
        width="100%",
        spacing="1",
        padding="12px",
        border_radius=R_LG,
        background=BG_CARD,
        border=f"1px solid {BORDER}",
    )


def _risk_row(risk: dict) -> rx.Component:
    """Single compact risk row: id+desc | owner | status badge | age | action btn."""
    return rx.hstack(
        # risk id + truncated description
        rx.vstack(
            rx.text(
                risk["risk_id"], font_size="12px", font_weight="600",
                color=T1, font_family=FONT, white_space="nowrap",
            ),
            rx.text(
                risk["risk_description"], font_size="11px", color=T3,
                font_family=FONT, white_space="nowrap",
                overflow="hidden", text_overflow="ellipsis",
                max_width="100%",
            ),
            spacing="0",
            width="28%",
            min_width="0",
        ),
        # owner
        rx.text(
            risk["risk_owner"], font_size="12px", color=T2,
            font_family=FONT, width="20%", white_space="nowrap",
            overflow="hidden", text_overflow="ellipsis",
        ),
        # status badge
        rx.el.span(
            risk["risk_status"],
            style={
                "font-size": "10px",
                "font-weight": "600",
                "padding": "2px 8px",
                "border-radius": R_PILL,
                "white-space": "nowrap",
                "font-family": FONT,
            },
            color=_status_color(risk["risk_status"]),
            background=_status_bg(risk["risk_status"]),
            width="18%",
        ),
        # days open
        rx.hstack(
            rx.text(
                risk["days_open"], font_size="12px",
                color=_age_color(risk["days_open"]),
                font_weight="600", font_family=FONT,
            ),
            rx.text("d", font_size="10px", color=T4, font_family=FONT),
            spacing="0",
            align="baseline",
            width="14%",
        ),
        # action button
        rx.box(
            rx.el.button(
                "Review",
                on_click=DashboardState.email_risk_owner(risk["risk_id"]),
                background="transparent",
                color=CYAN,
                border=f"1px solid rgba(62,231,224,0.25)",
                border_radius=R_SM,
                padding="3px 10px",
                font_size="11px",
                font_weight="600",
                font_family=FONT,
                cursor="pointer",
                transition=EASE,
                _hover={
                    "background": "rgba(62,231,224,0.08)",
                    "border_color": CYAN,
                },
            ),
            width="20%",
            text_align="right",
        ),
        align="center",
        width="100%",
        padding="6px 4px",
        border_radius=R_SM,
        transition=EASE,
        _hover={"background": "rgba(62,231,224,0.03)"},
    )


def _status_color(status) -> rx.Var:
    return rx.cond(
        status == "Critical", RED,
        rx.cond(status == "High", AMBER,
                rx.cond(status == "Open", BLUE, T3)))


def _status_bg(status) -> rx.Var:
    return rx.cond(
        status == "Critical", "rgba(255,90,95,0.12)",
        rx.cond(status == "High", "rgba(255,192,67,0.12)",
                rx.cond(status == "Open", "rgba(76,141,255,0.12)",
                        "rgba(138,147,166,0.08)")))


def _age_color(days) -> rx.Var:
    return rx.cond(
        days.to(int) > 60, RED,
        rx.cond(days.to(int) > 30, AMBER, T2))


# ═══════════════════════════════════════════════════════════════
# 5. Predictive Insight Card
# ═══════════════════════════════════════════════════════════════


def predictive_insight_card() -> rx.Component:
    """AI insight card — compact inline."""
    return rx.hstack(
        rx.el.span(
            "AI",
            style={
                "font-size": "10px", "font-weight": "700",
                "color": CYAN, "background": "rgba(62,231,224,0.14)",
                "border": f"1px solid rgba(62,231,224,0.35)",
                "border-radius": R_SM, "padding": "2px 6px",
                "font-family": FONT,
            },
        ),
        rx.vstack(
            rx.text("Claude Variance Insight", font_size="12px",
                    font_weight="600", color=T1, font_family=FONT),
            rx.text(
                DashboardState.variance_explanation,
                white_space="pre-wrap", color=T2, size="2",
                font_family=FONT, line_height="1.5",
            ),
            spacing="1", align="stretch", flex="1", min_width="0",
        ),
        spacing="3",
        align="start",
        padding="8px 12px",
        border_radius=R_MD,
        background=BG_INPUT,
        border=f"1px solid rgba(62,231,224,0.18)",
        width="100%",
    )


# ═══════════════════════════════════════════════════════════════
# 6. Mode Tabs
# ═══════════════════════════════════════════════════════════════


def analytics_mode_tabs() -> rx.Component:
    return rx.hstack(
        _mode_tab("Overview", "overview"),
        _mode_tab("Spend", "spend"),
        _mode_tab("Risk", "risk"),
        _mode_tab("Forecast", "forecast"),
        spacing="1",
        width="100%",
    )


def _mode_tab(label: str, mode: str) -> rx.Component:
    active = DashboardState.active_mode == mode
    return rx.el.button(
        label,
        on_click=DashboardState.set_active_mode(mode),
        background=rx.cond(active, "rgba(62,231,224,0.14)", "transparent"),
        color=rx.cond(active, CYAN, T3),
        border=rx.cond(active, f"1px solid {CYAN}", "1px solid transparent"),
        border_radius=R_PILL,
        padding="4px 12px",
        font_size="12px",
        font_weight="600",
        font_family=FONT,
        cursor="pointer",
        transition=EASE,
        _hover={"color": CYAN, "border_color": "rgba(62,231,224,0.30)"},
    )


# ═══════════════════════════════════════════════════════════════
# 7. Expanded Chart Modal
# ═══════════════════════════════════════════════════════════════


def expanded_chart_modal() -> rx.Component:
    """Full-screen chart overlay for detailed inspection."""
    return rx.cond(
        DashboardState.expanded_chart_id != "",
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            _expanded_chart_title(),
                            font_size="16px", font_weight="700",
                            color=T1, font_family=FONT,
                        ),
                        rx.spacer(),
                        rx.el.button(
                            rx.icon("x", size=16),
                            on_click=DashboardState.close_chart_modal,
                            title="Close",
                            background="transparent",
                            color=T3,
                            border="none",
                            cursor="pointer",
                            border_radius=R_SM,
                            padding="4px",
                            transition=EASE,
                            _hover={"color": RED},
                        ),
                        align="center",
                        width="100%",
                    ),
                    rx.text(
                        _expanded_chart_description(),
                        color=T3, font_size="12px", font_family=FONT,
                    ),
                    rx.box(
                        _expanded_chart_component(),
                        height="64vh",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.el.span(
                            "AI",
                            style={
                                "font-size": "10px", "font-weight": "700",
                                "color": CYAN, "background": "rgba(62,231,224,0.14)",
                                "border": f"1px solid rgba(62,231,224,0.35)",
                                "border-radius": R_SM, "padding": "2px 6px",
                                "font-family": FONT,
                            },
                        ),
                        rx.text(
                            _expanded_chart_insight(),
                            color=T2, font_size="12px", font_family=FONT,
                        ),
                        spacing="2",
                        align="start",
                        background=BG_INPUT,
                        border=f"1px solid {BORDER}",
                        border_radius=R_MD,
                        padding="8px 12px",
                        width="100%",
                    ),
                    spacing="3",
                    align="stretch",
                ),
                background=BG,
                border=f"1px solid {BORDER}",
                border_radius=R_LG,
                padding="16px",
                width="min(1200px, 92vw)",
                height="90vh",
                box_shadow="0 24px 64px rgba(0,0,0,0.55)",
            ),
            position="fixed",
            inset="0",
            display="flex",
            align_items="center",
            justify_content="center",
            background="rgba(6,10,18,0.78)",
            z_index="60",
        ),
        rx.box(),
    )


# ── modal helpers ──

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
        "Sector-level spend concentration and share proportions.",
        rx.cond(
            DashboardState.expanded_chart_id == "root_cause_variance",
            "Grouped variance drivers with axis context for root-cause interpretation.",
            rx.cond(
                DashboardState.expanded_chart_id == "trend_and_seasonality",
                "Monthly spend trend, cumulative variance, and predictive markers.",
                rx.cond(
                    DashboardState.expanded_chart_id == "risk_heatmap",
                    "5\u00d75 severity matrix with non-overlapping labels.",
                    "Unresolved risk age distribution with full bins.",
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
            "Review the predictive marker trajectory against monthly volatility.",
            "Use full-scale labels to validate concentration and outliers.",
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


# ═══════════════════════════════════════════════════════════════
# Legacy aliases (backward compat for any other imports)
# ═══════════════════════════════════════════════════════════════

# risk_owner_card — keep for tests or other callers
def risk_owner_card(risk: dict) -> rx.Component:
    """Legacy single risk card — wraps the compact row."""
    return _risk_row(risk)
