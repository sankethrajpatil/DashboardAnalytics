# DashboardAnalyticsForJJ

DashboardAnalyticsForJJ is a Claude-powered Spend, Variance, and Risk Analytics Dashboard built with Reflex for the interface, LangGraph for orchestration, and Anthropic-powered reasoning for explanations and agentic actions.

## Analytics Scope
- Combine spend and risk data into a single analytical workspace.
- Present executive metrics for purchase order activity, variance performance, and active risk exposure.
- Surface charts that explain concentration, trend, root cause, and unresolved aging.
- Support direct follow-up actions from the dashboard without leaving the analysis flow.

## Data Inputs
- Enterprise_Spend_Jan_2026.xlsx provides purchase order, spend, and variance data.
- RiskRegisterSample.xlsx provides risk identifier, owner, status, severity, and aging data.
- The risk heatmap uses deterministic proxy axes derived from the workbook because there are no native Likelihood and Impact columns.

## Executive Summary Metrics
- Total PO Volume: count of unique purchase orders in the active filter context.
- Average Variance: average variance from the spend detail dataset in the active filter context.
- Active Risk Count: count of risks that are still open or not closed.
- Addressable Spend %: addressable spend divided by total spend in the active filter context.

## Time Range Modes
- Support three dashboard time ranges: Today, This Week, This Month.
- Time range must drive all summary metrics and chart datasets.
- Time range selector should use compact futuristic pill controls with neon accent states.
- Selected time range should remain stable while users navigate dashboard sections.

## Dashboard Views
- Executive Summary for leadership-level metrics.
- Spend and Variance for sector concentration, variance attribution, and time-series analysis.
- Risk Analysis for severity concentration and aging distribution.
- Agent Actions for variance explanation, risk-owner email launch, and filtered report export.

## Chart Contracts
- Sector Treemap: area uses PO_Total_Amount, color uses PO_Status, grouped by Sector.
- Root Cause Variance Chart: grouped horizontal bar with X as summed Variance_vs_Budget and Y as Root_Cause.
- Trend and Seasonality Chart: dual-axis visualization with Monthly Spend on the primary axis and Cumulative Variance on the secondary axis, rendered as line and area.
- Risk Heatmap: 5x5 matrix using derived Likelihood versus derived Impact with risk-count intensity.
- Aging Risk Histogram: distribution of Days_Open with emphasis on long-tail unresolved risks.

## Chart Card and Layout Contract
- Render charts inside clean minimal cards with title and chart content only.
- Keep axis labels readable, aligned, and fully visible.
- Keep legends compact and non-overlapping.
- Use palette accents from Electric Cyan, Azure Pulse Blue, and Purple gradient.
- Use subtle thin grid lines and neon hover emphasis for data points.
- Apply rounded corners and consistent chart-card spacing and padding.
- Arrange charts in a responsive two-column or three-column grid.
- Keep chart card heights consistent and prevent overflow or clipping.
- Add an Expand or View Large button on every chart card.
- Expanded chart mode must include full legends, full axis labels, full description, and additional insights.

## Interaction Model
- Sidebar: Claude chat, action triggers, and guided explanations.
- Main area: filters, summary cards, charts, and supporting tables.
- User actions must pass through structured workflows so chart updates, explanations, and exports remain consistent with the visible state.

## Title and Filter Contract
- Title must be Dashboard Analytics — Spend | Risk | Forecast.
- Subtitle must reflect selected date range mode.
- Title block must be visually separated from filter and chart regions.
- Use futuristic title styling with Inter or SF Pro and strong weight.
- Include Electric Cyan accent bar under or beside the title.
- Filters must be compact by default with expandable Advanced Filters.
- Filters must support Show or Hide behavior for uncluttered views.
- Active filter chips must remain visible and styled as rounded neon-accent pills.

## Chat Panel Interaction Contract
- The Claude chat panel must be collapsible with smooth animation.
- The panel must support dock left, dock right, and floating draggable modes.
- The message input area must remain visible at all times and never be clipped.
- Primary chat buttons must be larger and neon-accented for stronger affordance.
- Chat bubbles must use improved spacing, padding, and rounded styling.
- Panel location preference and collapsed state must persist across reloads.
- Saved responses must remain available regardless of panel mode.

## Collapsible Navigation Contract
- The left navigation for Overview, Spend, Risk, and Forecast must support collapse and expand behavior.
- Include a clear toggle affordance such as a chevron icon, animated arrow, or hamburger control.
- Apply smooth width transitions in the 200 to 300ms ease-in-out range.
- Persist collapsed or expanded preference so users keep their preferred mode.
- In collapsed mode, show icon-only entries with hover tooltips.
- Preserve responsive behavior on small screens while keeping main dashboard content readable.
- Keep styling aligned with Deep Space Navy #0B1221 base and Electric Cyan #3EE7E0 accents.

## Implementation Principles
- Keep UI, analytics logic, workflow orchestration, and side-effect tools in separate modules.
- Use pandas for Excel ingestion and data normalization.
- Use Plotly for visual specifications rendered through Reflex.
- Use deterministic LangGraph nodes with explicit input and output contracts.
- Validate source data before exposing metrics, charts, or actions.
- Translate workflow outputs into Reflex-ready state through an explicit update_state step.

## Running The Project
Start the application with reflex run.

## Output Artifacts
- Exported reports are written to the Reports directory in the project root.

## Quality Gates
- Metric logic must be testable in isolation.
- Chart configuration must follow the documented chart contracts.
- Workflow tests must confirm node sequencing and structured outputs.
- Claude-generated changes should be checked against the rules and skills in the .claude directory before they are accepted.

## Comprehensive UI and UX Remediation Requirements
- Left navigation must use full labels with icons, clear active highlighting, collapse and expand behavior, collapsed hover tooltips, grouped spacing, section dividers, and Deep Space Navy plus Electric Cyan futuristic styling.
- Filters must render as a compact horizontal bar with Advanced Filters expand and collapse, active filter chips, grouped spacing, neon-accented toggles, and reduced visual dominance.
- Chat panel must be collapsible, support dock left and dock right and floating mode, and animate transitions smoothly.
- Chat input must remain visible at all times with larger size, stronger contrast, clear placeholder text, and a neon-accented Ask Claude action.
- Chat history must use spaced bubble styling, persistent scroll container behavior, and Save Response controls on assistant messages.
- KPI cards must use meaningful titles, icon markers, trend indicators, consistent neon-accented card styling, and clean grid alignment.
- Charts must support hover tooltips, legends, axis labels, smooth transitions, styled containers, responsive multi-column grids, and cyan-blue-purple palette consistency.
- Dashboard spacing system must follow 8px and 16px and 24px rhythm, section headers, and clear visual dividers for hierarchy.
- Time range UX must use Today and Week and Month pill toggles with active highlighting and full analytics recalculation for metrics and charts, with subtitle feedback.
- Every chart must provide Expand action opening a modal with full chart, full legend, full axis labels, additional insights, close control, and smooth motion.
- Predictive insight card must use icon, title, neon border, generous spacing, hover animation, and placement near relevant charts.
