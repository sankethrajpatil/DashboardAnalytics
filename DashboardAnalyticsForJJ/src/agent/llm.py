"""Anthropic client integration for deterministic variance explanations."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any

from anthropic import Anthropic
from dotenv import load_dotenv


@dataclass(frozen=True)
class ClaudeExplanationResult:
	"""Structured explanation payload returned to workflow callers."""

	message: str
	source: str
	confidence: str

	def as_dict(self) -> dict[str, str]:
		return {
			"message": self.message,
			"source": self.source,
			"confidence": self.confidence,
		}


class ClaudeVarianceExplainer:
	"""Generate variance explanations using Anthropic when configured."""

	def __init__(self, api_key: str | None = None, model: str = "claude-3-5-sonnet-latest") -> None:
		load_dotenv()
		resolved_key = api_key or os.getenv("ANTHROPIC_API_KEY")
		self._model = model
		self._client = Anthropic(api_key=resolved_key) if resolved_key and resolved_key != "YOUR_KEY_HERE" else None

	def explain_variance(self, context: dict[str, Any]) -> dict[str, str]:
		"""Explain a selected variance driver with a safe fallback path."""
		if self._client is None:
			return self._fallback_explanation(context).as_dict()

		prompt = self._build_prompt(context)
		try:
			response = self._client.messages.create(
				model=self._model,
				max_tokens=220,
				temperature=0,
				messages=[{"role": "user", "content": prompt}],
			)
			message = " ".join(
				block.text.strip()
				for block in response.content
				if hasattr(block, "text") and block.text.strip()
			)
			if not message:
				return self._fallback_explanation(context).as_dict()
			message = self._two_sentence_text(message)
			return ClaudeExplanationResult(
				message=message,
				source="anthropic",
				confidence="high",
			).as_dict()
		except Exception:
			return self._fallback_explanation(context).as_dict()

	def _build_prompt(self, context: dict[str, Any]) -> str:
		return (
			"You are explaining a spend variance to an executive audience. "
			"Use only the structured context provided. Keep the explanation concise, actionable, and specific. "
			"Mention the root cause, its materiality, recent trend behavior, and one recommended next step.\n\n"
			f"Context:\n{json.dumps(context, indent=2, default=str)}"
		)

	def _fallback_explanation(self, context: dict[str, Any]) -> ClaudeExplanationResult:
		root_cause = str(context.get("root_cause") or "the selected driver")
		variance_total = float(context.get("variance_total", 0.0))
		drift_direction = str(context.get("variance_drift", {}).get("direction", "stable"))
		concentration_share = float(context.get("concentration_risk", {}).get("top_share", 0.0)) * 100
		summary = (
			f"{root_cause} is contributing ${variance_total:,.0f} of variance in the current view. "
			f"Variance drift is {drift_direction} and the leading spend segment accounts for {concentration_share:.1f}% of filtered spend."
		)
		return ClaudeExplanationResult(
			message=self._two_sentence_text(summary),
			source="deterministic-fallback",
			confidence="medium",
		)

	def _two_sentence_text(self, text: str) -> str:
		sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]
		if len(sentences) >= 2:
			return f"{sentences[0]} {sentences[1]}"
		if len(sentences) == 1:
			base = sentences[0].rstrip(".!?")
			return f"{base}. Review recent transactions linked to this root cause."
		return "Variance signal is available but no explanatory sentence was produced. Review recent transactions linked to this root cause."


class ClaudeChatAssistant:
	"""Chat-oriented Anthropic client with memory and history context."""

	def __init__(self, api_key: str | None = None, model: str = "claude-3-5-sonnet-latest") -> None:
		load_dotenv()
		resolved_key = api_key or os.getenv("ANTHROPIC_API_KEY")
		self._model = model
		self._client = Anthropic(api_key=resolved_key) if resolved_key and resolved_key != "YOUR_KEY_HERE" else None

	def chat(
		self,
		user_message: str,
		chat_history: list[dict[str, str]],
		saved_memory: str,
		data_context: dict[str, Any],
	) -> dict[str, str]:
		"""Generate a chat answer with explicit memory and context injection."""
		prompt = self._build_chat_prompt(user_message, chat_history, saved_memory, data_context)
		if self._client is None:
			return {
			"assistant_message": self._fallback_response(user_message, saved_memory, data_context),
			"source": "deterministic-fallback",
			"model": "fallback",
		}
		try:
			response = self._client.messages.create(
				model=self._model,
				max_tokens=500,
				temperature=0,
				messages=[{"role": "user", "content": prompt}],
			)
			assistant_message = " ".join(
				block.text.strip()
				for block in response.content
				if hasattr(block, "text") and block.text.strip()
			)
			if not assistant_message:
				assistant_message = self._fallback_response(user_message, saved_memory, data_context)
			return {
				"assistant_message": assistant_message,
				"source": "anthropic",
				"model": self._model,
			}
		except Exception:
			return {
				"assistant_message": self._fallback_response(user_message, saved_memory, data_context),
				"source": "deterministic-fallback",
				"model": "fallback",
			}

	def _build_chat_prompt(
		self,
		user_message: str,
		chat_history: list[dict[str, str]],
		saved_memory: str,
		data_context: dict[str, Any],
	) -> str:
		recent_history = chat_history[-12:]
		prompt_payload = {
			"instructions": [
				"You are Claude in DashboardAnalyticsForJJ.",
				"Answer dataset and chart questions with concrete metrics and clear reasoning.",
				"Support follow-up questions by using prior history and saved memory.",
			],
			"saved_memory": saved_memory,
			"recent_chat_history": recent_history,
			"data_context": data_context,
			"user_message": user_message,
		}
		return json.dumps(prompt_payload, indent=2, default=str)

	def _fallback_response(self, user_message: str, saved_memory: str, data_context: dict[str, Any]) -> str:
		metrics = data_context.get("metrics", {})
		summary = (
			f"Current dashboard context shows Total PO Volume {metrics.get('total_po_volume', 'n/a')}, "
			f"Average Variance {metrics.get('average_variance', 'n/a')}, "
			f"Active Risk Count {metrics.get('active_risk_count', 'n/a')}, "
			f"and Addressable Spend % {metrics.get('addressable_spend_pct', 'n/a')}."
		)
		memory_hint = "Saved memory was considered." if saved_memory.strip() else "No saved memory was available yet."
		return (
			f"You asked: {user_message}. {summary} {memory_hint} "
			"Ask a follow-up about a chart, root cause, risk cluster, or spend concentration for a deeper answer."
		)
