"""Claude chatbot panel UI for the left dashboard rail."""

from __future__ import annotations

import reflex as rx

from src.state import DashboardState


# --- Custom scrollbar CSS for dark theme ---
_SCROLLBAR_CSS = {
	"&::-webkit-scrollbar": {"width": "6px"},
	"&::-webkit-scrollbar-track": {"background": "transparent"},
	"&::-webkit-scrollbar-thumb": {
		"background": "rgba(62, 231, 224, 0.25)",
		"border_radius": "8px",
	},
	"&::-webkit-scrollbar-thumb:hover": {
		"background": "rgba(62, 231, 224, 0.45)",
	},
	"scrollbar-width": "thin",
	"scrollbar-color": "rgba(62, 231, 224, 0.25) transparent",
}

# --- Markdown component map for dark-themed rendering ---
_MARKDOWN_COMPONENT_MAP = {
	"p": lambda text: rx.text(text, color="#D7E4F7", size="3", line_height="1.6", margin_bottom="0.3rem"),
	"h1": lambda text: rx.heading(text, size="4", color="#3EE7E0", margin_bottom="0.3rem"),
	"h2": lambda text: rx.heading(text, size="3", color="#3EE7E0", margin_bottom="0.25rem"),
	"h3": lambda text: rx.heading(text, size="2", color="#4C8DFF", margin_bottom="0.2rem"),
	"strong": lambda text: rx.text(text, as_="strong", color="#F5F7FA", font_weight="700"),
	"em": lambda text: rx.text(text, as_="em", color="#9BB3D1"),
	"li": lambda text: rx.el.li(text, color="#D7E4F7", font_size="13px", line_height="1.5", margin_left="0.5rem"),
	"ul": lambda children: rx.el.ul(children, padding_left="1rem", margin_bottom="0.3rem"),
	"ol": lambda children: rx.el.ol(children, padding_left="1rem", margin_bottom="0.3rem"),
	"code": lambda text: rx.code(text, color="#3EE7E0", background="rgba(62, 231, 224, 0.1)", padding="0.1rem 0.3rem", border_radius="4px", font_size="12px"),
}


# --- Auto-scroll JS triggered by a counter change ---
_AUTO_SCROLL_JS = """
(function() {
	var el = document.getElementById('chat-messages-scroll');
	if (el) { el.scrollTop = el.scrollHeight; }
})();
"""


def chat_panel() -> rx.Component:
	"""Render the futuristic Claude chat panel with dock and floating controls."""
	return rx.box(
		# Auto-scroll: invisible span keyed to scroll counter triggers re-render → script runs
		rx.el.span(
			rx.script(
				"setTimeout(function(){ var el = document.getElementById('chat-messages-scroll'); if (el) el.scrollTop = el.scrollHeight; }, 80);"
			),
			key=DashboardState.chat_scroll_counter.to(str),
			display="none",
		),
		rx.el.div(
			_header_row(),
			rx.cond(
				DashboardState.chat_panel_collapsed,
				rx.box(),
				rx.text(
					"Ask dataset questions, chart follow-ups, root-cause requests, or risk analysis prompts.",
					color="#9BB3D1",
					size="2",
					font_family="Inter, SF Pro, Poppins, sans-serif",
				),
			),
			rx.cond(
				DashboardState.chat_panel_collapsed,
				rx.box(),
				rx.box(
					rx.foreach(DashboardState.chat_messages, _chat_message_card),
					id="chat-messages-scroll",
					width="100%",
					flex="1 1 0",
					min_height="0",
					overflow_y="auto",
					display="flex",
					flex_direction="column",
					gap="0.75rem",
					padding_right="0.25rem",
					padding_bottom="0.35rem",
					**_SCROLLBAR_CSS,
				),
			),
			rx.cond(
				(DashboardState.chat_error != "") & (DashboardState.chat_panel_collapsed == False),
				rx.box(
					rx.text(DashboardState.chat_error, color="#FCA5A5", size="2"),
					background="#3A2430",
					padding="0.7rem",
					border_radius="12px",
					border="1px solid #FF5A5F",
					width="100%",
				),
				rx.box(),
			),
			rx.cond(
				DashboardState.chat_panel_collapsed,
				rx.box(),
				rx.box(
					_chat_input_zone(),
					width="100%",
					flex_shrink="0",
					background="#0B1221",
					padding_top="0.5rem",
				),
			),
			display="flex",
			flex_direction="column",
			gap="0.5rem",
			height="100%",
			overflow="hidden",
		),
		width=rx.cond(DashboardState.chat_panel_collapsed, "74px", "420px"),
		min_width=rx.cond(DashboardState.chat_panel_collapsed, "74px", "420px"),
		max_width=rx.cond(DashboardState.chat_panel_collapsed, "74px", "420px"),
		height=rx.cond(DashboardState.chat_panel_mode == "floating", "72vh", "100vh"),
		padding="1rem",
		background="#0B1221",
		border=rx.cond(DashboardState.chat_panel_mode == "floating", "1px solid #2A3650", "none"),
		border_left=rx.cond(DashboardState.chat_panel_mode == "right", "1px solid #1E2635", "none"),
		border_right=rx.cond(DashboardState.chat_panel_mode == "left", "1px solid #1E2635", "none"),
		box_shadow="0 16px 34px rgba(62, 231, 224, 0.16)",
		border_radius=rx.cond(DashboardState.chat_panel_mode == "floating", "14px", "0px"),
		overflow="hidden",
		display="flex",
		flex_direction="column",
		transition="all 240ms ease-in-out",
		position=rx.cond(DashboardState.chat_panel_mode == "floating", "fixed", "relative"),
		top=rx.cond(DashboardState.chat_panel_mode == "floating", DashboardState.chat_float_top, "auto"),
		left=rx.cond(DashboardState.chat_panel_mode == "floating", DashboardState.chat_float_left, "auto"),
		z_index=rx.cond(DashboardState.chat_panel_mode == "floating", "30", "1"),
	)


