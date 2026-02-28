# Per-session memory is managed directly in agent.py using lists of
# HumanMessage / AIMessage objects, which are passed to the agent prompt
# via the 'chat_history' MessagesPlaceholder on every invocation.
#
# This module is kept for extensibility (e.g. swapping to a persistent store).

from langchain_core.messages import HumanMessage, AIMessage

__all__ = ["HumanMessage", "AIMessage"]