def _header_row() -> rx.Component:
	return rx.vstack(
		rx.hstack(
			rx.hstack(
				rx.heading("Claude Chatbot", size="4", color="#3EE7E0", font_family="Inter, SF Pro, Poppins, sans-serif", white_space="nowrap"),
				rx.cond(
					DashboardState.chat_panel_mode == "floating",
					rx.badge("FLOAT", background="rgba(62, 231, 224, 0.18)", color="#3EE7E0", border_radius="999px"),
					rx.box(),
				),
				spacing="2",
				align="center",
				overflow="hidden",
			),
			rx.button(
				rx.cond(DashboardState.chat_panel_collapsed, ">", "<"),
				on_click=DashboardState.toggle_chat_panel,
				title="Collapse or expand chat panel",
				background="rgba(62, 231, 224, 0.16)",
				border="1px solid #3EE7E0",
				color="#3EE7E0",
				width="30px",
				height="30px",
				padding="0",
				border_radius="10px",
				transition="all 240ms ease-in-out",
				_hover={"box_shadow": "0 10px 22px rgba(62, 231, 224, 0.28)"},
			),
			justify="between",
			align="center",
			width="100%",
		),
		rx.cond(
			DashboardState.chat_panel_collapsed,
			rx.box(),
			rx.hstack(
				rx.button(
					"Right",
					on_click=DashboardState.move_chat_to_right,
					size="1",
					padding="0.35rem 0.55rem",
					border_radius="10px",
					background="rgba(76, 141, 255, 0.16)",
					border="1px solid #4C8DFF",
					color="#DCE9FF",
					font_size="11px",
				),
				rx.button(
					"Left",
					on_click=DashboardState.move_chat_to_left,
					size="1",
					padding="0.35rem 0.55rem",
					border_radius="10px",
					background="rgba(138, 147, 166, 0.12)",
					border="1px solid #4A556B",
					color="#DCE9FF",
					font_size="11px",
				),
				rx.button(
					"Float",
					on_click=DashboardState.set_chat_floating,
					size="1",
					padding="0.35rem 0.55rem",
					border_radius="10px",
					background="rgba(62, 231, 224, 0.2)",
					border="1px solid #3EE7E0",
					color="#3EE7E0",
					font_size="11px",
				),
				spacing="1",
				width="100%",
				flex_wrap="wrap",
			),
		),
		rx.cond(
			DashboardState.chat_panel_mode == "floating",
			rx.hstack(
				rx.text("Drag Panel", color="#8A93A6", size="2"),
				rx.button("←", on_click=DashboardState.nudge_chat(-30, 0), size="1", border_radius="8px", background="#18263D", color="#DCE9FF"),
				rx.button("↑", on_click=DashboardState.nudge_chat(0, -30), size="1", border_radius="8px", background="#18263D", color="#DCE9FF"),
				rx.button("↓", on_click=DashboardState.nudge_chat(0, 30), size="1", border_radius="8px", background="#18263D", color="#DCE9FF"),
				rx.button("→", on_click=DashboardState.nudge_chat(30, 0), size="1", border_radius="8px", background="#18263D", color="#DCE9FF"),
				spacing="1",
				align="center",
			),
			rx.box(),
		),
		spacing="2",
		width="100%",
	)


def _chat_input_zone() -> rx.Component:
	return rx.vstack(
		rx.text("Message", size="2", color="#8A93A6", font_family="Inter, SF Pro, Poppins, sans-serif"),
		rx.el.form(
			rx.el.input(
				name="chat_input",
				default_value=DashboardState.chat_input,
				placeholder="Ask Claude about this dashboard...",
				background="#111A2A",
				border="1px solid #2F3B54",
				color="#E6F0FF",
				border_radius="12px",
				padding="0.55rem 0.75rem",
				font_size="14px",
				line_height="1.4",
				height="40px",
				font_family="Inter, SF Pro, Poppins, sans-serif",
				width="100%",
				box_sizing="border-box",
				outline="none",
				box_shadow="0 0 0 1px rgba(62, 231, 224, 0.08)",
				_focus={"border": "1px solid #3EE7E0", "box_shadow": "0 0 0 3px rgba(62, 231, 224, 0.14)"},
				auto_complete="off",
			),
			rx.hstack(
				rx.el.button(
					rx.cond(DashboardState.is_chat_loading, "Thinking...", "Ask Claude"),
					type="submit",
					background="#3EE7E0",
					color="#0B1221",
					width="50%",
					border_radius="12px",
					padding="0.55rem 0.5rem",
					font_size="13px",
					font_weight="700",
					white_space="nowrap",
					border="none",
					cursor="pointer",
					transition="all 200ms ease-in-out",
					_hover={"transform": "translateY(-1px)", "box_shadow": "0 10px 22px rgba(62, 231, 224, 0.35)"},
				),
				rx.el.button(
					"Email Report",
					type="button",
					on_click=DashboardState.send_email_report,
					background="#4C8DFF",
					color="#0B1221",
					width="50%",
					border_radius="12px",
					padding="0.55rem 0.5rem",
					font_size="13px",
					font_weight="700",
					white_space="nowrap",
					overflow="hidden",
					text_overflow="ellipsis",
					border="none",
					cursor="pointer",
					transition="all 200ms ease-in-out",
					_hover={"transform": "translateY(-1px)", "box_shadow": "0 10px 22px rgba(76, 141, 255, 0.35)"},
				),
				width="100%",
				spacing="2",
				margin_top="0.5rem",
			),
			on_submit=DashboardState.handle_chat_submit,
			reset_on_submit=True,
			width="100%",
			display="flex",
			flex_direction="column",
			gap="0",
		),
		width="100%",
		spacing="2",
	)


def _chat_message_card(message: dict) -> rx.Component:
	"""Render one chat message card with optional save action."""
	is_assistant = message["role"] == "assistant"
	card_background = rx.cond(is_assistant, "#1E2635", "#132036")
	role_label = rx.cond(is_assistant, "Claude", "You")
	return rx.box(
		rx.vstack(
			rx.hstack(
				rx.text(role_label, color="#3EE7E0", size="2", font_weight="700"),
				rx.cond(
					is_assistant,
					rx.button(
						rx.cond(message["saved"], "Saved", "Save Response"),
						on_click=DashboardState.save_response(message["id"]),
						background=rx.cond(message["saved"], "#21463C", "#2A354A"),
						color="#E6F0FF",
						size="1",
						border_radius="12px",
						padding="0.45rem 0.75rem",
						transition="all 180ms ease",
						_hover={"background": "#3EE7E0", "color": "#0B1221"},
					),
					rx.box(),
				),
				justify="between",
				align="center",
				width="100%",
			),
			rx.cond(
				is_assistant,
				rx.markdown(
					message["content"],
					component_map=_MARKDOWN_COMPONENT_MAP,
					color="#D7E4F7",
					font_family="Inter, SF Pro, Poppins, sans-serif",
					line_height="1.6",
					width="100%",
				),
				rx.text(
					message["content"],
					color="#D7E4F7",
					size="3",
					white_space="pre-wrap",
					font_family="Inter, SF Pro, Poppins, sans-serif",
					line_height="1.5",
				),
			),
			spacing="3",
			align="stretch",
		),
		background=card_background,
		border="1px solid #2A354A",
		border_radius="12px",
		padding="0.95rem",
		transition="all 180ms ease",
		_hover={"border_color": "#3EE7E0", "transform": "translateY(-1px)"},
		width="100%",
	)
